# -*-: coding utf-8 -*-
"""The microphone setup command."""

import time

from ..base import Base
from ...utils.os_helpers import file_exists
from ...utils.os_helpers import is_raspi_os
from ...utils.microphone_setup import MicrophoneSetup, RespeakerMicrophoneSetup
from ...utils.snipsfile import Snipsfile

from ... import DEFAULT_SNIPSFILE_PATH, ASOUNDRC_DEST_PATH

from snipsmanagercore import pretty_printer as pp

class MicrophoneInstallerException(Exception):
    pass

class MicrophoneInstallerWarning(Exception):
    pass


# pylint: disable=too-few-public-methods
class MicrophoneInstaller(Base):
    """The microphone setup command."""

    def run(self):
        """ Command runner.

        Docopt command:
        
        snipsmanager setup microphone [--snipsfile=<snipsfile>] [<microphone_id> [--skip-asoundrc] [--update_asoundconf] [PARAMS ...]]
        """
        try:
            microphone_id = self.options['<microphone_id>']
            if microphone_id is not None:
                update_asoundrc = not self.options['--skip-asoundrc']
                update_asoundconf = self.options['--update-asoundconf']
                params = self.options['PARAMS']
                MicrophoneInstaller.install_from_params(microphone_id, update_asoundrc, update_asoundconf, params_list=params)
            else:
                MicrophoneInstaller.install(snipsfile_path=self.options['--snipsfile'])
        except MicrophoneInstallerWarning as e:
            pp.pwarning(str(e))
        except Exception as e:
            pp.perror(str(e))

    @staticmethod
    def install(snipsfile_path=None, silent=False):
        MicrophoneInstaller.print_start(silent=silent)
        if snipsfile_path is None:
            snipsfile_path = DEFAULT_SNIPSFILE_PATH
        if snipsfile_path is not None and not file_exists(snipsfile_path):
            raise SkillsInstallerException("Error setting up microphone: Snipsfile not found")
        snipsfile = Snipsfile(snipsfile_path)
        MicrophoneInstaller.install_from_snipsfile(snipsfile, silent=True)
        MicrophoneInstaller.print_done(silent)


    @staticmethod
    def install_from_snipsfile(snipsfile, silent=False):
        MicrophoneInstaller.print_start(silent=silent)
        if snipsfile is None:
            raise MicrophoneInstallerException("Error setting up microphone: Snipsfile not found")

        microphone_id = snipsfile.microphone_config.identifier
        params_dict = snipsfile.microphone_config.params
        modify_asoundrc = snipsfile.modify_asoundrc
        modify_asoundconf = snipsfile.modify_asoundconf

        MicrophoneInstaller.install_from_params(microphone_id, modify_asoundrc, modify_asoundconf, params_dict=params_dict, silent=True)
        MicrophoneInstaller.print_done(silent)


    @staticmethod
    def install_from_params(microphone_id, update_asoundrc, update_asoundconf, params_list=None, params_dict=None, silent=False):
        MicrophoneInstaller.print_start(microphone_id, silent)

        if not is_raspi_os():
            raise MicrophoneInstallerWarning("System is not Raspberry Pi. Skipping microphone setup")
        
        if update_asoundrc:
            message = pp.ConsoleMessage("Copying .asoundrc to {}".format(ASOUNDRC_DEST_PATH))
            message.start()
            MicrophoneSetup.setup_asoundrc(microphone_id)
            message.done()

        if microphone_id == 'respeaker':
            message = pp.ConsoleMessage("Installing ReSpeaker drivers")
            message.start()
            try:
                respeaker_params = MicrophoneInstaller.normalize_respeaker_params(params_list=params_list, params_dict=params_dict)
                RespeakerMicrophoneSetup.setup(respeaker_params['vendorId'], respeaker_params['productId'])
                message.done()
            except MicrophoneInstallerException as e:
                message.error()
                raise MicrophoneInstallerException(str(e))

        MicrophoneInstaller.print_done(silent)


    @staticmethod
    def normalize_respeaker_params(params_list=None, params_dict=None):
        vendor_id = None
        product_id = None
        exception = MicrophoneInstallerException("Error installing ReSpeaker drivers: you must provide both vendor id and product id")
        if params_list is not None:
            if len(params_list) < 2:
                raise exception
            vendor_id = params_list[0]
            product_id = params_list[1]
        elif params_dict is not None:
            if not 'vendor_id' in params_dict and not 'product_id' in params_dict:
                raise exception
            vendorId = params_dict['vendor_id']
            productId = params_dict['product_id']
        return { 'vendorId': vendorId, 'productId': productId }


    @staticmethod
    def print_start(microphone_id=None, silent=False):
        if not silent:
            if microphone_id is not None:
                pp.pcommand("Setting up microphone: {}".format(microphone_id))
            else:
                pp.pcommand("Setting up microphone")


    @staticmethod
    def print_done(silent=False):
        if not silent:
            pp.psuccess("Microphone setup successfully complete")
