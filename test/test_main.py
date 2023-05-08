#!/usr/bin/env python
"""
Unit test for Todowarrior.main

Usage: pylint -v

For more information, se the file README.md
"""

import os
import unittest
from unittest import mock

from todowarrior.main import get_access_token_from_login


class TestMain(unittest.TestCase):
    """
    This is the only testclass for this project
    """

    @mock.patch.dict(os.environ, {"TOODLEDO_CLIENT": "client_id:secret"},
                     clear=True)
    @mock.patch('secrets.choice')
    @mock.patch('builtins.input')
    @mock.patch('requests.post')
    def test_get_access_token_from_login(self, mock_post, mock_input,
                                         mock_secrets_choice):
        mock_secrets_choice.side_effect = list('12345678')
        mock_input.return_value = (
            'https://example.com/?code=abcdefg&state=12345678')
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
            },
            timeout=30)
        self.assertEqual(result, 'my_access_token')
