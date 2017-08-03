# -*-: coding utf-8 -*-
""" Skill definition from a YAML config. """

# pylint: disable=too-few-public-methods
class SkillDef:
    """ Skill definition from a YAML config. """

    # pylint: disable=too-many-arguments
    def __init__(self, package_name, class_name, pip, params, intent_defs, requires_tts):
        """ Initialisation.

        :param package_name: the name of the Python module.
        :param class_name: the name of the Python class.
        :param pip: the pip package (name or url).
        :param params: the parameters to pass to the skills constructor.
        :param intent_defs: a list of intent definitions.
        :param requires_tts: whether the skill requires TTS.
        """
        self.package_name = package_name
        self.class_name = class_name
        self.pip = pip
        self.params = params
        self.intent_defs = intent_defs
        self.requires_tts = requires_tts

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
