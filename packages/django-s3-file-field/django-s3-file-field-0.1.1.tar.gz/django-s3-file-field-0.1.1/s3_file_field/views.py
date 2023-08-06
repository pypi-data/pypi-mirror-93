from typing import Dict

from django.core import signing
from django.http.response import HttpResponseBase
from rest_framework import serializers
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response

from . import _multipart, _registry
from ._multipart import ObjectNotFoundException, TransferredPart, TransferredParts


class UploadInitializationRequestSerializer(serializers.Serializer):
    field_id = serializers.CharField()
    file_name = serializers.CharField(trim_whitespace=False)
    file_size = serializers.IntegerField(min_value=1)
    # part_size = serializers.IntegerField(min_value=1)


class PartInitializationResponseSerializer(serializers.Serializer):
    part_number = serializers.IntegerField(min_value=1)
    size = serializers.IntegerField(min_value=1)
    upload_url = serializers.URLField()


class UploadInitializationResponseSerializer(serializers.Serializer):
    object_key = serializers.CharField(trim_whitespace=False)
    upload_id = serializers.CharField()
    parts = PartInitializationResponseSerializer(many=True, allow_empty=False)
    upload_signature = serializers.CharField(trim_whitespace=False)


class TransferredPartRequestSerializer(serializers.Serializer):
    part_number = serializers.IntegerField(min_value=1)
    size = serializers.IntegerField(min_value=1)
    etag = serializers.CharField()

    def create(self, validated_data) -> TransferredPart:
        return TransferredPart(**validated_data)


class UploadCompletionRequestSerializer(serializers.Serializer):
    upload_signature = serializers.CharField(trim_whitespace=False)
    upload_id = serializers.CharField()
    parts = TransferredPartRequestSerializer(many=True, allow_empty=False)

    def create(self, validated_data) -> TransferredParts:
        parts = [
            TransferredPart(**part)
            for part in sorted(validated_data.pop('parts'), key=lambda part: part['part_number'])
        ]
        upload_signature = signing.loads(validated_data['upload_signature'])
        object_key = upload_signature['object_key']
        upload_id = validated_data['upload_id']
        return TransferredParts(parts=parts, object_key=object_key, upload_id=upload_id)


class UploadCompletionResponseSerializer(serializers.Serializer):
    complete_url = serializers.URLField()
    body = serializers.CharField(trim_whitespace=False)


class FinalizationRequestSerializer(serializers.Serializer):
    upload_signature = serializers.CharField(trim_whitespace=False)


class FinalizationResponseSerializer(serializers.Serializer):
    field_value = serializers.CharField(trim_whitespace=False)


@api_view(['POST'])
@parser_classes([JSONParser])
def upload_initialize(request: Request) -> HttpResponseBase:
    request_serializer = UploadInitializationRequestSerializer(data=request.data)
    request_serializer.is_valid(raise_exception=True)
    upload_request: Dict = request_serializer.validated_data
    field = _registry.get_field(upload_request['field_id'])

    # TODO The first argument to generate_filename() is an instance of the model.
    # We do not and will never have an instance of the model during field upload.
    # Maybe we need a different generate method/upload_to with a different signature?
    object_key = field.generate_filename(None, upload_request['file_name'])

    initialization = _multipart.MultipartManager.from_storage(field.storage).initialize_upload(
        object_key, upload_request['file_size']
    )

    # signals.s3_file_field_upload_prepare.send(
    #     sender=upload_prepare, name=name, object_key=object_key
    # )

    # We sign the field_id and object_key to create a "session token" for this upload
    upload_signature = signing.dumps(
        {
            'field_id': upload_request['field_id'],
            'object_key': object_key,
        }
    )

    response_serializer = UploadInitializationResponseSerializer(
        {
            'object_key': initialization.object_key,
            'upload_id': initialization.upload_id,
            'parts': initialization.parts,
            'upload_signature': upload_signature,
        }
    )
    return Response(response_serializer.data)


@api_view(['POST'])
@parser_classes([JSONParser])
def upload_complete(request: Request) -> HttpResponseBase:
    request_serializer = UploadCompletionRequestSerializer(data=request.data)
    request_serializer.is_valid(raise_exception=True)
    transferred_parts: TransferredParts = request_serializer.save()

    upload_signature = signing.loads(request_serializer.validated_data['upload_signature'])
    field = _registry.get_field(upload_signature['field_id'])

    # check if upload_prepare signed this less than max age ago
    # tsigner = TimestampSigner()
    # if object_key != tsigner.unsign(
    #     upload_sig, max_age=int(MultipartManager._url_expiration.total_seconds())
    # ):
    #     raise BadSignature()

    completed_upload = _multipart.MultipartManager.from_storage(field.storage).complete_upload(
        transferred_parts
    )

    # signals.s3_file_field_upload_finalize.send(
    #     sender=multipart_upload_finalize, name=name, object_key=object_key
    # )

    response_serializer = UploadCompletionResponseSerializer(
        {
            'complete_url': completed_upload.complete_url,
            'body': completed_upload.body,
        }
    )
    return Response(response_serializer.data)


@api_view(['POST'])
@parser_classes([JSONParser])
def finalize(request: Request) -> HttpResponseBase:
    request_serializer = FinalizationRequestSerializer(data=request.data)
    request_serializer.is_valid(raise_exception=True)

    upload_signature = signing.loads(request_serializer.validated_data['upload_signature'])
    field_id = upload_signature['field_id']
    object_key = upload_signature['object_key']

    field = _registry.get_field(field_id)

    # get_object_size implicitly verifies that the object exists.
    # We don't want to distribute the field value if the upload did not complete.
    try:
        size = _multipart.MultipartManager.from_storage(field.storage).get_object_size(object_key)
    except ObjectNotFoundException:
        return Response('Object not found', status=400)

    field_value = signing.dumps(
        {
            'object_key': object_key,
            'file_size': size,
        }
    )

    response_serializer = FinalizationResponseSerializer(
        {
            'field_value': field_value,
        }
    )
    return Response(response_serializer.data)
