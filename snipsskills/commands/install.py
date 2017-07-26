# -*-: coding utf-8 -*-
"""The install command."""

import os

from .base import Base
from ..utils.assistant_downloader import AssistantDownloader, \
    AssistantDownloaderException
from ..utils.intent_class_generator import IntentClassGenerator
from ..utils.snipsfile_parser import Snipsfile, SnipsfileParseException, \
    SnipsfileNotFoundError
from ..utils.pip_installer import PipInstaller

SNIPSFILE = "Snipsfile"
ASSISTANT_DIR = ".snips"
ASSISTANT_ZIP_FILENAME = "assistant.zip"
ASSISTANT_ZIP_PATH = "{}/{}".format(ASSISTANT_DIR, ASSISTANT_ZIP_FILENAME)
INTENTS_DIR = ".snips/intents"


# pylint: disable=too-few-public-methods
class Install(Base):
    """The install command."""

    def run(self):
        """ Command runner. """
        try:
            snipsfile = Snipsfile(SNIPSFILE)
        except SnipsfileNotFoundError:
            print("Snipsfile not found. Please create one.")
            return
        except SnipsfileParseException as err:
            print(err)
            return

        if snipsfile.assistant is None:
            print("No assistants found in Snipsfile.")

        print("Fetching assistant")
        try:
            AssistantDownloader.download(snipsfile.assistant,
                                         ASSISTANT_DIR,
                                         ASSISTANT_ZIP_FILENAME)
        except AssistantDownloaderException:
            print("Error downloading assistant. " +
                  "Make sure the provided URL in the Snipsfile is correct, " +
                  "and that there is a working network connection.")
            return

        print("Generating definitions")
        generator = IntentClassGenerator()
        generator.generate(ASSISTANT_ZIP_PATH, INTENTS_DIR)

        if snipsfile.skills is not None and len(snipsfile.skills) > 0:
            print("Installing skills")
            for skill in snipsfile.skills:
                print("Installing {}".format(skill))
                PipInstaller.install(skill)

        print("Cleaning up")
        os.remove(ASSISTANT_ZIP_PATH)
