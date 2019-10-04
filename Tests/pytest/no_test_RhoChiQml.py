import sys
import os
import pytest
from pytest_mock import mocker
from _pytest import monkeypatch
from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl
import f_common.cl_variable as rhochi_variable
import f_rcif.cl_rcif as rhochi_rcif

# tested module
from RhoChiQml import *

def test_Proxy_properties():
    proxy = Proxy()
    assert isinstance(proxy.proxy_data_changed, Signal)

def test_Proxy_init():
    proxy = Proxy()
    assert proxy._tmp_rcif_dir_name == ""
    assert proxy._project_opened == False
    assert proxy._model_refined == False
    assert proxy._time_stamp == None
    assert proxy.parameters == {}

def test_Proxy_toString():
    proxy = Proxy()
    assert proxy.toString("test") == "test"
    assert proxy.toString("test  ") == "test"
    assert proxy.toString(7) == "7"
    assert proxy.toString(1.23456789) == "1.23457"
    assert proxy.toString(1.23) == "1.23"
    assert proxy.toString(False) == "False"
    assert proxy.toString(None) == "None"
    assert "RhoChiQml.Proxy object" in proxy.toString(proxy)

def test_set_parameter():
    proxy = Proxy()

    # standard float
    value = 7.12
    assert proxy.set_parameter("P1", "p2", "name", value, include=True) == str(value)
    #assert proxy.parameters["P1 p2 name"] == {'fit':False, 'group':"P1", 'name':'name', 'subgroup':'p2', 'value':str(value)}
    orig_properties = proxy.parameters['P1 p2 name']
    assert  orig_properties == {'fit':False, 'group':"P1", 'name':'name', 'subgroup':'p2', 'value':str(value)}

    # try passing bad type
    assert proxy.set_parameter("P1", "p2", "name", False, include=True) == "False"
    # assure nothing changed
    assert  proxy.parameters['P1 p2 name'] == orig_properties

    # Try using Value instead
    value2 = rhochi_variable.Variable(7.12)
    assert proxy.set_parameter("P1", "p2", "name", value2, include=True) == str(value)
    new_properties = proxy.parameters['P1 p2 name']
    # but new_properties contains now another key.
    assert  new_properties == {'esd': '0.0', 'fit':True, 'group':"P1", 'name':'name', 'subgroup':'p2', 'value':str(value)}

def test_get_parameters():
    proxy = Proxy()

    value = 7.12
    proxy.set_parameter("P1", "p2", "name", value, include=True) == str(value)

    assert proxy.get_parameters() == [{'P1 p2 name':
                                       {'fit': False,
                                        'group': 'P1',
                                        'name': 'name',
                                        'subgroup': 'p2',
                                        'value': '7.12'}}]

def test_get_time_stamp():
    proxy = Proxy()
    proxy.set_time_stamp()
    import numpy
    assert proxy.get_time_stamp() == str(numpy.datetime64('now'))

def test_is_project_opened():
    proxy = Proxy()
    assert proxy.is_project_opened() == False

def test_get_project_dir_name():
    proxy = Proxy()
    assert proxy.get_project_dir_name() == ""
    # Now load something
    proxy.load_rhochi_model_and_update_proxy("file:Tests/Data/full.rcif")
    assert proxy.get_project_dir_name() == "Data"

def test_get_project_name():
    proxy = Proxy()
    assert proxy.get_project_name() == ""
    # Now load something
    proxy.load_rhochi_model_and_update_proxy("file:Tests/Data/full.rcif")
    assert proxy.get_project_name() == "Data"

def test_get_project_info():
    proxy = Proxy()
    assert proxy.get_project_info() == ""
    # Now load something
    proxy.load_rhochi_model_and_update_proxy("file:Tests/Data/full.rcif")
    assert proxy.get_project_info() == ""

