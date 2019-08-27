##########################################################
#
#  pytest runner for the easyDiffraction program
#
###########################################################
import sys
import os
import pytest
from pytest_mock import mock
from _pytest import monkeypatch

from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine

from App.easyDiffraction import MainWindow

def test_mainWindow(monkeypatch):

    current_location = os.path.abspath(os.path.dirname(sys.argv[1])) # pytest
    script_location = [os.path.join(current_location, '..', '..', 'App', 'easyDiffraction'), os.path.join(current_location, '..', '..', 'App')]
    #assert script_location == 'test'
    monkeypatch.setattr(sys, 'argv', script_location)

    widget = MainWindow()

    # test app
    assert widget.app.organizationName() == 'ESS'
    assert widget.app.organizationDomain() == 'esss.se'
    assert widget.app.applicationName() == 'easyDiffraction'

    assert isinstance(widget.engine, QQmlApplicationEngine)
    assert any('Imports' in s for s in widget.engine.importPathList())

    # test engine
    assert len(widget.engine.rootObjects()) == 1

    proxy = [1,2]
    widget.setupEngine(proxy=proxy)
    assert widget.engine.rootContext().contextProperty("proxy") == [1, 2]

