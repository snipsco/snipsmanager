# -*-: coding utf-8 -*-
""" pip module installer. """

import os
import pip

from .os_helpers import execute_command, is_valid_github_url, read_file

from .. import SNIPS_CACHE_DIR
from .. import DEB_VENV, SHELL_COMMAND

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
        PipInstaller.execute_pip("pip install --upgrade --quiet {} {}".format(no_cache, package_name))
    

    @staticmethod
    def install_url(url, force_download=False):
        if url.startswith("https://"):
            url = "git+" + url

        if not force_download and PipCache.is_installed(url):
            return

        PipInstaller.execute_pip("pip install --upgrade --quiet {}".format(url))
        PipCache.add(url)


    @staticmethod
    def execute_pip(command):
        is_venv_active = PipInstaller.activate_venv()
        try:
            (output, error) = execute_command(command, silent=False)
        except:
            execute_command("easy_install --upgrade pip", silent=False)
            (output, error) = execute_command(command, silent=False)
        if is_venv_active:
            PipInstaller.deactivate_venv()
        if error is not None and error.strip() != '':
            raise PipInstallerException(error)

    @staticmethod
    def activate_venv():
        try:
            print("COMMAND")
            execute_command("{} {}/bin/activate".format(SHELL_COMMAND, DEB_VENV), silent=True)
            print("\n")
            print("**************")
            print("USING VENV")
            print("\n")
            return True
        except Exception as e:
            print("\n")
            print("**************")
            print("NOT USING VENV")
            print(str(e))
            print("\n")
            return False

    @staticmethod
    def deactivate_venv():
        try:
            execute_command("deactivate", silent=True)
        except:
            pass


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
