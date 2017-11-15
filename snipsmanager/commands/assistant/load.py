# -*-: coding utf-8 -*-

import os
import shutil
import time

from ..base import Base
from ..session.login import Login
from ...utils.http_helpers import fetch_url
from ...utils.os_helpers import write_binary_file, file_exists, is_raspi_os
from ...utils.cache import Cache
from ...utils.snips import Snips
from ...utils.intent_class_generator import IntentClassGenerator
from .fetch import AssistantFetcher

from ... import SNIPS_CACHE_INTENTS_DIR

from snipsmanagercore import pretty_printer as pp


class AssistantLoaderException(Exception):
    pass


# pylint: disable=too-few-public-methods
class AssistantLoader(Base):

    def run(self):
        """ Command runner.

        Docopt command:
        
        snipsmanager load assistant [--file=<file> --platform-only]
        """
        try:
            generate_classes = not self.options['--platform-only']
            AssistantLoader.load(self.options['--file'], generate_classes=generate_classes)
        except Exception as e:
            pp.perror(str(e))


    @staticmethod
    def load(file_path=None, generate_classes=True):
        pp.pcommand("Loading assistant")

        if file_path is None:
            file_path = AssistantFetcher.SNIPS_TEMP_ASSISTANT_PATH

        message = pp.ConsoleMessage("Loading assistant from file {}".format(file_path))
        message.start()

        if file_path is not None and not file_exists(file_path):
            message.error()
            raise AssistantLoaderException("Error loading assistant: file {} not found".format(file_path))

        if is_raspi_os():
            if not Snips.is_installed():
                message.error()
                raise AssistantLoaderException("Error: loading an assistant requires the Snips platform to be installed. Please run 'curl https://install.snips.ai -sSf | sh' to install the Snips Platform")
            Snips.load_assistant(file_path)

        message.done()

        if generate_classes:
            AssistantLoader.generate_intent_classes(file_path)

        pp.psuccess("Assistant has been successfully loaded")

    @staticmethod
    def generate_intent_classes(file_path):
        message = pp.ConsoleMessage("Generating classes from assistant model")
        message.start()
        try:
            shutil.rmtree(SNIPS_CACHE_INTENTS_DIR)
        except Exception:
            pass
        IntentClassGenerator().generate(file_path, SNIPS_CACHE_INTENTS_DIR)
        message.done()
