# -*-: coding utf-8 -*-
""" Downloader for Snips assistants. """

import os
import json
from http_helpers import post_request_json

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen, Request, URLError

USER_AUTH_ROUTE = "https://private-gateway-dev.snips.ai/v1/user/auth"

class DownloaderException(Exception):
    """ Exceptions related to downloads of Snips assistants. """
    pass

# pylint: disable=too-few-public-methods
class Downloader(object):
    """ Downloader for Snips assistants. """

    @staticmethod
    def download(url, output_dir, filename):
        """ Download a file, and save it to a file.

        :param url: the URL of the file.
        :param output_dir: the directory where the file should be
                           saved.
        """
        try:
            response = urlopen(url)
        except Exception:
            raise DownloaderException()

        Downloader.save(response.read(),
                        output_dir,
                        filename)

    @staticmethod
    def save(content, output_dir, filename):
        """ Save content of a file.

        :param content: the content of the file to save.
        :param output_dir: the directory where the assistant should be
                           saved.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_filename = "{}/{}".format(output_dir, filename)
        with open(output_filename, "wb") as output_file:
            output_file.write(content)


class AuthDownloader(Downloader):
    def __init__(self, email, password):
        self.auth_url = USER_AUTH_ROUTE
        self.email = email
        self.password = password

    def retrieve_auth_token(self):
        data = {'email': self.email, 'password': self.password }

        try:
            response, response_headers = post_request_json(self.auth_url, data)
            token = response_headers.getheader('Authorization')
            return token
        except URLError:
            raise DownloaderException


    def download(self, url, output_dir, filename):
        try:
            token = self.retrieve_auth_token()
            request = Request(url, headers={'Authorization': token})
            response = urlopen(request)
            print response
        except Exception:
            raise DownloaderException()

        Downloader.save(response.read(),
                        output_dir,
                        filename)



