from distutils import log
from functools import lru_cache
import os
import platform
from subprocess import CalledProcessError, check_call
import sys
from typing import List, Tuple

from setuptools import Command

here = os.path.dirname(os.path.abspath(__file__))
is_repo = os.path.exists(os.path.join(here, '.git'))


def update_package_data(distribution):
    """Update package_data to catch changes during setup."""
    build_py = distribution.get_command_obj('build_py')
    # distribution.package_data = find_package_data()
    # re-init build_py options which load package_data
    build_py.finalize_options()


def js_prerelease(command, strict=False):
    """Decorate a command to building minified js/css prior to execution."""

    class DecoratedCommand(command):
        def run(self):
            jsdeps = self.distribution.get_command_obj('jsdeps')
            if not is_repo and all(os.path.exists(t) for t in jsdeps.targets):
                # sdist, nothing to do
                command.run(self)
                return

            try:
                self.distribution.run_command('jsdeps')
            except Exception as e:
                missing = [t for t in jsdeps.targets if not os.path.exists(t)]
                if strict or missing:
                    log.warn('rebuilding js and css failed')
                    if missing:
                        log.error('missing files: %s' % missing)
                    raise e
                else:
                    log.warn('rebuilding js and css failed (not a problem)')
                    log.warn(str(e))
            command.run(self)
            update_package_data(self.distribution)

    return DecoratedCommand


class NPM(Command):
    description = 'install package.json dependencies using npm'
    user_options: List[Tuple[str, str, str]] = []

    build_scripts = [('javascript-client', 'build'), ('widget', 'build')]
    targets = [os.path.join(here, 's3_file_field', 'static', 's3_file_field', 'widget.js')]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @property
    @lru_cache(maxsize=1)
    def npm_name(self):
        if platform.system() == 'Windows':
            return 'npm.cmd'
        return 'npm'

    @property
    @lru_cache(maxsize=1)
    def has_npm(self):
        try:
            check_call([self.npm_name, '--version'])
            return True
        except CalledProcessError:
            return False

    def install_and_build(self, project, build_script):
        project_root = os.path.join(here, project)

        log.info(f'Installing build dependencies of {project} with npm.  This may take a while...')
        check_call(
            [self.npm_name, 'install'],
            cwd=project_root,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        # Set the access and modified times of node_modules to now
        # TODO is this necessary?
        os.utime(os.path.join(project_root, 'node_modules'), None)

        log.info(f'Building {project} with npm.  This may take a while...')
        check_call(
            [self.npm_name, 'run', build_script],
            cwd=project_root,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

    def run(self):
        if not self.has_npm:
            log.error(
                '`npm` unavailable.  '
                "If you're running this command using sudo, make sure `npm` is available to sudo"
            )

        for project, build_script in self.build_scripts:
            self.install_and_build(project, build_script)

        for target in self.targets:
            if not os.path.exists(target):
                msg = f'Missing file: {target}'
                raise ValueError(msg)

        # update package data in case this created new files
        update_package_data(self.distribution)
