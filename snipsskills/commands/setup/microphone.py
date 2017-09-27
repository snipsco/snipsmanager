# -*-: coding utf-8 -*-
"""The microphone setup command."""

import time

from ..base import Base
from snipsskillscore import pretty_printer as pp

from ...utils.os_helpers import is_raspi_os
from ...utils.microphone_setup import MicrophoneSetup, RespeakerMicrophoneSetup

# pylint: disable=too-few-public-methods
class Microphone(Base):
    """The microphone setup command."""

    def run(self):
        """ Command runner.

        Docopt command:
        
        snipsskills setup microphone <microphone_id> [--skip_asoundrc] [--skip_asoundconf] [PARAMS ...]
        """

        microphone_id = self.options['<microphone_id>']
        update_asoundrc = not self.options['--skip_asoundrc']
        update_asoundconf = self.options['--update_asoundconf']
        params = self.options['PARAMS']

        Microphone.install(microphone_id, update_asoundrc, update_asoundconf, params)

    @staticmethod
    def install(microphone_id, update_asoundrc, update_asoundconf, params):

        pp.pcommand("Setting up microphone: {}".format(microphone_id))

        if not is_raspi_os():
            pp.pwarning("System is not Raspberry Pi. Skipping microphone setup.")
            return
        
        if update_asoundrc:
            message = pp.ConsoleMessage("Copying .asoundrc to {}".format(MicrophoneSetup.ASOUNDRC_DEST_PATH))
            message.start()
            MicrophoneSetup.setup_asoundrc(microphone_id)
            message.done()
            
        if update_asoundconf:
            message = pp.ConsoleMessage("Copying asound.conf to {}".format(MicrophoneSetup.ASOUNDCONF_DEST_PATH))
            message.start()
            MicrophoneSetup.setup_asoundconf()
            message.done()

        if microphone_id == 'respeaker':
            message = pp.ConsoleMessage("Installing ReSpeaker drivers")
            message.start()
            if len(params) < 2:
                message.error()
                if len(params) == 0:
                    reason = "missing product id and vendor id"
                elif len(params) == 1:
                    reason = "missing vendor id"
                pp.perror("Error installing ReSpeaker drivers: {}".format(reason))
            else:
                RespeakerMicrophoneSetup.setup(params[0], params[1])
                message.done()
