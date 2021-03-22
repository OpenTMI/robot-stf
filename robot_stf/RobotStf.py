"""
OpenSTF related keywords for robot-framework for local usage
"""
from robot_stf import __version__
from stf_appium_client import StfClient, Appium, AdbServer
import atexit


class RobotStf:
    """ RobotFramework STF plugin """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__
    StfClient = StfClient

    def __init__(self, hostname, token):
        self._stf = self.StfClient(hostname)
        self._stf.connect(token)
        self._devices = list()

        @atexit.register
        def exit():
            nonlocal self
            self.exit()

    def lock(self, requirements: dict, timeout_seconds: int = 60*60):
        """ Allocate phone and return it's details """
        device = self._stf.find_and_allocate(requirements=requirements, timeout_seconds=timeout_seconds)
        self._devices.append(device)
        return device

    def exit(self):
        for device in self._devices:
            if device.get('owner') is not None:
                self.logger.warn(f"exit:Release device {device.get('serial')}")
                self.unlock(device)
                self.stop_appium(device)
                self.stop_adb(device)

    def unlock(self, device):
        assert device.get('owner'), 'device not locked'
        self._stf.release(device)

    def setup_appium(self, device):
        self.start_adb(device)
        self.start_appium(device)

    def teardown_appium(self, device):
        self.stop_adb(device)
        self.stop_appium(device)

    def start_adb(self, device):
        assert device, 'device not locked'
        assert not device.get('adb'), 'device adb is already running'
        adb_adr = self._stf.remote_connect(device)
        device['remote_adb_url'] = adb_adr
        adb = AdbServer(adb_adr)
        device['adb'] = adb
        adb.connect(adb_adr)

    def stop_adb(self, device):
        assert device, 'device not locked'
        adb = device.get('adb')
        assert adb, 'device adb not running'
        adb.stop()
        self._stf.remote_disconnect(device)
        device['remote_adb_url'] = None
        device['adb'] = None

    def start_appium(self, device):
        assert device, 'device not locked'
        assert not device.get('appium'), 'device appium is already running'
        appium = Appium()
        device['appium'] = appium
        """ Start appium in local host and return appium url """
        appium.start()
        return f'http://localhost:{appium.port}'

    def stop_appium(self, device):
        assert device, 'device not locked'
        assert device.get('appium'), 'device appium is not running'
        appium = device.get('appium')
        appium.stop()
        device['appium'] = None
