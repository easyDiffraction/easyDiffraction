import os
from pathlib import Path
import pytest

from PyImports.ProjectSentinel import *

TEST_ZIP = os.path.join(os.getcwd(), 'Tests', 'Data', 'Fe3O4_project.zip')
TEST_ZIP_ERROR = os.path.join(os.getcwd(), 'Tests', 'Data', 'Fe3O4_project_error.zip')
TEST_CIF = os.path.join(os.getcwd(), 'Tests', 'Data', 'main.cif')
TEST_CIF_ERROR = os.path.join(os.getcwd(), 'Tests', 'Data', 'phases.cif')
TEST_DIR = os.path.join(os.getcwd(), 'Tests', 'Data')


def test_ProjectModel_creation():
    model = ProjectControl()
    assert os.path.exists(model.tempDir.name)
    assert model.manager.projectName == None
    assert model.manager.projectKeywords == ''
    assert model._project_file is None
    assert model._isValidCif is None
    assert model.main_rcif_path is None


def test_ProjectModel_loadProject_cif():
    model = ProjectControl()
    FILE = Path(TEST_CIF).as_uri()
    model.loadProject(FILE)

    assert model.manager.projectName == 'Fe3O4\n'
    assert model.manager.projectKeywords == 'neutron diffraction, powder, 1d'
    assert model._project_file is None
    assert model._isValidCif
    assert model.main_rcif_path == TEST_CIF


def test_ProjectModel_loadProject_cif_error():
    model = ProjectControl()
    FILE = Path(TEST_CIF_ERROR).as_uri()
    model.loadProject(FILE)

    assert model.manager.projectName is None
    assert model.manager.projectKeywords == ''
    assert model._project_file is None
    assert model._isValidCif is False
    assert model.main_rcif_path == TEST_CIF_ERROR


def test_ProjectModel_loadProject_zip():
    model = ProjectControl()
    FILE = Path(TEST_ZIP).as_uri()
    model.loadProject(FILE)

    assert model.manager.projectName == 'Fe3O4\n'
    assert model.manager.projectKeywords == 'neutron diffraction, powder, 1d'
    assert model._project_file == TEST_ZIP
    assert model._isValidCif
    TEMP_PATH = os.path.join(model.tempDir.name, 'main.cif')
    assert model.main_rcif_path == TEMP_PATH


def test_ProjectModel_writeMain():
    model = ProjectControl()

    def checker(name, keywords):
        with open(model.main_rcif_path, 'r') as f:
            line = f.readline()
            assert line == '_name %s\n' % name
            line = f.readline()
            assert line == '_keywords \'%s\'\n' % keywords
            line = f.readline()
            assert line == '_phases\n'
            line = f.readline()
            assert line == '_experiments\n'
        os.remove(model.main_rcif_path)

    model.writeMain()
    checker('Undefined', 'neutron powder diffraction, 1d')
    model.writeMain('Test')
    checker('Test', 'neutron powder diffraction, 1d')
    model.writeMain('Test', 'Testing')
    checker('Test', 'Testing')


def test_ProjectModel_createProject():
    model = ProjectControl()
    model.createProject(os.path.join(TEST_DIR, 'boo.zip'))
    assert os.path.exists(model.tempDir.name)
    assert model.manager.projectName is None
    assert model.manager.projectKeywords == ''
    assert model._project_file == os.path.join(TEST_DIR, 'boo.zip')
    assert model._isValidCif is None
    assert model.main_rcif_path is None

    model.createProject(os.path.join(TEST_DIR, 'boo'))
    assert os.path.exists(model.tempDir.name)
    assert model.manager.projectName is None
    assert model.manager.projectKeywords == ''
    assert model._project_file == os.path.join(TEST_DIR, 'boo.zip')
    assert model._isValidCif is None
    assert model.main_rcif_path is None


def test_check_project_dict():
    dict1 = {'a': 1,
             'b': 2,
             'phases': 3}
    dict2 = {
        'phases': [],
        'experiments': [],
        'calculations': []
    }
    dict3 = {
        'phases': 1,
        'experiments': 2,
        'calculations': 3
    }

    assert check_project_dict(dict1) == False
    assert check_project_dict(dict2) == False
    assert check_project_dict(dict3) == True


def test_check_if_zip():
    assert check_if_zip(TEST_ZIP) == True
    assert check_if_zip(TEST_CIF) == False


def test_check_project_file():
    assert check_project_file(TEST_ZIP) == True
    assert check_project_file(TEST_ZIP_ERROR) == False
    with pytest.raises(TypeError):
        err = check_project_file(TEST_CIF)


def test_make_temp_dir():
    folder = make_temp_dir()
    assert os.path.exists(folder.name) == True
    folder.cleanup()
    assert os.path.exists(folder.name) == False


def test_temp_project_dir():
    folder = temp_project_dir(TEST_ZIP)
    files = ['main.cif', 'phases.cif', 'experiments.cif']
    for file in files:
        assert os.path.isfile(os.path.join(folder.name, file)) == True
    folder.cleanup()


