# -*-: coding utf-8 -*-
""" Various messages. """

from .os_helpers import is_raspi_os, is_mac_os
from snipsskillscore.logging import log, TermincalColors

# pylint: disable=too-few-public-methods
class MessageUtils:

    @staticmethod
    def print_platform_message():
        detected_os = None
        if is_raspi_os():
            detected_os = "Raspberry Pi"
        elif is_mac_os():
            detected_os = "macOS"
        if detected_os is not None:
            print_check("Detected OS: {}".format(detected_os))


def print_check(message):
    print("{}{}{} {}".format(TermincalColors.OKGREEN, u'\u2713'.encode('utf8'), TermincalColors.ENDC, message))