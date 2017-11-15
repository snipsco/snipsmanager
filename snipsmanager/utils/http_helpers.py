# -*-: coding utf-8 -*-
""" HTTP helpers. """

import json
import urllib2

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

def post_request(url, data, headers):
    """
    :param url:
    :type url: basestring
    :param data:
    :type data: dict
    :param headers:
    :type headers: dict
    :return:
    :rtype: basestring
    """
    raw_data = json.dumps(data)
    req = Request(url, raw_data, headers)
    f = urllib2.urlopen(req)
    info = f.info()
    response = f.read()
    f.close()
    return response, info

def post_request_json(url, data, headers={}):
    """

    :param url:
    :type url: basestring
    :param data:
    :type data: dict
    :param headers:
    :type headers: dict
    :return:
    :rtype: dict
    """
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'

    response, info = post_request(url, data, headers)
    return json.loads(response), info

def fetch_url(url, headers=None):
    if headers is None:
        return urlopen(url).read()
    else:
        return urlopen(Request(url, headers=headers)).read()
