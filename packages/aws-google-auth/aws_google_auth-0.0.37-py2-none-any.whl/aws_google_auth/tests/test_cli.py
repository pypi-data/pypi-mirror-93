import aws_google_auth
# from . import prepare

import unittest
# from unittest.mock import patch
import mock
import datetime
import os

# from aws_google_auth import


class TestCli(unittest.TestCase):

    def setUp(self):
        pass

    # @mock.patch('aws_google_auth.raw_input', return_value='yes')
    # # @mock.patch('getpass.getpass', return_value='yes')
    # def test_when_there_is_no_profile_use_supplied_values(self, ri):
    #
    #     prepare.configparser = mock.Mock()
    #     config_without_non_existing_profile = mock.Mock()
    #     prepare.configparser.RawConfigParser = mock.Mock(return_value=config_without_non_existing_profile)
    #     config_without_non_existing_profile.has_section = mock.Mock(return_value=False)
    #
    #     aws_google_auth.cli([])
    #
    # def test_doesnt_store_none_profile(self):
    #
    #     # Given a profile has not been supplied
    #     config = type('', (), {})()
    #     config.profile = None
    #
    #     # When configuration is stored
    #     aws_google_auth._store.store_config = mock.Mock()
    #
    #     aws_google_auth._store(config=config,
    #                            aws_session_token=None)
    #
    #     # Then the configuration is not actually stored
    #     self.assertFalse(aws_google_auth._store.store_config.called)
    #
    # # @mock.patch('aws_google_auth._store.store_config')
    # def test_stores_default_profile(self, store_config=None):
    #
    #     # Given a profile has not been supplied
    #     config = type('', (), {})()
    #     config.profile = 'default'
    #     config.aws_credentials_location = '/tmp/creds'
    #     config.aws_config_location = '/tmp/config'
    #
    #     aws_session_token = {'Credentials': {'AccessKeyId': 'blart',
    #                                          'SecretAccessKey': 'bling',
    #                                          'SessionToken': 'blarg',
    #                                          'Expiration': datetime.datetime.now()}}
    #
    #     print aws_google_auth._store.store_config
    #
    #     # When configuration is stored
    #     aws_google_auth._store(config=config,
    #                            aws_session_token=aws_session_token)
    #
    #     # Then the configuration is not actually stored
    #     self.assertFalse(store_config.called)