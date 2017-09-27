# -*-: coding utf-8 -*-
""" snipsskills

Usage:
  snipsskills install bluetooth
  snipsskills fetch assistant [--id=<id> --url=<url> --file=<file>]
  snipsskills load assistant [--file=<file>]
  snipsskills setup microphone <microphone_id> [--skip_asoundrc] [--update_asoundconf] [PARAMS ...]
  snipsskills login
  snipsskills logout
"""

#   snipsskills install assistant
#   snipsskills install skill skill_url
#   snipsskills setup bluetooth
#   snipsskills setup systemd bluetooth
#   snipsskills setup systemd snips
#   snipsskills scaffold skill_name
#   snipsskills logs
#   snipsskills install
#   snipsskills install skills
#   snipsskills run
#   snipsskills setup systemd snipsskills


#   snipsskills install
#   snipsskills install [--snipsfile=<path> --email=<email> --password=<password> --yes]
#   snipsskills install bluetooth [--bt-mqtt-hostname=<localhost> --bt-mqtt-port=<9898>]
#   snipsskills run
#   snipsskills run [--snipsfile=<path>]
#   snipsskills scaffold
#   snipsskills -h | --help
#   snipsskills --version

# Options:
#   -h --help                         Show this screen.
#   --version                         Show version.
#   --snipsfile=<path>                Path to the Snipsfile.
#   --skill=<skillname>

# Examples:
#   snipsskills install

# Help:
#   For help using this tool, please open an issue on the Github repository:
#   https://github.com/snipsco/snipsskills


from docopt import docopt

from . import __version__ as VERSION

def main():
    """ Main entry point. """
    options = docopt(__doc__, version=VERSION)
    
    if options['setup'] == True and options['microphone'] == True:
        from snipsskills.commands.setup.microphone import Microphone
        Microphone(options).run()
    elif options['login'] == True:
        from snipsskills.commands.login import Login
        Login(options).run()
    elif options['logout'] == True:
        from snipsskills.commands.logout import Logout
        Logout(options).run()
    if options['fetch'] == True and options['assistant'] == True:
        from snipsskills.commands.assistant.fetch import AssistantFetcher
        AssistantFetcher(options).run()
    if options['load'] == True and options['assistant'] == True:
        from snipsskills.commands.assistant.load import AssistantLoader
        AssistantLoader(options).run()
    if options['install'] == True and options['bluetooth'] == True:
        from snipsskills.commands.install.bluetooth import BluetoothInstaller
        BluetoothInstaller(options).run()

    # elif options['install'] == True:
    #     from snipsskills.commands.install import Install
    #     Install(options).run()
    #     return
    # elif options['run'] == True:
    #     from snipsskills.commands.run import Run
    #     Run(options).run()
    #     return
    # elif options['scaffold'] == True:
    #     from snipsskills.commands.scaffold import Scaffold
    #     Scaffold().run()
