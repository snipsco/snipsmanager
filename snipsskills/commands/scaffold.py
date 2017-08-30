# -*-: coding utf-8 -*-
import os
from jinja2 import Environment, PackageLoader
from snipsskillscore.logging import log, log_error

from .base import Base
from ..utils.os_helpers import create_dir_verbose, write_text_file_verbose


from snipsskillscore.logging import log, log_success, log_error


# pylint: disable=too-few-public-methods
class Scaffold(Base):
    """
    The scaffold command.

    The goal is to generate the following structure for a Snips skill

    /[projectname]/
    /[projectname]/setup.py
    /[projectname]/README.rst
    /[projectname]/LICENSE.txt
    /[projectname]/MANIFEST.in
    /[projectname]/lint.cfg
    /[projectname]/setup.cfg
    /[projectname]/[projectname]
    /[projectname]/[projectname]/__init__.py
    /[projectname]/[projectname]/Snipsspec
    /[projectname]/tests
    /[projectname]/tests/__init__.py
    /[projectname]/tests/[projectname]_tests.py
    """

    def __init__(self, skill_name):
        self.project_name = skill_name
        self.jinja_env = Environment(
            loader=PackageLoader('snipsskills', 'templates'))

    def run(self):
        project_name = self.project_name
        current_directory = os.getcwd()

        try:
            log("Scaffolding {} structure".format(project_name))
            self.create_folders(project_name, current_directory)
            self.create_files(project_name, current_directory)

        except IOError as e:
            log_error(e.strerror)


    def create_folders(self, project_name, current_directory):
        root_directory = os.path.join(current_directory, project_name)

        if os.path.exists(root_directory) and os.listdir(root_directory):
            raise IOError()
        else:
            create_dir_verbose(root_directory, 0)

        directory_names = (project_name, 'tests')

        for directory in directory_names:
            directory_name = os.path.join(root_directory, directory)
            create_dir_verbose(directory_name, 1)

    def create_files(self, project_name, current_directory):
        root_directory = os.path.join(current_directory, project_name)

        self.write_setup(project_name, root_directory)
        self.write_snips_spec(project_name, root_directory)
        self.write_inits(project_name, root_directory)
        self.write_unit_tests(project_name, root_directory)
        self.write_readme(project_name, root_directory)
        self.write_license(project_name, root_directory)
        self.write_manifest(project_name, root_directory)
        self.write_configs(project_name, root_directory)

    def write_setup(self, project_name, root_directory):
        setup_path = os.path.join(root_directory, 'setup.py')

        SETUP_template = self.jinja_env.get_template('setup.py')
        setup_content = SETUP_template.render(project_name=project_name)
        write_text_file_verbose(setup_path, setup_content, 1)

    def write_snips_spec(self, project_name, root_directory):
        spec_path = os.path.join(root_directory, project_name, 'Snipsspec')

        spec_content = ''
        write_text_file_verbose(spec_path, spec_content, 2)

    def write_inits(self, project_name, root_directory):
        project_init = os.path.join(root_directory, project_name, '__init__.py')
        tests_init = os.path.join(root_directory, 'tests', '__init__.py')

        write_text_file_verbose(project_init, '', 2)
        write_text_file_verbose(tests_init, '', 2)

    def write_unit_tests(self, project_name, root_directory):
        pass

    def write_readme(self, project_name, root_directory):
        readme_path = os.path.join(root_directory, 'README.rst')

        README_template = self.jinja_env.get_template('README.rst')
        README_content = README_template.render(project_name=project_name)
        write_text_file_verbose(readme_path, README_content, 1)


    def write_license(self, project_name, root_directory):
        license_path = os.path.join(root_directory, 'LICENSE.txt')
        LICENSE_template = self.jinja_env.get_template('LICENSE.txt')

        write_text_file_verbose(license_path, LICENSE_template.render(), 1)

    def write_manifest(self, project_name, root_directory):
        manifest_path = os.path.join(root_directory, 'MANIFEST.in')

        MANIFEST_template = self.jinja_env.get_template('MANIFEST.in')
        manifest_content = MANIFEST_template.render(project_name=project_name)
        write_text_file_verbose(manifest_path, manifest_content, 1)

    def write_configs(self, project_name, root_directory):
        lint_path = os.path.join(root_directory, 'lint.cfg')
        setup_path = os.path.join(root_directory, 'setup.cfg')

        LINT_template = self.jinja_env.get_template('lint.cfg')
        SETUP_CONFIG_template = self.jinja_env.get_template('setup.cfg')

        lint_content = LINT_template.render()
        setup_content = SETUP_CONFIG_template.render()

        write_text_file_verbose(lint_path, lint_content, 1)
        write_text_file_verbose(setup_path, setup_content, 1)




