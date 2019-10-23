import pytest

from PySide2.QtCore import QUrl
from PySide2.QtGui import QStandardItemModel

import cryspy

# module for testing
from PyImports.Calculators.CryspyCalculator import CryspyCalculator

TEST_FILE = "file:Tests/Data/main.cif"

@pytest.fixture
def cal():
    file_path = QUrl(TEST_FILE).toLocalFile()
    calc = CryspyCalculator(file_path)
    return calc

def test_init(cal):
    # initial state of the object
    assert len(cal._app_dict) == 3
    assert len(cal._calculations_dict) == 1
    assert len(cal._info_dict) == 7
    assert len(cal._phases_dict) == 1
    assert len(cal._experiments_dict) == 1
    assert len(cal._calculations_dict) == 1

    assert cal._main_rcif_path == TEST_FILE.replace('file:','')

    assert len(cal._project_dict) == 6

def test_setAppDict(cal):

    assert 'name' in cal._app_dict.keys()
    assert cal._app_dict['name'] == 'easyDiffraction'
    assert 'version' in cal._app_dict.keys()
    assert 'url' in cal._app_dict.keys()

def test_setCalculatorDict(cal):

    assert 'name' in cal._calculator_dict.keys()
    assert cal._calculator_dict['name'] == 'CrysPy'
    assert 'version' in cal._calculator_dict.keys()
    assert 'url' in cal._calculator_dict.keys()

def test_setInfoDict(cal):

    assert len(cal._info_dict) == 7
    assert 'name' in cal._info_dict.keys()
    assert cal._info_dict['name'] == 'Fe3O4'
    assert 'refinement_datetime' in cal._info_dict.keys()
    assert 'experiment_ids' in cal._info_dict.keys()


def test_setPhasesDictFromCryspyObj(cal):
    # difficult test for creation of the phases dict
    cal._phases_dict.clear() # enforce
    assert cal._cryspy_obj.crystals != None

    cal.setPhasesDictFromCryspyObj()

    assert len(cal._phases_dict) == 1
    assert len(cal._phases_dict['Fe3O4']) == 4
    assert len(cal._phases_dict['Fe3O4']['cell']) == 6
    # cell
    assert cal._phases_dict['Fe3O4']['cell']['length_a']['value'] == 8.57
    assert cal._phases_dict['Fe3O4']['cell']['length_b']['hide'] == True
    assert cal._phases_dict['Fe3O4']['cell']['length_c']['max'] == 10.284
    assert cal._phases_dict['Fe3O4']['cell']['angle_beta']['error'] == None
    assert cal._phases_dict['Fe3O4']['cell']['angle_gamma']['constraint'] == None
    # space_group
    assert len(cal._phases_dict['Fe3O4']['space_group']) == 4
    assert cal._phases_dict['Fe3O4']['space_group']['crystal_system']['value'] == 'cubic'
    assert cal._phases_dict['Fe3O4']['space_group']['origin_choice']['value'] == '2'

    # atom sites
    assert len(cal._phases_dict['Fe3O4']['atom_site']) == 3
    assert list(cal._phases_dict['Fe3O4']['atom_site'].keys()) == ['Fe3A', 'Fe3B', 'O1']
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3A']['fract_x']['value'] == 0.125
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3B']['fract_y']['value'] == 0.5
    assert cal._phases_dict['Fe3O4']['atom_site']['O1']['fract_z']['value'] == 0.25521
    assert cal._phases_dict['Fe3O4']['atom_site']['O1']['fract_z']['error'] == 0.0
    assert cal._phases_dict['Fe3O4']['atom_site']['O1']['fract_z']['header'] == 'z'

    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3B']['scat_length_neutron']['value'] == 0.945

    # occupancy
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3A']['occupancy']['value'] == 1.0
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3A']['occupancy']['refine'] == False

    # ADP type
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3A']['adp_type']['header'] == 'Type'
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3A']['adp_type']['value'] == 'uani'
    assert cal._phases_dict['Fe3O4']['atom_site']['O1']['adp_type']['value'] == 'uiso'

    # Isotropic ADP
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3A']['B_iso_or_equiv']['header'] == 'Biso'
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3A']['B_iso_or_equiv']['value'] == 0.0
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3A']['B_iso_or_equiv']['max'] == 0.0
    assert cal._phases_dict['Fe3O4']['atom_site']['O1']['B_iso_or_equiv']['value'] == 0.0
    assert cal._phases_dict['Fe3O4']['atom_site']['O1']['B_iso_or_equiv']['constraint'] == None

    # Isotropic ADP
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3A']['u_11']['header'] == 'U11'
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3A']['u_11']['value'] == 0.0
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3A']['u_22']['value'] == 0.0
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3A']['u_23']['max'] == 0.0
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3B']['u_23']['value'] == 0.0
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3B']['u_23']['constraint'] == None

    # Anisotropic MSP
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3A']['chi_type']['value'] == 'cani'
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3A']['chi_11']['value'] == -0.5
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3A']['chi_33']['value'] == -0.5
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3A']['chi_23']['max'] == 0.0
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3B']['chi_23']['value'] == 0.0
    assert cal._phases_dict['Fe3O4']['atom_site']['Fe3B']['chi_23']['refine'] == False

