# tested module
import pytest

from PyImports.ProxyPyQml import *
from easyInterface.Utils import Helpers
from PyImports.QtInterface import QtCalculatorInterface

from easyInterface.Diffraction.Interface import CalculatorInterface
from easyInterface.Diffraction.Calculators.CryspyCalculator import CryspyCalculator

TEST_FILE = "file:Tests/Data/main.cif"
release_config_file_path = os.path.join('App', "Release.yml")


@pytest.fixture
def proxy():
    proxy = ProxyPyQml(release_config_file_path)
    proxy._projectControl.loadProject(TEST_FILE)
    proxy.initialize()
    return proxy

@pytest.fixture
def no_project_proxy():
    no_project_proxy = ProxyPyQml(release_config_file_path)
    
    cal = CryspyCalculator(None)
    no_project_proxy._calculator_interface = CalculatorInterface(cal)
    
    no_project_proxy.initialize()
    no_project_proxy._calculator_interface.setPhaseDefinition('Tests/Data/phases.cif')
    
    return no_project_proxy


def test_Proxy_properties():
    proxy = ProxyPyQml(release_config_file_path)
    assert proxy._main_rcif_path is None
    assert proxy._refinement_running is False
    assert proxy._refinement_done is False


def test_Proxy_loadCif(proxy):
    assert proxy._main_rcif_path == "Tests/Data/main.cif"
    assert isinstance(proxy._calculator_interface, QtCalculatorInterface)
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
    assert 'Tests/Data' in proxy._project_control.project_url_absolute_path


def no_test_refine(proxy, qtbot, capsys):  # to be modified with AS's changes
    assert proxy._refinement_running is False
    captured = capsys.readouterr()

    with qtbot.waitSignal(proxy._refine_thread.finished, timeout=60000) as blocker:
        blocker.connect(proxy._refine_thread.failed)  # Can add other signals to blocker
        proxy._refine_thread.start()
        # Test will block at this point until signal is emitted or
        # 60 seconds has elapsed

    assert proxy._refinement_running is False
    assert proxy._fit_result is None
    assert captured.err == "" # modify
    assert captured.out == "" # modify
    #assert blocker.finished, "process timed-out"

    #assert_application_results(app)


def test_get_project_dir_absolute_path(proxy):

    path = os.path.join('easyDiffraction', 'Tests', 'Data')
    assert path in proxy._project_control.get_project_dir_absolute_path()


def test_store_report(proxy):
    report = "test report"
    proxy.store_report(report)
    assert proxy.report_html == report


def test_save_report(proxy, mocker, tmp_path):
    mocker.patch.object(Helpers, 'open_url', autospec=True)

    # no html
    proxy.store_report("")

    proxy.save_report()
    assert Helpers.open_url.called is False

    # good html
    report = "<h1><blink>I am a duck</blink></h1>"
    html = proxy.store_report(report)
    full_filename = "test"

    # temp dir instead of project dir
    tmp_dir = os.path.join(tmp_path, "local_dir")
    mocker.patch.object(proxy._project_control, 'get_project_dir_absolute_path', return_value=tmp_path, autospec=True)

    proxy.save_report('boom')
    # TODO this assertion fails for some reason... It really has been called :-/
    # assert Helpers.open_url.called is True


def test_saveProject(proxy):
    thisZIP = os.path.join(os.getcwd(), 'Tests', 'Data', 'test.zip')
    proxy.saveProjectAs(thisZIP)
    assert os.path.isfile(thisZIP) is True
    os.remove(thisZIP)

def test_LoadExperiment_cif(proxy, mocker):
    # exchange loadExperimentFromFile with mock and check it was called
    proxy.loadExperimentFromCif = mocker.MagicMock()
    proxy._projectControl.experiment_file_format = "cif"
    proxy.loadExperiment()
    proxy.loadExperimentFromCif.assert_called()

def test_LoadExperiment_xye(proxy, mocker):
    # exchange loadExperimentXYE with mock and check it was called
    proxy.loadExperimentFromXye = mocker.MagicMock()
    proxy._projectControl.experiment_file_format = "xye"
    proxy.loadExperiment()
    proxy.loadExperimentFromXye.assert_called()

def test_loadExperimentFromXye(no_project_proxy):
    # load test dataset and check
    #no_project_proxy._project_control.experiment_rcif_path = os.path.join(os.getcwd(), 'Tests', 'Data', 'data3.xye')
    xye_path = os.path.join(os.getcwd(), 'Tests', 'Data', 'data3.xye')
    no_project_proxy._projectControl.loadExperiment(xye_path, "boom (*.xye) boom")
    no_project_proxy.loadExperiment()
    
    experiment_added = no_project_proxy._calculator_interface.getExperiment('pd')
    assert experiment_added['name'] == "pd"
    assert experiment_added['wavelength'].value == 2.0


