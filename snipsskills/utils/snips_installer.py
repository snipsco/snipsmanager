# -*-: coding utf-8 -*-
""" Utilities for managing the Snips SDK. """

import os
import subprocess

# pylint: disable=too-few-public-methods


SNIPS_INSTALL_COMMAND = "curl https://install.snips.ai -sSf"


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
        if not 'raspberry' in os.uname():
            raise SnipsUnsupportedPlatform()

        if version != None and SnipsInstaller.get_version() == version:
            return

        p1 = subprocess.Popen(SNIPS_INSTALL_COMMAND.split(), stdout=subprocess.PIPE)
        p2 = subprocess.Popen("sh", stdin=p1.stdout)
        output, error = p2.communicate()

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
        pass
