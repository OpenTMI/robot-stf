"""
OpenSTF related keywords for robot-framework for local usage
"""
import atexit
from RobotStf import __version__
from stf_appium_client import StfClient, Appium, AdbServer
from stf_appium_client.Logger import Logger
from stf_appium_client.tools import parse_requirements


def as_seconds(minutes: int):
    return minutes * 60


class RobotStf(Logger):
    """ RobotFramework STF plugin """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__
    StfClient = StfClient

    def __init__(self, hostname, token):
        super().__init__()
        self._stf = self.StfClient(hostname)
        self._stf.connect(token)
        self._devices = list()

        @atexit.register
        def exit():
            nonlocal self
            self.exit()

    def lock(self,
             requirements: str,
             wait_timeout=as_seconds(minutes=5),
             timeout_seconds: int = as_seconds(minutes=30),
             shuffle: bool = True):
        """ Allocate phone and return it's details """
        if isinstance(requirements, str):
            requirements = parse_requirements(requirements)
        self.logger.info(f'Requirements: {requirements}')
        device = self._stf.find_wait_and_allocate(
            requirements=requirements,
            wait_timeout=wait_timeout,
            timeout_seconds=timeout_seconds,
            shuffle=shuffle)
        self._devices.append(device)
        return device

    def exit(self):
        for device in self._devices:
            if device.get('owner') is not None:
                self.logger.warn(f"exit:Release device {device.get('serial')}")
                self.teardown_appium(device)
                try:
                    self.unlock(device)
                except Exception as error:
                    self.logger.warn(error)

    def unlock(self, device: dict):
        assert device.get('owner'), 'device not locked'
        self._stf.release(device)

    def setup_appium(self, device):
        self.start_adb(device)
        self.start_appium(device)

    def teardown_appium(self, device: dict):
        try:
            self.stop_appium(device)
        except AssertionError:
            pass
        try:
            self.stop_adb(device)
        except AssertionError:
            pass

    def start_adb(self, device: dict):
        assert device, 'device not locked'
        assert not device.get('adb'), 'device adb is already running'
        adb_adr = self._stf.remote_connect(device)
        device['remote_adb_url'] = adb_adr
        adb = AdbServer(adb_adr)
        device['adb'] = adb
        device['adb_port'] = adb.port
        adb.connect()
        return adb.port

    def stop_adb(self, device: dict):
        assert device, 'device not locked'
        adb = device.get('adb')
        assert adb, 'device adb not running'
        adb.kill()
        self._stf.remote_disconnect(device)
        device['remote_adb_uri'] = None
        device['adb'] = None
        device['adb_port'] = None

    def start_appium(self, device: dict):
        assert device, 'device not locked'
        assert not device.get('appium'), 'device appium is already running'
        appium = Appium()
        device['appium'] = appium
        """ Start appium in local host and return appium url """
        appium_uri = appium.start()
        device['appium_uri'] = appium_uri
        return appium_uri

    def stop_appium(self, device: dict):
        assert device, 'device not locked'
        assert device.get('appium'), 'device appium is not running'
        appium = device.get('appium')
        appium.stop()
        device['appium'] = None
        device['appium_uri'] = None
