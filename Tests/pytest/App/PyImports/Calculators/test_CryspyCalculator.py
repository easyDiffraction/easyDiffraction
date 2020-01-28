import pytest

from PySide2.QtCore import QUrl
from PySide2.QtGui import QStandardItemModel

import cryspy

# module for testing
from EasyInterface.Calculators.CryspyCalculator import CryspyCalculator
from EasyInterface.Calculators.CryspyCalculator import PHASE_SEGMENT, EXPERIMENT_SEGMENT
from EasyInterface.Interface import CalculatorInterface

TEST_FILE = "file:Tests/Data/main.cif"
fitdata_data = [0, 2, 3, 5]

@pytest.fixture
def cal():
    file_path = QUrl(TEST_FILE).toLocalFile()
    calc = CryspyCalculator(file_path)
    interface = CalculatorInterface(calc)
    return interface

def test_init(cal):
    # initial state of the object
    assert len(cal.project_dict['app']) == 3
    assert len(cal.project_dict['calculations']) == 1
    assert len(cal.project_dict['info']) == 6
    assert len(cal.project_dict['phases']) == 1
    assert len(cal.project_dict['experiments']) == 1

    assert cal.calculator._main_rcif_path == TEST_FILE.replace('file:', '')

    assert len(cal.project_dict) == 6


def test_setAppDict(cal):

    assert 'name' in cal.project_dict['app'].keys()
    assert cal.project_dict['app']['name'] == 'easyDiffraction'
    assert 'version' in cal.project_dict['app'].keys()
    assert 'url' in cal.project_dict['app'].keys()


def test_setCalculatorDict(cal):

    assert 'name' in cal.project_dict['calculator'].keys()
    assert cal.project_dict['calculator']['name'] == 'CrysPy'
    assert 'version' in cal.project_dict['calculator'].keys()
    assert 'url' in cal.project_dict['calculator'].keys()


def test_setInfoDict(cal):

    assert len(cal.project_dict['info']) == 6
    assert 'refinement_datetime' in cal.project_dict['info']
    assert 'modified_datetime' in cal.project_dict['info']
    assert 'experiment_ids' in cal.project_dict['info']
    assert 'pd' in cal.project_dict['info']['experiment_ids']
    assert 'phase_ids' in cal.project_dict['info']
    assert 'Fe3O4' in cal.project_dict['info']['phase_ids']


def test_setPhasesDictFromCryspyObj(cal):
    # difficult test for creation of the phases dict
    cal.project_dict['phases'].clear() # enforce
    assert cal.calculator._cryspy_obj.crystals != None

    cal.updatePhases()

    phase_dict = cal.project_dict['phases']

    assert len(phase_dict) == 1
    assert len(phase_dict['Fe3O4']) == 5
    assert len(phase_dict['Fe3O4']['cell']) == 6
    # cell
    assert phase_dict['Fe3O4']['cell']['length_a'].value == 8.36212
    assert phase_dict['Fe3O4']['cell']['length_b']['store']['hide'] is True
    assert phase_dict['Fe3O4']['cell']['length_c']['store'].max == 10.034544
    assert phase_dict['Fe3O4']['cell']['angle_beta']['store']['error'] == 0.0
    assert phase_dict['Fe3O4']['cell']['angle_gamma']['store']['constraint'] is None
    # space_group
    assert len(phase_dict['Fe3O4']['spacegroup']) == 4
    assert phase_dict['Fe3O4']['spacegroup']['crystal_system'].value == 'cubic'
    assert phase_dict['Fe3O4']['spacegroup']['origin_choice'].value == '2'

    # atom sites
    assert len(phase_dict['Fe3O4']['atom_site']) == 3
    assert list(phase_dict['Fe3O4']['atoms'].keys()) == ['Fe3A', 'Fe3B', 'O']
    assert phase_dict['Fe3O4']['atoms']['Fe3A']['fract_x'].value == 0.125
    assert phase_dict['Fe3O4']['atoms']['Fe3B']['fract_y'].value == 0.5
    assert phase_dict['Fe3O4']['atoms']['O']['fract_z'].value == 0.25521
    assert phase_dict['Fe3O4']['atoms']['O']['fract_z']['store']['error'] == 0.0
    assert phase_dict['Fe3O4']['atoms']['O']['fract_z']['header'] == 'z'

    assert phase_dict['Fe3O4']['atoms']['Fe3B']['scat_length_neutron'].value == 0.945

    # occupancy
    assert phase_dict['Fe3O4']['atoms']['Fe3A']['occupancy'].value == 1.0
    assert phase_dict['Fe3O4']['atoms']['Fe3A']['occupancy']['store']['refine'] is False

    # ADP type
    assert phase_dict['Fe3O4']['atoms']['Fe3A']['adp_type']['header'] == 'Type'
    assert phase_dict['Fe3O4']['atoms']['Fe3A']['adp_type'].value == 'Usio'
    assert phase_dict['Fe3O4']['atoms']['O']['adp_type'].value == 'Uiso'

    # Isotropic ADP
    assert phase_dict['Fe3O4']['atoms']['Fe3A']['U_iso_or_equiv']['header'] == 'Biso'
    assert phase_dict['Fe3O4']['atoms']['Fe3A']['U_iso_or_equiv'].value == 0.0
    assert phase_dict['Fe3O4']['atoms']['Fe3A']['U_iso_or_equiv']['store'].max == 0.0
    assert phase_dict['Fe3O4']['atoms']['O']['U_iso_or_equiv'].value == 0.0
    assert phase_dict['Fe3O4']['atoms']['O']['U_iso_or_equiv']['store']['constraint'] is None

    # Isotropic ADP
    assert phase_dict['Fe3O4']['atoms']['Fe3A']['ADP']['u_11']['header'] == 'U11'
    assert phase_dict['Fe3O4']['atoms']['Fe3A']['ADP']['u_11'].value is None
    assert phase_dict['Fe3O4']['atoms']['Fe3A']['ADP']['u_22'].value is None
    assert phase_dict['Fe3O4']['atoms']['Fe3A']['ADP']['u_23']['store'].max is None
    assert phase_dict['Fe3O4']['atoms']['Fe3B']['ADP']['u_23'].value is None
    assert phase_dict['Fe3O4']['atoms']['Fe3B']['ADP']['u_23']['store']['constraint'] is None

    # Anisotropic MSP
    assert phase_dict['Fe3O4']['atoms']['Fe3A']['MSP']['chi_type'].value == 'Cani'
    assert phase_dict['Fe3O4']['atoms']['Fe3A']['MSP']['chi_11'].value == -3.468
    assert phase_dict['Fe3O4']['atoms']['Fe3A']['MSP']['chi_33'].value == -3.468
    assert phase_dict['Fe3O4']['atoms']['Fe3A']['MSP']['chi_23']['store'].max == 0.0
    assert phase_dict['Fe3O4']['atoms']['Fe3B']['MSP']['chi_23'].value == 0.0
    assert phase_dict['Fe3O4']['atoms']['Fe3B']['MSP']['chi_23']['store']['refine'] is False

