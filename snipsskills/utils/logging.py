# -*-: coding utf-8 -*-
""" Logging utilities. """

import inspect

LOGGING_ENABLED = True


class TermincalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log_message(message):
    """ Print a log message.

    :param message: the message to print.
    """
    __log(message)


def log_error(message):
    """ Print an error message.

    :param message: the message to print.
    """
    __log(message, TermincalColors.FAIL)


def log_success(message):
    """ Print a success message.

    :param message: the message to print.
    """
    __log(message, TermincalColors.OKGREEN)


def log_warning(message):
    """ Print a warning message.

    :param message: the message to print.
    """
    __log(message, TermincalColors.WARNING)


def log_blue(message):
    """ Print a blue message.

    :param message: the message to print.
    """
    __log(message, TermincalColors.OKBLUE)


def __log(message, color=None):
    """ Print a message, optionally in a given color.

    :param message: the message to print.
    :param color: the color of the message.
    """
    if message is None:
        return
    if not color:
        print(message)
    else:
        print("{}{}{}".format(color, message, TermincalColors.ENDC))
