# -*-: coding utf-8 -*-
"""The run command."""

import os
import yaml

from .base import Base

from snipsskillscore.server import Server
from snipsskillscore.yaml_config import YamlConfig
from snipsskillscore.intent_parser import IntentParser as ip

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


def handle_intent(intent):
    print("Got intent: " + str(intent))

# pylint: disable=too-few-public-methods


class Run(Base):
    """The run command."""

    def run(self):
        """ Command runner. """
        try:
            config = YamlConfig('default', 'config.yaml')
        except IOError:
            print("No config.yaml file found. Using default config.")
            config = YamlConfig(None, yaml.load(DEFAULT_CONFIG), 'default')
        server = Server(config, handle_intent, [])
        server.start()
