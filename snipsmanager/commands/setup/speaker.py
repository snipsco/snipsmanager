
from ..base import Base
from ...utils.os_helpers import file_exists
from ...utils.os_helpers import is_raspi_os
from snipsmanagercore import pretty_printer as pp
from ...utils.snipsfile import Snipsfile
from ...utils.speaker_setup import  SpeakerSetup
from ... import DEFAULT_SNIPSFILE_PATH, ASOUNDRC_DEST_PATH, ASOUNDCONF_DEST_PATH

class SpeakerInstallerException(Exception):
    pass

class SpeakerInstallerWarning(Exception):
    pass

class SpeakerInstaller(Base):
    """Speaker setup command"""

    def run(self):

        try:
            speaker_id = self.options['<speaker_id>']
            if speaker_id is not None:
                update_asoundrc = not self.options['--skip-asoundrc']
                update_asoundconf = not self.options['--skip-asoundconf']
                params = self.options['PARAMS']
                SpeakerInstaller.install_from_params(speaker_id, update_asoundrc, update_asoundconf, params_list=params)
            else:
                SpeakerInstaller.install(snipsfile_path=self.options['--snipsfile'])
        except SpeakerInstallerWarning as e:
            pp.pwarning(str(e))
        except Exception as e:
            pp.perror(str(e))


    @staticmethod
    def install(snipsfile_path=None, silent=False):
        SpeakerInstaller.print_start(silent=silent)
        if snipsfile_path is None:
            snipsfile_path = DEFAULT_SNIPSFILE_PATH
        if snipsfile_path is not None and not file_exists(snipsfile_path):
            raise SkillsInstallerException("Error setting up speaker: Snipsfile not found")
        snipsfile = Snipsfile(snipsfile_path)
        SpeakerInstaller.install_from_snipsfile(snipsfile, silent=True)
        SpeakerInstaller.print_done(silent)

    @staticmethod
    def install_from_snipsfile(snipsfile, silent=False):
        SpeakerInstaller.print_start(silent=silent)
        if snipsfile is None:
            raise SpeakerInstallerException("Error setting up speaker: Snipsfile not found")

        speaker_id = snipsfile.speaker_config.identifier
        params_dict = snipsfile.speaker_config.params
        modify_asoundrc = snipsfile.speaker_config.modify_asoundrc
        modify_asoundconf = snipsfile.speaker_config.modify_asoundconf

        SpeakerInstaller.install_from_params(speaker_id, modify_asoundrc, modify_asoundconf, params_dict=params_dict, silent=True)
        SpeakerInstaller.print_done(silent)

    @staticmethod
    def install_from_params(speaker_id, update_asoundrc, update_asoundconf, params_list=None, params_dict=None, silent=False):
        SpeakerInstaller.print_start(speaker_id, silent)

        if not is_raspi_os():
            raise SpeakerInstallerWarning("System is not Raspberry Pi. Skipping speaker setup")

        message = pp.ConsoleMessage("Installing driver")
        message.start()
        SpeakerSetup.setup_driver(speaker_id)
        message.done()


        if update_asoundrc:
            message = pp.ConsoleMessage("Copying .asoundrc to {}".format(ASOUNDRC_DEST_PATH))
            message.start()
            SpeakerSetup.setup_asoundrc(speaker_id)
            message.done()

        if update_asoundconf:
            message = pp.ConsoleMessage("Copying asound.conf to {}".format(ASOUNDCONF_DEST_PATH))
            message.start()
            SpeakerSetup.setup_asoundconf(speaker_id)
            message.done()

        SpeakerInstaller.print_done(silent)


    @staticmethod
    def print_start(speaker_id=None, silent=False):
        if not silent:
            if speaker_id is not None:
                pp.pcommand("Setting up speaker: {}".format(speaker_id))
            else:
                pp.pcommand("Setting up speaker")


    @staticmethod
    def print_done(silent=False):
        if not silent:
            pp.psuccess("Speaker setup successfully complete")
