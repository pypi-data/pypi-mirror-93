import time
from datetime import datetime

try:
    import ujson as json
except ImportError:
    import json

import requests
# from requests_oauthlib import OAuth1
from requests.exceptions import HTTPError, ConnectionError, Timeout

from mysdk.urls import URLs


def __create_auth():
    """A private method to create the OAuth1 object, if necessary."""
    
    pass

def _make_request(url, method='get', data=None):
    """
    Makes a request to the MyShare API
    :param url: URL to be used. (required)
    :param method: HTTP method to be used. Defaults to 'GET'.
    :param data: Should be a dictionary with key-value pairs.
    :return: The result parsed to a JSON dictionary.
    """

    method = method.lower()

    if method == 'get':
        return requests.get(url)
    elif method == 'post':
        return requests.post(url, data=data)
    elif method == 'put':
        return requests.put(url, data=data)
    elif method == 'delete':
        return requests.delete(url, data=data)

