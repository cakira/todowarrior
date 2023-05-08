#!/usr/bin/env python

import os
import unittest
from unittest import mock

from todowarrior.main import get_access_token_from_login


class TestMain(unittest.TestCase):

    @mock.patch.dict(os.environ, {"TOODLEDO_CLIENT": "client_id:secret"},
                     clear=True)
    @mock.patch('random.choices', return_value=list('12345678'))
    @mock.patch('builtins.input',
                return_value='https://example.com/?code=abcdefg&state=12345678'
                )
    @mock.patch('requests.post')
    def test_get_access_token_from_login(self, mock_post, mock_input,
                                         mock_random_choices):
        mock_post.return_value.text = '{"access_token": "my_access_token"}'
        result = get_access_token_from_login()
        mock_post.assert_called_once_with(
            'https://api.toodledo.com/3/account/token.php',
            data={
                'grant_type': 'authorization_code',
                'code': 'abcdefg'
            },
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic Y2xpZW50X2lkOnNlY3JldA=='
            })
        self.assertEqual(result, 'my_access_token')
