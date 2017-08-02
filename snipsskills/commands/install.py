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
from ..utils.snips_installer import SnipsInstaller, SnipsUnsupportedPlatform
from ..utils.os_helpers import cmd_exists, is_raspi_os
from ..utils.microphone_setup import MicrophoneSetup

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
            print(err)
            return

        if not cmd_exists("snips"):
            try:
                log("Installing the Snips toolchain.")
                SnipsInstaller.install()
            except SnipsUnsupportedPlatform:
                log_error("Currently, the Snips SDK only runs on a Raspberry Pi. " +
                          "Skipping installation of the Snips SDK. " +
                          "If you wish to install the Snips SDK, " +
                          "run this command from a Raspberry Pi.")

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

        if cmd_exists("snips"):
            log("Loading Snips assistant.")
            SnipsInstaller.load_assistant(ASSISTANT_ZIP_PATH)

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

        log("Cleaning up.")
        os.remove(ASSISTANT_ZIP_PATH)
        log_success("All done! Run 'snipsskills run' to launch the skills server.")
