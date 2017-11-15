# -*-: coding utf-8 -*-
""" Dialogue definition from a YAML config. """

# pylint: disable=too-few-public-methods
class DialogueDef:
    """ Dialogue definition from a YAML config. """

    def __init__(self, name, action):
        """ Initialisation.

        :param name: the name of the dialogue event.
        :param action: the code to execute.
        """
        self.name = name
        self.action = action
