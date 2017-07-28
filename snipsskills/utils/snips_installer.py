# -*-: coding utf-8 -*-
""" Utilities for managing the Snips SDK. """

# pylint: disable=too-few-public-methods


class SnipsInstaller:
    """ Utilities for managing the Snips SDK. """

    @staticmethod
    def install(version=None):
        """ Install the Snips SDK.

        :param version: The version of the SDK to install, or None for latest.
        """
        if version != None and SnipsInstaller.get_version() == version:
            return

    @staticmethod
    def get_version():
        """ Get the version of the SDK if installed, or None. """
        return 1

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
