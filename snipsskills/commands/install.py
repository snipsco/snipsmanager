# -*-: coding utf-8 -*-
"""The install command."""

import os
import shutil

from .base import Base, ASSISTANT_DIR, ASSISTANT_ZIP_FILENAME, \
    ASSISTANT_ZIP_PATH, INTENTS_DIR, SNIPSFILE

from ..utils.snipsfile_parser import Snipsfile, SnipsfileParseException, \
    SnipsfileNotFoundError

from ..utils.assistant_downloader import AssistantDownloader, \
    AssistantDownloaderException
from ..utils.intent_class_generator import IntentClassGenerator
from ..utils.pip_installer import PipInstaller
from ..utils.snips import Snips, SnipsUnsupportedPlatform, SnipsInstallationFailure
from ..utils.os_helpers import cmd_exists, is_raspi_os, remove_file
from ..utils.microphone_setup import MicrophoneSetup
from ..utils.systemd import Systemd
from ..utils.bluetooth import Bluetooth

from snipsskillscore.logging import log, log_success, log_error


# pylint: disable=too-few-public-methods
class Install(Base):
    """The install command."""

    def run(self):
        """ Command runner. """
        try:
            snipsfile = Snipsfile(SNIPSFILE)
        except SnipsfileNotFoundError:
            log_error("Snipsfile not found. Please create one.")
            return
        except SnipsfileParseException as err:
            log_error(err)
            return

        if self.options['bluetooth'] == True:
            Install.setup_bluetooth(snipsfile.mqtt_hostname, snipsfile.mqtt_port)
            return

        if not Snips.is_installed():
            try:
                Snips.install()
            except SnipsUnsupportedPlatform:
                log_error("Currently, the Snips SDK only runs on a Raspberry Pi. " +
                          "Skipping installation of the Snips SDK. " +
                          "If you wish to install the Snips SDK, " +
                          "run this command from a Raspberry Pi.")
            except SnipsInstallationFailure as e:
                log_error("Error installing Snips {}".format(e))

        if snipsfile.assistant_url is None:
            log_error("No assistants found in Snipsfile.")
            return

        log("Fetching assistant.")
        try:
            AssistantDownloader.download(snipsfile.assistant_url,
                                         ASSISTANT_DIR,
                                         ASSISTANT_ZIP_FILENAME)
        except AssistantDownloaderException:
            log_error("Error downloading assistant. " +
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
            MicrophoneSetup.setup(snipsfile.microphone_config)
        else:
            log("System is not Raspberry Pi. Skipping microphone setup.")

        generator = IntentClassGenerator()
        generator.generate(ASSISTANT_ZIP_PATH, INTENTS_DIR)

        if snipsfile.skilldefs is not None and len(snipsfile.skilldefs) > 0:
            log("Installing skills.")
            for skill in snipsfile.skilldefs:
                log("Installing {}.".format(skill.package_name))
                PipInstaller.install(skill.package_name)

        if is_raspi_os():
            Systemd.setup()

        Install.setup_bluetooth(snipsfile.mqtt_hostname, snipsfile.mqtt_port)

        remove_file(ASSISTANT_ZIP_PATH)

        log_success("All done! Type 'snipsskills run' to launch the skills server. " +
                    "Make sure you have a running instance of the Snips SDK. " +
                    "If you have set up Snips Skills as a systemd service, " +
                    "you can also reboot your device " +
                    "and it will be run automatically at launch.")

    @staticmethod
    def setup_bluetooth(mqtt_hostname, mqtt_port):
        if not is_raspi_os():
            log("System is not Raspberry Pi. Skipping Bluetooth setup.")
            return
        Bluetooth.setup(mqtt_hostname, mqtt_port)
