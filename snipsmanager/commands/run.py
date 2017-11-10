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
from ..utils.addons import Addons

from .. import DEFAULT_SNIPSFILE_PATH, SNIPS_CACHE_INTENTS_DIR, logger

from snipsmanagercore.server import Server
# This is used potentially by code blocks in Snipsfile and Snipsspec files.
from snipsmanagercore.instant_time import InstantTime
from snipsmanagercore.time_interval import TimeInterval


path.append(SNIPS_CACHE_INTENTS_DIR)
path.append(os.path.join(SNIPS_CACHE_INTENTS_DIR, "intents"))

from intent_registry import IntentRegistry
from intents import *


class RunnerException(Exception):
    pass


class Runner(Base):
    """The run command."""

    # pylint: disable=undefined-variable,exec-used,eval-used
    def run(self):
        """ Command runner. """
        debug = self.options['--debug']
        try:
            snipsfile = self.options['--snipsfile']
            mqtt_hostname = self.options['--mqtt-host']
            mqtt_port = self.options['--mqtt-port']
            tts_service_id = self.options['--tts-service']
            locale = self.options['--locale']
            Runner.run_from_snipsfile_path(snipsfile_path=snipsfile, mqtt_hostname=mqtt_hostname, mqtt_port=mqtt_port, tts_service_id=tts_service_id, locale=locale)
        except Exception as e:
            if debug:
                raise e
            logger.error(str(e))


    @staticmethod
    def run_from_snipsfile_path(snipsfile_path=None, mqtt_hostname=None, mqtt_port=None, tts_service_id=None, locale=None):
        snipsfile_path = snipsfile_path or DEFAULT_SNIPSFILE_PATH
        if snipsfile_path is not None and not file_exists(snipsfile_path):
            raise RunnerException("Error running server: Snipsfile not found")
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


class BaseSkill:

    def __init__(self):
        pass

class SkillsRunner:

    def __init__(self, mqtt_hostname, mqtt_port, tts_service_id, locale, skilldefs=[]):
        logger.info("Starting Snips Manager")

        self.registry = IntentRegistry()
        self.server = Server(mqtt_hostname, mqtt_port, tts_service_id, locale, self.registry, self.handle_intent_async, self.handle_start_listening_async, self.handle_done_listening_async, logger)
        
        self.skilldefs = skilldefs
        self.skills = {}
        for skilldef in self.skilldefs:
            try:
                if skilldef.package_name is not None:
                    logger.info("Loading skill {}".format(skilldef.package_name))
                    class_name = skilldef.class_name or "Skill"
                    module_name = skilldef.package_name + "." + skilldef.package_name
                    exec("from {} import {}".format(module_name, class_name))
                    cls = eval(class_name)
                    if skilldef.requires_tts:
                        skilldef.params[tts_service] = self.server.tts_service
                    if skilldef.addons is not None:
                        for addon_id in skilldef.addons:
                            logger.info("Loading add-on {}".format(addon_id))
                            success = Addons.update_params(params=skilldef.params, addon_id=addon_id)
                            if not success:
                                logger.info("{} add-on was not loaded. Run `snipsmanager install addon {}` to setup add-on".format(addon_id, addon_id))
                    skill_instance = cls(**skilldef.params)
                    self.skills[skilldef.package_name] = skill_instance
                    logger.info("Successfully loaded skill {}".format(skilldef.package_name))
                elif skilldef.name is not None:
                    self.skills[skilldef.name] = BaseSkill()
                    logger.info("Successfully loaded skill {}".format(skilldef.name))
            except Exception as e:
                logger.error("Error loading skill {}: {}".format(
                    skilldef.package_name, str(e)))

    def start(self):
        logger.info("Starting the Snips Manager server.")
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
        tts_service = self.server.tts_service

        for skilldef in self.skilldefs:
            intent_def = skilldef.find(intent)
            if intent_def is None:
                continue
            if skilldef.package_name in self.skills:
                skill = self.skills[skilldef.package_name]
            elif skilldef.name in self.skills:
                skill = self.skills[skilldef.name]
            else:
                continue
            if intent_def.action.startswith("{%"):
                # Replace variables in scope with random variables
                # to prevent the skill from accessing/editing them.
                action = intent_def.action \
                    .replace("{%", "") \
                    .replace("%}", "") \
                    .replace("skilldef", "_snips_eejycfyrdfzilgfb") \
                    .replace("intent_def", "_snips_jkqdruouzuahmgns") \
                    .replace("snipsfile", "_snips_pdzdcpaygyjklngz") \
                    .strip()
                exec(action)
            else:
                getattr(skill, intent_def.action)()


    def handle_start_listening_async(self):
        """ Handle a start listening event."""
        thread = threading.Thread(target=self.handle_notification, args=("start_listening", ))
        thread.start()

    def handle_done_listening_async(self):
        """ Handle a done listening event."""
        thread = threading.Thread(target=self.handle_notification, args=("done_listening", ))
        thread.start()

    def handle_notification(self, name):
        """ Handle a start listening event asynchronously."""

        for skilldef in self.skilldefs:
            notification_def = skilldef.find_notification(name)
            if notification_def is None:
                continue
            if skilldef.package_name in self.skills:
                skill = self.skills[skilldef.package_name]
            elif skilldef.name in self.skills:
                skill = self.skills[skilldef.name]
            else:
                continue
            if notification_def.action.startswith("{%"):
                # Replace variables in scope with random variables
                # to prevent the skill from accessing/editing them.
                action = notification_def.action \
                    .replace("{%", "") \
                    .replace("%}", "") \
                    .replace("skilldef", "_snips_eejycfyrdfzilgfb") \
                    .replace("intent_def", "_snips_jkqdruouzuahmgns") \
                    .replace("snipsfile", "_snips_pdzdcpaygyjklngz") \
                    .strip()
                exec(action)
            else:
                getattr(skill, notification_def.action)()
