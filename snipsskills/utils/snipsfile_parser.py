# -*-: coding utf-8 -*-
""" Utilities for handline Snipsfiles. """

import os
import yaml

from ..models.skilldef import SkillDef
from ..models.intentdef import IntentDef


class SnipsfileParseException(Exception):
    """ Snipsfile parse exception class. """
    pass


class SnipsfileNotFoundError(Exception):
    """ Snipsfile not found error class. """
    pass

# pylint: disable=too-few-public-methods


def get(yaml_config, key, default_value=None):
    if hasattr(key, '__iter__') and len(key) > 0:
        key_list = key
        node = yaml_config
        for nkey in key_list:
            try:
                node = node[nkey]
            except Exception:
                return default_value
        return node

    try:
        return yaml_config[key]
    except Exception:
        return default_value


class Snipsfile:
    """ Utilities for handling Snipsfiles. """

    def __init__(self, snipsfile="Snipsfile"):
        """ Initialisation.

        :param snipsfile: name of the Snipsfile.
        """
        self.assistant_url = None
        self.skills = []
        self.parse(snipsfile)

    def parse(self, snipsfile):
        """ Parse the content of a Snipsfile. """

        if not os.path.isfile(snipsfile):
            raise SnipsfileNotFoundError(
                'No Snipsfile found. Please create one.')

        yaml_config = None
        with open(snipsfile, 'r') as yaml_file:
            try:
                yaml_config = yaml.load(yaml_file)
            except yaml.scanner.ScannerError as err:
                raise SnipsfileParseException("Error parsing Snipsfile: " +
                                              str(err))

        if not yaml_config:
            return

        self.assistant_url = get(yaml_config, 'assistant')
        if not self.assistant_url:
            raise SnipsfileParseException("No assistant definitions found.")

        self.locale = get(yaml_config, 'locale', 'en_US')
        self.logging = get(yaml_config, 'logging', True)
        self.default_location = get(
            yaml_config, 'default_location', 'Paris,fr')
        self.mqtt_hostname = get(
            yaml_config, ['mqtt_broker', 'hostname'], 'localhost')
        self.mqtt_port = get(yaml_config, ['mqtt_broker', 'port'], 9898)

        self.skills = []
        for skill in get(yaml_config, 'skills', []):
            package_name = get(skill, 'package_name')
            class_name = get(skill, 'class_name')
            pip = get(skill, 'pip')
            params = {}
            for key, value in get(skill, 'params', {}).iteritems():
                params[key] = value
            intent_defs = []
            for intent in get(skill, 'intents', []):
                name = get(intent, 'intent', None)
                action = get(intent, 'action', None)
                intent_defs.append(IntentDef(name, action))
            skilldef = SkillDef(package_name, class_name,
                                pip, params, intent_defs)
            self.skills.append(skilldef)
