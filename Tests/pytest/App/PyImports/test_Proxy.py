import sys
import os
import pytest
from pytest_mock import mocker
from _pytest import monkeypatch

from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl

from PyImports.Calculators.CryspyCalculator import *
from PyImports.Models.MeasuredDataModel import *
from PyImports.Models.CalculatedDataModel import *
from PyImports.Models.BraggPeaksModel import *
from PyImports.Models.CellParametersModel import *
from PyImports.Models.CellBoxModel import *
from PyImports.Models.AtomSitesModel import *
from PyImports.Models.AtomAdpsModel import *
from PyImports.Models.AtomMspsModel import *
from PyImports.Models.FitablesModel import *
from PyImports.Refinement import *
import PyImports.Helpers as Helpers

# tested module
from Proxy import *

TEST_FILE = "file:Tests/Data/main.rcif"
def test_Proxy_properties():
    proxy = Proxy()
    assert proxy._main_rcif_path == None
    assert proxy._refinement_running == False
    assert proxy._refinement_done == False

def test_Proxy_init():
    proxy = Proxy()
    proxy.init(TEST_FILE)
    assert proxy._main_rcif_path == "Tests/Data/main.rcif"
    assert isinstance(proxy._project_model, CryspyCalculator)
    assert isinstance(proxy._measured_data_model, MeasuredDataModel)
    assert isinstance(proxy._calculated_data_model, CalculatedDataModel)
    assert isinstance(proxy._bragg_peaks_model, BraggPeaksModel)
    assert isinstance(proxy._cell_parameters_model, CellParametersModel)
    assert isinstance(proxy._cell_box_model, CellBoxModel)
    assert isinstance(proxy._atom_sites_model, AtomSitesModel)
    assert isinstance(proxy._atom_adps_model, AtomAdpsModel)
    assert isinstance(proxy._atom_msps_model, AtomMspsModel)
    assert isinstance(proxy._fitables_model, FitablesModel)
    assert isinstance(proxy._refine_thread, Refiner)

    assert "\\easyDiffraction\\Tests\\Data" in proxy.project_dir_absolute_path
    assert "file:Tests/Data" in proxy.project_url_absolute_path

def test_Proxy_getProject():
    proxy = Proxy()
    assert proxy.getProject() == ""
    proxy.init(TEST_FILE)
    assert isinstance(proxy.getProject(), dict)

def test_Proxy_getCif():
    proxy = Proxy()
    assert proxy.getCif() == ""
    proxy.init(TEST_FILE)
    assert isinstance(proxy.getCif(), dict)

def test_Proxy_getMeasuredDataHeader():
    proxy = Proxy()
    assert isinstance(proxy.getMeasuredDataHeader(), QStandardItemModel)
    assert proxy.getMeasuredDataHeader().rowCount() == 0
    assert proxy.getMeasuredDataHeader().columnCount() == 0
    proxy.init(TEST_FILE)
    assert proxy.getMeasuredDataHeader().rowCount() == 1
    assert proxy.getMeasuredDataHeader().columnCount() == 7

def test_Proxy_getMeasuredData():
    proxy = Proxy()
    assert isinstance(proxy.getMeasuredData(), QStandardItemModel)
    assert proxy.getMeasuredData().rowCount() == 0
    assert proxy.getMeasuredData().columnCount() == 0
    proxy.init(TEST_FILE)
    assert proxy.getMeasuredData().rowCount() == 381
    assert proxy.getMeasuredData().columnCount() == 7

def test_Proxy_getCalculatedDataHeader():
    proxy = Proxy()
    assert isinstance(proxy.getCalculatedDataHeader(), QStandardItemModel)
    assert proxy.getCalculatedDataHeader().rowCount() == 0
    assert proxy.getCalculatedDataHeader().columnCount() == 0
    proxy.init(TEST_FILE)
    assert proxy.getCalculatedDataHeader().rowCount() == 0
    assert proxy.getCalculatedDataHeader().columnCount() == 0

def test_Proxy_getCalculatedData():
    proxy = Proxy()
    assert isinstance(proxy.getCalculatedData(), QStandardItemModel)
    assert proxy.getCalculatedData().rowCount() == 0
    assert proxy.getCalculatedData().columnCount() == 0
    proxy.init(TEST_FILE)
    assert proxy.getCalculatedData().rowCount() == 381
    assert proxy.getCalculatedData().columnCount() == 4

def test_Proxy_getBraggPeaks():
    proxy = Proxy()
    assert isinstance(proxy.getBraggPeaks(), QStandardItemModel)
    assert proxy.getBraggPeaks().rowCount() == 0
    assert proxy.getBraggPeaks().columnCount() == 0
    proxy.init(TEST_FILE)
    assert proxy.getBraggPeaks().rowCount() == 95
    assert proxy.getBraggPeaks().columnCount() == 4

