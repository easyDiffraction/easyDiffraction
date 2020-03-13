import sys
import pytest

from easyInterface import logger

ALL = set("darwin linux win32".split())
def pytest_configure(config):
    logger.setLevel(10)
    logger.addSysOutput()

def pytest_runtest_setup(item):
    supported_platforms = ALL.intersection(mark.name for mark in item.iter_markers())
    plat = sys.platform
    if supported_platforms and plat not in supported_platforms:
        pytest.skip("cannot run on platform {}".format(plat))

    