import os
import sys
import numpy

from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl

import f_rcif.cl_rcif as rhochi_rcif
import f_api_rcif.api_rcif_model as rhochi_model
import f_common.cl_variable as rhochi_variable

class Proxy(QObject):
    def __init__(self):
        QObject.__init__(self)

        self._tmp_rcif_dir_name = ""
        self._tmp_rcif_file_name = ""
        self._project_opened = False
        self._model_refined = False
        self._time_stamp = self.set_time_stamp()
        self.parameters = {}

    # -------------------------------------------------
    # ...
    # -------------------------------------------------

    def toString(self, d):
        if isinstance(d, str):
            return d.strip()
        elif isinstance(d, int):
            return str(d)
        elif isinstance(d, float):
            return str(round(d, 5))
        else:
            return str(d).strip()

    def set_parameter(self, group, subgroup, name, value, include=True):
        if (include):
            if isinstance(value, float):
                self.parameters[group + ' ' + subgroup + ' ' + name] = {'group':group, 'subgroup':subgroup, 'name':name, 'value':self.toString(value), 'fit':False}
                #print("OK: Parameter '{}' = '{}', type '{}'".format(name, self.toString(value), type(value)))
            elif isinstance(value, rhochi_variable.Variable):
                self.parameters[group + ' ' + subgroup + ' ' + name] = {'group':group, 'subgroup':subgroup, 'name':name, 'value':self.toString(value), 'fit':True, 'esd':self.toString(value.__getitem__(4))}
                #print("OK: Parameter '{}' = '{}({})', type '{}'".format(name, self.toString(value), self.toString(value.__getitem__(4)), type(value)))
            else:
                print("ERROR: Unknown type '{}'".format(type(value)))
        return self.toString(value)

    @Slot(result='QVariant')
    def get_parameters(self):
        list = []
        for key in self.parameters:
            #print(key, self.parameters[key])
            list.append({key: self.parameters[key]})
        #return self.parameters
        return list

    # -------------------------------------------------
    # Signals
    # -------------------------------------------------

    proxy_data_changed = Signal()

    # -------------------------------------------------
    # ...
    # -------------------------------------------------

    def get_time_stamp(self):
        return self._time_stamp

    def set_time_stamp(self):
        self._time_stamp = str(numpy.datetime64('now'))

    def is_project_opened(self):
        return self._project_opened

    def get_project_dir_name(self):
        return os.path.basename(os.path.dirname(self.rcif_file_absolute_path)) if self._project_opened else ""

    def get_project_name(self):
        return self.get_project_dir_name().split('_')[0] if self._project_opened else ""

    def get_project_info(self):
        return ", ".join(self.get_project_dir_name().split('_')[1:]) if self._project_opened else ""

    # -------------------------------------------------
    # ...
    # -------------------------------------------------

    def init_parameters(self):
        # -1
        self._tmp_rcif_file_name = ""
        self._tmp_rcif_dir_name = ""

        # A
        self._tmp_phase_name = ""
        self._tmp_phase_comment = ""

        # 0
        self._tmp_tth_list = ""
        self._tmp_int_u_list = ""
        self._tmp_sint_u_list = ""
        self._tmp_int_d_list = ""
        self._tmp_sint_d_list = ""
        self._tmp_int_u_mod_list = []
        self._tmp_int_d_mod_list = []
        self._tmp_pos_hkl_list = []
        self._tmp_h_list = []
        self._tmp_k_list = []
        self._tmp_l_list = []

        # 1
        self._tmp_singony = ""
        self._tmp_spgr_name = ""
        self._tmp_spgr_number = ""
        self._tmp_spgr_choice = ""

        # 2
        self._cell_length_a = ""
        self._cell_length_b = ""
        self._cell_length_c = ""
        self._cell_angle_alpha = ""
        self._cell_angle_beta = ""
        self._cell_angle_gamma = ""

        # 3
        self._atom_site_label_list = []
        self._atom_site_type_symbol_list = []
        self._atom_site_fract_x_list = []
        self._atom_site_fract_y_list = []
        self._atom_site_fract_z_list = []
        self._atom_site_occupancy_list = []
        self._atom_site_bscat_list = []

        # B
        self._tmp_no_symmetry_atom_site_fract_x_list = []
        self._tmp_no_symmetry_atom_site_fract_y_list = []
        self._tmp_no_symmetry_atom_site_fract_z_list = []
        self._tmp_no_symmetry_atom_site_bscat_list = []

        # 4
        self._atom_site_adp_type_list = []
        self._atom_site_b_iso_or_equiv_list = []
        self._atom_site_aniso_U_11_list = []
        self._atom_site_aniso_U_12_list = []
        self._atom_site_aniso_U_13_list = []
        self._atom_site_aniso_U_22_list = []
        self._atom_site_aniso_U_23_list = []
        self._atom_site_aniso_U_33_list = []

        # D
        self._atom_site_flag_m_list = []
        self._atom_site_type_m_list = []
        self._atom_site_chi_type_list = []
        self._atom_site_cani_chi_11_list = []
        self._atom_site_cani_chi_12_list = []
        self._atom_site_cani_chi_13_list = []
        self._atom_site_cani_chi_22_list = []
        self._atom_site_cani_chi_23_list = []
        self._atom_site_cani_chi_33_list = []

        # 5
        self._tmp_setup_wavelength = ""
        self._tmp_setup_zero_shift = ""
        self._tmp_setup_resolution_u = ""
        self._tmp_setup_resolution_v = ""
        self._tmp_setup_resolution_w = ""
        self._tmp_setup_resolution_x = ""
        self._tmp_setup_resolution_y = ""

    def change_data_from_rhochi_model(self):
        # reset
        self.init_parameters()

        # -1
        self._tmp_rcif_file_name = self.rcif._p_file_name
        #self._tmp_rcif_dir_name = os.path.dirname(os.path.abspath(os.path.join(self.rcif._p_file_dir, self.rcif._p_file_name)))
        self._tmp_rcif_dir_name = os.path.basename(self.rcif._p_file_dir)

        # A
        self._tmp_phase_name = self.model._list_crystal[0].get_val('name')
        self._tmp_phase_comment = 'Comment goes here'

        # 0
        if self.model._list_experiment:
            self._tmp_tth_list = self.model._list_experiment[0].get_val('observed_data').get_val('tth')
            self._tmp_int_u_list = self.model._list_experiment[0].get_val('observed_data').get_val('int_u')
            self._tmp_sint_u_list = self.model._list_experiment[0].get_val('observed_data').get_val('sint_u')
            self._tmp_int_d_list = self.model._list_experiment[0].get_val('observed_data').get_val('int_d')
            self._tmp_sint_d_list = self.model._list_experiment[0].get_val('observed_data').get_val('sint_d')
            self._tmp_int_u_mod_list, self._tmp_int_d_mod_list, d_info = self.model._list_experiment[0].calc_profile(self._tmp_tth_list, self.model._list_crystal)
            self._tmp_pos_hkl_list = d_info['crystal'][0]['tth_hkl']
            self._tmp_h_list = d_info['crystal'][0]['h']
            self._tmp_k_list = d_info['crystal'][0]['k']
            self._tmp_l_list = d_info['crystal'][0]['l']

        # 1
        self._tmp_singony = self.model._list_crystal[0].get_val('space_groupe').get_val('singony')
        self._tmp_spgr_name = self.model._list_crystal[0].get_val('space_groupe').get_val('spgr_name')
        self._tmp_spgr_number = self.model._list_crystal[0].get_val('space_groupe').get_val('spgr_number')
        self._tmp_spgr_choice = self.model._list_crystal[0].get_val('space_groupe').get_val('spgr_choice')

        # 2
        self._cell_length_a = self.set_parameter('sample', 'cell', 'a', self.model._list_crystal[0].get_val('cell').get_val('a'))
        self._cell_length_b = self.set_parameter('sample', 'cell', 'b', self.model._list_crystal[0].get_val('cell').get_val('b'))
        self._cell_length_c = self.set_parameter('sample', 'cell', 'c', self.model._list_crystal[0].get_val('cell').get_val('c'))
        self._cell_angle_alpha = self.set_parameter('sample', 'cell', 'alpha', self.model._list_crystal[0].get_val('cell').get_val('alpha'))
        self._cell_angle_beta = self.set_parameter('sample', 'cell', 'beta', self.model._list_crystal[0].get_val('cell').get_val('beta'))
        self._cell_angle_gamma = self.set_parameter('sample', 'cell', 'gamma', self.model._list_crystal[0].get_val('cell').get_val('gamma'))

        # 3
        for a in self.model._list_crystal[0].get_val('atom_site')._list_atom_type:
            self._atom_site_label_list.append(self.toString(a.get_val('name')))
            self._atom_site_type_symbol_list.append(self.toString(a.get_val('type_n')))
            self._atom_site_fract_x_list.append(self.toString(a.get_val('x')))
            self._atom_site_fract_y_list.append(self.toString(a.get_val('y')))
            self._atom_site_fract_z_list.append(self.toString(a.get_val('z')))
            self._atom_site_occupancy_list.append(self.toString(a.get_val('occupation')))
            self._atom_site_bscat_list.append(self.toString(a.get_val('b_scat')))

        # B
        for x_unique, y_unique, z_unique, b in zip(self._atom_site_fract_x_list, self._atom_site_fract_y_list, self._atom_site_fract_z_list, self._atom_site_bscat_list):
            x_equivalent_list = self.model._list_crystal[0].get_val('space_groupe').calc_xyz_mult(float(x_unique),float(y_unique),float(z_unique))[0]
            y_equivalent_list = self.model._list_crystal[0].get_val('space_groupe').calc_xyz_mult(float(x_unique),float(y_unique),float(z_unique))[1]
            z_equivalent_list = self.model._list_crystal[0].get_val('space_groupe').calc_xyz_mult(float(x_unique),float(y_unique),float(z_unique))[2]
            for x, y, z in zip(x_equivalent_list, y_equivalent_list, z_equivalent_list):
                self._tmp_no_symmetry_atom_site_fract_x_list.append(float(x))
                self._tmp_no_symmetry_atom_site_fract_y_list.append(float(y))
                self._tmp_no_symmetry_atom_site_fract_z_list.append(float(z))
                self._tmp_no_symmetry_atom_site_bscat_list.append(float(b))
        for x, y, z, b in zip(self._tmp_no_symmetry_atom_site_fract_x_list, self._tmp_no_symmetry_atom_site_fract_y_list, self._tmp_no_symmetry_atom_site_fract_z_list, self._tmp_no_symmetry_atom_site_bscat_list):
            if x == 0.0:
                self._tmp_no_symmetry_atom_site_fract_x_list.append(1.0)
                self._tmp_no_symmetry_atom_site_fract_y_list.append(y)
                self._tmp_no_symmetry_atom_site_fract_z_list.append(z)
                self._tmp_no_symmetry_atom_site_bscat_list.append(b)
            if y == 0.0:
                self._tmp_no_symmetry_atom_site_fract_x_list.append(x)
                self._tmp_no_symmetry_atom_site_fract_y_list.append(1.0)
                self._tmp_no_symmetry_atom_site_fract_z_list.append(z)
                self._tmp_no_symmetry_atom_site_bscat_list.append(b)
            if z == 0.0:
                self._tmp_no_symmetry_atom_site_fract_x_list.append(x)
                self._tmp_no_symmetry_atom_site_fract_y_list.append(y)
                self._tmp_no_symmetry_atom_site_fract_z_list.append(1.0)
                self._tmp_no_symmetry_atom_site_bscat_list.append(b)

        # 4
        for a in self.model._list_crystal[0].get_val('atom_site')._list_atom_type:
            self._atom_site_adp_type_list.append(self.toString(a.get_val('adp_type')))
            self._atom_site_b_iso_or_equiv_list.append(self.toString(a.get_val('b_iso')))
            self._atom_site_aniso_U_11_list.append(self.toString(a.get_val('u_11')))
            self._atom_site_aniso_U_12_list.append(self.toString(a.get_val('u_12')))
            self._atom_site_aniso_U_13_list.append(self.toString(a.get_val('u_13')))
            self._atom_site_aniso_U_22_list.append(self.toString(a.get_val('u_22')))
            self._atom_site_aniso_U_23_list.append(self.toString(a.get_val('u_23')))
            self._atom_site_aniso_U_33_list.append(self.toString(a.get_val('u_33')))

        # D
        for a in self.model._list_crystal[0].get_val('atom_site')._list_atom_type:
            flag_m = a.get_val('flag_m')
            label = self.toString(a.get_val('name'))
            self._atom_site_flag_m_list.append(flag_m)
            self._atom_site_type_m_list.append(self.toString(a.get_val('type_m')))
            self._atom_site_chi_type_list.append(self.toString(a.get_val('chi_type')))
            self._atom_site_cani_chi_11_list.append(self.set_parameter('sample', label, '\u03C711', a.get_val('chi_11'), flag_m))
            self._atom_site_cani_chi_12_list.append(self.set_parameter('sample', label, '\u03C712', a.get_val('chi_12'), flag_m))
            self._atom_site_cani_chi_13_list.append(self.set_parameter('sample', label, '\u03C713', a.get_val('chi_13'), flag_m))
            self._atom_site_cani_chi_22_list.append(self.set_parameter('sample', label, '\u03C722', a.get_val('chi_22'), flag_m))
            self._atom_site_cani_chi_23_list.append(self.set_parameter('sample', label, '\u03C723', a.get_val('chi_23'), flag_m))
            self._atom_site_cani_chi_33_list.append(self.set_parameter('sample', label, '\u03C733', a.get_val('chi_33'), flag_m))

        # 5
        if self.model._list_experiment:
            self._tmp_setup_wavelength = self.set_parameter('instrument', 'general', 'Wavelength', self.model._list_experiment[0].get_val('setup').get_val('wave_length'))
            self._tmp_setup_zero_shift = self.set_parameter('instrument', 'general', 'Zero shift', self.model._list_experiment[0].get_val('setup').get_val('zero_shift'))
            self._tmp_setup_resolution_u = self.set_parameter('instrument', 'resolution', 'U', self.model._list_experiment[0].get_val('setup').get_val('resolution').get_val('u'))
            self._tmp_setup_resolution_v = self.set_parameter('instrument', 'resolution', 'V', self.model._list_experiment[0].get_val('setup').get_val('resolution').get_val('v'))
            self._tmp_setup_resolution_w = self.set_parameter('instrument', 'resolution', 'W', self.model._list_experiment[0].get_val('setup').get_val('resolution').get_val('w'))
            self._tmp_setup_resolution_x = self.set_parameter('instrument', 'resolution', 'X', self.model._list_experiment[0].get_val('setup').get_val('resolution').get_val('x'))
            self._tmp_setup_resolution_y = self.set_parameter('instrument', 'resolution', 'Y', self.model._list_experiment[0].get_val('setup').get_val('resolution').get_val('y'))

        # emit signal
        #self.proxy_data_changed.emit()

    # -------------------------------------------------
    # QML accessible methods: Proxy parameters
    # -------------------------------------------------

    # -1
    @Slot(result=str)
    def tmp_rcif_file_name(self):
        return self._tmp_rcif_file_name
    @Slot(result=str)
    def tmp_rcif_dir_name(self):
        #return self._tmp_rcif_dir_name[:65] + (self._tmp_rcif_dir_name[65:] and '...')
        return self._tmp_rcif_dir_name

    # A
    @Slot(result=str)
    def tmp_phase_name(self):
        return str(self._tmp_phase_name)
    @Slot(result=str)
    def tmp_phase_comment(self):
        return str(self._tmp_phase_comment)

    # 0
    @Slot(result='QVariant')
    def tmp_tth_list(self):
        if self._tmp_tth_list != "":
            return self._tmp_tth_list.tolist()
        else:
            return []
    @Slot(result='QVariant')
    def tmp_int_u_list(self):
        return self._tmp_int_u_list.tolist() if self._tmp_int_u_list != "" else []
    @Slot(result='QVariant')
    def tmp_sint_u_list(self):
        return self._tmp_sint_u_list.tolist() if self._tmp_int_u_list != "" else []
    @Slot(result='QVariant')
    def tmp_int_d_list(self):
        return self._tmp_int_d_list.tolist() if self._tmp_int_u_list != "" else []
    @Slot(result='QVariant')
    def tmp_sint_u_list(self):
        return self._tmp_sint_u_list.tolist() if self._tmp_int_u_list != "" else []
    @Slot(result='QVariant')
    def tmp_int_d_list(self):
        return self._tmp_int_d_list.tolist() if self._tmp_int_u_list != "" else []
    @Slot(result='QVariant')
    def tmp_int_u_mod_list(self):
        return self._tmp_int_u_mod_list.tolist() if self._tmp_int_u_list != "" else []
    @Slot(result='QVariant')
    def tmp_int_d_mod_list(self):
        return self._tmp_int_d_mod_list.tolist() if self._tmp_int_u_list != "" else []
    @Slot(result='QVariant')
    def tmp_pos_hkl_list(self):
        return self._tmp_pos_hkl_list.tolist() if self._tmp_int_u_list != "" else []
    @Slot(result='QVariant')
    def tmp_h_list(self):
        return self._tmp_h_list.tolist() if self._tmp_int_u_list != "" else []
    @Slot(result='QVariant')
    def tmp_k_list(self):
        return self._tmp_k_list.tolist() if self._tmp_int_u_list != "" else []
    @Slot(result='QVariant')
    def tmp_l_list(self):
        return self._tmp_l_list.tolist() if self._tmp_int_u_list != "" else []

    # 1
    @Slot(result=str)
    def tmp_singony(self):
        return str(self._tmp_singony)
    @Slot(result=str)
    def tmp_spgr_name(self):
        return str(self._tmp_spgr_name)
    @Slot(result=str)
    def tmp_spgr_number(self):
        return str(self._tmp_spgr_number)
    @Slot(result=str)
    def tmp_spgr_choice(self):
        return str(self._tmp_spgr_choice)

    # 2
    @Slot(result=str)
    def cell_length_a(self):
        return self._cell_length_a
    @Slot(result=str)
    def cell_length_b(self):
        return self._cell_length_b
    @Slot(result=str)
    def cell_length_c(self):
        return self._cell_length_c
    @Slot(result=str)
    def cell_angle_alpha(self):
        return self._cell_angle_alpha
    @Slot(result=str)
    def cell_angle_beta(self):
        return self._cell_angle_beta
    @Slot(result=str)
    def cell_angle_gamma(self):
        return self._cell_angle_gamma

    # 3
    @Slot(result='QVariant')
    def atom_site_label_list(self):
        return self._atom_site_label_list
    @Slot(result='QVariant')
    def atom_site_type_symbol_list(self):
        return self._atom_site_type_symbol_list
    @Slot(result='QVariant')
    def atom_site_fract_x_list(self):
        return self._atom_site_fract_x_list
    @Slot(result='QVariant')
    def atom_site_fract_y_list(self):
        return self._atom_site_fract_y_list
    @Slot(result='QVariant')
    def atom_site_fract_z_list(self):
        return self._atom_site_fract_z_list
    @Slot(result='QVariant')
    def atom_site_occupancy_list(self):
        return self._atom_site_occupancy_list
    @Slot(result='QVariant')
    def atom_site_bscat_list(self):
        return self._atom_site_bscat_list

    # B
    @Slot(result='QVariant')
    def tmp_no_symmetry_atom_site_fract_x_list(self):
        return self._tmp_no_symmetry_atom_site_fract_x_list
    @Slot(result='QVariant')
    def tmp_no_symmetry_atom_site_fract_y_list(self):
        return self._tmp_no_symmetry_atom_site_fract_y_list
    @Slot(result='QVariant')
    def tmp_no_symmetry_atom_site_fract_z_list(self):
        return self._tmp_no_symmetry_atom_site_fract_z_list
    @Slot(result='QVariant')
    def tmp_no_symmetry_atom_site_bscat_list(self):
        return self._tmp_no_symmetry_atom_site_bscat_list

    # 4
    @Slot(result='QVariant')
    def atom_site_adp_type_list(self):
        return self._atom_site_adp_type_list
    @Slot(result='QVariant')
    def atom_site_b_iso_or_equiv_list(self):
        return self._atom_site_b_iso_or_equiv_list
    @Slot(result='QVariant')
    def atom_site_aniso_U_11_list(self):
        return self._atom_site_aniso_U_11_list
    @Slot(result='QVariant')
    def atom_site_aniso_U_12_list(self):
        return self._atom_site_aniso_U_12_list
    @Slot(result='QVariant')
    def atom_site_aniso_U_13_list(self):
        return self._atom_site_aniso_U_13_list
    @Slot(result='QVariant')
    def atom_site_aniso_U_22_list(self):
        return self._atom_site_aniso_U_22_list
    @Slot(result='QVariant')
    def atom_site_aniso_U_23_list(self):
        return self._atom_site_aniso_U_23_list
    @Slot(result='QVariant')
    def atom_site_aniso_U_33_list(self):
        return self._atom_site_aniso_U_33_list

    # D
    @Slot(result='QVariant')
    def atom_site_flag_m_list(self):
        return self._atom_site_flag_m_list
    @Slot(result='QVariant')
    def atom_site_type_m_list(self):
        return self._atom_site_type_m_list
    @Slot(result='QVariant')
    def atom_site_chi_type_list(self):
        return self._atom_site_chi_type_list
    @Slot(result='QVariant')
    def atom_site_cani_chi_11_list(self):
        return self._atom_site_cani_chi_11_list
    @Slot(result='QVariant')
    def atom_site_cani_chi_12_list(self):
        return self._atom_site_cani_chi_12_list
    @Slot(result='QVariant')
    def atom_site_cani_chi_13_list(self):
        return self._atom_site_cani_chi_13_list
    @Slot(result='QVariant')
    def atom_site_cani_chi_22_list(self):
        return self._atom_site_cani_chi_22_list
    @Slot(result='QVariant')
    def atom_site_cani_chi_23_list(self):
        return self._atom_site_cani_chi_23_list
    @Slot(result='QVariant')
    def atom_site_cani_chi_33_list(self):
        return self._atom_site_cani_chi_33_list

    # 5
    @Slot(result=str)
    def tmp_setup_wavelength(self):
        return self.toString(self._tmp_setup_wavelength)
    @Slot(result=str)
    def tmp_setup_zero_shift(self):
        return self.toString(self._tmp_setup_zero_shift)
    @Slot(result=str)
    def tmp_setup_resolution_u(self):
        return self.toString(self._tmp_setup_resolution_u)
    @Slot(result=str)
    def tmp_setup_resolution_v(self):
        return self.toString(self._tmp_setup_resolution_v)
    @Slot(result=str)
    def tmp_setup_resolution_w(self):
        return self.toString(self._tmp_setup_resolution_w)
    @Slot(result=str)
    def tmp_setup_resolution_x(self):
        return self.toString(self._tmp_setup_resolution_x)
    @Slot(result=str)
    def tmp_setup_resolution_y(self):
        return self.toString(self._tmp_setup_resolution_y)

    # -------------------------------------------------
    # QML accessible methods: Misc
    # -------------------------------------------------

    @Slot(result=str)
    def get_project_dir_absolute_path(self):
        #print("111", str(self.rcif_file_absolute_path), str(os.path.dirname(self.rcif_file_absolute_path)))
        return str(QUrl.fromLocalFile(os.path.dirname(self.rcif_file_absolute_path)).toString())

    @Slot(result=str)
    def rcif_as_string(self):
        return '\n'.join(rhochi_model.conv_model_to_rcif(self.model).save_to_str())

    @Slot(str)
    def load_rhochi_model_and_update_proxy(self, path):
        print("load_rhochi_model_and_update_proxy")
        path = QUrl(path).toLocalFile()
        self.rcif_file_absolute_path = path
        self.rcif = rhochi_rcif.RCif()
        self.rcif.load_from_file(self.rcif_file_absolute_path)
        self.model = rhochi_model.conv_rcif_to_model(self.rcif)
        self.parameters = {}
        self.init_parameters()
        self.change_data_from_rhochi_model()
        self.set_time_stamp()
        self._project_opened = True
        self.proxy_data_changed.emit()

    @Slot(result=bool)
    def refine(self):
        print("refine")
        res = self.model.refine_model()
        self.change_data_from_rhochi_model()
        self.set_time_stamp()
        self.proxy_data_changed.emit()
        return res.success

    # -------------------------------------------------
    # QML accessible properties
    # -------------------------------------------------

    time_stamp = Property(str, get_time_stamp, notify=proxy_data_changed)
    #time_stamp = Property(str, get_time_stamp, notify=proxy_data_changed)
    project_name = Property(str, get_project_name, notify=proxy_data_changed)
    project_info = Property(str, get_project_info, notify=proxy_data_changed)
    project_dir_absolute_path = Property(str, get_project_dir_absolute_path, notify=proxy_data_changed)
    project_opened = Property(bool, is_project_opened, notify=proxy_data_changed)

