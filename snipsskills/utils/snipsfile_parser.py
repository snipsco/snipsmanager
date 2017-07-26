# -*-: coding utf-8 -*-
""" Utilities for handline Snipsfiles. """

import os
import yaml


class SnipsfileParseException(Exception):
    """ Snipsfile parse exception class. """
    pass


class SnipsfileNotFoundError(Exception):
    """ Snipsfile not found error class. """
    pass

# pylint: disable=too-few-public-methods


class Snipsfile:
    """ Utilities for handling Snipsfiles. """

    def __init__(self, snipsfile="Snipsfile"):
        """ Initialisation.

        :param snipsfile: name of the Snipsfile.
        """
        self.assistant = None
        self.skills = []
        self.parse(snipsfile)

    def parse(self, snipsfile):
        """ Parse the content of a Snipsfile. """

        if not os.path.isfile(snipsfile):
            raise SnipsfileNotFoundError(
                'No Snipsfile found. Please create one.')

        with open(snipsfile, 'r') as ymlfile:
            try:
                yml = yaml.load(ymlfile)
            except yaml.scanner.ScannerError as err:
                raise SnipsfileParseException("Error parsing Snipsfile: " +
                                              str(err))
            try:
                self.assistant = yml['assistant']
            except TypeError:
                raise SnipsfileParseException(
                    "No assistant definitions found.")
            try:
                self.skills = yml['skills']
            except TypeError:
                pass