def test_setExperimentsDictFromCryspyObj(cal):
    # difficult test for creation of the experiment dict
    cal._experiments_dict.clear() # enforce
    assert cal._cryspy_obj.crystals != None

    cal.setExperimentsDictFromCryspyObj()

    assert len(cal._experiments_dict) == 1
    assert len(cal._experiments_dict['pnd']) == 6
    # wavelength
    assert len(cal._experiments_dict['pnd']['wavelength']) == 4
    assert cal._experiments_dict['pnd']['wavelength']['value'] == 0.84
    assert cal._experiments_dict['pnd']['wavelength']['url'] == ''

    # offset
    assert len(cal._experiments_dict['pnd']['offset']) == 10
    assert cal._experiments_dict['pnd']['offset']['value'] == -0.1
    assert cal._experiments_dict['pnd']['offset']['error'] == 0.0
    assert cal._experiments_dict['pnd']['offset']['refine'] == True

    # phase
    assert len(cal._experiments_dict['pnd']['phase']) == 1
    assert len(cal._experiments_dict['pnd']['phase']['scale']) == 10
    assert cal._experiments_dict['pnd']['phase']['scale']['value'] == 0.02
    assert cal._experiments_dict['pnd']['phase']['scale']['refine'] == True
    assert cal._experiments_dict['pnd']['phase']['scale']['error'] == 0.0

    # background
    assert len(cal._experiments_dict['pnd']['background']) == 3
    assert cal._experiments_dict['pnd']['background']['4.5']['ttheta'] == 4.5
    assert len(cal._experiments_dict['pnd']['background']['4.5']['intensity']) == 7
    assert cal._experiments_dict['pnd']['background']['4.5']['intensity']['value'] == 256.0
    assert cal._experiments_dict['pnd']['background']['80.0']['ttheta'] == 80.0
    assert len(cal._experiments_dict['pnd']['background']['80.0']['intensity']) == 7
    assert cal._experiments_dict['pnd']['background']['80.0']['intensity']['value'] == 65.0

    # resolution
    assert len(cal._experiments_dict['pnd']['resolution']) == 5
    assert len(cal._experiments_dict['pnd']['resolution']['u']) == 10
    assert cal._experiments_dict['pnd']['resolution']['u']['value'] == 16.9776
    assert cal._experiments_dict['pnd']['resolution']['u']['refine'] == False
    assert len(cal._experiments_dict['pnd']['resolution']['y']) == 10
    assert cal._experiments_dict['pnd']['resolution']['u']['value'] == 16.9776
    assert cal._experiments_dict['pnd']['resolution']['u']['error'] == 0.0
    assert cal._experiments_dict['pnd']['resolution']['u']['hide'] == False


    # measured_pattern
    assert len(cal._experiments_dict['pnd']['measured_pattern']) == 7
    assert 5.0 in cal._experiments_dict['pnd']['measured_pattern']['x']
    assert len(cal._experiments_dict['pnd']['measured_pattern']['y_obs_lower']) == 381
    assert cal._experiments_dict['pnd']['measured_pattern']['y_obs_lower'][380] == pytest.approx(762.959046)