def test_create_project_zip():
    data_dir = 'Tests/Data/'

    temp1 = make_temp_dir()
    saveName1 = os.path.join(temp1.name, 'aa.zip')
    FILE = Path(saveName1).as_uri()
    create_project_zip(data_dir, FILE)
    isSaved, saveName2 = create_project_zip(data_dir, FILE)
    assert isSaved == True
    assert saveName1 == str(saveName2)
    assert os.path.isfile(saveName1) == True
    temp1.cleanup()

    temp1 = make_temp_dir()
    saveName1 = os.path.join(temp1.name, 'aa')
    saveName3 = saveName1 + '.zip'
    FILE = Path(saveName1).as_uri()
    isSaved, saveName2 = create_project_zip(data_dir, FILE)
    assert isSaved == True
    assert str(saveName2) == saveName3
    assert os.path.isfile(saveName3) == True
    temp1.cleanup()

    temp1 = make_temp_dir()
    FILE = Path(os.path.join(temp1.name, 'aa.zip')).as_uri()
    with pytest.raises(FileNotFoundError):
        isSaved, saveName2 = create_project_zip('Dummy/Dir', FILE)
    temp1.cleanup()

def test_LoadExperiment_cif():
    cif_path = os.path.join(os.getcwd(), 'Tests', 'Data', 'experiments.cif')
    model = ProjectControl()
    model.loadExperiment(cif_path)
    assert model.experiment_file_format == "cif"

def test_LoadExperiment_xye_unpolarized():
    xye_path = os.path.join(os.getcwd(), 'Tests', 'Data', 'data3.xye')
    model = ProjectControl()
    model.loadExperiment(xye_path)
    assert "PHASE_NAME" in model._cif_string
    assert "_setup_wavelength      2.00" in model._cif_string

def test_LoadExperiment_xye_polarized():
    xye_path = os.path.join(os.getcwd(), 'Tests', 'Data', 'data5.xye')
    model = ProjectControl()
    model.loadExperiment(xye_path)
    assert "PHASE_NAME" in model._cif_string
    assert "_setup_wavelength      2.40" in model._cif_string

def test_LoadExperiment_exception():
    dummy_path = "dummy_path.txt"
    model = ProjectControl()
    with pytest.raises(IOError):
        model.loadExperiment(dummy_path)

@pytest.fixture
def pm():
    return ProjectManager()


@pytest.mark.skipif(sys.platform.startswith("linux"), reason="Skipped on Ubuntu")
@pytest.mark.parametrize('state', [True, False])
def test_ProjectManager_set_get_isValidSaveState(pm, qtbot, state):
    assert pm.validSaveState is False
    with qtbot.waitSignal(pm.projectSaveChange) as blocker:
        pm.validSaveState = state
    assert blocker.args == [state]
    assert pm.validSaveState == state

@pytest.mark.skipif(sys.platform.startswith("linux"), reason="Skipped on Ubuntu")
def test_ProjectManager_projectNameChanged(pm, qtbot):
    value = 'Foo'
    assert pm.projectName is None
    with qtbot.waitSignal(pm.projectDetailChange):
        pm.projectName = value
    assert pm.projectName == value


@pytest.mark.skipif(sys.platform.startswith("linux"), reason="Skipped on Ubuntu")
def test_ProjectManager_projectKeywordsChanged(pm, qtbot):
    value = ['Foo']
    assert pm.projectKeywords == ''
    with qtbot.waitSignal(pm.projectDetailChange):
        pm.projectKeywords = value
    assert pm.projectKeywords == value[0]


@pytest.mark.skipif(sys.platform.startswith("linux"), reason="Skipped on Ubuntu")
def test_ProjectManager_projectExperimentsChanged(pm, qtbot):
    value = 'Foo'
    assert pm.projectExperiments is None
    with qtbot.waitSignal(pm.projectDetailChange):
        pm.projectExperiments = value
    assert pm.projectExperiments == value


@pytest.mark.skipif(sys.platform.startswith("linux"), reason="Skipped on Ubuntu")
def test_ProjectManager_projectInstrumentsChanged(pm, qtbot):
    value = 'Foo'
    assert pm.projectInstruments is None
    with qtbot.waitSignal(pm.projectDetailChange):
        pm.projectInstruments = value
    assert pm.projectInstruments == value


@pytest.mark.skipif(sys.platform.startswith("linux"), reason="Skipped on Ubuntu")
def test_ProjectManager_projectModifiedChanged(pm, qtbot):
    value = datetime.now()
    assert isinstance(pm.projectModified, str)
    with qtbot.waitSignal(pm.projectDetailChange):
        pm.projectModified = value
    assert pm.projectModified == value.strftime("%d/%m/%Y, %H:%M")


def test_ProjectManager_reset(pm):
    value = 'Foo'
    pm.validSaveState = True
    pm.projectName = value
    pm.projectKeywords = [value]
    pm.projectExperiments = value
    pm.projectInstruments = value
    now = datetime.now()
    pm.projectModified = now

    pm.resetManager()
    assert pm.validSaveState is False
    assert pm.projectName is None
    assert pm.projectKeywords == ''
    assert pm.projectExperiments is None
    assert pm.projectInstruments is None
    assert pm.projectModified == now.strftime("%d/%m/%Y, %H:%M")
