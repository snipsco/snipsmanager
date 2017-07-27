# -*-: coding utf-8 -*-
"""The run command."""
# pylint: disable=too-few-public-methods,import-error

import glob
import os
import sys
import yaml

from sys import path

from snipsskillscore.server import Server
from snipsskillscore.yaml_config import YamlConfig

from .base import Base, SNIPSFILE, ASSISTANT_DIR, ASSISTANT_ZIP_FILENAME, \
    ASSISTANT_ZIP_PATH, INTENTS_DIR

from ..utils.snipsfile_parser import Snipsfile, SnipsfileParseException, \
    SnipsfileNotFoundError

BINDINGS_FILE = "bindings.py"
INTENT_REGISTRY_FILE = ".snips/intents/intent_registry.py"

path.append(".snips/intents")
path.append(".snips/intents/intents")

from intent_registry import IntentRegistry
from intents import *

DEFAULT_CONFIG = """
default:
    locale: en_US
    logging: True
    tts:
        service: snips
    mqtt_broker:
        hostname: localhost
        port: 9898
"""


class Run(Base):
    """The run command."""

    # pylint: disable=undefined-variable,exec-used
    def run(self):
        """ Command runner. """
        try:
            self.snipsfile = Snipsfile(SNIPSFILE)
        except SnipsfileNotFoundError:
            print("Snipsfile not found. Please create one.")
            return
        except SnipsfileParseException as err:
            print(err)
            return

        self.skills = {}
        for skilldef in self.snipsfile.skills:
            module_name = skilldef.package_name + "." + skilldef.package_name
            exec("from {} import {}".format(module_name, skilldef.class_name))
            cls = eval(skilldef.class_name)
            self.skills[skilldef.package_name] = cls(**skilldef.params)

        registry = IntentRegistry()
        server = Server(self.snipsfile, registry, self.handle_intent)
        server.start()

    def handle_intent(self, intent):
        for skilldef in self.snipsfile.skills:
            intent_def = skilldef.find(intent)
            if intent_def != None:
                skill = self.skills[skilldef.package_name]
                getattr(skill, intent_def.action)()
