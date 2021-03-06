import unittest
from shutil import which
from unittest.mock import patch
from RobotStf.RobotStf import RobotStf


class TestRobotStf(unittest.TestCase):

    @patch('RobotStf.RobotStf.StfClient', autospec=True)
    def test_construct(self, stf_client):
        stf = RobotStf('localhost', 'token')
        self.assertIsInstance(stf, RobotStf)
        stf_client.assert_called_once_with('localhost')
        stf._stf.connect.assert_called_once_with('token')

    @patch('RobotStf.RobotStf.StfClient', autospec=True)
    def test_setup_appium(self, stf_client):
        if not (which('adb') and which('appium')):
            self.skipTest('adb or Appium is missing!')
        stf = RobotStf('localhost', 'token')
        stf._stf.find_wait_and_allocate.return_value = {'serial': '1'}
        stf._stf.remote_connect.return_value = 'localhost'
        device = stf.lock({})
        stf.setup_appium(device)
        stf.teardown_appium(device)
