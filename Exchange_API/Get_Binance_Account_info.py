import urllib.parse
import hashlib
import hmac
import base64
import requests
import time
import json

api_key = ''
secret_key = ''
api_url = "https://api.binance.us"

# get binanceus signature
def get_binanceus_signature(data, secret):
    postdata = urllib.parse.urlencode(data)
    message = postdata.encode()
    byte_key = bytes(secret, 'UTF-8')
    mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
    return mac

# Attaches auth headers and returns results of a POST request
def binanceus_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['X-MBX-APIKEY'] = api_key
    signature = get_binanceus_signature(data, api_sec)
    params={
        **data,
        "signature": signature,
        }
    req = requests.get((api_url + uri_path), params=params, headers=headers)
    return req.text

uri_path = "/api/v3/account"
data = {
    "timestamp": int(round(time.time() * 1000)),
}

get_account_result = binanceus_request(uri_path, data, api_key, secret_key)

result_obj = json.loads(get_account_result)

print("GET {}: {}".format(uri_path, json.dumps(result_obj, indent=4)))