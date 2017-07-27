# -*-: coding utf-8 -*-
"""The run command."""
# pylint: disable=too-few-public-methods,import-error

import os
import yaml

from snipsskillscore.server import Server
from snipsskillscore.yaml_config import YamlConfig

from .base import Base

BINDINGS_FILE = "bindings.py"

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
            config = YamlConfig('config.yaml', None, 'default')
        except IOError:
            print("No config.yaml file found. Using default config.")
            config = YamlConfig(None, yaml.load(DEFAULT_CONFIG), 'default')

        if not os.path.isfile(BINDINGS_FILE):
            print("No bindings.py file found.")
        with open(BINDINGS_FILE, 'r') as bindings_file:
            exec(bindings_file.read())
            server = Server(config, handle_intent, [])
            server.start()
