# -*-: coding utf-8 -*-
"""The microphone setup command."""

import os
import shutil
import time

from ..base import Base
from ..login import Login
from ...utils.http_helpers import fetch_url
from ...utils.os_helpers import write_binary_file, file_exists, is_raspi_os
from ...utils.cache import Cache
from ...utils.snips import Snips
from .fetch import AssistantFetcher

from snipsskills import SNIPS_CACHE_DIR

from snipsskillscore import pretty_printer as pp


class AssistantLoaderException(Exception):
    pass


# pylint: disable=too-few-public-methods
class AssistantLoader(Base):
    """The microphone setup command."""

    def run(self):
        """ Command runner.

        Docopt command:
        
        snipsskills load assistant [--file=<file>]
        """
        try:
            AssistantLoader.load(self.options['--file'])
        except Exception as e:
            pp.perror(str(e))


    @staticmethod
    def load(file_path=None):
        pp.pcommand("Loading assistant.")

        if not is_raspi_os():
            raise AssistantLoaderException("Error: loading an assistant is only available on a Raspberry Pi.")

        if not Snips.is_installed():
            raise AssistantLoaderException("Error: loading an assistant requires the Snips platform to be installed. Please run 'curl https://install.snips.ai -sSf | sh' to install the Snips Platform.")

        if file_path is not None:
            message = pp.ConsoleMessage("Loading assistant from file {}".format(file_path))
        else:
            message = pp.ConsoleMessage("Loading assistant")
        message.start()

        if file_path is not None and not file_exists(file_path):
            message.error()
            raise AssistantLoaderException("Error loading assistant: file {} not found.".format(file_path))

        if file_path is None:
            file_path = AssistantFetcher.SNIPS_TEMP_ASSISTANT_PATH

        Snips.load_assistant(file_path)
        message.done()