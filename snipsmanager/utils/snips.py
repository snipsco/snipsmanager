# -*-: coding utf-8 -*-
""" Utilities for managing the Snips SDK. """

import os
import subprocess

from .os_helpers import cmd_exists, is_raspi_os, ask_yes_no, execute_command

try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, 'wb')

# pylint: disable=too-few-public-methods


SNIPS_INSTALL_COMMAND = "curl https://install.snips.ai -sSf"
SNIPS_INSTALL_ASSISTANT_COMMAND = "snips-install-assistant"
SNIPS_CONFIG_PATH="/usr/share/snips"


class SnipsUnsupportedPlatform(Exception):
    """ Unsupported platform exception class. """
    pass


class SnipsNotFound(Exception):
    """ Snips command not found exception class. """
    pass


class SnipsRuntimeFailure(Exception):
    """ Snips runtime failure exception class. """
    pass


class SnipsInstallationFailure(Exception):
    """ Snips installation failure exception class. """
    pass


class Snips:
    """ Utilities for managing the Snips SDK. """

    @staticmethod
    def is_installed():
        """ Check if the Snips SDK is installed. """
        return cmd_exists("snips") or cmd_exists("snips-asr") or cmd_exists("snips-hotword")

    @staticmethod
    def load_assistant(assistant_zip_path):
        """ Load an assistant file for the Snips SDK.

        :param assistant_zip_path: The path to the assistant.zip file.
        """
        if not cmd_exists(SNIPS_INSTALL_ASSISTANT_COMMAND):
            execute_command("sudo rm -rf " + SNIPS_CONFIG_PATH + "/assistant")
            execute_command("sudo unzip " + assistant_zip_path + " -d " + SNIPS_CONFIG_PATH)
            return

        command = "{} {}".format(SNIPS_INSTALL_ASSISTANT_COMMAND, assistant_zip_path)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        return process.returncode
