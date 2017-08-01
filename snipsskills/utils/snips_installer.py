# -*-: coding utf-8 -*-
""" Utilities for managing the Snips SDK. """

import os
import subprocess

from .os_helpers import cmd_exists, is_raspi_os

# pylint: disable=too-few-public-methods


SNIPS_INSTALL_COMMAND = "curl https://install.snips.ai -sSf"
SNIPS_INSTALL_ASSISTANT_COMMAND = "snips-install-assistant {}"


class SnipsUnsupportedPlatform(Exception):
    """ Unsupported platform exception class. """
    pass


class SnipsInstaller:
    """ Utilities for managing the Snips SDK. """

    @staticmethod
    def install(version=None):
        """ Install the Snips SDK.

        :param version: The version of the SDK to install, or None for latest.
        """
        if cmd_exists("snips"):
            return

        if not 'arm' in " ".join(os.uname()):
            raise SnipsUnsupportedPlatform()

        if version != None and SnipsInstaller.get_version() == version:
            return

        curl_command = subprocess.Popen(
            SNIPS_INSTALL_COMMAND.split(), stdout=subprocess.PIPE)
        sh_command = subprocess.Popen("sh", stdin=curl_command.stdout)
        output, error = sh_command.communicate()

        # Hack to prevent the logout / login issue
        usermod_command = subprocess.Popen(
            "sudo usermod -aG docker pi".split(), stdout=subprocess.PIPE)
        output, error = usermod_command.communicate()

        curl_command = subprocess.Popen(
            SNIPS_INSTALL_COMMAND.split(), stdout=subprocess.PIPE)
        sh_command = subprocess.Popen("sh", stdin=curl_command.stdout)
        output, error = sh_command.communicate()

    @staticmethod
    def get_version():
        """ Get the version of the SDK if installed, or None. """
        return None

    @staticmethod
    def is_installed():
        """ Check if the Snips SDK is installed. """
        return SnipsInstaller.get_version() != None

    @staticmethod
    def load_assistant(assistant_zip_path):
        """ Load an assistant file for the Snips SDK.

        :param assistant_zip_path: The path to the assistant.zip file.
        """
        process = subprocess.Popen(
            SNIPS_INSTALL_ASSISTANT_COMMAND.format(assistant_zip_path).split(),
            stdout=subprocess.PIPE)
        output, error = process.communicate()
