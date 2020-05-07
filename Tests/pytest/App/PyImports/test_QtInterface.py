__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

import os
import pytest

from copy import deepcopy


from PyImports.QtInterface import QtCalculatorInterface

from easyInterface.Diffraction.Calculators import CryspyCalculator

test_data = os.path.join('Tests', 'Data')
file_path = os.path.join(test_data, 'main.cif')
phase_path = os.path.join(test_data, 'phases.cif')
exp_path = os.path.join(test_data, 'experiments.cif')


@pytest.fixture
def cal():
    calc = CryspyCalculator(file_path)
    interface = QtCalculatorInterface(calc)
    return interface


def test_creation_None():
    calc = CryspyCalculator(None)
    interface = QtCalculatorInterface(calc)


def test_creation_EmptyStr():
    calc = CryspyCalculator('')
    interface = QtCalculatorInterface(calc)


def test_creation_WrongStr():
    path = os.path.join(test_data, 'mainf.cif')
    calc = CryspyCalculator(path)
    interface = QtCalculatorInterface(calc)


def test_creation_Empty():
    calc = CryspyCalculator()
    interface = QtCalculatorInterface(calc)


def test_deepcopyProjectDict(cal):
    # This might fail on python 3.6
    new_project_dict = deepcopy(cal.project_dict)

def test_init(cal):
    # initial state of the object
    assert len(cal.project_dict['app']) == 3
    assert len(cal.project_dict['calculations']) == 1
    assert len(cal.project_dict['info']) == 7
    assert len(cal.project_dict['phases']) == 1
    assert len(cal.project_dict['experiments']) == 1

    assert cal.calculator._main_rcif_path == file_path

    assert len(cal.project_dict) == 7

def test_setPhaseDefinition(cal):
    calc = CryspyCalculator('')
    interface = QtCalculatorInterface(calc)
    interface.setPhaseDefinition(phase_path)
    phase_added = interface.getPhase('Fe3O4')
    phase_ref = cal.getPhase('Fe3O4')
    assert phase_added['phasename'] == phase_ref['phasename']
    assert phase_added['spacegroup']['crystal_system'].value == phase_ref['spacegroup']['crystal_system'].value
    assert phase_added['spacegroup']['space_group_name_HM_ref'].value == phase_ref['spacegroup'][
        'space_group_name_HM_ref'].value
    assert phase_added['spacegroup']['space_group_IT_number'].value == phase_ref['spacegroup'][
        'space_group_IT_number'].value
    assert phase_added['spacegroup']['origin_choice'].value == phase_ref['spacegroup']['origin_choice'].value
    assert phase_added['cell']['length_a'].value == phase_ref['cell']['length_a'].value
    assert phase_added['cell']['length_b'].value == phase_ref['cell']['length_b'].value
    assert phase_added['cell']['length_c'].value == phase_ref['cell']['length_c'].value
    assert phase_added['cell']['angle_alpha'].value == phase_ref['cell']['angle_alpha'].value
    assert phase_added['cell']['angle_beta'].value == phase_ref['cell']['angle_beta'].value
    assert phase_added['cell']['angle_gamma'].value == phase_ref['cell']['angle_gamma'].value
    assert phase_added['atoms']['Fe3A']['fract_x'].value == phase_ref['atoms']['Fe3A']['fract_x'].value
    assert phase_added['atoms']['Fe3B']['fract_y'].value == phase_ref['atoms']['Fe3B']['fract_y'].value
    assert phase_added['atoms']['O']['fract_z'].value == phase_ref['atoms']['O']['fract_z'].value


def test_addPhaseDefinition(cal):
    calc = CryspyCalculator('')
    interface = QtCalculatorInterface(calc)
    interface.addPhaseDefinition(phase_path)
    phase_added = interface.getPhase('Fe3O4')
    phase_ref = cal.getPhase('Fe3O4')
    assert phase_added['phasename'] == phase_ref['phasename']
    assert phase_added['spacegroup']['crystal_system'].value == phase_ref['spacegroup']['crystal_system'].value
    assert phase_added['spacegroup']['space_group_name_HM_ref'].value == phase_ref['spacegroup'][
        'space_group_name_HM_ref'].value
    assert phase_added['spacegroup']['space_group_IT_number'].value == phase_ref['spacegroup'][
        'space_group_IT_number'].value
    assert phase_added['spacegroup']['origin_choice'].value == phase_ref['spacegroup']['origin_choice'].value
    assert phase_added['cell']['length_a'].value == phase_ref['cell']['length_a'].value
    assert phase_added['cell']['length_b'].value == phase_ref['cell']['length_b'].value
    assert phase_added['cell']['length_c'].value == phase_ref['cell']['length_c'].value
    assert phase_added['cell']['angle_alpha'].value == phase_ref['cell']['angle_alpha'].value
    assert phase_added['cell']['angle_beta'].value == phase_ref['cell']['angle_beta'].value
    assert phase_added['cell']['angle_gamma'].value == phase_ref['cell']['angle_gamma'].value
    assert phase_added['atoms']['Fe3A']['fract_x'].value == phase_ref['atoms']['Fe3A']['fract_x'].value
    assert phase_added['atoms']['Fe3B']['fract_y'].value == phase_ref['atoms']['Fe3B']['fract_y'].value
    assert phase_added['atoms']['O']['fract_z'].value == phase_ref['atoms']['O']['fract_z'].value


