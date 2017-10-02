# -*-: coding utf-8 -*-
""" The base command. """

# SNIPSFILE = "Snipsfile"
# ASSISTANT_DIR = ".snips"
# ASSISTANT_ZIP_FILENAME = "assistant.zip"
# ASSISTANT_ZIP_PATH = "{}/{}".format(ASSISTANT_DIR, ASSISTANT_ZIP_FILENAME)
# INTENTS_DIR = ".snips/intents"

# pylint: disable=too-few-public-methods
class Base(object):
    """ The base command. """

    def __init__(self, options, *args, **kwargs):
        """ Initialisation.

        :param options: command-line options.
        :param *args, **kwargs: extra arguments.
        """
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self.snipsfile = None

    def run(self):
        """ Command runner. """
        raise NotImplementedError(
            'You must implement the run() method yourself!')
