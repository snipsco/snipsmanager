# -*-: coding utf-8 -*-
"""The install command."""

import os
import shutil

from .base import Base, ASSISTANT_DIR, ASSISTANT_ZIP_FILENAME, \
    ASSISTANT_ZIP_PATH, INTENTS_DIR

from ..utils.assistant_downloader import AssistantDownloader, \
    AssistantDownloaderException
from ..utils.intent_class_generator import IntentClassGenerator
from ..utils.pip_installer import PipInstaller
from ..utils.snips_installer import SnipsInstaller, SnipsUnsupportedPlatform


# pylint: disable=too-few-public-methods
class Install(Base):
    """The install command."""

    def run(self):
        """ Command runner. """
        snipsfile = Base.load_snipsfile()

        snips_sdk_version = SnipsInstaller.get_version()
        if snips_sdk_version is not None and \
                snipsfile.snips_sdk_version == snips_sdk_version:
            print("Found Snips SDK version {} on the system.".format(
                snips_sdk_version))
        else:
            try:
                print("Installing the Snips toolchain.")
                SnipsInstaller.install(snips_sdk_version)
            except SnipsUnsupportedPlatform:
                print("\033[91mCurrently, Snips only runs on a Raspberry Pi. " +
                      "Please run this command from a Raspberry Pi.\033[0m")
                return

        if snipsfile.assistant_url is None:
            print("No assistants found in Snipsfile.")

        print("Fetching assistant")
        try:
            AssistantDownloader.download(snipsfile.assistant_url,
                                         ASSISTANT_DIR,
                                         ASSISTANT_ZIP_FILENAME)
        except AssistantDownloaderException:
            print("Error downloading assistant. " +
                  "Make sure the provided URL in the Snipsfile is correct, " +
                  "and that there is a working network connection.")
            return

        print("Loading Snips assistant.")
        SnipsInstaller.load_assistant(ASSISTANT_ZIP_PATH)

        print("Generating definitions.")
        try:
            shutil.rmtree(INTENTS_DIR)
        except Exception:
            pass

        generator = IntentClassGenerator()
        generator.generate(ASSISTANT_ZIP_PATH, INTENTS_DIR)

        if snipsfile.skills is not None and len(snipsfile.skills) > 0:
            print("Installing skills.")
            for skill in snipsfile.skills:
                print("Installing {}.".format(skill.package_name))
                PipInstaller.install(skill.package_name)

        print("Cleaning up.")
        os.remove(ASSISTANT_ZIP_PATH)
