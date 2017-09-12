import json
import urllib2

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
    req = urllib2.Request(url,
                          raw_data,
                          headers)
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
