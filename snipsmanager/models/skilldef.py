# -*-: coding utf-8 -*-
""" Skill definition from a YAML config. """

# pylint: disable=too-few-public-methods
class SkillDef:
    """ Skill definition from a YAML config. """

    # pylint: disable=too-many-arguments
    def __init__(self, name, package_name, class_name, url, params, intent_defs, notification_defs, requires_tts, addons):
        """ Initialisation.

        :param name: skill name.
        :param package_name: the name of the Python module.
        :param class_name: the name of the Python class.
        :param url: the url package (name or url).
        :param params: the parameters to pass to the skills constructor.
        :param intent_defs: a list of intent definitions.
        :param notification_defs: a list of notification definitions.
        :param requires_tts: whether the skill requires TTS.
        :param addons: addon modules.
        """
        self.name = name
        self.package_name = package_name
        self.class_name = class_name
        self.url = url
        self.params = params
        self.intent_defs = intent_defs
        self.notification_defs = notification_defs
        self.requires_tts = requires_tts
        self.addons = addons

    def find(self, intent):
        """ Find an intent definition in the list of intents that the skill
            declares.

        :param intent: the intent object to look for.
        :return: an intent definition, from the skill definition, if found,
                 or None.
        """
        for intent_def in self.intent_defs:
            if intent_def.name == intent.intentName:
                return intent_def
        return None

    def find_notification(self, name):
        """ Find a notification definition in the list of notifications
            that the skill declares.

        :param name: the name of the notification object to look for.
        :return: a notification definition, from the skill definition,
                 if found, or None.
        """
        for notification_def in self.notification_defs:
            if notification_def.name == name:
                return notification_def
        return None
