"""Packaging settings."""

from setuptools import Command, find_packages, setup
from snipsmanager import __version__
from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=snipsmanager', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name = 'snipsmanager',
    version = __version__,
    description = 'Snips Skills Manager',
    long_description = long_description,
    url = 'https://github.com/snipsco/snipsmanager',
    author = 'Snips',
    author_email = 'labs@snips.ai',
    license='MIT',
    keywords = ['cli', 'snips'],
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = [
        'docopt',
        'python-dateutil',
        'Jinja2',
        'pyyaml',
        'pip',
        'snipsmanagercore'
    ],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'snipsmanager=snipsmanager.cli:main',
        ],
    },
    include_package_data=True,
    cmdclass = { 'test': RunTests }
)
