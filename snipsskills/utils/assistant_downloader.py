# -*-: coding utf-8 -*-
""" Downloader for Snips assistants. """

import os

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

class AssistantDownloaderException(Exception):
    """ Exceptions related to downloads of Snips assistants. """
    pass

# pylint: disable=too-few-public-methods
class AssistantDownloader:
    """ Downloader for Snips assistants. """

    @staticmethod
    def download(url, output_dir, assistant_filename):
        """ Download an assistant, and save it to a file.

        :param url: the assistant URL.
        :param output_dir: the directory where the assistant should be
                           saved.
        """
        try:
            response = urlopen(url)
        except Exception:
            raise AssistantDownloaderException()

        AssistantDownloader.save_assistant(response.read(),
                                           output_dir, assistant_filename)

    @staticmethod
    def save_assistant(content, output_dir, assistant_filename):
        """ Save content of an assisant.

        :param content: the content of the file to save.
        :param output_dir: the directory where the assistant should be
                           saved.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_filename = "{}/{}".format(output_dir, assistant_filename)
        with open(output_filename, "wb") as output_file:
            output_file.write(content)
