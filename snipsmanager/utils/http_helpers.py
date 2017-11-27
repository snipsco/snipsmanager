# -*-: coding utf-8 -*-
""" HTTP helpers. """

import json
import urllib2
import requests
from ..commands.session.login import Login

try:
    from urllib.request import urlopen, Request
    import requests
except ImportError:
    from urllib2 import urlopen, Request
    import requests

def fetch_url(url, headers=None):
    if headers is None:
        return urlopen(url).read()
    else:
        return urlopen(Request(url, headers=headers)).read()

def check_auth(f):
    def decorated(*args, **kwargs):
        response = f(*args, **kwargs)
        if (type(response) is not requests.Response):
            return response
        if (response.status_code == 401):
            raise InvalidTokenException("Could not validate authentication token")
        response.raise_for_status()
        return response

    return decorated

