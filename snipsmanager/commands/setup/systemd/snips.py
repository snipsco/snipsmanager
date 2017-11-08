# -*-: coding utf-8 -*-
"""The microphone setup command."""

import time

from ...base import Base
from ....utils.os_helpers import is_raspi_os, which
from ....utils.systemd import Systemd

from snipsmanagercore import pretty_printer as pp

class SystemdSnipsException(Exception):
    pass


class SystemdSnips(Base):

    SNIPS_SERVICE_NAME = "snips"
    SNIPS_SCRIPT = "{snips_bin_path}"

    def run(self):
        try:
            SystemdSnips.setup()
        except Exception as e:
            pp.perror(str(e))

    @staticmethod
    def setup():
        pp.pcommand("Setting up Snips as a Systemd service")

        if not is_raspi_os():
            raise SystemdSnipsException("Snips Systemd configuration is only available on Raspberry Pi. Skipping Systemd setup")

        snips_path = which('snips')
        if snips_path is None:
            raise SystemdSnipsException("Error: cannot find command 'snips' on the system. Make sure the Snips Platform is correctly installed. Skipping Systemd setup")

        command = SystemdSnips.SNIPS_SCRIPT.format(snips_bin_path=snips_path)
        
        contents = Systemd.get_template(SystemdSnips.SNIPS_SERVICE_NAME)
        contents = contents.replace("{{SNIPS_COMMAND}}", command)
        Systemd.write_systemd_file(SystemdSnips.SNIPS_SERVICE_NAME, None, contents)
        Systemd.enable_service(None, SystemdSnips.SNIPS_SERVICE_NAME)

        pp.psuccess("Successfully set up Snips as a Systemd service")
