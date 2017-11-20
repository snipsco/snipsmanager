# -*-: coding utf-8 -*-
""" Downloader for Snips assistants. """

import os
import shutil

from .os_helpers import cmd_exists, is_raspi_os, execute_command, pipe_commands

from .. import ASOUNDCONF_DEST_PATH

# pylint: disable=too-few-public-methods
class MicrophoneSetup:
    """ Downloader for Snips assistants. """

    ASOUNDCONF_PATH = "../config/asound.conf"

    @staticmethod
    def setup_asoundconf(microphone_id):
        if not is_raspi_os():
            return
        if microphone_id == 'respeaker':
            MicrophoneSetup._copy_asoundconf("asound.conf.respeaker")
        elif microphone_id == 'jabra':
            MicrophoneSetup._copy_asoundconf("asound.conf.jabra")
        else:
            MicrophoneSetup._copy_asoundconf("asound.conf.default")


    @staticmethod
    def _copy_asoundconf(asoundconf_file):
        """ Copy asound.conf configuration to local path.

        :param asoundconf_file: the name of the asound.conf configuration, as
                              present in the config folder.
        """
        this_dir, this_filename = os.path.split(__file__)
        asoundconf_path = os.path.join(this_dir, MicrophoneSetup.ASOUNDCONF_PATH, asoundconf_file)
        shutil.copy2(asoundconf_path, ASOUNDCONF_DEST_PATH)


class RespeakerMicrophoneSetup:

    @staticmethod
    def setup(vendor_id, product_id):
        if not is_raspi_os():
            return

        execute_command("sudo rm -f /lib/udev/rules.d/50-rspk.rules")

        echo_command = ("echo ACTION==\"add\", SUBSYSTEMS==\"usb\", ATTRS{{idVendor}}==\"{}\", " +
                        "ATTRS{{idProduct}}==\"{}\", MODE=\"660\", GROUP=\"plugdev\"") \
            .format(vendor_id, product_id)
        tee_command = "sudo tee --append /lib/udev/rules.d/50-rspk.rules"
        pipe_commands(echo_command, tee_command, silent=True)

        execute_command("sudo adduser pi plugdev")
        execute_command("sudo udevadm control --reload")
        execute_command("sudo udevadm trigger")
