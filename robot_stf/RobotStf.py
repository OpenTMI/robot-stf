"""
OpenSTF related keywords for robot-framework for local usage
"""
from robot_stf import __version__
from stf_appium_client import StfClient, Appium, AdbServer
import atexit


class RobotStf:
    """ RobotFramework Lockable plugin """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, hostname, token):
        self._stf = StfClient(hostname)
        self._stf.connect(token)
        self._adb = AdbServer()
        self._appium = Appium()
        self._device = None

    def lock(self, requirements: dict, timeout_seconds: int = 60*60):
        """ Allocate phone and return it's details """
        self._device = self._stf.find_and_allocate(requirements=requirements, timeout_seconds=timeout_seconds)

        @atexit.register
        def exit():
            nonlocal self
            self.exit()

        return self._device

    def exit(self):
        if not self._device:
            return
        if self._device.get('owner') is not None:
            self.logger.warn(f"exit:Release device {self._device.get('serial')}")
            self.unlock()
            self.stop_appium()
            self.stop_adb()

    def unlock(self):
        assert self._device, 'device not locked'
        self._stf.release(self._device)

    def start_adb(self):
        assert self._device, 'device not locked'
        adb_adr = self._stf.remote_connect(self._device)
        self._device['remote_adb_url'] = adb_adr
        self._adb.connect(adb_adr)

    def stop_adb(self):
        assert self._device, 'device not locked'
        self._adb.stop()
        self._stf.remote_disconnect(self._device)
        self._device['remote_adb_url'] = None

    def start_appium(self):
        assert self._device, 'device not locked'
        """ Start appium in local host and return appium url """
        self._appium.start()
        return f'http://localhost:{self._appium.port}'

    def stop_appium(self):
        assert self._device, 'device not locked'
        self._appium.stop()
