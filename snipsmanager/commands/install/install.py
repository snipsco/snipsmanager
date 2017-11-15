# -*-: coding utf-8 -*-

import os

from ..base import Base
from ...utils.os_helpers import file_exists
from ...utils.os_helpers import is_raspi_os
from ...utils.snipsfile import Snipsfile

from ..assistant.fetch import AssistantFetcher
from ..assistant.load import AssistantLoader
from ..setup.microphone import MicrophoneInstaller
from ..setup.speaker import SpeakerInstaller
from ..setup.systemd.bluetooth import SystemdBluetooth
from ..setup.systemd.snipsmanager import SystemdSnipsManager
from .skills import SkillsInstaller, SkillsInstallerWarning
from .bluetooth import BluetoothInstaller

from ... import DEFAULT_SNIPSFILE_PATH

from snipsmanagercore import pretty_printer as pp


class GlobalInstallerException(Exception):
    pass


class GlobalInstallerWarning(Exception):
    pass


class GlobalInstaller(Base):
    
    def run(self):
        pp.silent = self.options['--silent']
        debug = self.options['--debug']
        try:
            GlobalInstaller.install(self.options['--snipsfile'], skip_bluetooth=self.options['--skip-bluetooth'], skip_systemd=self.options['--skip-systemd'], email=self.options['--email'], password=self.options['--password'], force_download=self.options['--force-download'])
        except GlobalInstallerWarning as e:
            if debug:
                raise e
            pp.pwarning(str(e))
        except Exception as e:
            if debug:
                raise e
            pp.perror(str(e))


    @staticmethod
    def install(snipsfile_path=None, skip_bluetooth=False, skip_systemd=False, email=None, password=None, force_download=False):
        snipsfile_path = snipsfile_path or DEFAULT_SNIPSFILE_PATH
        if snipsfile_path is not None and not file_exists(snipsfile_path):
            raise GlobalInstallerException("Error running installer: Snipsfile not found")
        snipsfile = Snipsfile(snipsfile_path)
        GlobalInstaller.install_from_snipsfile(snipsfile, skip_bluetooth=skip_bluetooth, skip_systemd=skip_systemd, email=email, password=password, force_download=force_download)


    @staticmethod
    def install_from_snipsfile(snipsfile, skip_bluetooth=False, skip_systemd=False, email=None, password=None, force_download=False):
        pp.pheader("Running Snips Manager installer")

        if snipsfile is None:
            raise GlobalInstallerException("Error running installer: no Snipsfile provided")

        try:
            AssistantFetcher.fetch(email=email, password=password, force_download=force_download)
            AssistantLoader.load()
        except Exception as e:
            pp.pwarning(str(e))

        try:
            SkillsInstaller.install(force_download=force_download)
        except Exception as e:
            pp.pwarning(str(e))
        
        try:
            MicrophoneInstaller.install()
        except Exception as e:
            pp.pwarning(str(e))

        try:
            SpeakerInstaller.install()
        except Exception as e:
            pp.pwarning(str(e))

        if not skip_bluetooth and is_raspi_os():
            try:
                BluetoothInstaller.install(force_download=force_download)
            except Exception as e:
                pp.pwarning(str(e))

        if not skip_systemd and is_raspi_os():
            try:
                SystemdBluetooth.setup()
            except Exception as e:
                pp.pwarning(str(e))
            try:
                SystemdSnipsManager.setup()
            except Exception as e:
                pp.pwarning(str(e))

        if not skip_systemd:
            pp.pheadersuccess("Snips Manager installer complete! You can now reboot your device, or manually run 'snipsmanager run' to start the Snips Manager server")
        else:
            pp.pheadersuccess("Snips Manager installer complete! Now run 'snipsmanager run' to start the Snips Manager server.")
