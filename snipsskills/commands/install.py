# -*-: coding utf-8 -*-
"""The install command."""

import os
import shutil
import sys
from zipfile import is_zipfile

from .base import Base, ASSISTANT_DIR, ASSISTANT_ZIP_FILENAME, \
    ASSISTANT_ZIP_PATH, INTENTS_DIR, SNIPSFILE

from ..utils.snipsfile_parser import Snipsfile, SnipsfileParseException, \
    SnipsfileNotFoundError

from ..utils.assistant_downloader import AssistantDownloader, \
    DownloaderException, Downloader
from ..utils.intent_class_generator import IntentClassGenerator
from ..utils.pip_installer import PipInstaller
from ..utils.snips import Snips, SnipsUnsupportedPlatform, SnipsInstallationFailure
from ..utils.os_helpers import cmd_exists, is_raspi_os, remove_file, create_dir, ask_for_input, ask_for_password, \
    get_user_email_git
from ..utils.microphone_setup import MicrophoneSetup
from ..utils.systemd import Systemd
from ..utils.bluetooth import Bluetooth

from snipsskillscore.logging import log, log_success, log_error, log_warning


# pylint: disable=too-few-public-methods
class Install(Base):
    """The install command."""

    def run(self):
        """ Command runner. """
        if self.options['bluetooth'] == True \
                and (self.options['--bt-mqtt-hostname'] is not None and len(self.options['--bt-mqtt-hostname']) > 0) \
                and self.options['--bt-mqtt-port'] is not None:
            mqtt_hostname = self.options['--bt-mqtt-hostname']
            mqtt_port = self.options['--bt-mqtt-port']

            Install.setup_bluetooth(mqtt_hostname, mqtt_port, answer_yes=True)
            return

        answer_yes = None
        if self.options['--yes'] == True:
            answer_yes = True

        try:
            snipsfile = Snipsfile(SNIPSFILE)
        except SnipsfileNotFoundError:
            log_error("Snipsfile not found. Please create one.")
            return
        except SnipsfileParseException as err:
            log_error(err)
            return

        if self.options['bluetooth'] == True:
            Install.setup_bluetooth(snipsfile.mqtt_hostname, snipsfile.mqtt_port, answer_yes=answer_yes)
            return

        if not Snips.is_installed():
            try:
                Snips.install(answer_yes=answer_yes)
            except SnipsUnsupportedPlatform:
                log_warning("Currently, the Snips SDK only runs on a Raspberry Pi. " +
                          "Skipping installation of the Snips SDK. " +
                          "If you wish to install the Snips SDK, " +
                          "run this command from a Raspberry Pi.")
            except SnipsInstallationFailure as e:
                log_warning("Error installing Snips {}".format(e))

        if snipsfile.assistant_id is not None:
            try:
                if (self.options['--password'] is not None and self.options['--email'] is not None):
                    email = self.options['--email'].strip()
                    password = self.options['--password'].strip()
                else:
                    email, password = self.log_user_in()

                AssistantDownloader(email, password, snipsfile.assistant_id).download(ASSISTANT_DIR,
                                                                                      ASSISTANT_ZIP_FILENAME)
            except:
                log_error("Error fetching the assistant from the console. " +
                          "Make sure the provided assistant ID is correct, " +
                          "and that there is a working network connection.")
                sys.exit()
        elif snipsfile.assistant_file is not None:
            if os.path.isfile(snipsfile.assistant_file):
                create_dir(".snips")
                shutil.copy(src=snipsfile.assistant_file, dst=ASSISTANT_ZIP_PATH)
            else:
                log_error("Error loading assistant. Could not find file {}. Please ensure it is available.".format(snipsfile.assistant_file))
                sys.exit()
        elif snipsfile.assistant_url is not None:
            try:
                Downloader.download(snipsfile.assistant_url,
                                    ASSISTANT_DIR,
                                    ASSISTANT_ZIP_FILENAME)
            except DownloaderException:
                print("Error downloading assistant. " +
                      "Make sure the provided URL in the Snipsfile is correct, " +
                      "and that there is a working network connection.")
                return

        if Snips.is_installed():
            log("Loading Snips assistant.")
            Snips.load_assistant(ASSISTANT_ZIP_PATH)

        log("Generating definitions.")
        try:
            shutil.rmtree(INTENTS_DIR)
        except Exception:
            pass

        if is_raspi_os():
            log("Setting up microphone.")
            MicrophoneSetup.setup(snipsfile.microphone_config, snipsfile.asoundrc)
        else:
            log("System is not Raspberry Pi. Skipping microphone setup.")

        generator = IntentClassGenerator()
        generator.generate(ASSISTANT_ZIP_PATH, INTENTS_DIR)

        if snipsfile.skilldefs is not None and len(snipsfile.skilldefs) > 0:
            log("Installing skills.")
            for skill in snipsfile.skilldefs:
                if skill.pip is not None:
                    log("Installing {}.".format(skill.pip))
                    PipInstaller.install(skill.pip)
                else:
                    log("Installing failed. Missing pip or url key for {}".format(skill.package_name))

        if is_raspi_os():
            Systemd.setup(use_default_values=answer_yes)

        Install.setup_bluetooth(snipsfile.mqtt_hostname, snipsfile.mqtt_port, answer_yes=answer_yes)

        remove_file(ASSISTANT_ZIP_PATH)

        log_success("All done! Type 'snipsskills run' to launch the skills server. " +
                    "Make sure you have a running instance of the Snips SDK. " +
                    "If you have set up Snips Skills as a systemd service, " +
                    "you can also reboot your device " +
                    "and it will be run automatically at launch.")

    @staticmethod
    def setup_bluetooth(mqtt_hostname, mqtt_port, answer_yes=None):
        if not is_raspi_os():
            log("System is not Raspberry Pi. Skipping Bluetooth setup.")
            return
        Bluetooth.setup(mqtt_hostname, mqtt_port, answer_yes=answer_yes)

    def log_user_in(self):
        log("To download your assistant, you need to log in using your Snips Console credentials.")
        email = ask_for_input("Email address: ")
        password = ask_for_password("Password: ")
        return email, password
