# -*-: coding utf-8 -*-
"""The daemon command."""
# pylint: disable=too-few-public-methods,import-error

import os
import subprocess
import time
import threading

from sys import path

from snipsskillscore.logging import log, log_success, log_warning, log_error


class RPCInstall(Base):
    """The run command."""

    # pylint: disable=undefined-variable,exec-used,eval-used
    def run(self):
        """ Command runner. """
        
        # Setup systemd

        pass
