# -*-: coding utf-8 -*-
""" Utilities for managing the Snips SDK. """

import os
import subprocess

from .os_helpers import cmd_exists, is_raspi_os, ask_yes_no

from snipsskillscore.logging import log, log_success, log_warning, log_error

try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, 'wb')

# pylint: disable=too-few-public-methods


SNIPS_INSTALL_COMMAND = "curl https://install.snips.ai -sSf"
SNIPS_INSTALL_ASSISTANT_COMMAND = "snips-install-assistant {}"


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
    def install(answer_yes=None):
        """ Install the Snips SDK. """
        if Snips.is_installed():
            return

        if ask_yes_no("Would you like to install the Snips SDK?", answer_yes) == False:
            return

        log("Installing the Snips SDK.")

        if not is_raspi_os():
            raise SnipsUnsupportedPlatform()

        curl_command = subprocess.Popen(
            SNIPS_INSTALL_COMMAND.split(), stdout=subprocess.PIPE)
        sh_command = subprocess.Popen("sh", stdin=curl_command.stdout)
        output, error = sh_command.communicate()
        rc = sh_command.returncode

        if (rc > 0):
            raise SnipsInstallationFailure(output)
        else:
            log_success("The Snips SDK was successfully installed.")

    @staticmethod
    def run():
        """ Run the Snips SDK. """
        if not Snips.is_installed():
            raise SnipsNotFound()

        try:
            subprocess.Popen(
                "snips", stdout=DEVNULL, stderr=subprocess.STDOUT)
        except OSError as e:
            raise SnipsRuntimeFailure(str(e))

    @staticmethod
    def is_installed():
        """ Check if the Snips SDK is installed. """
        return cmd_exists("snips")

    @staticmethod
    def load_assistant(assistant_zip_path):
        """ Load an assistant file for the Snips SDK.

        :param assistant_zip_path: The path to the assistant.zip file.
        """
        process = subprocess.Popen(
            SNIPS_INSTALL_ASSISTANT_COMMAND.format(assistant_zip_path).split(),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        return process.returncode
