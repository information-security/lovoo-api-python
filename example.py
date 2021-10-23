import api
import urllib.parse
import requests
import json
import time
import uuid


# # An example not related to Lovoo
# CONSUMER_KEY = 'dpf43f3p2l4k3l03'
# CLIENT_SECRET = 'kd94hf93k423kf44'
# TOKEN = ''
# TOKEN_SECRET = ''
# URL = 'https://photos.example.net/initiate'
# NOUNCE = 'wIjqoS'
# TIMESTAMP = '137131200'
# CALLBACK_URL = 'http://printer.example.com/ready'
# signature = sign_request(CONSUMER_KEY, CLIENT_SECRET, TOKEN, TOKEN_SECRET, URL, NOUNCE, TIMESTAMP, 'POST', CALLBACK_URL,
#                          '')
#
# print('sig:', signature)
# print('sig_quote:', urllib.parse.quote_plus(signature), "\n\n")
#
# # Example 1, Lovoo
# # Secret encoding
# client_secret = secret_hash('[----------- PASSWORD ----------]')
# CONSUMER_KEY = '[---------         EMAIL ADDRESS     ---------]'
# CLIENT_SECRET = client_secret
# TOKEN = ''
# TOKEN_SECRET = ''
# URL = 'https://api.lovoo.com/oauth/requestToken'
# NOUNCE = '1067181181103988144'
# TIMESTAMP = '1611253904'
# CALLBACK_URL = ''
# signature = sign_request(CONSUMER_KEY, CLIENT_SECRET, TOKEN, TOKEN_SECRET, URL, NOUNCE, TIMESTAMP)
#
# print('sig:', signature)
# print('sig_quote:', urllib.parse.quote_plus(signature), "\n\n")
#
# # Example 2, Lovoo
# # Secret encoding
# client_secret = secret_hash('[----------- PASSWORD ----------]')
# CONSUMER_KEY = '[---------         EMAIL ADDRESS     ---------]'
# CLIENT_SECRET = client_secret
# TOKEN = '129ca30332c4'
# TOKEN_SECRET = 'd225563be3355831'
# URL = 'https://api.lovoo.com/oauth/accessToken'
# NOUNCE = '-7073626281147787265'
# TIMESTAMP = '1611253904'
# CALLBACK_URL = ''
# signature = sign_request(CONSUMER_KEY, CLIENT_SECRET, TOKEN, TOKEN_SECRET, URL, NOUNCE, TIMESTAMP)
#
# print('sig:', signature)
# print('sig_quote:', urllib.parse.quote_plus(signature), "\n\n")

# client_secret = secret_hash('[----------- PASSWORD ----------]')
# CONSUMER_KEY = '[---------         EMAIL ADDRESS     ---------]'
# CLIENT_SECRET = client_secret
# TOKEN = 'f125dd330dfea749'
# TOKEN_SECRET = '814620fe0182813523f1a0b6'
# URL = 'https://api.lovoo.com/conversations' #?requests=none&resultLimit=40&resultPage=1&sort=distance
# NOUNCE = '966633488118422596'
# TIMESTAMP = '1614226470'
# CALLBACK_URL = ''
# payload = {
#     'requests': 'none',
#     'resultLimit': '40',
#     'resultPage': '1',
#     'sort': 'distance'
# }
# signature = sign_request(CONSUMER_KEY, CLIENT_SECRET, TOKEN, TOKEN_SECRET, URL, NOUNCE, TIMESTAMP, 'GET', payload)
# signature_quoted = urllib.parse.quote_plus(signature)
#
# print('sig:', signature)
# print('sig_quote:', signature_quoted)

