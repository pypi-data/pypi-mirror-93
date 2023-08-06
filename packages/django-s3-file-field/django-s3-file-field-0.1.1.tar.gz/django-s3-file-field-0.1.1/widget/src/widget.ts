import './style.scss';
import S3FileInput from './S3FileInput';

function attachToFileInputs(): void {
  document.querySelectorAll<HTMLInputElement>('input[data-s3fileinput]')
    .forEach((element) => {
      // eslint-disable-next-line no-new
      new S3FileInput(element);
    });
}

if (document.readyState !== 'loading') {
  attachToFileInputs();
} else {
  document.addEventListener('DOMContentLoaded', attachToFileInputs.bind(this));
}
