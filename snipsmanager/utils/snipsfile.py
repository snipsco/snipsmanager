# -*-: coding utf-8 -*-
""" Utilities for handline Snipsfiles. """

import pkgutil
import os
import yaml

from ..models.skilldef import SkillDef
from ..models.intentdef import IntentDef
from ..models.notificationdef import NotificationDef


class SnipsfileParseException(Exception):
    """ Snipsfile parse exception class. """
    pass


class SnipsfileNotFoundError(Exception):
    """ Snipsfile not found error class. """
    pass


class SnipsspecNotFoundError(Exception):
    """ Snipsspec not found error class. """
    pass

# pylint: disable=too-few-public-methods


def get(yaml_config, key_path, default_value=None):
    """ Get a value in a yaml_config, or return a default value.

    :param yaml_config: the YAML config.
    :param key: a key to look for. This can also be a list, looking at
                more depth.
    :param default_value: a default value to return in case the key is
                          not found.
    :return: the value at the given key path, or default_value if not found.
    """
    if len(key_path) == 0:
        return default_value

    node = yaml_config
    for key in key_path:
        try:
            node = node[key]
        except Exception:
            return default_value
    return node


def find_intent(intent_name, intent_defs):
    """ Find an intent by name in a list of intent definitions.

    :param intent_name: the name of the intent to look for.
    :param intent_defs: a list of intent definitions.
    :return: the intent_def with matching name, or None.
    """
    for intent_def in intent_defs:
        if intent_def.name == intent_name:
            return intent_def
    return None


def find_notification(notification_name, notification_defs):
    """ Find a notification by name in a list of notification definitions.

    :param notification_name: the name of the notification to look for.
    :param notification_defs: a list of notification definitions.
    :return: the notification_def with matching name, or None.
    """
    for notification_def in notification_defs:
        if notification_def.name == notification_name:
            return notification_def
    return None

# pylint: disable=too-many-instance-attributes,too-many-locals


class Snipsfile:
    """ Utilities for handling Snipsfiles. """

    def __init__(self, snipsfile="Snipsfile"):
        """ Initialisation.

        :param snipsfile: path for the Snipsfile.
        """
        self.assistant_url = None

        if not os.path.isfile(snipsfile):
            raise SnipsfileNotFoundError(
                'No Snipsfile found at path {}.'.format(snipsfile))

        yaml_config = None
        with open(snipsfile, 'r') as yaml_file:
            try:
                yaml_config = yaml.load(yaml_file)
            except yaml.scanner.ScannerError as err:
                raise SnipsfileParseException("Error parsing Snipsfile: " +
                                              str(err))

        if not yaml_config:
            return

        self.assistant_id = get(yaml_config, ['assistant_id'])
        self.assistant_file = get(yaml_config, ['assistant_file'])
        self.assistant_url = get(yaml_config, ['assistant_url'])
        self.snips_sdk_version = get(yaml_config, ['snips_sdk', 'version'])
        self.locale = get(yaml_config, ['locale'], 'en_US')
        self.tts_service = get(yaml_config, ['tts', 'service'])
        self.default_location = get(
            yaml_config, ['default_location'], 'Paris,fr')
        self.mqtt_hostname = get(
            yaml_config, ['mqtt_broker', 'hostname'], 'localhost')
        self.mqtt_port = get(yaml_config, ['mqtt_broker', 'port'], 1883)
        self.modify_asoundrc = get(yaml_config, ['modify_asoundrc'], True)
        self.modify_asoundconf = get(yaml_config, ['modify_asoundconf'], False)
        self.microphone_config = MicrophoneConfig(yaml_config)
        self.speaker_config = SpeakerConfig(yaml_config)

        self.skilldefs = []
        for skill in get(yaml_config, ['skills'], []):
            url = get(skill, ['url'], get(skill, ['pip']))
            package_name = get(skill, ['package_name'])

            params = {}
            for key, value in get(skill, ['params'], {}).items():
                params[key] = value
        
            snipsspec_file = None
            try:
                if package_name is not None:
                    snipsspec_file = SnipsSpec(package_name)
            except (SnipsspecNotFoundError, SnipsfileParseException) as e:
                pass

            name = self.get_skill_attribute(skill, snipsspec_file, 'name')
            class_name = self.get_skill_attribute(skill, snipsspec_file, 'class_name')
            requires_tts = self.get_skill_attribute(skill, snipsspec_file, 'requires_tts', False)
            addons = self.get_skill_attribute(skill, snipsspec_file, 'addons', [])
            intent_defs = self.get_intent_defs(skill, snipsspec_file)
            notification_defs = self.get_notification_defs(skill, snipsspec_file)

            self.skilldefs.append(SkillDef(name, package_name, class_name, url,
                                           params, intent_defs, notification_defs,
                                           requires_tts, addons))

    def get_skill_attribute(self, skill, snipsspec_file, attribute_name, default_value=None):
        """ Get an attribute for a skill. The value, if provided, by the Snipsfile
            takes precedence over that of the Snipsspec file.

        :param skill: the skill def, as extracted from the Snipsfile.
        :param snipsspec_file: a SnipsSpec object, holding a fallback value
                               for the class name.
        :param default_value: the default value to return if not found.
        :return: the attribute of the skill.
        """
        package_name = get(skill, [attribute_name])
        if package_name is not None:
            return package_name
        if snipsspec_file is not None:
            try:
                return getattr(snipsspec_file, attribute_name)
            except AttributeError:
                pass
        return default_value

    def get_intent_defs(self, skill, snipsspec_file):
        """ Get the intent definitions for a skill. The definitions for the
            skills found in skill has precendence over those in the
            snipsspec_file definitions, which act as fallbacks.


        :param skill: the skill def, as extracted from the Snipsfile.
        :param snipsspec_file: a SnipsSpec object, holding a fallback list of
                               intents.
        :return: the list of intents for the skill.
        """
        intents_snipsfile = []
        for intent in get(skill, ['intents'], []):
            name = get(intent, ['intent'])
            action = get(intent, ['action'])
            intents_snipsfile.append(IntentDef(name, action))

        if snipsspec_file is None:
            return intents_snipsfile

        try:
            intents_snipsspec = snipsspec_file.intent_defs
        except AttributeError as e:
            return intents_snipsfile

        intents = []
        for intent in intents_snipsfile:
            intents.append(intent)

        for intent in intents_snipsspec:
            found = find_intent(intent.name, intents_snipsfile)
            if not found:
                intents.append(intent)
        return intents

    def get_notification_defs(self, skill, snipsspec_file):
        """ Get the intent definitions for a skill. The definitions for the
            skills found in skill has precendence over those in the
            snipsspec_file definitions, which act as fallbacks.


        :param skill: the skill def, as extracted from the Snipsfile.
        :param snipsspec_file: a SnipsSpec object, holding a fallback list of
                               intents.
        :return: the list of intents for the skill.
        """
        notifications_snipsfile = []
        for notification in get(skill, ['notifications'], []):
            name = get(notification, ['name'])
            action = get(notification, ['action'])
            notifications_snipsfile.append(NotificationDef(name, action))

        if snipsspec_file is None:
            return notifications_snipsfile

        try:
            notifications_snipsspec = snipsspec_file.notification_defs
        except AttributeError as e:
            return notifications_snipsfile

        notifications = []
        for notification in notifications_snipsfile:
            notifications.append(intent)

        for notification in notifications_snipsspec:
            found = find_notification(notification.name, notifications_snipsfile)
            if not found:
                notifications.append(notification)
        return notifications

    def get_skill_urls(self):
        skill_urls = []
        for skilldef in self.skilldefs:
            if skilldef.url is not None and skilldef.url.strip() != "":
                skill_urls.append(skilldef.url)
        return skill_urls

    def get_num_skills_without_url(self):
        num = 0
        for skilldef in self.skilldefs:
            if skilldef.url is None:
                num = num + 1
        return num


