# -*-: coding utf-8 -*-
""" snipsskills

Usage:
  snipsskills install [--snipsfile=<snipsfile_path> --skip-bluetooth --skip-systemd --force-download --silent --debug] [--email=<email> --password=<password>]
  snipsskills install bluetooth [--force-download]
  snipsskills install skill <skill_url> [--force-download --debug]
  snipsskills install skills [--snipsfile=<snipsfile_path> --silent]
  snipsskills install addon <addon_id> [--silent --non-interactive] [PARAMS ...]
  snipsskills fetch assistant [--snipsfile=<snipsfile_path>] [--id=<id> --url=<url> --file=<file>] [--email=<email> --password=<password>] [--force-download]
  snipsskills load assistant [--file=<file> --platform-only]
  snipsskills setup microphone [--snipsfile=<snipsfile_path>] [<microphone_id> [--skip-asoundrc] [--update-asoundconf] [PARAMS ...]]
  snipsskills setup speaker [--snipsfile=<snipsfile_path>] [<speaker_id> [--skip-asoundrc] [--update-asoundconf] [PARAMS ...]]
  snipsskills setup systemd bluetooth [--mqtt-host=<mqtt_host> --mqtt-port=<mqtt_port>]
  snipsskills setup systemd snips
  snipsskills setup systemd skills [--snipsfile=<snipsfile_path>]
  snipsskills run [--snipsfile=<snipsfile_path>] [--mqtt-host=<mqtt_host> --mqtt-port=<mqtt_port> --tts-service=<tts_service> --locale=<locale>] [--debug]
  snipsskills login [--email=<email> --password=<password>]
  snipsskills logout
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

import os
import sys

from docopt import docopt
from snipsskillscore import pretty_printer as pp

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
            from snipsskills.commands.setup.microphone import MicrophoneInstaller
            MicrophoneInstaller(options).run()
        elif options['setup'] == True and options['speaker'] == True:
            from snipsskills.commands.setup.speaker import SpeakerInstaller
            SpeakerInstaller(options).run()
        elif options['setup'] == True and options['systemd'] == True and options['bluetooth'] == True:
            from snipsskills.commands.setup.systemd.bluetooth import SystemdBluetooth
            SystemdBluetooth(options).run()
        elif options['setup'] == True and options['systemd'] == True and options['snips'] == True:
            from snipsskills.commands.setup.systemd.snips import SystemdSnips
            SystemdSnips(options).run()
        elif options['setup'] == True and options['systemd'] == True and options['skills'] == True:
            from snipsskills.commands.setup.systemd.snipsskills import SystemdSnipsSkills
            SystemdSnipsSkills(options).run()
        elif options['login'] == True:
            from snipsskills.commands.session.login import Login
            Login(options).run()
        elif options['logout'] == True:
            from snipsskills.commands.session.logout import Logout
            Logout(options).run()
        elif options['fetch'] == True and options['assistant'] == True:
            from snipsskills.commands.assistant.fetch import AssistantFetcher
            AssistantFetcher(options).run()
        elif options['load'] == True and options['assistant'] == True:
            from snipsskills.commands.assistant.load import AssistantLoader
            AssistantLoader(options).run()
        elif options['install'] == True and options['bluetooth'] == True:
            from snipsskills.commands.install.bluetooth import BluetoothInstaller
            BluetoothInstaller(options).run()
        elif options['install'] == True and options['skill'] == True:
            from snipsskills.commands.install.skill import SkillInstaller
            SkillInstaller(options).run()
        elif options['install'] == True and options['addon'] == True:
            from snipsskills.commands.install.addon import AddonInstaller
            AddonInstaller(options).run()
        elif options['install'] == True and options['skills'] == True:
            from snipsskills.commands.install.skills import SkillsInstaller
            SkillsInstaller(options).run()
        elif options['install'] == True:
            from snipsskills.commands.install.install import GlobalInstaller
            GlobalInstaller(options).run()
    except KeyboardInterrupt:
        try:
            print("\n")
            pp.perror("Snips Skills installer interrupted")
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    try:
        if options['run'] == True:
            from snipsskills.commands.run import Runner
            Runner(options).run()
    except KeyboardInterrupt:
        try:
            print("\n")
            logger.error("Snips Skills server stopped")
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    # elif options['scaffold'] == True:
    #     from snipsskills.commands.scaffold import Scaffold
    #     Scaffold().run()

if __name__ == '__main__':
    main()