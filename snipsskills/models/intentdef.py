# -*-: coding utf-8 -*-
""" Intent definition from a YAML config. """

# pylint: disable=too-few-public-methods
class IntentDef:
    """ Intent definition from a YAML config. """

    def __init__(self, name, action):
        """ Initialisation.

        :param name: the name of the intent.
        :param action: the code to execute.
        """
        self.name = name
        self.action = action
