#!/usr/bin/env python

import base64
import json
import os
import random
import requests
import string
import sys
import urllib.parse
from urllib.parse import urlparse, parse_qs


def get_access_token_from_login():
    # Toodledo OAuth2 settings
    toodledo_client_envvar = os.getenv('TOODLEDO_CLIENT')
    TOODLEDO_CLIENT_ID, TOODLEDO_CLIENT_SECRET = toodledo_client_envvar.split(
        ':')

    random_string = ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=8))

    # Generate the authorization URL and prompt the user to authorize the app
    site = (f'https://api.toodledo.com/3/account/authorize.php' +
            f'?response_type=code&client_id={TOODLEDO_CLIENT_ID}' +
            f'&state={random_string}&scope=basic%20tasks')
    print('Please go to this URL to authorize the application:', site)

    # Get the authorization code from the user and exchange it for an access token
    authorization_code_full_uri = input(
        '\nEnter the authorization code from the website: ')

    query = parse_qs(urlparse(authorization_code_full_uri).query)
    if query['state'][0] != random_string:
        sys.exit('Error in URI')

    authorization_code = query['code'][0]

    client_id = urllib.parse.quote(TOODLEDO_CLIENT_ID.encode('utf8'))
    clientSecret = urllib.parse.quote(TOODLEDO_CLIENT_SECRET.encode('utf8'))

    code_bytes = f"{client_id}:{clientSecret}".encode('ascii')
    base64_bytes = base64.b64encode(code_bytes)
    base64_code = base64_bytes.decode('ascii')

    url = "https://api.toodledo.com/3/account/token.php"

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': f"Basic {base64_code}"
    }

    data = {
        "grant_type": "authorization_code",
        'code': authorization_code,
    }

    response = requests.post(url, data=data, headers=headers)
    access_token = json.loads(response.text)['access_token']
    # TODO: use refresh token
    return access_token


def main(argv):
    access_token = get_access_token_from_login()
    EPOCH = 1672542000

    print('\nGetting data')
    url = ('http://api.toodledo.com/3/tasks/get.php' +
           f'?access_token={access_token}&after={EPOCH}')

    response = requests.post(url)
    print(response)
    print(response.text)
    print()

    tasks = json.loads(response.text)

    for task in tasks[1:]:
        print(task['title'])


if __name__ == "__main__":
    main(sys.argv)
