import os
import shutil
from .os_helpers import is_raspi_os, execute_command
from .. import ASOUNDCONF_DEST_PATH

class SpeakerSetup:
    ASOUNDCONF_PATH = "../config/asound.conf/"
    SOUND_DRIVER_PATH = "../config/drivers/"

    @staticmethod
    def setup_asoundconf(speaker_id):
        if not is_raspi_os():
            return
        elif speaker_id == 'adafruit-bonnet':
            SpeakerSetup._copy_asoundconf("asound.conf.speakerbonnet")


    @staticmethod
    def setup_driver(speaker_id):
        if not is_raspi_os():
            return
        elif speaker_id == 'adafruit-bonnet':
            SpeakerSetup._install_driver("adafruit_bonnet.sh")

    @staticmethod
    def _copy_asoundconf(asoundconf_file):
        """ Copy asoundconf configuration to local path.

        :param asoundconf_file: the name of the asoundconf configuration, as
                                present in the config folder.
        """
        this_dir, this_filename = os.path.split(__file__)
        asoundconf_path = os.path.join(this_dir, SpeakerSetup.ASOUNDCONF_PATH, asoundconf_file)
        destination = os.path.expanduser(ASOUNDCONF_DEST_PATH)
        shutil.copy2(asoundconf_path, destination)


    @staticmethod
    def _install_driver(driver_file):
        if not is_raspi_os():
            return
        this_dir, this_filename = os.path.split(__file__)
        driver_path = os.path.join(this_dir, SpeakerSetup.SOUND_DRIVER_PATH, driver_file)
        execute_command("sudo chmod a+x " + driver_path)
        execute_command(driver_path + " -y")
