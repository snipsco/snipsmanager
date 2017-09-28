# -*-: coding utf-8 -*-
""" pip module installer. """

from .os_helpers import execute_command
import pip


class PipInstallerException(Exception):
    pass

# pylint: disable=too-few-public-methods
class PipInstaller:
    """ pip module installer. """

    @staticmethod
    def install(url_or_pip):
        """ Install a Python module.

        :param url_or_pip: URL of the module, or pip ID.
        """
        if url_or_pip.startswith("https://"):
            url_or_pip = "git+" + url_or_pip

        command = "pip install --upgrade --quiet {}".format(url_or_pip)
        (output, error) = execute_command(command, silent=False)
        if error is not None and error.strip() != '':
        	raise PipInstallerException(error)
