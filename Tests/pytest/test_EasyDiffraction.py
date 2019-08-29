##########################################################
#
#  pytest runner for the easyDiffraction program
#
#  tests can be run by either typing
#  > pytest Tests
#  or running the wrapper script
#  > python runTests.py
#
###########################################################
import sys
import os
import pytest
from pytest_mock import mocker
from _pytest import monkeypatch

from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine

from App.easyDiffraction import MainWindow

def test_mainWindow(monkeypatch, mocker):

    if len(sys.argv) > 1: # when run directly with pytest
        current_location = os.path.abspath(os.path.dirname(sys.argv[1]))
    else: # when run through the runTests.py wrapper
        current_location = os.path.abspath(os.path.dirname(sys.argv[0])) # pytest
    
    script_location = [os.path.join(current_location, 'App', 'easyDiffraction'), os.path.join(current_location, 'App')]
    # Make the main script think it's been run from the command line by overwriting its sys.argv[]
    monkeypatch.setattr(sys, 'argv', script_location)

    mocker.patch.object(QQmlApplicationEngine, 'load')

    widget = MainWindow()

    # test app
    assert widget.app.organizationName() == 'ESS'
    assert widget.app.organizationDomain() == 'esss.se'
    assert widget.app.applicationName() == 'easyDiffraction'

    assert isinstance(widget.engine, QQmlApplicationEngine)
    assert any('Imports' in s for s in widget.engine.importPathList())

    # test engine
    QQmlApplicationEngine.load.assert_called_once()

    proxy = [1,2]
    widget.setupEngine(proxy=proxy)
    assert widget.engine.rootContext().contextProperty("proxy") == [1, 2]

