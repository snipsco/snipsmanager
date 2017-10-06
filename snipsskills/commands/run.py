# -*-: coding utf-8 -*-
"""The run command."""
# pylint: disable=too-few-public-methods,import-error,wrong-import-position,wrong-import-order,wildcard-import,wrong-import-position,wrong-import-order

import os
import subprocess
import time
import threading

from sys import path

from .base import Base
from ..utils.snipsfile import Snipsfile
from ..utils.os_helpers import file_exists

from .. import DEFAULT_SNIPSFILE_PATH, SNIPS_CACHE_INTENTS_DIR, logger

from snipsskillscore.server import Server
# This is used potentially by code blocks in Snipsfile and Snipsspec files.
from snipsskillscore.instant_time import InstantTime
from snipsskillscore.time_interval import TimeInterval


path.append(SNIPS_CACHE_INTENTS_DIR)
path.append(os.path.join(SNIPS_CACHE_INTENTS_DIR, "intents"))

from intent_registry import IntentRegistry
from intents import *

#INTENT_REGISTRY_FILE = ".snips/intents/intent_registry.py"


class RunnerException(Exception):
    pass


class Runner(Base):
    """The run command."""

    # pylint: disable=undefined-variable,exec-used,eval-used
    def run(self):
        """ Command runner. """
        try:
            snipsfile = self.options['--snipsfile']
            mqtt_hostname = self.options['--mqtt-host']
            mqtt_port = self.options['--mqtt-port']
            tts_service_id = self.options['--tts-service']
            locale = self.options['--locale']
            Runner.run_from_snipsfile_path(snipsfile_path=snipsfile, mqtt_hostname=mqtt_hostname, mqtt_port=mqtt_port, tts_service_id=tts_service_id, locale=locale)

        except Exception as e:
            logger.error(str(e))


    @staticmethod
    def run_from_snipsfile_path(snipsfile_path=None, mqtt_hostname=None, mqtt_port=None, tts_service_id=None, locale=None):
        snipsfile_path = snipsfile_path or DEFAULT_SNIPSFILE_PATH
        if snipsfile_path is not None and not file_exists(snipsfile_path):
            raise RunnerException("Error running skills server: Snipsfile not found")
        snipsfile = Snipsfile(snipsfile_path)
        Runner.run_from_snipsfile(snipsfile, mqtt_hostname=mqtt_hostname, mqtt_port=mqtt_port, tts_service_id=tts_service_id, locale=locale)


    @staticmethod
    def run_from_snipsfile(snipsfile, mqtt_hostname=None, mqtt_port=None, tts_service_id=None, locale=None):
        Runner.run_with_params(
            mqtt_hostname=mqtt_hostname or snipsfile.mqtt_hostname,
            mqtt_port=mqtt_port or snipsfile.mqtt_port,
            tts_service_id=tts_service_id or snipsfile.tts_service,
            locale=locale or snipsfile.locale,
            skilldefs=snipsfile.skilldefs)


    @staticmethod
    def run_with_params(mqtt_hostname, mqtt_port, tts_service_id, locale, skilldefs=[]):
        skillsRunner = SkillsRunner(mqtt_hostname, mqtt_port, tts_service_id, locale, skilldefs)
        skillsRunner.start()


class SkillsRunner:

    def __init__(self, mqtt_hostname, mqtt_port, tts_service_id, locale, skilldefs=[]):
        logger.info("Starting Snips Skills")

        self.registry = IntentRegistry()
        self.server = Server(mqtt_hostname, mqtt_port, tts_service_id, locale, self.registry, self.handle_intent_async, logger)

        self.skilldefs = skilldefs
        self.skills = {}
        for skilldef in self.skilldefs:
            try:
                logger.info("Loading skill {}".format(skilldef.package_name))
                if skilldef.package_name is None:
                    logger.error("Error loading skill: required entry 'package_name' not found for the skill definition in your Snipsfile")
                    continue
                class_name = skilldef.class_name or "Skill"
                module_name = skilldef.package_name + "." + skilldef.package_name
                exec("from {} import {}".format(module_name, class_name))
                cls = eval(class_name)
                skill_instance = cls(**skilldef.params)
                if skilldef.requires_tts:
                    skill_instance = cls(tts_service=self.server.tts_service, **skilldef.params)
                else:
                    skill_instance = cls(**skilldef.params)
                self.skills[skilldef.package_name] = skill_instance
                logger.info("Successfully loaded skill {}".format(skilldef.package_name))
            except Exception as e:
                logger.error("Error loading skill {}: {}".format(
                    skilldef.package_name, str(e)))

    def start(self):
        logger.info("Starting the Snips Skills server.")
        self.server.start()

    def handle_intent_async(self, intent, payload=None):
        """ Handle an intent asynchronously.

        :param intent: the incoming intent to handle.
        """
        thread = threading.Thread(target=self.handle_intent, args=(intent, payload, ))
        thread.start()

    def handle_intent(self, intent, payload=None):
        """ Handle an intent.

        :param intent: the incoming intent to handle.
        """
        for skilldef in self.skilldefs:
            intent_def = skilldef.find(intent)
            if intent_def is None:
                continue
            if not skilldef.package_name in self.skills:
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