def test_Proxy_getBraggPeaksTicks():
    proxy = Proxy()
    assert isinstance(proxy.getBraggPeaksTicks(), QStandardItemModel)
    assert proxy.getBraggPeaksTicks().rowCount() == 0
    assert proxy.getBraggPeaksTicks().columnCount() == 0
    proxy.init(TEST_FILE)
    assert proxy.getBraggPeaksTicks().rowCount() == 665
    assert proxy.getBraggPeaksTicks().columnCount() == 2

def test_Proxy_getCellParameters():
    proxy = Proxy()
    assert isinstance(proxy.getCellParameters(), QStandardItemModel)
    assert proxy.getCellParameters().rowCount() == 0
    assert proxy.getCellParameters().columnCount() == 0
    proxy.init(TEST_FILE)
    assert proxy.getCellParameters().rowCount() == 1
    assert proxy.getCellParameters().columnCount() == 1

def test_Proxy_getCellBox():
    proxy = Proxy()
    assert isinstance(proxy.getCellBox(), QStandardItemModel)
    assert proxy.getCellBox().rowCount() == 0
    assert proxy.getCellBox().columnCount() == 0
    proxy.init(TEST_FILE)
    assert proxy.getCellBox().rowCount() == 3084
    assert proxy.getCellBox().columnCount() == 1

def test_Proxy_getAtomSites():
    proxy = Proxy()
    assert isinstance(proxy.getAtomSites(), QStandardItemModel)
    assert proxy.getAtomSites().rowCount() == 0
    assert proxy.getAtomSites().columnCount() == 0
    proxy.init(TEST_FILE)
    assert proxy.getAtomSites().rowCount() == 3
    assert proxy.getAtomSites().columnCount() == 1

def test_Proxy_getAtomAdps():
    proxy = Proxy()
    assert isinstance(proxy.getAtomAdps(), QStandardItemModel)
    assert proxy.getAtomAdps().rowCount() == 0
    assert proxy.getAtomAdps().columnCount() == 0
    proxy.init(TEST_FILE)
    assert proxy.getAtomAdps().rowCount() == 3
    assert proxy.getAtomAdps().columnCount() == 1

def test_Proxy_getAtomMsps():
    proxy = Proxy()
    assert isinstance(proxy.getAtomMsps(), QStandardItemModel)
    assert proxy.getAtomMsps().rowCount() == 0
    assert proxy.getAtomMsps().columnCount() == 0
    proxy.init(TEST_FILE)
    assert proxy.getAtomMsps().rowCount() == 3
    assert proxy.getAtomMsps().columnCount() == 1

def test_Proxy_getFitables():
    proxy = Proxy()
    assert isinstance(proxy.getFitables(), QStandardItemModel)
    assert proxy.getFitables().rowCount() == 0
    assert proxy.getFitables().columnCount() == 0
    proxy.init(TEST_FILE)
    assert proxy.getFitables().rowCount() == 34
    assert proxy.getFitables().columnCount() == 1

def no_test_refine(qtbot, capsys):  # to be modified with AS's changes
    proxy = Proxy()
    proxy.init(TEST_FILE)

    assert proxy._refinement_running == False
    captured = capsys.readouterr()

    with qtbot.waitSignal(proxy._refine_thread.finished, timeout=60000) as blocker:
        blocker.connect(proxy._refine_thread.failed)  # Can add other signals to blocker
        proxy._refine_thread.start()
        # Test will block at this point until signal is emitted or
        # 60 seconds has elapsed

    assert proxy._refinement_running == False
    assert proxy._fit_result == None
    assert captured.err == "" # modify
    assert captured.out == "" # modify
    #assert blocker.finished, "process timed-out"

    #assert_application_results(app)

def test_get_project_dir_absolute_path():
    proxy = Proxy()
    proxy.init(TEST_FILE)

    path = os.path.join('easyDiffraction', 'Tests', 'Data')
    assert path in proxy.get_project_dir_absolute_path()

def test_store_report():
    proxy = Proxy()
    report = "test report"

    proxy.store_report(report)

    assert proxy.report_html == report

def test_save_report(mocker, tmp_path):
    proxy = Proxy()
    proxy.init(TEST_FILE)
    mocker.patch.object(Helpers, 'open_url', autospec=True)

    # no html
    proxy = Proxy()
    proxy.init(TEST_FILE)
    proxy.store_report("")

    proxy.save_report()
    assert Helpers.open_url.called == False

    # good html
    report = "<h1><blink>I am a duck</blink></h1>"
    html = proxy.store_report(report)
    full_filename = "test"

    # temp dir instead of project dir
    tmp_dir = os.path.join(tmp_path,"local_dir")
    mocker.patch.object(proxy, 'get_project_dir_absolute_path', return_value=tmp_path, autospec=True)

    proxy.save_report()
    assert Helpers.open_url.called == True


    


    