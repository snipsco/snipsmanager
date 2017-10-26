# -*-: coding utf-8 -*-
"""The microphone setup command."""

import os
import time

from ...base import Base
from ....utils.os_helpers import is_raspi_os, which
from ....utils.systemd import Systemd

from .... import DEFAULT_SNIPSFILE_PATH

from snipsskillscore import pretty_printer as pp

class SystemdSnipsSkillsException(Exception):
    pass


class SystemdSnipsSkills(Base):

    SNIPSSKILLS_SERVICE_NAME = "snipsskills"
    SNIPSSKILLS_COMMAND = "snipsskills"

    def run(self):
        snipsfile_path = self.options['--snipsfile_path'] or os.getcwd()
        try:
            SystemdSnipsSkills.setup(snipsfile_path=snipsfile_path)
        except Exception as e:
            pp.perror(str(e))


    @staticmethod
    def setup(snipsfile_path=None):
        pp.pcommand("Setting up Snips Skills as a Systemd service")

        snipsfile_path = snipsfile_path or DEFAULT_SNIPSFILE_PATH
        working_directory = os.path.dirname(snipsfile_path)
        
        if not is_raspi_os():
            raise SystemdSnipsSkillsException("Snips Systemd configuration is only available on Raspberry Pi. Skipping Systemd setup")

        snipsskills_path = which('snipsskills')
        if snipsskills_path is None:
            raise SystemdSnipsSkillsException("Error: cannot find command 'snipsskills' on the system. Make sure the Snips Skills CLI is correctly installed. Skipping Systemd setup")

        contents = Systemd.get_template(SystemdSnipsSkills.SNIPSSKILLS_SERVICE_NAME)
        contents = contents.replace("{{SNIPSSKILLS_COMMAND}}", snipsskills_path)
        contents = contents.replace("{{WORKING_DIRECTORY}}", working_directory)
        Systemd.write_systemd_file(SystemdSnipsSkills.SNIPSSKILLS_SERVICE_NAME, None, contents)
        Systemd.enable_service(None, SystemdSnipsSkills.SNIPSSKILLS_SERVICE_NAME)

        pp.psuccess("Successfully set up Snips Skills as a Systemd service")
