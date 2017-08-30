# -*-: coding utf-8 -*-
""" snipsskills

Usage:
  snipsskills install
  snipsskills install [--snipsfile=<path>]
  snipsskills install bluetooth
  snipsskills run
  snipsskills run [--snipsfile=<path>]
  snipsskills -h | --help
  snipsskills --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.
  --snipsfile=<path>                Path to the Snipsfile.

Examples:
  snipsskills install

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/snipsco/snipsskills
"""


from docopt import docopt

from . import __version__ as VERSION

def main():
    """ Main entry point. """
    options = docopt(__doc__, version=VERSION)

    if options['install'] == True:
        from snipsskills.commands.install import Install
        Install(options).run()
        return
    elif options['run'] == True:
        from snipsskills.commands.run import Run
        Run(options).run()
        return
