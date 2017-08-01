# -*-: coding utf-8 -*-
"""The run command."""
# pylint: disable=too-few-public-methods,import-error

import asyncio
import os
import subprocess
from sys import path

from snipsskillscore.server import Server
from snipsskillscore.thread_handler import ThreadHandler

from .base import Base

path.append(".snips/intents")
path.append(".snips/intents/intents")

# pylint: disable=wrong-import-position,wrong-import-order
from intent_registry import IntentRegistry
# pylint: disable=wildcard-import,wrong-import-position,wrong-import-order
from intents import *

BINDINGS_FILE = "bindings.py"
INTENT_REGISTRY_FILE = ".snips/intents/intent_registry.py"

import threading


class Run(Base):
    """The run command."""

    # pylint: disable=undefined-variable,exec-used,eval-used
    def run(self):
        """ Command runner. """
        self.snipsfile = Base.load_snipsfile()

        self.ioloop = asyncio.get_event_loop()

        self.skills = {}
        for skilldef in self.snipsfile.skilldefs:
            module_name = skilldef.package_name + "." + skilldef.package_name
            exec("from {} import {}".format(module_name, skilldef.class_name))
            cls = eval(skilldef.class_name)
            self.skills[skilldef.package_name] = cls(**skilldef.params)

        self.thread_handler = ThreadHandler()

        registry = IntentRegistry()
        server = Server(self.snipsfile, registry, self.handle_intent)
        server.start()

    def handle_intent(self, intent):
        if self.ioloop is None:
            self.ioloop = asyncio.get_event_loop()
        wait_tasks = asyncio.wait(
            [self.ioloop.create_task(self.handle_intent_async(intent))])
        self.ioloop.run_until_complete(wait_tasks)

    async def handle_intent_async(self, intent):
        """ Handle an intent.

        :param intent: the incoming intent to handle.
        """
        for skilldef in self.snipsfile.skilldefs:
            intent_def = skilldef.find(intent)
            if intent_def != None:
                skill = self.skills[skilldef.package_name]
                if intent_def.action.startswith("{%"):
                    action = intent_def.action \
                        .replace("{%", "") \
                        .replace("%}", "") \
                        .strip()
                    exec(action)
                else:
                    getattr(skill, intent_def.action)()
