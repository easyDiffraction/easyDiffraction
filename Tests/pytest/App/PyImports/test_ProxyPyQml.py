# tested module
from PyImports.ProxyPyQml import *
from PyImports.ProjectSentinel import ProjectManager
TEST_FILE = "file:Tests/Data/main.cif"


def test_Proxy_properties():
    manager = ProjectManager()
    proxy = Proxy(manager)
    assert proxy._main_rcif_path == None
    assert proxy._refinement_running == False
    assert proxy._refinement_done == False


def test_Proxy_loadCif():
    manager = ProjectManager()
    proxy = Proxy(manager)
    proxy.project_control.loadProject(TEST_FILE)
    proxy.initialize()
    assert proxy._main_rcif_path == "Tests/Data/main.cif"
    assert isinstance(proxy._calculator, CryspyCalculator)
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

    #assert "\\easyDiffraction\\Tests\\Data" in proxy.project_dir_absolute_path
    assert 'Tests/Data' in proxy.project_control.project_url_absolute_path



def no_test_refine(qtbot, capsys):  # to be modified with AS's changes
    manager = ProjectManager()
    proxy = Proxy(manager)
    proxy.project_control.loadProject(TEST_FILE)
    proxy.initialize()

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
    manager = ProjectManager()
    proxy = Proxy(manager)
    proxy.project_control.loadProject(TEST_FILE)
    proxy.initialize()

    path = os.path.join('easyDiffraction', 'Tests', 'Data')
    assert path in proxy.project_control.get_project_dir_absolute_path()



def test_store_report():
    manager = ProjectManager()
    proxy = Proxy(manager)
    report = "test report"

    proxy.store_report(report)

    assert proxy.report_html == report


def test_save_report(mocker, tmp_path):
    manager = ProjectManager()
    proxy = Proxy(manager)
    proxy.project_control.loadProject(TEST_FILE)
    mocker.patch.object(Helpers, 'open_url', autospec=True)

    # no html
    manager = ProjectManager()
    proxy = Proxy(manager)
    proxy.project_control.loadProject(TEST_FILE)
    proxy.initialize()

    proxy.store_report("")

    proxy.save_report()
    assert Helpers.open_url.called == False

    # good html
    report = "<h1><blink>I am a duck</blink></h1>"
    html = proxy.store_report(report)
    full_filename = "test"

    # temp dir instead of project dir
    tmp_dir = os.path.join(tmp_path,"local_dir")
    mocker.patch.object(proxy.project_control, 'get_project_dir_absolute_path', return_value=tmp_path, autospec=True)

    proxy.save_report()
    assert Helpers.open_url.called == True


def test_saveProject():
    manager = ProjectManager()
    proxy = Proxy(manager)
    proxy.project_control.loadProject(TEST_FILE)
    proxy.initialize()
    thisZIP = os.path.join(os.getcwd(), 'Tests', 'Data', 'test.zip')
    proxy.saveProject(thisZIP)
    assert os.path.isfile(thisZIP) == True
    os.remove(thisZIP)
