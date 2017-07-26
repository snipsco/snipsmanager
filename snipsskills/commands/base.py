# -*-: coding utf-8 -*-
""" The base command. """


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

    def run(self):
        """ Command runner. """
        raise NotImplementedError(
            'You must implement the run() method yourself!')
