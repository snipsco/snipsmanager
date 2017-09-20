# -*-: coding utf-8 -*-
""" Downloader for Snips assistants. """

import os
import shutil
import subprocess

from .os_helpers import cmd_exists, is_raspi_os, execute_command, pipe_commands


def copy_asoundrc(filename):
    """ Copy asoundrc configuration to local path.

    :param filename: the name of the asoundrc configuration, as
                     present in the config folder.
    """
    this_dir, this_filename = os.path.split(__file__)
    asoundrc_path = os.path.join(this_dir, "../config/asoundrc", filename)
    destination = os.path.expanduser('~/.asoundrc')
    shutil.copy2(asoundrc_path, destination)

# pylint: disable=too-few-public-methods


class MicrophoneSetup:
    """ Downloader for Snips assistants. """

    @staticmethod
    def setup(microphone_config=None, modify_asoundrc=True):
        """ Setup microphone.

        :param microphone_id: the microphone id, e.g. 'respeaker'.
        """
        if microphone_config is not None and microphone_config.identifier == 'respeaker':
            RespeakerMicrophoneSetup.setup(microphone_config.params, modify_asoundrc)
        elif microphone_config is not None and microphone_config.identifier == 'jabra':
            JabraMicrophoneSetup.setup(modify_asoundrc)
        else:
            DefaultMicrophoneSetup.setup("asoundrc.default", modify_asoundrc)


class DefaultMicrophoneSetup:

    @staticmethod
    def setup(asoundrc_file="asoundrc.default",  modify_asoundrc=True):
        if not is_raspi_os():
            return
        if modify_asoundrc is True:
            copy_asoundrc(asoundrc_file)


class JabraMicrophoneSetup:

    @staticmethod
    def setup(modify_asoundrc = True):
        DefaultMicrophoneSetup.setup("asoundrc.jabra", modify_asoundrc)


class RespeakerMicrophoneSetup:

    @staticmethod
    def setup(params, modify_asoundrc=True):
        if not is_raspi_os():
            return

        execute_command("sudo rm -f /lib/udev/rules.d/50-rspk.rules")

        echo_command = ("echo ACTION==\"add\", SUBSYSTEMS==\"usb\", ATTRS{{idVendor}}==\"{}\", " +
                        "ATTRS{{idProduct}}==\"{}\", MODE=\"660\", GROUP=\"plugdev\"") \
            .format(params["vendor_id"], params["product_id"])
        tee_command = "sudo tee --append /lib/udev/rules.d/50-rspk.rules"
        pipe_commands(echo_command, tee_command, silent=True)

        execute_command("sudo adduser pi plugdev")
        execute_command("sudo udevadm control --reload")
        execute_command("sudo udevadm trigger")

        if modify_asoundrc is True:
            copy_asoundrc("asoundrc.respeaker")
