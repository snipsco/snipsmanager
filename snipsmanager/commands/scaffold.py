# -*-: coding utf-8 -*-
import os
from jinja2 import Environment, PackageLoader

from .base import Base
from ..utils.os_helpers import create_dir_verbose, write_text_file_verbose, ask_yes_no, ask_for_input, \
    get_user_email_git, email_is_valid
from ..utils.wizard import Wizard


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

    def __init__(self):
        self.jinja_env = Environment(
            loader=PackageLoader('snipsmanager', 'templates'))

        self.wizard = Wizard()
        self.wizard.add_question(
            description="Give your skill a name. For instance: lightskill, gardeningskill, etc ...",
            text="Project name? ",
            input_function=ask_for_input,
            input_validation=lambda x: len(x) > 0)
        self.wizard.add_question(description="A short sentence to describe what your skill does.",
                                 text="Description? ",
                                 input_function=ask_for_input,
                                 input_validation=lambda x: len(x) > 0)
        self.wizard.add_question(description="",
                                 text="Author? ",
                                 input_function=ask_for_input,
                                 input_validation=lambda x: True)
        self.wizard.add_question(description="",
                                 text="Email address? ",
                                 input_function=ask_for_input,
                                 input_validation=email_is_valid,
                                 default_value=get_user_email_git())

    def run(self):
        current_directory = os.getcwd()

        project_name, description, author, email = [question.answer() for question in self.wizard]
        print "\n"

        try:
            # log("Scaffolding {} structure".format(project_name))
            self.create_folders(current_directory, project_name)
            self.create_files(current_directory=current_directory, project_name=project_name, description=description,
                              author=author, email=email)

        except IOError as e:
            pass
            # log_error(e.strerror)

    def retrieve_user_information(self):
        """
        The templates need the following variables from the user :
            - project_name
            - pypi identifier
            - description
            - author
            - email
            - github_url
        """

    def create_folders(self, current_directory, project_name):
        root_directory = os.path.join(current_directory, project_name)

        if os.path.exists(root_directory) and os.listdir(root_directory):
            raise IOError()
        else:
            create_dir_verbose(root_directory, 0)

        directory_names = (project_name, 'tests')

        for directory in directory_names:
            directory_name = os.path.join(root_directory, directory)
            create_dir_verbose(directory_name, 1)

    def create_files(self, current_directory, project_name, description, author, email):
        root_directory = os.path.join(current_directory, project_name)

        self.write_setup(root_directory, project_name, email, description, author)
        self.write_snips_spec(project_name, root_directory)
        self.write_inits(project_name, root_directory)
        self.write_unit_tests(project_name, root_directory)
        self.write_readme(project_name, root_directory)
        self.write_manifest(project_name, root_directory)
        self.write_configs(project_name, root_directory)

    def write_setup(self, root_directory, project_name, email, description, author):
        setup_path = os.path.join(root_directory, 'setup.py')

        SETUP_template = self.jinja_env.get_template('setup.py')
        setup_content = SETUP_template.render(project_name=project_name, email=email, description=description,
                                              author=author)
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
