# -*-: coding utf-8 -*-
""" Downloader for Snips assistants. """

import requests

class Auth:

    AUTH_URL = "https://external-gateway.snips.ai/v1/user/auth"

    @staticmethod
    def retrieve_token(email, password):
        data = { 'email': email, 'password': password }
        response = requests.post(Auth.AUTH_URL, json=data)
        token = response.headers['Authorization']
        return token
