#!/usr/bin/env python
"""
Unit test for Todowarrior.main

Usage: pylint -v

For more information, se the file README.md
"""

import os
import pathlib
import unittest
from unittest import mock

from todowarrior.main import get_access_token
from todowarrior.main import get_access_token_from_login


class TestMain(unittest.TestCase):
    """
    This is the only testclass for this project
    """

    @mock.patch('xdg.xdg_config_home')
    @mock.patch('pathlib.Path.is_file')
    @mock.patch('builtins.open')
    @mock.patch('json.load')
    def test_get_access_token_viable_token(self, mock_json_load, mock_open,
                                           mock_is_file, mock_xdg_config_home):
        my_custom_folder = pathlib.Path('my_folder')
        mock_xdg_config_home.return_value = my_custom_folder
        mock_is_file.return_value = True
        mock_json_load.return_value = {"access_token": "01234567abcdef"}
        access_token = get_access_token()
        mock_open.assert_called_once_with(my_custom_folder / 'todowarrior' /
                                          'credentials.json',
                                          encoding='utf-8')
        self.assertEqual('01234567abcdef', access_token)

    @mock.patch('xdg.xdg_config_home')
    @mock.patch('pathlib.Path.is_file', lambda _: False)
    @mock.patch('todowarrior.main.get_access_token_from_login')
    @mock.patch('builtins.open')
    @mock.patch('json.dump')
    def test_get_access_token_file_does_not_exist(
            self, mock_json_dump, mock_open, mock_get_access_token_from_login,
            mock_xdg_config_home):
        my_custom_folder = pathlib.Path('my_folder')
        mock_xdg_config_home.return_value = my_custom_folder
        mock_get_access_token_from_login.return_value = 'my_access_token'
        mock_open.side_effect = mock.mock_open(read_data='1')
        access_token = get_access_token()
        mock_get_access_token_from_login.assert_called_once()
        self.assertEqual('my_access_token', access_token)
        mock_open.assert_called_once_with(my_custom_folder / 'todowarrior' /
                                          'credentials.json',
                                          'w',
                                          encoding='utf-8')
        mock_json_dump.assert_called_once_with(
            {'access_token': 'my_access_token'}, mock_open())

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
