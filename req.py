#import logging
import requests
import json

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def request(url, params, data, type, headers):

    #   A wrapper for python requests module with retries.
    #   Performs a request, if HTTP Response is 500 - 504, retries with exponential back-off
    #   Supports get, post and put requests

    max_reties = 5
    backoff_factor = 0.3
    #logging.basicConfig(level=logging.DEBUG)
    output = {}

    try:
        s = requests.Session()
        retries = Retry(total=max_reties, backoff_factor=backoff_factor, status_forcelist=[ 500, 502, 503, 504 ])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        s.mount('https://', HTTPAdapter(max_retries=retries))

        if type == 'get':
            r = s.get(url, params=params, data=data, timeout=30, headers=headers)
            output['response'] = r
            return output
        elif type == 'post':
            r = s.post(url, params=params, data=data, timeout=30, headers=headers)
            output['response'] = r
            return output
        elif type == 'put':
            r = s.put(url, params=params, data=data, timeout=30, headers=headers)
            output['response'] = r
            return output
        else:
            output['error'] = "Error: Invalid request type %s" % type
            return output

    except requests.exceptions.RequestException as e:
        output['error'] = e
        return output

def request_json(url, params, data, type, headers):

    output = {}

    #   A wrapper for request function to keep error handling code away from main code block
    #   Requests json from a HTTP endpoint. Returns error if not valid json
    #   Supports get, post and put requests

    r = request(url, params, data, type, headers)
    if 'response' in r:
        if r['response'].status_code == 200:
            try:
                json.loads(r['response'].text)
                output['response'] = r['response'].json()
                return output
            except Exception as e:
                output['error'] = "Error (No valid json response): %s" % e
                return output
        else:
            output['error'] = "Error (HTTP %d): %s" % (r['response'].status_code, r['response'].text)
            return output
    else:
        output['error'] = "Error (No valid response from server): %s" % r['error']
        return output