if __name__ == '__main__':


    headers = {
        'accept': 'application/json',
        'kissapi-app-version': '9100',
        'kissapi-version': '1.35.0',
        'kissapi-device-os': '23',
        'kissapi-device-model': 'Samsung Galaxy S7',
        'tz': 'America/New_York',
        'kissapi-device': 'android',
        'kissapi-app-package-id': 'net.lovoo.android',
        'kissapi-android-fingerprint': 'Android/vbox86p/vbox86p:6.0/MRA58K/634:userdebug/test-keys',
        'kissapi-app': 'lovoo',
        'kissapi-apptype': 'google',
        'user-agent': 'LOVOO/9100 Dalvik/2.1.0 (Linux; U; Android 6.0; Samsung Galaxy S7 Build/MRA58K) okhttp/3.12.3',
        'authorization': 'OAuth oauth_consumer_key="USERNAME%40gmail.com", oauth_nonce="966633488118422596", oauth_signature="p26woLrirSAeKp2WJB46sbrVYBY%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1614226470", oauth_token="f125dd330dfea749", oauth_version="1.0"',
        'kissapi-android-id': '976e8f61b02ca8c',
        'kissapi-app-id': 'cba29289-508f-4bae-b50e-3f243e1a887c?identifier=lovoo.prod.firebase',
        'kissapi-gpsa-id': 'cba29289-508f-4bae-b50e-3f243e1a887c?identifier=lovoo.prod.firebase',
        'kissapi-gpsa-on': 'true',
        'kissapi-mac': 'aba6d505ed142b7f2667eee7cd06efd0',
        'kissapi-notihash': 'e3959d398ac3',
        'kissapi-update-user-hash': 'c0d7b24b0bbb770e35549a938604ca57',
        'kissapi-ad-id': '119075c86648e9c96f647867f90afb98',
        'kissapi-ad-name': 'Organic'
    }


    CONSUMER_KEY = input('Enter your email address: ')
    client_secret = api.secret_hash(input('Enter your password: '))
    print(str(int(time.time())))
    print(CONSUMER_KEY)

   #################### REQUEST TOKEN

    CONSUMER_KEY_QUOTED = urllib.parse.quote_plus(CONSUMER_KEY)
    CLIENT_SECRET = client_secret
    TOKEN = ''
    TOKEN_SECRET = ''
    URL = 'https://api.lovoo.com/oauth/requestToken'
    NOUNCE = str(uuid.uuid1().time)
    TIMESTAMP = str(int(time.time()))
    CALLBACK_URL = ''
    signature = api.sign_request(CONSUMER_KEY, CLIENT_SECRET, TOKEN, TOKEN_SECRET, URL, NOUNCE, TIMESTAMP)
    signature_quoted = urllib.parse.quote_plus(signature)

    print('sig:', signature)
    print('sig_quote:', signature_quoted)

    headers['authorization'] = f'OAuth oauth_consumer_key="{CONSUMER_KEY_QUOTED}", oauth_nonce="{NOUNCE}", oauth_signature="{signature_quoted}", oauth_signature_method="HMAC-SHA1", oauth_timestamp="{TIMESTAMP}"'
    if TOKEN != '':
        headers['authorization'] += f', oauth_token="{TOKEN}", oauth_version="1.0"'
    else:
        headers['authorization'] += ', oauth_version="1.0"'

    r = requests.get('https://api.lovoo.com/oauth/requestToken', headers=headers)
    print('Web response:')
    print(r.json(), "\n\n")

    if int(r.json()['statusCode']) != 200:
        exit(0)

    #################### ACCESS TOKEN

    CLIENT_SECRET = client_secret
    TOKEN = r.json()['response']['key']
    TOKEN_SECRET = r.json()['response']['secret']
    URL = 'https://api.lovoo.com/oauth/accessToken'
    NOUNCE = str(uuid.uuid1().time)
    TIMESTAMP = str(int(time.time()))
    CALLBACK_URL = ''
    signature = api.sign_request(CONSUMER_KEY, CLIENT_SECRET, TOKEN, TOKEN_SECRET, URL, NOUNCE, TIMESTAMP)
    signature_quoted = urllib.parse.quote_plus(signature)

    print('sig:', signature)
    print('sig_quote:', signature_quoted)

    headers['authorization'] = f'OAuth oauth_consumer_key="{CONSUMER_KEY_QUOTED}", oauth_nonce="{NOUNCE}", oauth_signature="{signature_quoted}", oauth_signature_method="HMAC-SHA1", oauth_timestamp="{TIMESTAMP}"'
    if TOKEN != '':
        headers['authorization'] += f', oauth_token="{TOKEN}", oauth_version="1.0"'
    else:
        headers['authorization'] += ', oauth_version="1.0"'
    r = requests.get('https://api.lovoo.com/oauth/accessToken', headers=headers)
    print('Web response:')
    print(r.json(), "\n\n")

    if int(r.json()['statusCode']) != 200:
        exit(0)

   #################### GET CONVERSATIONS

    CLIENT_SECRET = client_secret
    TOKEN = r.json()['response']['key']
    TOKEN_SECRET = r.json()['response']['secret']
    URL = 'https://api.lovoo.com/conversations' #?requests=none&resultLimit=40&resultPage=1&sort=distance
    NOUNCE = str(uuid.uuid1().time)
    TIMESTAMP = str(int(time.time()))
    CALLBACK_URL = ''
    payload = {
        'requests': 'none',
        'resultLimit': '40',
        'resultPage': '1',
        'sort': 'distance'
    }
    signature = api.sign_request(CONSUMER_KEY, CLIENT_SECRET, TOKEN, TOKEN_SECRET, URL, NOUNCE, TIMESTAMP, 'GET', payload)
    signature_quoted = urllib.parse.quote_plus(signature)

    print('sig:', signature)
    print('sig_quote:', signature_quoted)

    headers['authorization'] = f'OAuth oauth_consumer_key="{CONSUMER_KEY_QUOTED}", oauth_nonce="{NOUNCE}", oauth_signature="{signature_quoted}", oauth_signature_method="HMAC-SHA1", oauth_timestamp="{TIMESTAMP}"'
    if TOKEN != '':
        headers['authorization'] += f', oauth_token="{TOKEN}", oauth_version="1.0"'
    else:
        headers['authorization'] += ', oauth_version="1.0"'
    r = requests.get('https://api.lovoo.com/conversations?requests=none&resultLimit=40&resultPage=1&sort=distance', headers=headers)
    print('Web response:')
    print(r.json(), "\n\n")
