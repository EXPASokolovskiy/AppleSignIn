import time
import jwt
import requests


with open('cart_file.p8', 'r') as cert_file:
    PRIVATE_KEY = cert_file.read()

ACCESS_TOKEN_URL = 'https://appleid.apple.com/auth/token'

apple_config = {
    "TeamID": "2YU52K5E4A",  # Apple dev team ID
    "ClientID": "com.capital.investmate.test",  # App bundle ID
    "RedirectURI": "",  # Not required
    "KeyID": "FJF7JW8WJY",  # Private Key ID
    "AESCert": PRIVATE_KEY  # Private Key
}

ACCESS_TOKEN = b''  # Access token from Device


def apple_sign_in(token):
    client_secret = get_key_and_secret()

    response_data = {}
    headers = {'content-type': "application/x-www-form-urlencoded"}
    data = {
        'client_id': apple_config["ClientID"],
        'client_secret': client_secret,
        'code': token,
        'grant_type': 'authorization_code',
    }

    res = requests.post(ACCESS_TOKEN_URL, data=data, headers=headers)

    response_dict = res.json()
    id_token = response_dict.get('id_token', None)

    if id_token:
        decoded = jwt.decode(id_token, '', verify=False)
        response_data.update({'email': decoded['email']}) if 'email' in decoded else None
        response_data.update({'uid': decoded['sub']}) if 'sub' in decoded else None

    return response_dict, response_data


def get_key_and_secret():
    headers = {
        'alg': 'ES256',
        'kid': apple_config["KeyID"]
    }

    payload = {
        'iss': apple_config["TeamID"],
        'iat': round(time.time()),
        'exp': round(time.time() + 15776999),
        'aud': 'https://appleid.apple.com',
        'sub': apple_config["ClientID"],
    }

    client_secret = jwt.encode(
        payload,
        apple_config["AESCert"],
        algorithm='ES256',
        headers=headers
    )

    return client_secret


if __name__ == '__main__':
    print(apple_sign_in(ACCESS_TOKEN))
