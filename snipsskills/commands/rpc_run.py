# -*-: coding utf-8 -*-
"""The daemon command."""
# pylint: disable=too-few-public-methods,import-error

import os
import subprocess
import time
import threading

from sys import path

from snipsskillscore.logging import log, log_success, log_warning, log_error
from ..utils.rpc_daemon import RPCDaemon

from .base import Base


class RPCRun(Base):
    """TheRPC run command."""

    # pylint: disable=undefined-variable,exec-used,eval-used
    def run(self):
        """ Command runner. """

        snipsfile_path = self.options['--snipsfile']
        if snipsfile_path is None or len(snipsfile_path) == 0:
            snipsfile_path = SNIPSFILE

        try:
            self.snipsfile = Snipsfile(snipsfile_path)
        except SnipsfileNotFoundError:
            log_error("Snipsfile not found. Please create one.")
            return
        except SnipsfileParseException as err:
            log_error(err)
            return

        daemon = RPCDaemon(self.snipsfile.mqtt_hostname,
                        self.snipsfile.mqtt_port,
                        self.snipsfile.logging)

        log("Starting the Snips Daemon server.")
        daemon.start()
