import os
from pathlib import Path

from PyImports.ProjectModel import ProjectControl

TEST_ZIP = os.path.join(os.getcwd(), 'Tests', 'Data', 'Fe3O4_project.zip')
TEST_ZIP_ERROR = os.path.join(os.getcwd(), 'Tests', 'Data', 'Fe3O4_project_error.zip')
TEST_CIF = os.path.join(os.getcwd(), 'Tests', 'Data', 'main.cif')
TEST_CIF_ERROR = os.path.join(os.getcwd(), 'Tests', 'Data', 'phases.cif')
TEST_DIR = os.path.join(os.getcwd(), 'Tests', 'Data')

def test_ProjectModel_creation():
    model = ProjectControl()
    assert os.path.exists(model.tempDir.name)
    assert model.name is None
    assert model.keywords is None
    assert model._projectFile is None
    assert model._isValidCif is None
    assert model.main_rcif_path is None


def test_ProjectModel_loadProject_cif():
    model = ProjectControl()
    FILE = Path(TEST_CIF).as_uri()
    model.loadProject(FILE)

    assert model.name == 'Fe3O4\n'
    assert model.keywords == '\'neutron diffraction, powder, 1d\'\n'
    assert model._projectFile is None
    assert model._isValidCif
    assert model.main_rcif_path == TEST_CIF


def test_ProjectModel_loadProject_cif_error():
    model = ProjectControl()
    FILE = Path(TEST_CIF_ERROR).as_uri()
    model.loadProject(FILE)

    assert model.name is None
    assert model.keywords is None
    assert model._projectFile is None
    assert model._isValidCif is False
    assert model.main_rcif_path == TEST_CIF_ERROR


def test_ProjectModel_loadProject_zip():
    model = ProjectControl()
    FILE = Path(TEST_ZIP).as_uri()
    model.loadProject(FILE)

    assert model.name == 'Fe3O4 \n'
    assert model.keywords == '\'neutron diffraction, powder, 1d\' \n'
    assert model._projectFile == TEST_ZIP
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
            assert line == '_keywords %s\n' % keywords
            line = f.readline()
            assert line == '_phases\n'
            line = f.readline()
            assert line == '_experiments\n'
        os.remove(model.main_rcif_path)

    model.writeMain()
    checker('Undefined', '\'neutron diffraction, powder, 1d\'')
    model.writeMain('Test')
    checker('Test', '\'neutron diffraction, powder, 1d\'')
    model.writeMain('Test', 'Testing')
    checker('Test', 'Testing')

def test_ProjectModel_createProject():
    model = ProjectControl()
    model.createProject(os.path.join(TEST_DIR, 'boo.zip'))
    assert os.path.exists(model.tempDir.name)
    assert model.name is None
    assert model.keywords is None
    assert model._projectFile == os.path.join(TEST_DIR, 'boo.zip')
    assert model._isValidCif is None
    assert model.main_rcif_path is None

    model.createProject(os.path.join(TEST_DIR, 'boo'))
    assert os.path.exists(model.tempDir.name)
    assert model.name is None
    assert model.keywords is None
    assert model._projectFile == os.path.join(TEST_DIR, 'boo.zip')
    assert model._isValidCif is None
    assert model.main_rcif_path is None