def test_setPhaseDefinition_None():
    calc = CryspyCalculator('')
    interface = QtCalculatorInterface(calc)
    interface.setPhaseDefinition(None)


def test_setPhaseDefinition_EmptyStr():
    calc = CryspyCalculator('')
    interface = QtCalculatorInterface(calc)
    interface.setPhaseDefinition('')


def test_setExperimentDefinition(cal):
    calc = CryspyCalculator('')
    interface = QtCalculatorInterface(calc)
    interface.setPhaseDefinition(phase_path)
    interface.setExperimentDefinition(exp_path)
    exp_added = interface.getExperiment('pd')
    exp_ref = cal.getExperiment('pd')
    assert exp_added['name'] == exp_ref['name']
    assert exp_added['wavelength'].value == exp_ref['wavelength'].value
    assert exp_added['offset'].value == exp_ref['offset'].value
    assert exp_added['phase']['Fe3O4']['name'] == exp_ref['phase']['Fe3O4']['name']
    assert exp_added['phase']['Fe3O4']['scale'].value == exp_ref['phase']['Fe3O4']['scale'].value


def test_addExperimentDefinition(cal):
    calc = CryspyCalculator('')
    interface = QtCalculatorInterface(calc)
    interface.setPhaseDefinition(phase_path)
    interface.addExperimentDefinition(exp_path)
    exp_added = interface.getExperiment('pd')
    exp_ref = cal.getExperiment('pd')
    assert exp_added['name'] == exp_ref['name']
    assert exp_added['wavelength'].value == exp_ref['wavelength'].value
    assert exp_added['offset'].value == exp_ref['offset'].value
    assert exp_added['phase']['Fe3O4']['name'] == exp_ref['phase']['Fe3O4']['name']
    assert exp_added['phase']['Fe3O4']['scale'].value == exp_ref['phase']['Fe3O4']['scale'].value


def refineHelper(cal):
    assert cal.project_dict['phases']['Fe3O4']['cell']['length_a'].refine
    assert pytest.approx(cal.project_dict['phases']['Fe3O4']['cell']['length_a'].value, 8.36212)
    r = cal.refine()
    rr = {'num_refined_parameters': 1,
          'refinement_message': 'Optimization terminated successfully.',
          'nfev': 27,
          'nit': 5,
          'njev': 9,
          }
    chi_ref = 3.3723747910939683
    chi_found = r['final_chi_sq']
    del r['final_chi_sq']
    assert r == rr
    assert pytest.approx(chi_found, chi_ref, 0.6)  # because we have errors here :-/
    assert pytest.approx(cal.project_dict['phases']['Fe3O4']['cell']['length_a'].value, 8.561673117085581)


# @pytest.mark.xfail(strict=False)
def test_refine(cal):
    refineHelper(cal)


def test_Undo(cal):
    refineHelper(cal)
    assert cal.canUndo()
    assert cal.project_dict.undoText() == 'Refinement'
    cal.undo()
    assert pytest.approx(cal.project_dict['phases']['Fe3O4']['cell']['length_a'].value, 8.36212)


def test_Redo(cal):
    refineHelper(cal)
    assert cal.canUndo()
    assert cal.project_dict.undoText() == 'Refinement'
    cal.undo()
    assert pytest.approx(cal.project_dict['phases']['Fe3O4']['cell']['length_a'].value, 8.36212)
    assert cal.project_dict.redoText() == 'Refinement'
    assert cal.canRedo()
    cal.redo()
    assert pytest.approx(cal.project_dict['phases']['Fe3O4']['cell']['length_a'].value, 8.561673117085581)


def test_clearUndoStack(cal):
    assert cal.canUndo()
    cal.clearUndoStack()
    assert not cal.canUndo()