def test_init_parameters():
    # test several random parameters
    proxy = Proxy()
    assert not hasattr(proxy, "_tmp_phase_name")
    assert not hasattr(proxy, "_tmp_tth_list")
    assert not hasattr(proxy, "_tmp_l_list")
    assert not hasattr(proxy, "_tmp_spgr_name")
    assert not hasattr(proxy, "_cell_angle_alpha")
    assert not hasattr(proxy, "_atom_site_aniso_U_33_list")
    proxy.init_parameters()
    assert hasattr(proxy, "_tmp_phase_name")
    assert hasattr(proxy, "_tmp_tth_list")
    assert hasattr(proxy, "_tmp_l_list")
    assert hasattr(proxy, "_tmp_spgr_name")
    assert hasattr(proxy, "_cell_angle_alpha")
    assert hasattr(proxy, "_atom_site_aniso_U_33_list")

    assert proxy._tmp_phase_name == ""
    assert proxy._tmp_tth_list == ""
    assert proxy._tmp_l_list == []
    assert proxy._tmp_spgr_name == ""
    assert proxy._cell_angle_alpha == ""
    assert proxy._atom_site_aniso_U_33_list == []

def test_change_data_from_rhochi_model():
    proxy = Proxy()
    # initial parameters are the same as in the init_parameters test
    # Let's change data then
    proxy.load_rhochi_model_and_update_proxy("file:Tests/Data/full.rcif")

    assert proxy._tmp_phase_name == "Fe3O4"
    assert proxy._tmp_rcif_file_name == "full.rcif"
    assert proxy._tmp_singony == "Cubic"
    assert proxy._cell_length_a == "8.7"
    assert proxy._tmp_setup_wavelength == "0.84"
    assert proxy._tmp_spgr_name == "Fd-3m"
    assert proxy._cell_angle_alpha == "90.0"
    assert proxy._atom_site_aniso_U_33_list == ['0.0','0.0','0.0']

def test_get_project_dir_absolute_path():
    proxy = Proxy()
    proxy.load_rhochi_model_and_update_proxy("file:Tests/Data/full.rcif")

    assert "easyDiffraction\Tests\Data" in proxy.get_project_dir_absolute_path()

def test_get_project_url_absolute_path():
    proxy = Proxy()
    proxy.load_rhochi_model_and_update_proxy("file:Tests/Data/full.rcif")

    assert proxy.get_project_url_absolute_path() == "file:Tests/Data"

def test_rcif_as_string():
    #return '\n'.join(rhochi_model.conv_model_to_rcif(self.model).save_to_str())
    proxy = Proxy()
    proxy.load_rhochi_model_and_update_proxy("file:Tests/Data/full.rcif")

    content = proxy.rcif_as_string()
    
    # important parts
    assert "Fe3A 2.0 1.0 cani Fe3 -3.45 0.0 0.0 -3.45 0.0 -3.45" in content
    assert "_space_group_name_H-M_alt Fd-3m" in content
    assert len(content) == 1950


def test_load_rhochi_model_and_update_proxy():

    proxy = Proxy()
    # pristine state
    assert not hasattr(proxy, "rcif_file_absolute_path")
    assert not hasattr(proxy, "rcif")
    assert not hasattr(proxy, "model")
    assert proxy._project_opened == False
    proxy.load_rhochi_model_and_update_proxy("file:Tests/Data/full.rcif")
    # make sure all aspects change on the call
    assert proxy.rcif_file_absolute_path == "Tests/Data/full.rcif"
    assert isinstance(proxy.rcif, rhochi_rcif.RCif)
    assert isinstance(proxy.model, dict)
    assert proxy._project_opened == True

def test_refine():
    proxy = Proxy()
    proxy.load_rhochi_model_and_update_proxy("file:Tests/Data/full.rcif")
    t1 = proxy.get_time_stamp()

    #assert proxy.refine() == True # test for successful refinement

    #t2 = proxy.get_time_stamp()
    #assert t1 != t2

    # assert refined value
    ### solve issue with Windows!

