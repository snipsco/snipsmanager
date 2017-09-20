# -*-: coding utf-8 -*-
""" snipsskills

Usage:
  snipsskills install
  snipsskills install [--snipsfile=<path> --email=<email> --password=<password> --yes]
  snipsskills install bluetooth [--bt-mqtt-hostname=localhost --bt-mqtt-port=9898]
  snipsskills run
  snipsskills run [--snipsfile=<path>]
  snipsskills scaffold
  snipsskills -h | --help
  snipsskills --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.
  --snipsfile=<path>                Path to the Snipsfile.
  --skill=<skillname>

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
    elif options['scaffold'] == True:
        from snipsskills.commands.scaffold import Scaffold
        Scaffold().run()
