# -*-: coding utf-8 -*-

import os

from ..base import Base
from ...utils.addons import Addons
from ...utils.os_helpers import ask_for_input

from snipsmanagercore import pretty_printer as pp

class AddonInstallerException(Exception):
    pass

class AddonInstallerWarning(Exception):
    pass


class AddonInstaller(Base):
    
    SPOTIFY_LOGIN_URL = "https://snips-spotify-login.herokuapp.com"

    def run(self):
        pp.silent = self.options['--silent']
        interactive = not self.options['--non-interactive']
        addon_id = self.options['<addon_id>']
        try:
            if addon_id == "spotify":
                AddonInstaller.install_spotify_addon(params=self.options['PARAMS'], interactive=interactive)
            else:
                raise AddonInstallerException("Error: Unknown add-on {}".format(addon_id))
        except AddonInstallerWarning as e:
            pp.pwarning(str(e))
        except Exception as e:
            pp.perror(str(e))


    @staticmethod
    def install_spotify_addon(params=None, interactive=True):
        pp.pcommand("Installing Spotify add-on")

        if params is None or len(params) == 0:
            if interactive:
                pp.psubmessage("You need to provide a Spotify token", indent=True)
                pp.psubmessage("Please open \033[1m\033[4m{}\033[0m in a web browser and follow the instructions to obtain it".format(AddonInstaller.SPOTIFY_LOGIN_URL), indent=True)
                token = ask_for_input("Spotify token:")
            else:
                pp.pwarning("Spotify add-on not installed. Please provide the Spotify token as a parameter, or omit the `--non-interative` flag")
                return
        else:
            token = params[0]

        Addons.install("spotify", [token])

        pp.psuccess("Spotify add-on installed")