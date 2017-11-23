# -*-: coding utf-8 -*-
""" Downloader for Snips assistants. """

import requests

class Auth:

    AUTH_URL = "https://external-gateway.snips.ai/v1/user/auth"
    AUTH_VALIDATE_URL = "https://external-gateway.snips.ai/v1/user/validate"

    @staticmethod
    def retrieve_token(email, password):
        data = { 'email': email, 'password': password }
        response = requests.post(Auth.AUTH_URL, json=data)
        token = response.headers['Authorization']
        return token

    @staticmethod
    def validate_token(token):
        if token is None:
            return False

        response = requests.post(Auth.AUTH_VALIDATE_URL, json={'token': token}, headers={'Authorization': token, 'Accept': 'application/json'})
        if (response.status_code == 200):
            return True
        return False