def test_setCalculationsDictFromCryspyObj(cal):
    cal._calculations_dict.clear() # enforce

    assert cal._cryspy_obj.crystals != None

    cal.setCalculationsDictFromCryspyObj()

    assert len(cal._calculations_dict) == 1

    assert len(cal._calculations_dict['pnd']) == 5
    # chi^2
    assert len(cal._calculations_dict['pnd']['chi_squared']) == 4
    assert cal._calculations_dict['pnd']['chi_squared']['value'] == pytest.approx(27413.09694)
    assert cal._calculations_dict['pnd']['chi_squared']['url'] == ''
    # n_res
    assert len(cal._calculations_dict['pnd']['n_res']) == 4
    assert cal._calculations_dict['pnd']['n_res']['value'] == 381
    assert cal._calculations_dict['pnd']['n_res']['tooltip'] == ''
    # bragg_peaks
    assert len(cal._calculations_dict['pnd']['bragg_peaks']) == 1
    assert sum(cal._calculations_dict['pnd']['bragg_peaks']['Fe3O4']['h']) == 748
    assert sum(cal._calculations_dict['pnd']['bragg_peaks']['Fe3O4']['ttheta']) == pytest.approx(5406.403839)
    # calculated_pattern
    assert len(cal._calculations_dict['pnd']['calculated_pattern']) == 4
    assert len(cal._calculations_dict['pnd']['calculated_pattern']['x']) == 381
    assert sum(cal._calculations_dict['pnd']['calculated_pattern']['x']) == 16002.0
    assert sum(cal._calculations_dict['pnd']['calculated_pattern']['y_diff_upper']) == pytest.approx(87828.141076)

    # calculated data limits
    assert len(cal._calculations_dict['pnd']['limits']) == 2
    assert cal._calculations_dict['pnd']['limits']['main']['x_min'] == 4.0
    assert cal._calculations_dict['pnd']['limits']['main']['y_max'] == pytest.approx(6134.188081)
    assert cal._calculations_dict['pnd']['limits']['difference']['y_min'] == pytest.approx(-1069.54322)
    assert cal._calculations_dict['pnd']['limits']['difference']['y_max'] == pytest.approx(4671.01719)

def test_setProjectDictFromCryspyObj(cal):

    cal._info_dict.clear() # enforce
    cal._project_dict.clear() # enforce

    assert cal._cryspy_obj.crystals != None

    cal.setProjectDictFromCryspyObj()

    assert len(cal._info_dict) == 7
    assert cal._info_dict['name'] == 'Fe3O4'
    assert cal._info_dict['phase_ids'] == ['Fe3O4']
    assert cal._info_dict['experiment_ids'] == ['pnd']

    assert len(cal._project_dict) == 6
    assert isinstance(cal._project_dict['app'], dict)
    assert len(cal._project_dict['app']) == 3
    assert cal._project_dict['app']['name'] == "easyDiffraction"
    assert cal._project_dict['app']['url'] == "http://easydiffraction.github.io"

    assert 'calculator' in list(cal._project_dict.keys())
    assert 'info' in list(cal._project_dict.keys())
    assert 'phases' in list(cal._project_dict.keys())

def test_phasesCount(cal):
    assert cal.phasesCount() == 1

def test_experimentsCount(cal):
    assert cal.experimentsCount() == 1

def test_phasesIds(cal):
    assert cal.phasesIds() == ['Fe3O4']

def test_experimentsIds(cal):
    assert cal.experimentsIds() == ['pnd']

def test_asDict(cal):
    assert cal.asDict() == cal._project_dict

def test_name(cal):
    assert cal.name() == 'Fe3O4'

def test_asCifDict(cal):
    d = cal.asCifDict()

    assert isinstance(d, dict)
    assert 'data_Fe3O4' in d['phases']
    assert 'data_pnd' in d['experiments']
    assert '_refln_index_h' in d['calculations']

def test_refine(cal, mocker):

    class mocked_scipy_res():
        message = "test1"
        nfev = 1
        nit = 2
        njev = 42
        fun = 0.01

    mocker.patch.object(cal._cryspy_obj, 'refine', return_value=mocked_scipy_res(), autospec=True)

    ret = cal.refine()

    cal._cryspy_obj.refine.assert_called_once()

    assert ret['final_chi_sq'] == 0.01
    assert ret['nfev'] == 1
    assert ret['refinement_message'] == "test1"
    assert ret['njev'] == 42
    assert ret['nit'] == 2
