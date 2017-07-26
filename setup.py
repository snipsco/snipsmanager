"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from snipsskills import __version__


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
        errno = call(['py.test', '--cov=snipsskills', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name = 'snipsskills',
    version = __version__,
    description = 'Snips Skills Manager',
    long_description = long_description,
    url = 'https://github.com/snipsco/snipsskills',
    author = 'Snips',
    author_email = 'michael.fester@snips.ai',
    license='MIT',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = ['cli', 'snips'],
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt', 'Jinja2', 'pyyaml', 'urllib2', 'pip', 'snipsskillscore'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'snipsskills=snipsskills.cli:main',
        ],
    },
    package_data={'': ['templates', 'config']},
    include_package_data=True,
    cmdclass = {'test': RunTests},
)
