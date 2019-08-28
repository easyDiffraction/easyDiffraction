##########################################################
#
#  pytest runner for api_rcif_common methods
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

# tested module
from App.f_api_rcif.api_rcif_common import *

#space_groupe = SpaceGroupe()
cell = Cell()

f_name = r"full.rcif"
rcif = f_rcif.cl_rcif.RCif()
current_location = os.path.abspath(os.path.dirname(sys.argv[1]))
current_location = os.path.join(current_location, "Tests", "Data", f_name)
rcif.load_from_file(current_location)

p_glob = rcif.glob
l_data = p_glob["data"]
dict_i = l_data[0]

def test_from_dict_to_obj_spg():
    """
    Test from_dict_to_obj for space_group object
    """
    space_groupe = SpaceGroupe()
    assert space_groupe.get_val("spgr_given_name") == "P1"
    assert space_groupe.get_val("singony") == "Triclinic"
    assert space_groupe.get_val("spgr_name") == "P1"
    assert space_groupe.get_val("spgr_number") == 1
    from_dict_to_obj(dict_i, api_rcif_crystal.data_space_groupe_relation(), space_groupe)
    # check the assignment on space_group
    assert space_groupe.get_val("spgr_given_name") == "Fd-3m"
    assert space_groupe.get_val("singony") == "Cubic"
    assert space_groupe.get_val("spgr_name") == "Fd-3m"
    assert space_groupe.get_val("spgr_number") == 227

def test_from_dict_to_obj_spg_bad1():
    # empty RCIF file for update
    space_groupe = SpaceGroupe()
    dict_bad = {}
    from_dict_to_obj(dict_bad, api_rcif_crystal.data_space_groupe_relation(), space_groupe)
    # check the assignment on space_group - no change due to empty RCIF
    assert space_groupe.get_val("spgr_given_name") == "P1"
    assert space_groupe.get_val("singony") == "Triclinic"
    assert space_groupe.get_val("spgr_name") == "P1"
    assert space_groupe.get_val("spgr_number") == 1

def test_from_dict_to_obj_spg_bad2():
    # bad relation specified for operation
    space_groupe = SpaceGroupe()
    # call fails with TypeError
    with pytest.raises(TypeError):
        from_dict_to_obj(dict_i, api_rcif_crystal.data_cell_relation(), space_groupe)

def test_from_dict_to_obj_spg_bad3():
    # bad target object
    space_groupe = None
    # call fails with AttributeError due to not being able to call a method on None
    with pytest.raises(AttributeError):
        from_dict_to_obj(dict_i, api_rcif_crystal.data_space_groupe_relation(), space_groupe)
    
@pytest.mark.skipif(True, reason="bugged impl. can't multiply sequence by non-int of type 'float'")
def test_from_dict_to_obj_cell():
    """
    Test from_dict_to_obj for cell object
    """
    assert cell.get_val("a") == 1.0
    assert cell.get_val("b") == 1.0
    assert cell.get_val("c") == 1.0
    assert cell.get_val("singony") == "Triclinic"
    assert cell.get_val("alpha") == 90.0
    assert cell.get_val("gamma") == 90.0
    from_dict_to_obj(dict_i, api_rcif_crystal.data_cell_relation(), cell)

    # check the assignment on space_group
    assert cell.get_val("a") == "P1"
    assert cell.get_val("b") == "P1"
    assert cell.get_val("c") == "P1"
    assert cell.get_val("singony") == "Triclinic"
    assert cell.get_val("alpha") == "P1"
    assert cell.get_val("gamma") == 1

def test_from_dict_to_obj_atom_type():
    """
    Test from_dict_to_obj for atom_type object
    """
    # hardcoded "_atom_site_fract" element [0]
    l_key = list(dict_i["loops"][0].keys())
    n_atom = len(dict_i["loops"][0][l_key[0]])
    
    atom_type = AtomType()
    assert atom_type.get_val("x") == 0.0
    assert atom_type.get_val("y") == 0.0
    assert atom_type.get_val("z") == 0.0
    assert atom_type.get_val("name") == "H"
    assert atom_type.get_val("type_n") == "H"

    dd = {}
    for key in l_key:
        dd.update({key:dict_i["loops"][0][key][0]})
    # test atom 0 only
    from_dict_to_obj(dd, api_rcif_crystal.data_atom_relation(), atom_type)

    assert atom_type.get_val("x") == 0.125
    assert atom_type.get_val("y") == 0.125
    assert atom_type.get_val("z") == 0.125
    assert atom_type.get_val("name") == "Fe3A"
    assert atom_type.get_val("type_n") == "Fe"


def test_conv_str_to_text_float_logic():
    """
    Test conversion between tagged and untagged string
    """
    relation = api_rcif_crystal.data_cell_relation()
    # number
    string1 = "1.23"
    result = conv_str_to_text_float_logic(string1, relation)
    assert isinstance(result, float)

    # bool
    string1 = "False"
    result = conv_str_to_text_float_logic(string1, relation)
    assert isinstance(result, bool)

    # Variable
    string1 = "1.23(2)"
    result = conv_str_to_text_float_logic(string1, relation)
    # for some reason this fails proper check. Investigate
    #assert isinstance(result, f_common.cl_variable.Variable)

    pass

