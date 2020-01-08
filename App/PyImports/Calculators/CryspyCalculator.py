import os
import time
import logging
import operator
from functools import reduce
from datetime import datetime
import numpy as np
import cryspy
import pycifstar
from cryspy.scripts.cl_rhochi import RhoChi

from PySide2.QtCore import QObject, Signal

PHASE_SEGMENT = "_phases"
EXPERIMENT_SEGMENT = "_experiments"

class CryspyCalculator(QObject):
    def __init__(self, main_rcif_path, parent=None):
        super().__init__(parent)
        logging.info("")
        # internal dicts
        self._app_dict = {}
        self._calculator_dict = {}
        self._info_dict = {}
        self._phases_dict = {}
        self._experiments_dict = {}
        self._calculations_dict = {}
        # cryspy
        self._main_rcif_path = main_rcif_path
        self._main_rcif = None
        self._phases_path = ""
        self._phase_name = ""
        self._experiments_path = ""
        self.final_chi_square = None
        self._cryspy_obj = self._createCryspyObj() #cryspy.rhochi_read_file(self._main_rcif_path)
        # project dict
        self._project_dict = {}
        self.setProjectDictFromCryspyObj()

    def updateExps(self, exp_path):
        """
        Parse the relevant phases file and update the corresponding model
        """
        self._experiments_path = exp_path
        rcif_content = ""

        # This will read the CIF file
        if os.path.isfile(self._experiments_path):
            with open(self._experiments_path, 'r') as f:
                exp_rcif_content = f.read()
                rcif_content += exp_rcif_content

        phase_segment = self._cryspy_obj.crystals[0].to_cif
        experiment_segment = rcif_content

        # find the name of the new phase
        data_segment = phase_segment.find('data_')  # first instance only
        data_segment_length = len('data_')
        end_loc = data_segment + phase_segment[data_segment:].find('\n')
        phase_name = phase_segment[data_segment + data_segment_length:end_loc].strip()

        # Concatenate the corrected experiment and the new CIF
        rcif_content = experiment_segment + phase_segment

        # This will update the CrysPy object
        self._cryspy_obj.from_cif(rcif_content)

        self._cryspy_obj.experiments[0]._Pd__phase._PdPhase__pd_phase_label[0] = phase_name

        # This will re-create all local directories
        self.setProjectDictFromCryspyObj()

        # This will notify the GUI models changed
        self.projectDictChanged.emit()

    def updatePhases(self, phases_path):
        """
        Parse the relevant phases file and update the corresponding model
        """
        self._phases_path = phases_path
        rcif_content = ""

        # This will read the CIF file
        if os.path.isfile(self._phases_path):
            with open(self._phases_path, 'r') as f:
                phases_rcif_content = f.read()
                rcif_content += phases_rcif_content

        # find the name of the new phase
        data_segment = phases_rcif_content.find('data_') # first instance only
        data_segment_length = len('data_')
        end_loc = data_segment + phases_rcif_content[data_segment:].find('\n')
        new_phase_name = phases_rcif_content[data_segment+data_segment_length:end_loc].strip()

        experiment_segment = ''
        if len(self._cryspy_obj.experiments) > 0:
            experiment_segment = self._cryspy_obj.experiments[0].to_cif

        # Concatenate the corrected experiment and the new CIF
        rcif_content = rcif_content + "\n" + experiment_segment

        # This will update the CrysPy object
        self._cryspy_obj.from_cif(rcif_content)

        if len(self._cryspy_obj.experiments) > 0:
            self._cryspy_obj.experiments[0]._Pd__phase._PdPhase__pd_phase_label[0] = new_phase_name

        # This will re-create all local directories
        self.setProjectDictFromCryspyObj()

        # This will notify the GUI models changed
        self.projectDictChanged.emit()

    def replacePhaseInSegment(self, segment, new_phase_name):
        """
        Replaces original phase name with the given name in a segment
        """
        segment_content = self._parseSegment(segment)
        old_phase_name = self._phase_name
        if old_phase_name and old_phase_name != new_phase_name:
            segment_content = segment_content.replace(old_phase_name, new_phase_name)
            # update old phase name
            self._phase_name = new_phase_name

        # return the new segment
        return segment_content

    def replaceDataInSegment(self, segment_content, new_data_name):
        """
        Replaces original phase name with the given name in a string representation of segment
        """
        if not segment_content:
            return segment_content

        data_keyword = 'data_'
        # Find old data name location
        data_loc = segment_content.find(data_keyword)

        # End of replaced text is the first occurence of EOL
        data_loc_end = segment_content[data_loc:].find('\n')

        # Length of 'data_' string
        data_len = len(data_keyword)
        # Location of the string to be replaced
        data_loc_start = data_loc + data_len

        # New string = 'data_<new_data_name>\n...'
        new_segment = segment_content[:data_loc_start]
        new_segment += new_data_name
        # append the rest of the string
        new_segment += segment_content[data_loc_end+data_loc_start-data_len:]

        # return the new segment
        return new_segment

    def _parseSegment(self, segment=""):
        """Parse the given segment info from the main rcif file"""
        if not segment:
            return ""
        if segment not in (PHASE_SEGMENT, EXPERIMENT_SEGMENT):
            return ""
        rcif_dir_name = os.path.dirname(self._main_rcif_path)
        self._main_rcif = pycifstar.read_star_file(self._main_rcif_path)
        rcif_content = ""
        if segment in str(self._main_rcif):
            segment_rcif_path = os.path.join(rcif_dir_name, self._main_rcif[segment].value)
            if os.path.isfile(segment_rcif_path):
                with open(segment_rcif_path, 'r') as f:
                    segment_rcif_content = f.read()
                    rcif_content += segment_rcif_content
        return rcif_content

    def _createCryspyObj(self):
        """Create cryspy object from separate rcif files"""
        phase_segment = self._parseSegment(PHASE_SEGMENT)
        full_rcif_content = self._parseSegment(EXPERIMENT_SEGMENT) + phase_segment
        # update the phase name global
        self._setPhaseName(phase_segment)
        #rho_chi = cryspy.RhoChi()
        #rho_chi.from_cif(full_rcif_content)
        rho_chi = RhoChi().from_cif(full_rcif_content)
        return rho_chi

    def _setPhaseName(self, phase_segment):
        """
        Set the phase name in state
        """
        if not phase_segment:
            self._phase_name = ''
            return
        data_keyword = 'data_'
        data_keyword_length = len(data_keyword)
        data_segment = phase_segment.find(data_keyword)
        end_loc = data_segment + phase_segment[data_segment:].find('\n')
        self._phase_name = phase_segment[data_segment+data_keyword_length:end_loc].strip()

        return

    def writeMainCif(self, saveDir):
        main_block = self._main_rcif
        if len(self._cryspy_obj.crystals) > 0:
            main_block["_phases"].value = 'phases.cif'
        if len(self._cryspy_obj._RhoChi__experiments) > 0:
            main_block["_experiments"].value = 'experiments.cif'
        main_block.to_file(os.path.join(saveDir, 'main.cif'))

    def writePhaseCif(self, saveDir):
        phases_block = pycifstar.Global()
        # TODO write output for multiple phases
        if len(self._cryspy_obj.crystals) > 0:
            phases_block.take_from_string(self._cryspy_obj.crystals[0].to_cif)
        phases_block.to_file(os.path.join(saveDir, 'phases.cif'))

    def writeExpCif(self, saveDir):
        exp_block = pycifstar.Global()
        if len(self._cryspy_obj._RhoChi__experiments) > 0:
            exp_block.take_from_string(self._cryspy_obj._RhoChi__experiments[0].to_cif)
        exp_block.to_file(os.path.join(saveDir, 'experiments.cif'))

    def saveCifs(self, saveDir):
        self.writeMainCif(saveDir)
        self.writePhaseCif(saveDir)
        self.writeExpCif(saveDir)


    def setAppDict(self):
        """Set application state"""
        self._app_dict = {
            'name': 'easyDiffraction',
            'version': '0.3.9',
            'url': 'http://easydiffraction.org'
        }

    def setCalculatorDict(self):
        """Set calculator state"""
        self._calculator_dict = {
            'name': 'CrysPy',
            'version': '0.1.13',
            'url': 'https://github.com/ikibalin/cryspy'
        }

    def setInfoDict(self):
        """Set additional project info"""
        # try:
        name = self._main_rcif["_name"].value if "_name" in str(self._main_rcif) else 'Unknown'
        # except AttributeError:
        #     return
        keywords = self._main_rcif["_keywords"].value.split(', ') if "_keywords" in str(self._main_rcif) else ['']
        self._info_dict = {
            'name': name,
            'keywords': keywords,
            'phase_ids': [],
            'experiment_ids': [],
            'created_datetime': '',
            'modified_datetime': '',
            'refinement_datetime': ''
        }

    def _addPhasesDescription(self):
        """ ... """
        for phase in self._phases_dict.values():
            # Space group
            space_group = phase['space_group']
            space_group['crystal_system']['header'] = 'Crystal system'
            space_group['crystal_system']['tooltip'] = 'The name of the system of geometric crystal classes of space groups (crystal system) to which the space group belongs.'
            space_group['crystal_system']['url'] = 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Ispace_group_crystal_system.html'
            space_group['space_group_name_H-M_alt']['header'] = 'Symbol'
            space_group['space_group_name_H-M_alt']['tooltip'] = 'The Hermann-Mauguin symbol of space group.'
            space_group['space_group_name_H-M_alt']['url'] = 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Ispace_group_name_H-M_alt.html'
            space_group['space_group_IT_number']['header'] = 'Number'
            space_group['space_group_IT_number']['tooltip'] = 'The number as assigned in International Tables for Crystallography Vol. A.'
            space_group['space_group_IT_number']['url'] = 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Ispace_group_crystal_system.html'
            space_group['origin_choice']['header'] = 'Setting'
            # Unit cell parameters
            cell = phase['cell']
            cell['length_a']['header'] = 'a (Å)'
            cell['length_a']['tooltip'] = 'Unit-cell length of the selected structure in angstroms.'
            cell['length_a']['url'] = 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Icell_length_.html'
            cell['length_b']['header'] = 'b (Å)'
            cell['length_b']['tooltip'] = cell['length_a']['tooltip']
            cell['length_b']['url'] = cell['length_a']['url']
            cell['length_c']['header'] = 'c (Å)'
            cell['length_c']['tooltip'] = cell['length_a']['tooltip']
            cell['length_c']['url'] = cell['length_a']['url']
            cell['angle_alpha']['header'] = 'alpha (°)'
            cell['angle_alpha']['tooltip'] = 'Unit-cell angle of the selected structure in degrees.'
            cell['angle_alpha']['url'] = 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Icell_angle_.html'
            cell['angle_beta']['header'] = 'beta (°)'
            cell['angle_beta']['tooltip'] = cell['angle_alpha']['tooltip']
            cell['angle_beta']['url'] = cell['angle_alpha']['url']
            cell['angle_gamma']['header'] = 'gamma (°)'
            cell['angle_gamma']['tooltip'] = cell['angle_alpha']['tooltip']
            cell['angle_gamma']['url'] = cell['angle_alpha']['url']
            # Atom sites
            for atom_site in phase['atom_site'].values():
                # Atom sites symbol
                atom_site['type_symbol']['header'] = 'Atom'
                atom_site['type_symbol']['tooltip'] = 'A code to identify the atom species occupying this site.'
                atom_site['type_symbol']['url'] = 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_type_symbol.html'
                # Atom site neutron scattering length
                atom_site['scat_length_neutron']['header'] = ''
                atom_site['scat_length_neutron']['tooltip'] = ''
                atom_site['scat_length_neutron']['url'] = ''
                # Atom site coordinates
                atom_site['fract_x']['header'] = 'x'
                atom_site['fract_x']['tooltip'] = 'Atom-site coordinate as fractions of the unit cell length.'
                atom_site['fract_x']['url'] = 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html'
                atom_site['fract_y']['header'] = 'y'
                atom_site['fract_y']['tooltip'] = atom_site['fract_x']['tooltip']
                atom_site['fract_y']['url'] = atom_site['fract_x']['url']
                atom_site['fract_z']['header'] = 'z'
                atom_site['fract_z']['tooltip'] = atom_site['fract_x']['tooltip']
                atom_site['fract_z']['url'] = atom_site['fract_x']['url']
                # Atom site occupancy
                atom_site['occupancy']['header'] = 'Occupancy'
                atom_site['occupancy']['tooltip'] = 'The fraction of the atom type present at this site.'
                atom_site['occupancy']['url'] = 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_occupancy.html'
                # Atom site ADP type
                atom_site['adp_type']['header'] = 'Type'
                atom_site['adp_type']['tooltip'] = 'A standard code used to describe the type of atomic displacement parameters used for the site.'
                atom_site['adp_type']['url'] = 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_adp_type.html'
                # Atom site isotropic ADP
                atom_site['B_iso_or_equiv']['header'] = 'Biso'
                atom_site['B_iso_or_equiv']['tooltip'] = 'Isotropic atomic displacement parameter, or equivalent isotropic atomic displacement parameter, B(equiv), in angstroms squared.'
                atom_site['B_iso_or_equiv']['url'] = 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_B_iso_or_equiv.html'
                # Atom site anisotropic ADP
                if 'u_11' in atom_site.keys():
                    atom_site['u_11']['header'] = 'U11'
                    atom_site['u_11']['tooltip'] = 'Anisotropic atomic displacement component in angstroms squared.'
                    atom_site['u_11']['url'] = 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_aniso_U_.html'
                    atom_site['u_22']['header'] = 'U22'
                    atom_site['u_22']['tooltip'] = atom_site['u_11']['tooltip']
                    atom_site['u_22']['url'] = atom_site['u_11']['url']
                    atom_site['u_33']['header'] = 'U33'
                    atom_site['u_33']['tooltip'] = atom_site['u_11']['tooltip']
                    atom_site['u_33']['url'] = atom_site['u_11']['url']
                    atom_site['u_12']['header'] = 'U12'
                    atom_site['u_12']['tooltip'] = atom_site['u_11']['tooltip']
                    atom_site['u_12']['url'] = atom_site['u_11']['url']
                    atom_site['u_13']['header'] = 'U13'
                    atom_site['u_13']['tooltip'] = atom_site['u_11']['tooltip']
                    atom_site['u_13']['url'] = atom_site['u_11']['url']
                    atom_site['u_23']['header'] = 'U23'
                    atom_site['u_23']['tooltip'] = atom_site['u_11']['tooltip']
                    atom_site['u_23']['url'] = atom_site['u_11']['url']
                # Atom site MSP
                if 'chi_11' in atom_site.keys():
                    atom_site['chi_type']['header'] = 'Type'
                    atom_site['chi_type']['tooltip'] = ''
                    atom_site['chi_type']['url'] = ''
                    atom_site['chi_11']['header'] = 'Chi11'
                    atom_site['chi_11']['tooltip'] = ''
                    atom_site['chi_11']['url'] = ''
                    atom_site['chi_22']['header'] = 'Chi22'
                    atom_site['chi_22']['tooltip'] = atom_site['chi_11']['tooltip']
                    atom_site['chi_22']['url'] = atom_site['chi_11']['url']
                    atom_site['chi_33']['header'] = 'Chi33'
                    atom_site['chi_33']['tooltip'] = atom_site['chi_11']['tooltip']
                    atom_site['chi_33']['url'] = atom_site['chi_11']['url']
                    atom_site['chi_12']['header'] = 'Chi12'
                    atom_site['chi_12']['tooltip'] = atom_site['chi_11']['tooltip']
                    atom_site['chi_12']['url'] = atom_site['chi_11']['url']
                    atom_site['chi_13']['header'] = 'Chi13'
                    atom_site['chi_13']['tooltip'] = atom_site['chi_11']['tooltip']
                    atom_site['chi_13']['url'] = atom_site['chi_11']['url']
                    atom_site['chi_23']['header'] = 'Chi23'
                    atom_site['chi_23']['tooltip'] = atom_site['chi_11']['tooltip']
                    atom_site['chi_23']['url'] = atom_site['chi_11']['url']

    def _createObjDict(self, obj):
        """ ... """
        if isinstance(obj, cryspy.common.cl_fitable.Fitable):
            return {
                'value': obj.value,
                'error': obj.sigma,
                'min': obj.value * 0.8,
                'max': obj.value * 1.2,
                'constraint': obj.constraint,
                'hide': obj.constraint_flag,
                'refine': obj.refinement
            }
        return {'value': obj}

    def setPhasesDictFromCryspyObj(self):
        """Set phases (sample model tab in GUI)"""
        self._phases_dict.clear()
        for calculator_phase in self._cryspy_obj.crystals:
            calculator_phase_name = calculator_phase.data_name
            self._phases_dict[calculator_phase_name] = {}
            # Space group
            project_space_group = self._phases_dict[calculator_phase_name]['space_group'] = {}
            calculator_space_group = calculator_phase.space_group
            project_space_group['crystal_system'] = self._createObjDict(calculator_space_group.crystal_system)
            project_space_group['space_group_name_H-M_alt'] = self._createObjDict(calculator_space_group.name_hm_ref)
            project_space_group['space_group_IT_number'] = self._createObjDict(calculator_space_group.it_number)
            project_space_group['origin_choice'] = self._createObjDict(calculator_space_group.it_coordinate_system_code)
            # Unit cell parameters
            project_cell = self._phases_dict[calculator_phase_name]['cell'] = {}
            claculator_cell = calculator_phase.cell
            project_cell['length_a'] = self._createObjDict(claculator_cell.length_a)
            project_cell['length_b'] = self._createObjDict(claculator_cell.length_b)
            project_cell['length_c'] = self._createObjDict(claculator_cell.length_c)
            project_cell['angle_alpha'] = self._createObjDict(claculator_cell.angle_alpha)
            project_cell['angle_beta'] = self._createObjDict(claculator_cell.angle_beta)
            project_cell['angle_gamma'] = self._createObjDict(claculator_cell.angle_gamma)
            # Atom sites
            self._phases_dict[calculator_phase_name]['atom_site'] = {}
            for i, label in enumerate(calculator_phase.atom_site.label):
                project_atom_site = self._phases_dict[calculator_phase_name]['atom_site'][label] = {}
                calculator_atom_site = calculator_phase.atom_site
                # Atom sites symbol
                project_atom_site['type_symbol'] = self._createObjDict(calculator_atom_site.type_symbol[i])
                # Atom site neutron scattering length
                project_atom_site['scat_length_neutron'] = self._createObjDict(calculator_atom_site.scat_length_neutron[i])
                # Atom site coordinates
                project_atom_site['fract_x'] = self._createObjDict(calculator_atom_site.fract_x[i])
                project_atom_site['fract_y'] = self._createObjDict(calculator_atom_site.fract_y[i])
                project_atom_site['fract_z'] = self._createObjDict(calculator_atom_site.fract_z[i])
                # Atom site occupancy
                project_atom_site['occupancy'] = self._createObjDict(calculator_atom_site.occupancy[i])
                # Atom site ADP type
                project_atom_site['adp_type'] = self._createObjDict(calculator_atom_site.adp_type[i])
                # Atom site isotropic ADP
                project_atom_site['B_iso_or_equiv'] = self._createObjDict(calculator_atom_site.b_iso_or_equiv[i])
            # Atom site anisotropic ADP
            if calculator_phase.atom_site_aniso is not None:
                for i, label in enumerate(calculator_phase.atom_site_aniso.label):
                    project_atom_site = self._phases_dict[calculator_phase_name]['atom_site'][label]
                    calculator_atom_site = calculator_phase.atom_site_aniso
                    project_atom_site['u_11'] = self._createObjDict(calculator_atom_site.u_11[i])
                    project_atom_site['u_22'] = self._createObjDict(calculator_atom_site.u_22[i])
                    project_atom_site['u_33'] = self._createObjDict(calculator_atom_site.u_33[i])
                    project_atom_site['u_12'] = self._createObjDict(calculator_atom_site.u_12[i])
                    project_atom_site['u_13'] = self._createObjDict(calculator_atom_site.u_13[i])
                    project_atom_site['u_23'] = self._createObjDict(calculator_atom_site.u_23[i])
            # Atom site MSP
            if calculator_phase.atom_site_susceptibility is not None:
                for i, label in enumerate(calculator_phase.atom_site_susceptibility.label):
                    project_atom_site = self._phases_dict[calculator_phase_name]['atom_site'][label]
                    calculator_atom_site = calculator_phase.atom_site_susceptibility
                    project_atom_site['chi_type'] = self._createObjDict(calculator_atom_site.chi_type[i])
                    project_atom_site['chi_11'] = self._createObjDict(calculator_atom_site.chi_11[i])
                    project_atom_site['chi_22'] = self._createObjDict(calculator_atom_site.chi_22[i])
                    project_atom_site['chi_33'] = self._createObjDict(calculator_atom_site.chi_33[i])
                    project_atom_site['chi_12'] = self._createObjDict(calculator_atom_site.chi_12[i])
                    project_atom_site['chi_13'] = self._createObjDict(calculator_atom_site.chi_13[i])
                    project_atom_site['chi_23'] = self._createObjDict(calculator_atom_site.chi_23[i])
            # Atom sites for structure view (all the positions inside unit cell of 1x1x1)
            atom_site_list = [[], [], [], []]
            for x, y, z, scat_length_neutron in zip(calculator_phase.atom_site.fract_x, calculator_phase.atom_site.fract_y, calculator_phase.atom_site.fract_z, calculator_phase.atom_site.scat_length_neutron):
                x_array, y_array, z_array, _ = calculator_phase.space_group.calc_xyz_mult(x.value, y.value, z.value)
                scat_length_neutron_array = np.full_like(x_array, scat_length_neutron)
                atom_site_list[0] += x_array.tolist()
                atom_site_list[1] += y_array.tolist()
                atom_site_list[2] += z_array.tolist()
                atom_site_list[3] += scat_length_neutron_array.tolist()
            for x, y, z, scat_length_neutron in zip(atom_site_list[0], atom_site_list[1], atom_site_list[2], atom_site_list[3]):
                if x == 0.0:
                    atom_site_list[0].append(1.0)
                    atom_site_list[1].append(y)
                    atom_site_list[2].append(z)
                    atom_site_list[3].append(scat_length_neutron)
                if y == 0.0:
                    atom_site_list[0].append(x)
                    atom_site_list[1].append(1.0)
                    atom_site_list[2].append(z)
                    atom_site_list[3].append(scat_length_neutron)
                if z == 0.0:
                    atom_site_list[0].append(x)
                    atom_site_list[1].append(y)
                    atom_site_list[2].append(1.0)
                    atom_site_list[3].append(scat_length_neutron)
            self._phases_dict[calculator_phase_name]['atom_site_list'] = {}
            self._phases_dict[calculator_phase_name]['atom_site_list']['fract_x'] = atom_site_list[0]
            self._phases_dict[calculator_phase_name]['atom_site_list']['fract_y'] = atom_site_list[1]
            self._phases_dict[calculator_phase_name]['atom_site_list']['fract_z'] = atom_site_list[2]
            self._phases_dict[calculator_phase_name]['atom_site_list']['scat_length_neutron'] = atom_site_list[3]
        self._addPhasesDescription()


    def setExperimentsDictFromCryspyObj(self):
        """Set experiments (Experimental data tab in GUI)"""

        self._experiments_dict.clear()

        for experiment in self._cryspy_obj.experiments:

            # Experiment label
            self._experiments_dict[experiment.data_name] = {}

            # Main parameters
            self._experiments_dict[experiment.data_name]['wavelength'] = {
                'header': 'Wavelength (Å)',
                'tooltip': '',
                'url': '',
                'value': experiment.setup.wavelength.value,
                'error': experiment.setup.wavelength.sigma,
                'min': experiment.setup.wavelength.value * 0.8,
                'max': experiment.setup.wavelength.value * 1.2,
                'constraint': experiment.setup.wavelength.constraint,
                'hide': experiment.setup.wavelength.constraint_flag,
                'refine': experiment.setup.wavelength.refinement }
            self._experiments_dict[experiment.data_name]['offset'] = {
                'header': '',
                'tooltip': '',
                'url': '',
                'value': experiment.setup.offset_ttheta.value,
                'error': experiment.setup.offset_ttheta.sigma,
                'min': experiment.setup.offset_ttheta.value * 0.8,
                'max': experiment.setup.offset_ttheta.value * 1.2,
                'constraint': experiment.setup.offset_ttheta.constraint,
                'hide': experiment.setup.offset_ttheta.constraint_flag,
                'refine': experiment.setup.offset_ttheta.refinement }

            # Scale
            # ONLY 1st scale parameter is currently taken into account!!!
            self._experiments_dict[experiment.data_name]['phase'] = {}
            self._experiments_dict[experiment.data_name]['phase']['scale'] = {
                'header': '',
                'tooltip': '',
                'url': '',
                'value': experiment.phase.scale[0].value,
                'error': experiment.phase.scale[0].sigma,
                'min': experiment.phase.scale[0].value * 0.8,
                'max': experiment.phase.scale[0].value * 1.2,
                'constraint': experiment.phase.scale[0].constraint,
                'hide': experiment.phase.scale[0].constraint_flag,
                'refine': experiment.phase.scale[0].refinement }

            # Background
            self._experiments_dict[experiment.data_name]['background'] = {}
            for ttheta, intensity in zip(experiment.background.ttheta, experiment.background.intensity):
                index = str(ttheta)
                self._experiments_dict[experiment.data_name]['background'][index] = {}
                self._experiments_dict[experiment.data_name]['background'][index]['ttheta'] = ttheta
                self._experiments_dict[experiment.data_name]['background'][index]['intensity'] = {
                    'value': intensity.value,
                    'error': intensity.sigma,
                    'min': intensity.value * 0.8,
                    'max': intensity.value * 1.2,
                    'constraint': intensity.constraint,
                    'hide': intensity.constraint_flag,
                    'refine': intensity.refinement }

            # Instrument resolution
            self._experiments_dict[experiment.data_name]['resolution'] = {}
            self._experiments_dict[experiment.data_name]['resolution']['u'] = {
                'header': 'U',
                'tooltip': '',
                'url': '',
                'value': experiment.resolution.u.value,
                'error': experiment.resolution.u.sigma,
                'min': experiment.resolution.u.value * 0.8,
                'max': experiment.resolution.u.value * 1.2,
                'constraint': experiment.resolution.u.constraint,
                'hide': experiment.resolution.u.constraint_flag,
                'refine': experiment.resolution.u.refinement }
            self._experiments_dict[experiment.data_name]['resolution']['v'] = {
                'header': 'V',
                'tooltip': '',
                'url': '',
                'value': experiment.resolution.v.value,
                'error': experiment.resolution.v.sigma,
                'min': experiment.resolution.v.value * 0.8,
                'max': experiment.resolution.v.value * 1.2,
                'constraint': experiment.resolution.v.constraint,
                'hide': experiment.resolution.v.constraint_flag,
                'refine': experiment.resolution.v.refinement }
            self._experiments_dict[experiment.data_name]['resolution']['w'] = {
                'header': 'W',
                'tooltip': '',
                'url': '',
                'value': experiment.resolution.w.value,
                'error': experiment.resolution.w.sigma,
                'min': experiment.resolution.w.value * 0.8,
                'max': experiment.resolution.w.value * 1.2,
                'constraint': experiment.resolution.w.constraint,
                'hide': experiment.resolution.w.constraint_flag,
                'refine': experiment.resolution.w.refinement }
            self._experiments_dict[experiment.data_name]['resolution']['x'] = {
                'header': 'X',
                'tooltip': '',
                'url': '',
                'value': experiment.resolution.x.value,
                'error': experiment.resolution.x.sigma,
                'min': experiment.resolution.x.value * 0.8,
                'max': experiment.resolution.x.value * 1.2,
                'constraint': experiment.resolution.x.constraint,
                'hide': experiment.resolution.x.constraint_flag,
                'refine': experiment.resolution.x.refinement }
            self._experiments_dict[experiment.data_name]['resolution']['y'] = {
                'header': 'Y',
                'tooltip': '',
                'url': '',
                'value': experiment.resolution.y.value,
                'error': experiment.resolution.y.sigma,
                'min': experiment.resolution.y.value * 0.8,
                'max': experiment.resolution.y.value * 1.2,
                'constraint': experiment.resolution.y.constraint,
                'hide': experiment.resolution.y.constraint_flag,
                'refine': experiment.resolution.y.refinement }

            # Measured data points
            logging.info("measured data points: start")
            x_obs = np.array(experiment.meas.ttheta)
            y_obs_up = np.array(experiment.meas.intensity_up)
            sy_obs_up = np.array(experiment.meas.intensity_up_sigma)
            y_obs_down = np.array(experiment.meas.intensity_down)
            sy_obs_down = np.array(experiment.meas.intensity_down_sigma)
            y_obs = y_obs_up + y_obs_down
            sy_obs = np.sqrt(np.square(sy_obs_up) + np.square(sy_obs_down))
            y_obs_upper = y_obs + sy_obs
            y_obs_lower = y_obs - sy_obs
            self._experiments_dict[experiment.data_name]['measured_pattern'] = {
                'x': x_obs.tolist(),
                'y_obs_up': y_obs_up.tolist(),
                'sy_obs_up': sy_obs_up.tolist(),
                'y_obs_down': y_obs_down.tolist(),
                'sy_obs_down': sy_obs_down.tolist(),
                'y_obs_upper': y_obs_upper.tolist(),
                'y_obs_lower': y_obs_lower.tolist(),
            }
            logging.info("measured data points: end")

    def setCalculationsDictFromCryspyObj(self):
        """Set calculated data (depends on phases and experiments from above)"""
        self._calculations_dict.clear()

        for experiment in self._cryspy_obj.experiments:

            # Experiment label
            self._calculations_dict[experiment.data_name] = {}

            # Calculated chi squared and number of data points used for refinement
            logging.info("calc_chi_sq start") # profiling
            chi_sq = 0.0
            n_res = 1
            chi_sq, n_res = experiment.calc_chi_sq(self._cryspy_obj.crystals)
            logging.info("calc_chi_sq end") # profiling

            self.final_chi_square = chi_sq / n_res

            # Main parameters
            self._info_dict['chi_squared'] = {
                'header': '',
                'tooltip': '',
                'url': '',
                'value': float(self.final_chi_square) }
            self._info_dict['n_res'] = {
                'header': '',
                'tooltip': '',
                'url': '',
                'value': int(n_res) }

            # Calculated data
            logging.info("calc_profile start") # profiling
            calculated_pattern, bragg_peaks, _ = experiment.calc_profile(np.array(experiment.meas.ttheta), self._cryspy_obj.crystals)
            logging.info("calc_profile end") # profiling

            # Bragg peaks
            offset = self._experiments_dict[experiment.data_name]['offset']['value']
            self._calculations_dict[experiment.data_name]['bragg_peaks'] = {}
            for index, crystal in enumerate(self._cryspy_obj.crystals):
                self._calculations_dict[experiment.data_name]['bragg_peaks'][crystal.data_name] = {
                    'h': bragg_peaks[index].index_h,
                    'k': bragg_peaks[index].index_k,
                    'l': bragg_peaks[index].index_l,
                    'ttheta': (np.array(bragg_peaks[index].ttheta) + offset).tolist()
                }

            # Calculated diffraction pattern
            logging.info("calculated diffraction pattern: start")
            x_calc = np.array(calculated_pattern.ttheta)
            y_obs_up = np.array(experiment.meas.intensity_up)
            sy_obs_up = np.array(experiment.meas.intensity_up_sigma)
            y_obs_down = np.array(experiment.meas.intensity_down)
            sy_obs_down = np.array(experiment.meas.intensity_down_sigma)
            y_obs = y_obs_up + y_obs_down
            sy_obs = np.sqrt(np.square(sy_obs_up) + np.square(sy_obs_down))
            y_obs_upper = y_obs + sy_obs
            y_obs_lower = y_obs - sy_obs
            y_calc_up = np.array(calculated_pattern.intensity_up_total)
            y_calc_down = np.array(calculated_pattern.intensity_down_total)
            y_calc = y_calc_up + y_calc_down
            y_diff_upper = y_obs + sy_obs - y_calc
            y_diff_lower = y_obs - sy_obs - y_calc
            self._calculations_dict[experiment.data_name]['calculated_pattern'] = {
                'x': x_calc.tolist(),
                'y_calc': y_calc.tolist(),
                'y_diff_lower': y_diff_lower.tolist(),
                'y_diff_upper': y_diff_upper.tolist()
            }
            logging.info("calculated diffraction pattern: end")

            # Calculated data limits
            # !!!!!!!!!!
            self._calculations_dict[experiment.data_name]['limits'] = {}
            self._calculations_dict[experiment.data_name]['limits']['main'] = {
                'x_min': np.amin(x_calc).item(),
                'x_max': np.amax(x_calc).item(),
                'y_min': np.amin([np.amin(y_calc_down), np.amin(y_obs_lower)]).item(),
                'y_max': np.amax([np.amax(y_calc_up), np.amax(y_obs_upper)]).item()
                }
            self._calculations_dict[experiment.data_name]['limits']['difference'] = {
                'y_min': np.amin(y_diff_lower).item(),
                'y_max': np.amax(y_diff_upper).item()
                }

    def setProjectDictFromCryspyObj(self):
        """Combine all the data to one project dictionary"""
        self._cryspy_obj.apply_constraint()
        self.setAppDict()
        self.setCalculatorDict()
        self.setInfoDict()
        self.setPhasesDictFromCryspyObj()
        self.setExperimentsDictFromCryspyObj()
        self.setCalculationsDictFromCryspyObj()
        self._info_dict['phase_ids'] = list(self._phases_dict.keys())
        self._info_dict['experiment_ids'] = list(self._experiments_dict.keys())
        self._info_dict['modified_datetime'] = datetime.fromtimestamp(os.path.getmtime(self._main_rcif_path)).strftime('%d %b %Y, %H:%M:%S')
        self._info_dict['refinement_datetime'] = str(np.datetime64('now'))
        self._project_dict = {
            'app': self._app_dict,
            'calculator': self._calculator_dict,
            'info': self._info_dict,
            'phases': self._phases_dict,
            'experiments': self._experiments_dict,
            'calculations': self._calculations_dict,
        }

    def setCryspyObjFromPhases(self):
        """Set phases (sample model tab in GUI)"""
        for phase in self._cryspy_obj.crystals:

            # Unit cell parameters
            phase.cell.length_a.value = self._phases_dict[phase.data_name]['cell']['length_a']['value']
            phase.cell.length_b.value = self._phases_dict[phase.data_name]['cell']['length_b']['value']
            phase.cell.length_c.value = self._phases_dict[phase.data_name]['cell']['length_c']['value']
            phase.cell.length_a.refinement = self._phases_dict[phase.data_name]['cell']['length_a']['refine']
            phase.cell.length_b.refinement = self._phases_dict[phase.data_name]['cell']['length_b']['refine']
            phase.cell.length_c.refinement = self._phases_dict[phase.data_name]['cell']['length_c']['refine']

            # Atom site coordinates
            for label, x, y, z in zip(phase.atom_site.label, phase.atom_site.fract_x, phase.atom_site.fract_y, phase.atom_site.fract_z):
                x.value = self._phases_dict[phase.data_name]['atom_site'][label]['fract_x']['value']
                y.value = self._phases_dict[phase.data_name]['atom_site'][label]['fract_y']['value']
                z.value = self._phases_dict[phase.data_name]['atom_site'][label]['fract_z']['value']
                x.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['fract_x']['refine']
                y.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['fract_y']['refine']
                z.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['fract_z']['refine']

            # Atom site occupancy
            for label, occupancy in zip(phase.atom_site.label, phase.atom_site.occupancy):
                occupancy.value = self._phases_dict[phase.data_name]['atom_site'][label]['occupancy']['value']
                occupancy.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['occupancy']['refine']

            # Isotropic ADP
            for label, b_iso in zip(phase.atom_site.label, phase.atom_site.b_iso_or_equiv):
                b_iso.value = self._phases_dict[phase.data_name]['atom_site'][label]['B_iso_or_equiv']['value']
                b_iso.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['B_iso_or_equiv']['refine']

            # Anisotropic ADP
            if phase.atom_site_aniso is not None:
                for label, u_11, u_22, u_33, u_12, u_13, u_23 in zip(phase.atom_site_aniso.label,
                    phase.atom_site_aniso.u_11, phase.atom_site_aniso.u_22, phase.atom_site_aniso.u_33,
                    phase.atom_site_aniso.u_12, phase.atom_site_aniso.u_13, phase.atom_site_aniso.u_23):
                        u_11.value = self._phases_dict[phase.data_name]['atom_site'][label]['u_11']['value']
                        u_22.value = self._phases_dict[phase.data_name]['atom_site'][label]['u_22']['value']
                        u_33.value = self._phases_dict[phase.data_name]['atom_site'][label]['u_33']['value']
                        u_12.value = self._phases_dict[phase.data_name]['atom_site'][label]['u_12']['value']
                        u_13.value = self._phases_dict[phase.data_name]['atom_site'][label]['u_13']['value']
                        u_23.value = self._phases_dict[phase.data_name]['atom_site'][label]['u_23']['value']
                        u_11.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['u_11']['refine']
                        u_22.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['u_22']['refine']
                        u_33.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['u_33']['refine']
                        u_12.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['u_12']['refine']
                        u_13.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['u_13']['refine']
                        u_23.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['u_23']['refine']

            # Anisotropic MSP
            if phase.atom_site_susceptibility is not None:
                for label, chi_11, chi_22, chi_33, chi_12, chi_13, chi_23 in zip(phase.atom_site_susceptibility.label,
                    phase.atom_site_susceptibility.chi_11, phase.atom_site_susceptibility.chi_22, phase.atom_site_susceptibility.chi_33,
                    phase.atom_site_susceptibility.chi_12, phase.atom_site_susceptibility.chi_13, phase.atom_site_susceptibility.chi_23):
                        chi_11.value = self._phases_dict[phase.data_name]['atom_site'][label]['chi_11']['value']
                        chi_22.value = self._phases_dict[phase.data_name]['atom_site'][label]['chi_22']['value']
                        chi_33.value = self._phases_dict[phase.data_name]['atom_site'][label]['chi_33']['value']
                        chi_12.value = self._phases_dict[phase.data_name]['atom_site'][label]['chi_12']['value']
                        chi_13.value = self._phases_dict[phase.data_name]['atom_site'][label]['chi_13']['value']
                        chi_23.value = self._phases_dict[phase.data_name]['atom_site'][label]['chi_23']['value']
                        chi_11.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['chi_11']['refine']
                        chi_22.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['chi_22']['refine']
                        chi_33.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['chi_33']['refine']
                        chi_12.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['chi_12']['refine']
                        chi_13.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['chi_13']['refine']
                        chi_23.refinement = self._phases_dict[phase.data_name]['atom_site'][label]['chi_23']['refine']

    def setCryspyObjFromExperiments(self):
        """Set experiments (Experimental data tab in GUI)"""
        for experiment in self._cryspy_obj.experiments:

            # Main parameters
            experiment.setup.offset_ttheta.value = self._experiments_dict[experiment.data_name]['offset']['value']
            experiment.setup.offset_ttheta.refinement = self._experiments_dict[experiment.data_name]['offset']['refine']
            experiment.setup.wavelength.value = self._experiments_dict[experiment.data_name]['wavelength']['value']
            experiment.setup.wavelength.refinement = self._experiments_dict[experiment.data_name]['wavelength']['refine']

            # Scale
            # ONLY 1st scale parameter is currently taken into account!!!
            experiment.phase.scale[0].value = self._experiments_dict[experiment.data_name]['phase']['scale']['value']
            experiment.phase.scale[0].refinement = self._experiments_dict[experiment.data_name]['phase']['scale']['refine']

            # Background
            for ttheta, intensity in zip(experiment.background.ttheta, experiment.background.intensity):
                index = str(ttheta)
                intensity.value = self._experiments_dict[experiment.data_name]['background'][index]['intensity']['value']
                intensity.refinement = self._experiments_dict[experiment.data_name]['background'][index]['intensity']['refine']

            # Instrument resolution
            experiment.resolution.u.value = self._experiments_dict[experiment.data_name]['resolution']['u']['value']
            experiment.resolution.v.value = self._experiments_dict[experiment.data_name]['resolution']['v']['value']
            experiment.resolution.w.value = self._experiments_dict[experiment.data_name]['resolution']['w']['value']
            experiment.resolution.x.value = self._experiments_dict[experiment.data_name]['resolution']['x']['value']
            experiment.resolution.y.value = self._experiments_dict[experiment.data_name]['resolution']['y']['value']
            experiment.resolution.u.refinement = self._experiments_dict[experiment.data_name]['resolution']['u']['refine']
            experiment.resolution.v.refinement = self._experiments_dict[experiment.data_name]['resolution']['v']['refine']
            experiment.resolution.w.refinement = self._experiments_dict[experiment.data_name]['resolution']['w']['refine']
            experiment.resolution.x.refinement = self._experiments_dict[experiment.data_name]['resolution']['x']['refine']
            experiment.resolution.y.refinement = self._experiments_dict[experiment.data_name]['resolution']['y']['refine']

    def setCryspyObjFromProjectDict(self):
        """Set all the cryspy parameters from project dictionary"""
        self.setCryspyObjFromPhases()
        self.setCryspyObjFromExperiments()

    projectDictChanged = Signal()

    def getByPath(self, keys):
        """Access a nested object in root by key sequence."""
        return reduce(operator.getitem, keys, self._project_dict)

    def setByPath(self, keys, value):
        """Get a value in a nested object in root by key sequence."""
        self.getByPath(keys[:-1])[keys[-1]] = value
        self.setCryspyObjFromProjectDict() # updates value in cryspy obj (actually all values, which is too expensive...)
        logging.info(value)
        # Temporarly disable this check below and update model even if just 'fit' checkbox is changed.
        #if not isinstance(value, bool):
        #self.setCalculationsDictFromCryspyObj() # updates back calculated curve, if something is changed but Fit checkBox
        self.setProjectDictFromCryspyObj()
        self.projectDictChanged.emit()

    def phasesCount(self):
        """Returns number of phases in the project."""
        return len(self._project_dict['phases'].keys())

    def experimentsCount(self):
        """Returns number of experiments in the project."""
        return len(self._project_dict['experiments'].keys())

    def phasesIds(self):
        """Returns labels of the phases in the project."""
        return list(self._project_dict['phases'].keys())

    def experimentsIds(self):
        """Returns labels of the experiments in the project."""
        return list(self._project_dict['experiments'].keys())

    def asDict(self): ### asProjectDict
        """Return data dict."""
        return self._project_dict

    def name(self):
        return self._project_dict["info"]["name"]

    def asCifDict(self):
        """..."""
        logging.info("")
        #logging.info(self._cryspy_obj.experiments[0].to_cif)
        #logging.info("asCifDict")
        experiments = {}
        calculations = {}
        phases = {}
        if len(self._cryspy_obj.experiments) > 0:
            #experiments = "data_" + self._cryspy_obj.experiments[0].data_name + "\n" + self._cryspy_obj.experiments[0].params_to_cif + "\n" + self._cryspy_obj.experiments[0].data_to_cif # maybe meas_to_cif
            #calculations = self._cryspy_obj.experiments[0].calc_to_cif
            experiments = '' # temporarily disable, because not implemented yet in cryspy 0.2.0
            calculations = '' # temporarily disable, because not implemented yet in cryspy 0.2.0
        if len(self._cryspy_obj.crystals) > 0:
            phases = self._cryspy_obj.crystals[0].to_cif
        return {
            'phases': phases,
            'experiments': experiments,
            'calculations': calculations
            }

    def refine(self):
        """refinement ..."""
        scipy_refinement_res = self._cryspy_obj.refine()
        #logging.info(scipy_refinement_res)
        self.setProjectDictFromCryspyObj()
        self.projectDictChanged.emit()
        try:
            return {
                "num_refined_parameters": len(scipy_refinement_res.x),
                "refinement_message":scipy_refinement_res.message,
                "nfev":scipy_refinement_res.nfev,
                "nit":scipy_refinement_res.nit,
                "njev":scipy_refinement_res.njev,
                "final_chi_sq":float(self.final_chi_square),
                #"final_chi_sq":float(scipy_refinement_res.fun),
            }
        except:
             return { "refinement_message":"Unknow problems during refinement" }
