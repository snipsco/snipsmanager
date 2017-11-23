# -*-: coding utf-8 -*-
""" HTTP helpers. """

import json
import urllib2
import requests

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
