# -*-: coding utf-8 -*-

import os
import time

from ...base import Base
from ....utils.os_helpers import is_raspi_os, which
from ....utils.systemd import Systemd

from .... import DEFAULT_SNIPSFILE_PATH

from snipsmanagercore import pretty_printer as pp

class SystemdSnipsManagerException(Exception):
    pass


class SystemdSnipsManager(Base):

    SNIPSMANAGER_SERVICE_NAME = "snipsmanager"
    SNIPSMANAGER_COMMAND = "snipsmanager"

    def run(self):
        snipsfile_path = self.options['--snipsfile_path'] or os.getcwd()
        try:
            SystemdSnipsManager.setup(snipsfile_path=snipsfile_path)
        except Exception as e:
            pp.perror(str(e))


    @staticmethod
    def setup(snipsfile_path=None):
        pp.pcommand("Setting up Snips Manager as a Systemd service")

        snipsfile_path = snipsfile_path or DEFAULT_SNIPSFILE_PATH
        working_directory = os.path.dirname(snipsfile_path)
        
        if not is_raspi_os():
            raise SystemdSnipsManagerException("Snips Systemd configuration is only available on Raspberry Pi. Skipping Systemd setup")

        snipsmanager_path = which('snipsmanager')
        if snipsmanager_path is None:
            raise SystemdSnipsManagerException("Error: cannot find command 'snipsmanager' on the system. Make sure the Snips Manager CLI is correctly installed. Skipping Systemd setup")

        contents = Systemd.get_template(SystemdSnipsManager.SNIPSMANAGER_SERVICE_NAME)
        contents = contents.replace("{{SNIPSMANAGER_COMMAND}}", snipsmanager_path)
        contents = contents.replace("{{WORKING_DIRECTORY}}", working_directory)
        Systemd.write_systemd_file(SystemdSnipsManager.SNIPSMANAGER_SERVICE_NAME, None, contents)
        Systemd.enable_service(None, SystemdSnipsManager.SNIPSMANAGER_SERVICE_NAME)

        pp.psuccess("Successfully set up Snips Manager as a Systemd service")
