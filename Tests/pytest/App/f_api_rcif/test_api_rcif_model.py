##########################################################
#
#  pytest runner for api_rcif_model methods
#
###########################################################
import sys
import os
import pytest
from pytest_mock import mock
from _pytest import monkeypatch


# internal imports
import f_rcif.cl_rcif
import f_common.cl_variable
from f_crystal.cl_crystal import SpaceGroupe, Cell, AtomType
from App.f_api_rcif import api_rcif_crystal
import f_rhochi_model.cl_model 

# utilities
from Tests.pytest.Utilities import TEST_DATA0, TEST_RCIF, relation_tester

# tested module
from App.f_api_rcif.api_rcif_model import *

#space_groupe = SpaceGroupe()
cell = Cell()

def test_conv_rcif_to_model():

    model = conv_rcif_to_model(TEST_RCIF)

    assert isinstance(model, f_rhochi_model.cl_model.Model)

def test_conv_data_to_crystal():

    pass

def test_conv_data_to_experiment_single():

    pass

def test_conv_data_to_experiment_single_domain():

    pass

def test_conv_data_to_experiment_powder_1d():

    pass

def test_conv_data_to_experiment_powder_2d():

    pass

def test_conv_data_to_experiment_powder_texture_2d():

    pass

def test_conv_model_to_rcif():
    pass

def test_conv_crystal_to_data():
    pass

def test_conv_experiment_single_to_data():
    pass

def test_conv_experiment_single_domain_to_data():
    pass

def test_conv_experiment_powder_1d_to_data():
    pass

def test_conv_experiment_powder_2d_to_data():
    pass

def test_data_space_groupe_relation():
    relation = data_space_groupe_relation()
    relation_tester(relation, 2)

def test_data_cell_relation():
    relation = data_cell_relation()
    relation_tester(relation, 6)

def test_data_atom_relation():
    relation = data_atom_relation()
    relation_tester(relation, 8)

def test_data_bscat_relation():
    relation = data_bscat_relation()
    relation_tester(relation, 2)

def test_data_adp_relation():
    relation = data_adp_relation()
    relation_tester(relation, 7)

def test_data_chi_relation():
    relation = data_chi_relation()
    relation_tester(relation, 11)

def test_data_experiment_powder_1d_relation():
    relation = data_experiment_powder_1d_relation()
    relation_tester(relation, 6)

def test_data_background_powder_1d_relation():
    relation = data_background_powder_1d_relation()
    relation_tester(relation, 1)

#-------------------------
def test_data_observed_data_powder_1d_relation():
    relation = data_observed_data_powder_1d_relation()
    relation_tester(relation, 3)

def test_data_beam_polarization_powder_1d_relation():
    relation = data_beam_polarization_powder_1d_relation()
    relation_tester(relation, 2)

def test_data_resolution_powder_1d_relation():
    relation = data_resolution_powder_1d_relation()
    relation_tester(relation, 5)

def test_data_asymmetry_powder_1d_relation():
    relation = data_asymmetry_powder_1d_relation()
    relation_tester(relation, 4)

def test_data_zero_shift_powder_1d_relation():
    relation = data_zero_shift_powder_1d_relation()
    relation_tester(relation, 1)

def test_data_exclude_powder_1d_relation():
    relation = data_exclude_powder_1d_relation()
    relation_tester(relation, 2)

def test_data_experiment_powder_2d_relation():
    relation = data_exclude_powder_1d_relation()
    relation_tester(relation, 2)

def test_data_background_powder_2d_relation():
    relation = data_background_powder_2d_relation()
    relation_tester(relation, 1)

def test_data_observed_data_powder_2d_relation():
    relation = data_observed_data_powder_2d_relation()
    relation_tester(relation, 5)

def test_data_beam_polarization_powder_2d_relation():
    relation = data_beam_polarization_powder_2d_relation()
    relation_tester(relation, 2)

def test_data_resolution_powder_2d_relation():
    relation = data_resolution_powder_2d_relation()
    relation_tester(relation, 5)

def test_data_asymmetry_powder_2d_relation():
    relation = data_asymmetry_powder_2d_relation()
    relation_tester(relation, 4)

def test_data_zero_shift_powder_2d_relation():
    relation = data_zero_shift_powder_2d_relation()
    relation_tester(relation, 1)

def test_data_experiment_powder_texture_2d_relation():
    relation = data_experiment_powder_texture_2d_relation()
    relation_tester(relation, 12)

def test_data_background_powder_texture_2d_relation():
    relation = data_background_powder_texture_2d_relation()
    relation_tester(relation, 1)

def test_data_observed_data_powder_texture_2d_relation():
    relation = data_observed_data_powder_texture_2d_relation()
    relation_tester(relation, 5)

def test_data_beam_polarization_powder_texture_2d_relation():
    relation = data_beam_polarization_powder_texture_2d_relation()
    relation_tester(relation, 2)

def test_data_resolution_powder_texture_2d_relation():
    relation = data_resolution_powder_texture_2d_relation()
    relation_tester(relation, 5)

def test_data_asymmetry_powder_texture_2d_relation():
    relation = data_asymmetry_powder_texture_2d_relation()
    relation_tester(relation, 4)

def test_data_zero_shift_powder_texture_2d_relation():
    relation = data_zero_shift_powder_texture_2d_relation()
    relation_tester(relation, 1)

def test_data_experiment_single_relation():
    relation = data_experiment_single_relation()
    relation_tester(relation, 2)

def test_data_observed_data_single_relation():
    relation = data_observed_data_single_relation()
    relation_tester(relation, 1)

def test_data_beam_polarization_single_relation():
    relation = data_beam_polarization_single_relation()
    relation_tester(relation, 2)

def test_data_extinction_single_relation():
    relation = data_extinction_single_relation()
    relation_tester(relation, 2)

def test_data_experiment_single_domain_relation():
    relation = data_experiment_single_domain_relation()
    relation_tester(relation, 2)

def test_data_observed_data_single_domain_relation():
    relation = data_observed_data_single_domain_relation()
    relation_tester(relation, 1)

def test_data_beam_polarization_single_domain_relation():
    relation = data_beam_polarization_single_domain_relation()
    relation_tester(relation, 2)

def test_data_extinction_single_domain_relation():
    relation = data_extinction_single_domain_relation()
    relation_tester(relation, 2)

def test_data_domain_single_domain_relation():
    relation = data_domain_single_domain_relation()
    relation_tester(relation, 1)
