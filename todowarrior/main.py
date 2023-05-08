#!/usr/bin/env python
"""
Todowarrior - Synchronize Toodledo and Taskwarrior

This file doesn't include a "usage" because it's still not usable.

For more information, see the file README.md.
"""

import base64
import json
import os
import secrets
import string
import sys
import urllib.parse
from urllib.parse import urlparse, parse_qs

import requests

REQUESTS_TIMEOUT_SECONDS = 30


def get_access_token_from_login():
    # Toodledo OAuth2 settings
    toodledo_client_envvar = os.getenv('TOODLEDO_CLIENT')
    toodledo_client_id, toodledo_client_secret = toodledo_client_envvar.split(
        ':')

    random_string = ''.join(
        secrets.choice(string.ascii_uppercase + string.digits)
        for _ in range(8))

    # Generate the authorization URL and prompt the user to authorize the app
    site = ('https://api.toodledo.com/3/account/authorize.php' +
            f'?response_type=code&client_id={toodledo_client_id}' +
            f'&state={random_string}&scope=basic%20tasks')
    print('Please go to this URL to authorize the application:', site)

    # Get the authorization code from the user
    authorization_code_full_uri = input(
        '\nEnter the authorization code from the website: ')

    query = parse_qs(urlparse(authorization_code_full_uri).query)
    if secrets.compare_digest(query['state'][0], random_string) is False:
        sys.exit('Error in URI')

    authorization_code = query['code'][0]

    # Exchange the authorization code for an access token
    client_id = urllib.parse.quote(toodledo_client_id.encode('utf8'))
    client_secret = urllib.parse.quote(toodledo_client_secret.encode('utf8'))

    code_bytes = f"{client_id}:{client_secret}".encode('ascii')
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

    response = requests.post(url,
                             data=data,
                             headers=headers,
                             timeout=REQUESTS_TIMEOUT_SECONDS)
    access_token = json.loads(response.text)['access_token']
    # TODO: use refresh token
    return access_token


def main(_argv):
    access_token = get_access_token_from_login()

    print('\nGetting data')
    url = ('http://api.toodledo.com/3/tasks/get.php' +
           f'?access_token={access_token}')

    response = requests.post(url, timeout=REQUESTS_TIMEOUT_SECONDS)
    print(response)
    print(response.text)
    print()

    tasks = json.loads(response.text)

    for task in tasks[1:]:
        print(task['title'])


if __name__ == "__main__":
    main(sys.argv)