def test_setExperimentsDictFromCryspyObj(cal):
    # difficult test for creation of the experiment dict
    cal.project_dict['experiments'].clear() # enforce
    assert cal.calculator._cryspy_obj.experiments != None

    cal.updateExperiments()

    experiment_dict = cal.project_dict['experiments']

    assert len(experiment_dict) == 1
    assert len(experiment_dict['pd']) == 7
    # wavelength
    assert len(experiment_dict['pd']['wavelength']) == 4
    assert experiment_dict['pd']['wavelength'].value == 0.84
    assert experiment_dict['pd']['wavelength']['url'] == ''

    # offset
    assert len(experiment_dict['pd']['offset']) == 4
    assert experiment_dict['pd']['offset'].value == -0.385404
    assert experiment_dict['pd']['offset']['store']['error'] == 0.0
    assert experiment_dict['pd']['offset']['store']['refine'] is False

    # phase
    assert len(experiment_dict['pd']['phase']) == 1
    assert len(experiment_dict['pd']['phase']['scale']) == 4
    assert experiment_dict['pd']['phase']['scale'].value == 0.02381
    assert experiment_dict['pd']['phase']['scale']['store']['refine'] is False
    assert experiment_dict['pd']['phase']['scale']['store']['error'] == 0.0

    # background
    assert len(experiment_dict['pd']['background']) == 3
    assert experiment_dict['pd']['background']['4.5']['ttheta'] == 4.5
    assert len(experiment_dict['pd']['background']['4.5']['intensity']) == 4
    assert experiment_dict['pd']['background']['4.5']['intensity'].value == 256.0
    assert experiment_dict['pd']['background']['80.0']['ttheta'] == 80.0
    assert len(experiment_dict['pd']['background']['80.0']['intensity']) == 4
    assert experiment_dict['pd']['background']['80.0']['intensity'].value == 65.0

    # resolution
    assert len(experiment_dict['pd']['resolution']) == 5
    assert len(experiment_dict['pd']['resolution']['u']) == 4
    assert experiment_dict['pd']['resolution']['u'].value == 16.9776
    assert experiment_dict['pd']['resolution']['u']['store']['refine'] is False
    assert len(experiment_dict['pd']['resolution']['y']) == 4
    assert experiment_dict['pd']['resolution']['v'].value == -2.8357
    assert experiment_dict['pd']['resolution']['v']['store']['error'] == 0.0
    assert experiment_dict['pd']['resolution']['v']['store']['hide'] is False


    # measured_pattern
    assert len(experiment_dict['pd']['measured_pattern']) == 7
    assert 5.0 in experiment_dict['pd']['measured_pattern']['x']
    assert len(experiment_dict['pd']['measured_pattern'].y_obs_lower) == 381
    assert experiment_dict['pd']['measured_pattern'].y_obs_lower[380] == pytest.approx(762.959046)

