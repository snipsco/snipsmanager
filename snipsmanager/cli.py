# -*-: coding utf-8 -*-
""" snipsmanager

Usage:
  snipsmanager install [--snipsfile=<snipsfile_path> --skip-bluetooth --skip-systemd --force-download --silent --debug] [--email=<email> --password=<password>]
  snipsmanager install bluetooth [--force-download]
  snipsmanager install skill <skill_url> [--force-download --debug]
  snipsmanager install skills [--snipsfile=<snipsfile_path> --silent]
  snipsmanager install addon <addon_id> [--silent --non-interactive] [PARAMS ...]
  snipsmanager fetch assistant [--snipsfile=<snipsfile_path>] [--id=<id> --url=<url> --file=<file>] [--email=<email> --password=<password>] [--force-download]
  snipsmanager load assistant [--file=<file> --platform-only]
  snipsmanager setup microphone [--snipsfile=<snipsfile_path>] [<microphone_id> [--skip-asoundrc] [--update-asoundconf] [PARAMS ...]]
  snipsmanager setup speaker [--snipsfile=<snipsfile_path>] [<speaker_id> [--skip-asoundrc] [--update-asoundconf] [PARAMS ...]]
  snipsmanager setup systemd bluetooth [--mqtt-host=<mqtt_host> --mqtt-port=<mqtt_port>]
  snipsmanager setup systemd snips
  snipsmanager setup systemd skills [--snipsfile=<snipsfile_path>]
  snipsmanager run [--snipsfile=<snipsfile_path>] [--mqtt-host=<mqtt_host> --mqtt-port=<mqtt_port> --tts-service=<tts_service> --locale=<locale>] [--debug]
  snipsmanager login [--email=<email> --password=<password>]
  snipsmanager logout
  snipsmanager -h | --help
  snipsmanager --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.
  --snipsfile=<path>                Path to the Snipsfile.
  --skill=<skillname>

Examples:
  snipsmanager install

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/snipsco/snipsmanager
"""

import os
import sys

from docopt import docopt
from snipsmanagercore import pretty_printer as pp

from . import logger
from . import __version__ as VERSION

def matches_options(options, option_string):
    values = option_string.split("/")
    for value in values:
        if options[value] != True:
            return False
    return True

def main():
    """ Main entry point. """
    options = docopt(__doc__, version=VERSION)

    try:
        if options['setup'] == True and options['microphone'] == True:
            from snipsmanager.commands.setup.microphone import MicrophoneInstaller
            MicrophoneInstaller(options).run()
        elif options['setup'] == True and options['speaker'] == True:
            from snipsmanager.commands.setup.speaker import SpeakerInstaller
            SpeakerInstaller(options).run()
        elif options['setup'] == True and options['systemd'] == True and options['bluetooth'] == True:
            from snipsmanager.commands.setup.systemd.bluetooth import SystemdBluetooth
            SystemdBluetooth(options).run()
        elif options['setup'] == True and options['systemd'] == True and options['skills'] == True:
            from snipsmanager.commands.setup.systemd.snipsmanager import Systemdsnipsmanager
            Systemdsnipsmanager(options).run()
        elif options['login'] == True:
            from snipsmanager.commands.session.login import Login
            Login(options).run()
        elif options['logout'] == True:
            from snipsmanager.commands.session.logout import Logout
            Logout(options).run()
        elif options['fetch'] == True and options['assistant'] == True:
            from snipsmanager.commands.assistant.fetch import AssistantFetcher
            AssistantFetcher(options).run()
        elif options['load'] == True and options['assistant'] == True:
            from snipsmanager.commands.assistant.load import AssistantLoader
            AssistantLoader(options).run()
        elif options['install'] == True and options['bluetooth'] == True:
            from snipsmanager.commands.install.bluetooth import BluetoothInstaller
            BluetoothInstaller(options).run()
        elif options['install'] == True and options['skill'] == True:
            from snipsmanager.commands.install.skill import SkillInstaller
            SkillInstaller(options).run()
        elif options['install'] == True and options['addon'] == True:
            from snipsmanager.commands.install.addon import AddonInstaller
            AddonInstaller(options).run()
        elif options['install'] == True and options['skills'] == True:
            from snipsmanager.commands.install.skills import SkillsInstaller
            SkillsInstaller(options).run()
        elif options['install'] == True:
            from snipsmanager.commands.install.install import GlobalInstaller
            GlobalInstaller(options).run()
    except KeyboardInterrupt:
        try:
            print("\n")
            pp.perror("Snips Manager installer interrupted")
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    try:
        if options['run'] == True:
            from snipsmanager.commands.run import Runner
            Runner(options).run()
    except KeyboardInterrupt:
        try:
            print("\n")
            logger.error("Snips Manager server stopped")
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    # elif options['scaffold'] == True:
    #     from snipsmanager.commands.scaffold import Scaffold
    #     Scaffold().run()

if __name__ == '__main__':
    main()