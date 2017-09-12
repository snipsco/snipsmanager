# -*-: coding utf-8 -*-
"""The run command."""
# pylint: disable=too-few-public-methods,import-error

import os
import subprocess
import time
import threading

from sys import path

from ..utils.snipsfile_parser import Snipsfile, SnipsfileParseException, \
    SnipsfileNotFoundError
from ..utils.snips import Snips, SnipsNotFound, SnipsRuntimeFailure

from snipsskillscore.logging import log, log_success, log_warning, log_error
from snipsskillscore.server import Server
from snipsskillscore.instant_time import InstantTime
from snipsskillscore.time_interval import TimeInterval

from .base import Base, SNIPSFILE

path.append(".snips/intents")
path.append(".snips/intents/intents")

# pylint: disable=wrong-import-position,wrong-import-order
from intent_registry import IntentRegistry
# pylint: disable=wildcard-import,wrong-import-position,wrong-import-order
from intents import *

BINDINGS_FILE = "bindings.py"
INTENT_REGISTRY_FILE = ".snips/intents/intent_registry.py"


class Run(Base):
    """The run command."""

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

        registry = IntentRegistry()
        server = Server(self.snipsfile.mqtt_hostname,
                        self.snipsfile.mqtt_port,
                        self.snipsfile.logging,
                        self.snipsfile.tts_service,
                        self.snipsfile.locale,
                        registry,
                        self.handle_intent_async)

        self.skills = {}
        for skilldef in self.snipsfile.skilldefs:
            module_name = skilldef.package_name + "." + skilldef.package_name
            exec("from {} import {}".format(module_name, skilldef.class_name))
            cls = eval(skilldef.class_name)
            try:
                if skilldef.requires_tts:
                    skill_instance = cls(
                        tts_service=server.tts_service, **skilldef.params)
                else:
                    skill_instance = cls(**skilldef.params)
                self.skills[skilldef.package_name] = skill_instance
            except Exception as e:
                log_warning("Error loading skill {}: {}".format(
                    skilldef.package_name, str(e)))

        log("Starting the Snips Skills server.")
        server.start()

    def handle_intent_async(self, intent):
        """ Handle an intent asynchronously.

        :param intent: the incoming intent to handle.
        """
        thread = threading.Thread(target=self.handle_intent,
                                  args=(intent,))
        thread.start()

    def handle_intent(self, intent):
        """ Handle an intent.

        :param intent: the incoming intent to handle.
        """
        for skilldef in self.snipsfile.skilldefs:
            intent_def = skilldef.find(intent)
            if intent_def is None:
                continue
            skill = self.skills[skilldef.package_name]
            if intent_def.action.startswith("{%"):
                # Replace variables in scope with random variables
                # to prevent the skill from accessing/editing them.
                action = intent_def.action \
                    .replace("{%", "") \
                    .replace("%}", "") \
                    .replace("skilldef", "_snips_eejycfyrdfzilgfb") \
                    .replace("intent_def", "_snips_jkqdruouzuahmgns") \
                    .replace("snipsfile", "_snips_pdzdcpaygyjklngz") \
                    .replace("tts_service", "_snips_bxzbomfguxlyxswo") \
                    .strip()
                exec(action)
            else:
                getattr(skill, intent_def.action)()