def test_setCalculationsDictFromCryspyObj(cal):
    cal.project_dict['calculations'].clear()

    assert cal.calculator._cryspy_obj.crystals != None

    cal.updateCalculations()

    calculation_dict = cal.project_dict['calculations']

    assert len(calculation_dict) == 1

    assert len(calculation_dict['pd']) == 4
    # bragg_peaks
    assert len(calculation_dict['pd']['bragg_peaks']) == 1
    assert sum(calculation_dict['pd']['bragg_peaks']['Fe3O4']['h']) == 681
    assert sum(calculation_dict['pd']['bragg_peaks']['Fe3O4']['ttheta']) == pytest.approx(5027.87268)
    # calculated_pattern
    assert len(calculation_dict['pd']['calculated_pattern']) == 4
    assert len(calculation_dict['pd']['calculated_pattern']['x']) == 381
    assert sum(calculation_dict['pd']['calculated_pattern']['x']) == 16002.0
    assert sum(calculation_dict['pd']['calculated_pattern']['y_diff_upper']) == pytest.approx(37056.915414296)

    # calculated data limits
    assert len(calculation_dict['pd']['limits']) == 2
    assert calculation_dict['pd']['limits']['main']['x_min'] == 4.0
    assert calculation_dict['pd']['limits']['main']['y_max'] == pytest.approx(6134.188081)
    assert calculation_dict['pd']['limits']['difference']['y_min'] == pytest.approx(-4087.48283)
    assert calculation_dict['pd']['limits']['difference']['y_max'] == pytest.approx(4601.62523)

def test_setProjectDictFromCryspyObj(cal):

    cal._info_dict.clear() # enforce
    cal._project_dict.clear() # enforce

    assert cal._cryspy_obj.crystals != None

    cal.setProjectDictFromCryspyObj()

    assert len(cal._info_dict) == 9
    assert cal._info_dict['name'] == 'Fe3O4'
    assert cal._info_dict['phase_ids'] == ['Fe3O4']
    assert cal._info_dict['experiment_ids'] == ['pd']

    # chi^2
    assert len(cal._info_dict['chi_squared']) == 4
    assert cal._info_dict['chi_squared']['value'] == pytest.approx(71.95038568442936)
    assert cal._info_dict['chi_squared']['url'] == ''
    # n_res
    assert len(cal._info_dict['n_res']) == 4
    assert cal._info_dict['n_res']['value'] == 381
    assert cal._info_dict['n_res']['tooltip'] == ''

    assert len(cal._project_dict) == 6
    assert isinstance(cal._project_dict['app'], dict)
    assert len(cal._project_dict['app']) == 3
    assert cal._project_dict['app']['name'] == "easyDiffraction"
    assert cal._project_dict['app']['url'] == "http://easydiffraction.org"

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
    assert cal.experimentsIds() == ['pd']

def test_asDict(cal):
    assert cal.asDict() == cal._project_dict

def test_name(cal):
    assert cal.name() == 'Fe3O4'

def test_asCifDict(cal):
    d = cal.asCifDict()

    assert isinstance(d, dict)
    assert 'data_Fe3O4' in d['phases']
    assert 'data_pd' in d['experiments']
    assert '_refln_index_h' in d['calculations']

@pytest.mark.parametrize("fit_len", fitdata_data)
def test_refine(cal, mocker, fit_len):

    class mocked_scipy_res():
        message = "test1"
        nfev = 1
        nit = 2
        njev = 42
        fun = 0.01
        x = [y for y in range(fit_len)]

    mocker.patch.object(cal._cryspy_obj, 'refine', return_value=mocked_scipy_res(), autospec=True)

    ret = cal.refine()

    cal._cryspy_obj.refine.assert_called_once()

    assert pytest.approx(ret['final_chi_sq'], 71.95038568442936)
    assert ret['nfev'] == 1
    assert ret['refinement_message'] == "test1"
    assert ret['njev'] == 42
    assert ret['nit'] == 2
    assert ret['num_refined_parameters'] == fit_len

def test_updatePhases(cal):
    """
    Load another phase file and check if the content is correctly updated
    """
    NEW_PHASE_FILE = "file:Tests/Data/phases_2.cif"
    file_path = QUrl(NEW_PHASE_FILE).toLocalFile()

    cal.updatePhases(file_path)

    assert cal.phasesIds() == ['Fe2Co1O4']
    assert cal.name() == 'Fe3O4'

    d = cal.asCifDict()
    assert 'data_Fe2Co1O4' in d['phases']
    assert 'data_pd' in d['experiments']

def test_parseSegment(cal):
    """
    parsing of the experiment or phase segment
    """
    exp_segment = cal._parseSegment(segment=EXPERIMENT_SEGMENT)

    phase_segment = cal._parseSegment(segment=PHASE_SEGMENT)

    bad_segment = cal._parseSegment(segment='poop')

    empty_segment = cal._parseSegment()

    assert bad_segment == ''
    assert empty_segment == ''

    assert 'Fe3O4' in exp_segment
    assert 'n_radiation_wavelength' in exp_segment

    assert 'Fe3O4' in phase_segment
    assert 'cell_length_a' in phase_segment
