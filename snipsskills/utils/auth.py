# -*-: coding utf-8 -*-
""" Downloader for Snips assistants. """

from http_helpers import post_request_json

class Auth:

    AUTH_URL = "https://external-gateway.snips.ai/v1/user/auth"

    @staticmethod
    def retrieve_token(email, password):
        data = { 'email': email, 'password': password }
        response, response_headers = post_request_json(Auth.AUTH_URL, data)
        token = response_headers.getheader('Authorization')
        return token
