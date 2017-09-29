# -*-: coding utf-8 -*-
""" pip module installer. """

import os
import pip

from .os_helpers import execute_command, is_valid_github_url, read_file

from .. import SNIPS_CACHE_DIR

class PipInstallerException(Exception):
    pass

# pylint: disable=too-few-public-methods
class PipInstaller:
    """ pip module installer. """

    @staticmethod
    def install(url_or_pip, force_download=False):
        """ Install a Python module.

        :param url_or_pip: URL of the module, or pip ID.
        """
        if is_valid_github_url(url_or_pip):
            PipInstaller.install_url(url_or_pip, force_download=force_download)
        else:
            PipInstaller.install_pip(url_or_pip, force_download=force_download)


    @staticmethod
    def install_pip(package_name, force_download=False):
        no_cache = "--no-cache" if force_download else ""
        command = "pip install --upgrade --quiet {} {}".format(no_cache, package_name)
        (output, error) = execute_command(command, silent=False)
        if error is not None and error.strip() != '':
            raise PipInstallerException(error)
    

    @staticmethod
    def install_url(url, force_download=False):
        if url.startswith("https://"):
            url = "git+" + url

        if not force_download and PipCache.is_installed(url):
            return

        command = "pip install --upgrade --quiet {}".format(url)
        (output, error) = execute_command(command, silent=False)
        if error is not None and error.strip() != '':
            raise PipInstallerException(error)

        PipCache.add(url)


class PipCache:

    STORE_FILE = os.path.join(SNIPS_CACHE_DIR, "pip_cache")

    @staticmethod
    def is_installed(github_url):
        cache = read_file(PipCache.STORE_FILE)
        if cache is not None and cache.strip() != '':
            return cache.find(github_url) != -1
        return False

    @staticmethod
    def add(github_url):
        if PipCache.is_installed(github_url):
            return
        with open(PipCache.STORE_FILE, "a") as f:
            f.write(github_url + "\n")