# pylint: disable=too-many-instance-attributes,too-many-locals
class SnipsSpec:
    """ Utilities for handling Snipsfiles. """

    def __init__(self, package_name):
        """ Initialisation.

        :param package_name: the name of the skills package, in which to look
                             for a Snipsspec file.
        """
        try:
            data = pkgutil.get_data(package_name, 'Snipsspec')
        except IOError:
            raise SnipsspecNotFoundError('No Snipsspec found for package {}.'.format(package_name))

        if data is None:
            raise SnipsspecNotFoundError('No data in Snipsspec found for package {}.'.format(package_name))

        yaml_config = None
        try:
            yaml_config = yaml.load(data)
        except yaml.scanner.ScannerError as err:
            raise SnipsfileParseException("Error parsing Snipsfile for package {}: {}".format(package_name, str(err)))

        if not yaml_config:
            return

        self.package_name = get(yaml_config, ['package_name'])
        self.class_name = get(yaml_config, ['class_name'])
        self.requires_tts = get(yaml_config, ['requires_tts'])
        self.addons = get(yaml_config, ['addons'])

        self.intent_defs = []
        for intent in get(yaml_config, ['intents'], []):
            name = get(intent, ['intent'])
            action = get(intent, ['action'])
            self.intent_defs.append(IntentDef(name, action))

        self.notification_defs = []
        for notification in get(yaml_config, ['notifications'], []):
            name = get(notification, ['name'])
            action = get(notification, ['action'])
            self.notification_defs.append(NotificationDef(name, action))


# pylint: disable=too-many-instance-attributes,too-many-locals
class MicrophoneConfig:
    """ Config holder for microphone. """

    def __init__(self, yaml_config):
        """ Initialisation.

        :param yaml_config: the YAML configuration
        """
        self.identifier = get(yaml_config, ['microphone','identifier'])
        self.params = {}
        for key, value in get(yaml_config, ['microphone','params'], {}).items():
            self.params[key] = value


# pylint: disable=too-many-instance-attributes,too-many-locals
class SpeakerConfig:
    """ Config holder for speaker. """

    def __init__(self, yaml_config):
        self.identifier = get(yaml_config, ['speaker', 'identifier'])
        self.modify_asoundrc = get(yaml_config, ['speaker', 'modify_asoundrc'], True)
        self.modify_asoundconf = get(yaml_config, ['speaker', 'modify_asoundconf'], True)
        self.params = {}
        for key, value in get(yaml_config, ['speaker', 'params'], {}).items():
            self.params[key] = value
