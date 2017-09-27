# -*-: coding utf-8 -*-
""" Downloader for Snips assistants. """

from http_helpers import post_request_json
import os
import json
import re

from ..utils.os_helpers import email_is_valid

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen, Request, URLError

USER_AUTH_ROUTE = "https://external-gateway.snips.ai/v1/user/auth"

class Auth:

    @staticmethod
    def retrieve_token(self, email, password):
        data = { 'email': email, 'password': password }
        response, response_headers = post_request_json(AUTH_URL, data)
        token = response_headers.getheader('Authorization')
        return token


class AuthException(Exception):
    pass


class AuthExceptionInvalidCredentials(AuthException):
    pass


class AuthExceptionInvalidAssistantId(AuthException):
    pass


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

    def __init__(self, email, password, assistantId):
        self.email = email
        self.password = password
        self.assistant_id = assistantId
        self.validate_input()


    @property
    def auth_url(self):
        raise NotImplementedError

    @property
    def download_url(self):
        raise NotImplementedError

    def validate_input(self):
        if not email_is_valid(self.email):
            raise AuthExceptionInvalidCredentials("Error, Email is not valid")

        if len(self.password) < 1:
            raise AuthExceptionInvalidCredentials("Error, password is too short")

        if len(self.assistant_id) < 14:
            raise AuthExceptionInvalidAssistantId("Error, assistantId is too short")

    def retrieve_auth_token(self):
        data = {'email': self.email, 'password': self.password}

        try:
            response, response_headers = post_request_json(self.auth_url, data)
            token = response_headers.getheader('Authorization')
            return token
        except URLError:
            raise DownloaderException

    def download(self, output_dir, filename):
        try:
            token = self.retrieve_auth_token()
            request = Request(self.download_url, headers={'Authorization': token, 'Accept': 'application/json'})
            response = urlopen(request)
        except Exception:
            raise DownloaderException()

        Downloader.save(response.read(),
                        output_dir,
                        filename)


class AssistantDownloader(AuthDownloader):
    auth_url = "https://external-gateway.snips.ai/v1/user/auth"
    download_url = "https://external-gateway.snips.ai/v1/assistant/{}/download"

    def __init__(self, email, password, assistantId):
        AuthDownloader.__init__(self, email, password, assistantId)
        self.download_url = self.download_url.format(self.assistant_id)
