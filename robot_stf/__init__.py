""" robot-lockable """
from pkg_resources import get_distribution, DistributionNotFound


try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = "unknown"

__pypi_url__ = "https://pypi.python.org/pypi/robot-stf"
__robot_info__ = get_distribution("robotframework")

from robot_stf.RobotStf import RobotStf  # pylint: disable=wrong-import-position
