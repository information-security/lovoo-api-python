import urllib.parse


# MD5 hashing of an input string
def md5(data: str):
    import hashlib
    return hashlib.md5(data.encode('utf-8')).hexdigest()


def normalize_params(params: dict):
    # Comply with https://tools.ietf.org/html/draft-hammer-oauth-10
    # params must be sorted alphabetically first by keys and then values
    params = dict(sorted(params.items(), key=lambda x: (x[0], x[1]), reverse=False))
    p_encoded = '&'.join(
        ["{}={}".format(urllib.parse.quote_plus(k), urllib.parse.quote_plus(v)) for k, v in params.items() if v != ''])
    # Percent encode
    p_quoted = urllib.parse.quote_plus(p_encoded)
    return p_quoted


def generate_base_string(params: str, url: str, method: str = 'GET'):
    # Comply with https://tools.ietf.org/html/draft-hammer-oauth-10
    base_str = method + '&' + urllib.parse.quote_plus(url) + '&' + params
    return base_str


# Secret hashing used in Lovoo
def secret_hash(pwd: str) -> str:
    pwd = md5("SALTforPW" + pwd)
    return md5("SALTforSecret" + pwd)


def sign_request(client_identifier: str, client_secret: str, token: str, token_secret: str, url: str, nounce: str,
                 timestamp: str, method: str = 'GET', payload: dict = None, callback_url: str = '', oauth_version: str = '1.0'):
    from hashlib import sha1
    import hmac
    import base64

    params = {
        'oauth_callback': callback_url,
        'oauth_consumer_key': client_identifier,
        'oauth_nonce': nounce,
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': timestamp,
        'oauth_token': token,
        'oauth_version': oauth_version
    }

    # Normalize parameters
    if payload is not None:
        params = {**params, **payload}
    np = normalize_params(params)
    # Generate base string
    base_string = generate_base_string(np, url, method)

    if token != '':
        key = (f"{client_secret}&{token_secret}").encode()
    else:
        key = (client_secret + '&').encode()

    raw = base_string.encode()

    hashed = hmac.new(key, raw, sha1)

    # The signature
    return base64.b64encode(hashed.digest()).decode().rstrip('\n')