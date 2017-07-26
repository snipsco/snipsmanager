# -*-: coding utf-8 -*-
""" snipsskills

Usage:
  snipsskills install
  snipsskills run
  snipsskills -h | --help
  snipsskills --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  snipsskills install

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/snipsco/snipsskills
"""


from docopt import docopt

from snipsskills.commands.install import Install
from snipsskills.commands.run import Run

from . import __version__ as VERSION


def main():
    """ Main entry point. """
    options = docopt(__doc__, version=VERSION)

    for (key, value) in options.items():
        if not value:
            continue
        if key == 'install':
            command = Install(options)
            command.run()
        elif key == 'run':
            command = Run(options)
            command.run()
