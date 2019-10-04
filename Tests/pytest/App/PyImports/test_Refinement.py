import sys
import os
import pytest
from pytest_mock import mocker
from _pytest import monkeypatch

from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl

# tested module
from PyImports.Refinement import *

class tstRefiner():
    def tstRun(self):
        return "done"
    def tstBadRun(self):
        raise RuntimeError("friday")

def test_Refiner(qtbot):
    refiner = tstRefiner()
    r = Refiner(refiner, 'tstRun')

    assert isinstance(r._obj, tstRefiner)
    assert r.method_name == 'tstRun'

    # run the good "refinement"
    with qtbot.waitSignal(r.finished):
        result = r.run()
    assert result == 'done'

    # run the bad "refinement"
    r = Refiner(refiner, 'tstBadRun')
    with qtbot.waitSignal(r.failed):
        result = r.run()
    assert result == 'friday'
