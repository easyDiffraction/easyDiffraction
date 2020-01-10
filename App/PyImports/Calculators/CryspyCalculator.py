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
                #atom_site['B_iso_or_equiv']['header'] = 'Biso'
                #atom_site['B_iso_or_equiv']['tooltip'] = 'Isotropic atomic displacement parameter, or equivalent isotropic atomic displacement parameter, B(equiv), in angstroms squared.'
                #atom_site['B_iso_or_equiv']['url'] = 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_B_iso_or_equiv.html'
                atom_site['U_iso_or_equiv']['header'] = 'Uiso'
                atom_site['U_iso_or_equiv']['tooltip'] = 'Isotropic atomic displacement parameter, or equivalent isotropic atomic displacement parameter, U(equiv), in angstroms squared.'
                atom_site['U_iso_or_equiv']['url'] = 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_U_iso_or_equiv.html'

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


    def _addExperimentsDescription(self):
        """ ... """

        for experiment in self._experiments_dict.values():

            # Experimental setup
            experiment['wavelength']['header'] = 'Wavelength (Å)'
            experiment['wavelength']['tooltip'] = ''
            experiment['wavelength']['url'] = ''
            experiment['offset']['header'] = ''
            experiment['offset']['tooltip'] = ''
            experiment['offset']['url'] = ''

            # Instrument resolution
            experiment['resolution']['u']['header'] = 'U'
            experiment['resolution']['u']['tooltip'] = ''
            experiment['resolution']['u']['url'] = ''
            experiment['resolution']['u']['header'] = 'V'
            experiment['resolution']['u']['tooltip'] = ''
            experiment['resolution']['u']['url'] = ''
            experiment['resolution']['u']['header'] = 'W'
            experiment['resolution']['u']['tooltip'] = ''
            experiment['resolution']['u']['url'] = ''
            experiment['resolution']['u']['header'] = 'X'
            experiment['resolution']['u']['tooltip'] = ''
            experiment['resolution']['u']['url'] = ''
            experiment['resolution']['u']['header'] = 'Y'
            experiment['resolution']['u']['tooltip'] = ''
            experiment['resolution']['u']['url'] = ''


    def _createProjDictFromObj(self, obj):
        """ ... """
        if not isinstance(obj, cryspy.common.cl_fitable.Fitable):
            return { 'value': obj }
        return {
            'value': obj.value,
            'error': obj.sigma,
            'min': obj.value * 0.8,
            'max': obj.value * 1.2,
            'constraint': obj.constraint,
            'hide': obj.constraint_flag,
            'refine': obj.refinement
        }


    def setPhasesDictFromCryspyObj(self):
        """Set phases (sample model tab in GUI)"""

        self._phases_dict.clear()

        for calculator_phase in self._cryspy_obj.crystals:
            calculator_phase_name = calculator_phase.data_name
            project_phase = self._phases_dict[calculator_phase_name] = {}

            # Space group
            project_space_group = project_phase['space_group'] = {}
            calculator_space_group = calculator_phase.space_group
            project_space_group['crystal_system'] = self._createProjDictFromObj(calculator_space_group.crystal_system)
            project_space_group['space_group_name_H-M_alt'] = self._createProjDictFromObj(calculator_space_group.name_hm_ref)
            project_space_group['space_group_IT_number'] = self._createProjDictFromObj(calculator_space_group.it_number)
            project_space_group['origin_choice'] = self._createProjDictFromObj(calculator_space_group.it_coordinate_system_code)

            # Unit cell parameters
            project_cell = project_phase['cell'] = {}
            claculator_cell = calculator_phase.cell
            project_cell['length_a'] = self._createProjDictFromObj(claculator_cell.length_a)
            project_cell['length_b'] = self._createProjDictFromObj(claculator_cell.length_b)
            project_cell['length_c'] = self._createProjDictFromObj(claculator_cell.length_c)
            project_cell['angle_alpha'] = self._createProjDictFromObj(claculator_cell.angle_alpha)
            project_cell['angle_beta'] = self._createProjDictFromObj(claculator_cell.angle_beta)
            project_cell['angle_gamma'] = self._createProjDictFromObj(claculator_cell.angle_gamma)

            # Atom sites
            project_phase['atom_site'] = {}
            for i, label in enumerate(calculator_phase.atom_site.label):
                project_atom_site = project_phase['atom_site'][label] = {}
                calculator_atom_site = calculator_phase.atom_site

                # Atom sites symbol
                project_atom_site['type_symbol'] = self._createProjDictFromObj(calculator_atom_site.type_symbol[i])

                # Atom site neutron scattering length
                project_atom_site['scat_length_neutron'] = self._createProjDictFromObj(calculator_atom_site.scat_length_neutron[i])

                # Atom site coordinates
                project_atom_site['fract_x'] = self._createProjDictFromObj(calculator_atom_site.fract_x[i])
                project_atom_site['fract_y'] = self._createProjDictFromObj(calculator_atom_site.fract_y[i])
                project_atom_site['fract_z'] = self._createProjDictFromObj(calculator_atom_site.fract_z[i])

                # Atom site occupancy
                project_atom_site['occupancy'] = self._createProjDictFromObj(calculator_atom_site.occupancy[i])

                # Atom site ADP type
                project_atom_site['adp_type'] = self._createProjDictFromObj(calculator_atom_site.adp_type[i])

                # Atom site isotropic ADP
                project_atom_site['U_iso_or_equiv'] = self._createProjDictFromObj(calculator_atom_site.u_iso_or_equiv[i])

            # Atom site anisotropic ADP
            if calculator_phase.atom_site_aniso is not None:
                for i, label in enumerate(calculator_phase.atom_site_aniso.label):
                    project_atom_site = project_phase['atom_site'][label]
                    calculator_atom_site = calculator_phase.atom_site_aniso
                    project_atom_site['u_11'] = self._createProjDictFromObj(calculator_atom_site.u_11[i])
                    project_atom_site['u_22'] = self._createProjDictFromObj(calculator_atom_site.u_22[i])
                    project_atom_site['u_33'] = self._createProjDictFromObj(calculator_atom_site.u_33[i])
                    project_atom_site['u_12'] = self._createProjDictFromObj(calculator_atom_site.u_12[i])
                    project_atom_site['u_13'] = self._createProjDictFromObj(calculator_atom_site.u_13[i])
                    project_atom_site['u_23'] = self._createProjDictFromObj(calculator_atom_site.u_23[i])

            # Atom site MSP
            if calculator_phase.atom_site_susceptibility is not None:
                for i, label in enumerate(calculator_phase.atom_site_susceptibility.label):
                    project_atom_site = project_phase['atom_site'][label]
                    calculator_atom_site = calculator_phase.atom_site_susceptibility
                    project_atom_site['chi_type'] = self._createProjDictFromObj(calculator_atom_site.chi_type[i])
                    project_atom_site['chi_11'] = self._createProjDictFromObj(calculator_atom_site.chi_11[i])
                    project_atom_site['chi_22'] = self._createProjDictFromObj(calculator_atom_site.chi_22[i])
                    project_atom_site['chi_33'] = self._createProjDictFromObj(calculator_atom_site.chi_33[i])
                    project_atom_site['chi_12'] = self._createProjDictFromObj(calculator_atom_site.chi_12[i])
                    project_atom_site['chi_13'] = self._createProjDictFromObj(calculator_atom_site.chi_13[i])
                    project_atom_site['chi_23'] = self._createProjDictFromObj(calculator_atom_site.chi_23[i])

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
            project_phase['atom_site_list'] = {}
            project_phase['atom_site_list']['fract_x'] = atom_site_list[0]
            project_phase['atom_site_list']['fract_y'] = atom_site_list[1]
            project_phase['atom_site_list']['fract_z'] = atom_site_list[2]
            project_phase['atom_site_list']['scat_length_neutron'] = atom_site_list[3]

        self._addPhasesDescription()


    def setExperimentsDictFromCryspyObj(self):
        """Set experiments (Experimental data tab in GUI)"""

        self._experiments_dict.clear()

        for calculator_experiment in self._cryspy_obj.experiments:
            calculator_experiment_name = calculator_experiment.data_name
            project_experiment = self._experiments_dict[calculator_experiment_name] = {}

            # Experimental setup
            calculator_setup = calculator_experiment.setup
            project_experiment['wavelength'] = self._createProjDictFromObj(calculator_setup.wavelength)
            project_experiment['offset'] = self._createProjDictFromObj(calculator_setup.offset_ttheta)

            # Scale
            project_experiment['phase'] = {}
            project_experiment['phase']['scale'] = self._createProjDictFromObj(calculator_experiment.phase.scale[0]) # ONLY 1st scale parameter is currently taken into account!!!

            # Background
            project_background = project_experiment['background'] = {}
            calculator_background = calculator_experiment.background
            for ttheta, intensity in zip(calculator_background.ttheta, calculator_background.intensity):
                index = str(ttheta)
                project_background[index] = {}
                project_background[index]['ttheta'] = ttheta
                project_background[index]['intensity'] = self._createProjDictFromObj(intensity)

            # Instrument resolution
            project_resolution = project_experiment['resolution'] = {}
            calculator_resolution = calculator_experiment.resolution
            project_resolution['u'] = self._createProjDictFromObj(calculator_resolution.u)
            project_resolution['v'] = self._createProjDictFromObj(calculator_resolution.v)
            project_resolution['w'] = self._createProjDictFromObj(calculator_resolution.w)
            project_resolution['x'] = self._createProjDictFromObj(calculator_resolution.x)
            project_resolution['y'] = self._createProjDictFromObj(calculator_resolution.y)

            # Measured data points
            logging.info("measured data points: start")
            #logging.info(calculator_experiment.meas)
            x_obs = np.array(calculator_experiment.meas.ttheta)
            if calculator_experiment.meas.intensity[0] is not None:
                y_obs =  np.array(calculator_experiment.meas.intensity)
                sy_obs =  np.array(calculator_experiment.meas.intensity_sigma)
            elif calculator_experiment.meas.intensity_up[0] is not None:
                y_obs_up = np.array(calculator_experiment.meas.intensity_up)
                sy_obs_up = np.array(calculator_experiment.meas.intensity_up_sigma)
                y_obs_down = np.array(calculator_experiment.meas.intensity_down)
                sy_obs_down = np.array(calculator_experiment.meas.intensity_down_sigma)
                y_obs = y_obs_up + y_obs_down
                sy_obs = np.sqrt(np.square(sy_obs_up) + np.square(sy_obs_down))
            y_obs_upper = y_obs + sy_obs
            y_obs_lower = y_obs - sy_obs
            self._experiments_dict[calculator_experiment_name]['measured_pattern'] = {
                'x': x_obs.tolist(),
                #'y_obs_up': y_obs_up.tolist(),
                #'sy_obs_up': sy_obs_up.tolist(),
                #'y_obs_down': y_obs_down.tolist(),
                #'sy_obs_down': sy_obs_down.tolist(),
                'y_obs_upper': y_obs_upper.tolist(),
                'y_obs_lower': y_obs_lower.tolist(),
            }
            logging.info("measured data points: end")

        self._addExperimentsDescription()


    def setCalculationsDictFromCryspyObj(self):
        """Set calculated data (depends on phases and experiments from above)"""

        self._calculations_dict.clear()

        for calculator_experiment in self._cryspy_obj.experiments:
            calculator_experiment_name = calculator_experiment.data_name
            project_experiment = self._calculations_dict[calculator_experiment_name] = {}

            # Experiment label
            self._calculations_dict[calculator_experiment_name] = {}

            # Calculated chi squared and number of data points used for refinement
            logging.info("calc_chi_sq start") # profiling
            chi_sq = 0.0
            n_res = 1
            chi_sq, n_res = calculator_experiment.calc_chi_sq(self._cryspy_obj.crystals)
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
            calculated_pattern, bragg_peaks, _ = calculator_experiment.calc_profile(np.array(calculator_experiment.meas.ttheta), self._cryspy_obj.crystals)
            logging.info("calc_profile end") # profiling

            # Bragg peaks
            offset = self._experiments_dict[calculator_experiment_name]['offset']['value']
            self._calculations_dict[calculator_experiment_name]['bragg_peaks'] = {}
            for index, crystal in enumerate(self._cryspy_obj.crystals):
                self._calculations_dict[calculator_experiment_name]['bragg_peaks'][crystal.data_name] = {
                    'h': bragg_peaks[index].index_h,
                    'k': bragg_peaks[index].index_k,
                    'l': bragg_peaks[index].index_l,
                    'ttheta': (np.array(bragg_peaks[index].ttheta) + offset).tolist()
                }

            # Calculated diffraction pattern
            logging.info("calculated diffraction pattern: start")
            #logging.info(calculated_pattern)
            x_calc = np.array(calculated_pattern.ttheta)
            if calculator_experiment.meas.intensity[0] is not None:
                y_obs =  np.array(calculator_experiment.meas.intensity)
                sy_obs =  np.array(calculator_experiment.meas.intensity_sigma)
                ###y_calc = np.array(calculated_pattern.intensity_total)
                y_calc_up = np.array(calculated_pattern.intensity_up_total)
                ###y_calc_down = np.array(calculated_pattern.intensity_down_total)
                y_calc = y_calc_up ###+ y_calc_down
            elif calculator_experiment.meas.intensity_up[0] is not None:
                y_obs_up = np.array(calculator_experiment.meas.intensity_up)
                sy_obs_up = np.array(calculator_experiment.meas.intensity_up_sigma)
                y_obs_down = np.array(calculator_experiment.meas.intensity_down)
                sy_obs_down = np.array(calculator_experiment.meas.intensity_down_sigma)
                y_obs = y_obs_up + y_obs_down
                sy_obs = np.sqrt(np.square(sy_obs_up) + np.square(sy_obs_down))
                y_calc_up = np.array(calculated_pattern.intensity_up_total)
                y_calc_down = np.array(calculated_pattern.intensity_down_total)
                y_calc = y_calc_up + y_calc_down
            y_obs_upper = y_obs + sy_obs
            y_obs_lower = y_obs - sy_obs
            y_diff_upper = y_obs + sy_obs - y_calc
            y_diff_lower = y_obs - sy_obs - y_calc
            self._calculations_dict[calculator_experiment_name]['calculated_pattern'] = {
                'x': x_calc.tolist(),
                'y_calc': y_calc.tolist(),
                'y_diff_lower': y_diff_lower.tolist(),
                'y_diff_upper': y_diff_upper.tolist()
            }
            logging.info("calculated diffraction pattern: end")

            # Calculated data limits
            self._calculations_dict[calculator_experiment_name]['limits'] = {}
            self._calculations_dict[calculator_experiment_name]['limits']['main'] = {
                'x_min': np.amin(x_calc).item(),
                'x_max': np.amax(x_calc).item(),
                #'y_min': np.amin([np.amin(y_calc_down), np.amin(y_obs_lower)]).item(),
                #'y_max': np.amax([np.amax(y_calc_up), np.amax(y_obs_upper)]).item()
                'y_min': np.amin([np.amin(y_calc), np.amin(y_obs_lower)]).item(),
                'y_max': np.amax([np.amax(y_calc), np.amax(y_obs_upper)]).item()
                }
            self._calculations_dict[calculator_experiment_name]['limits']['difference'] = {
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


    def _setCalculatorObjFromProjectDict(self, calculator_obj, project_dict):
        """ ... """
        if not isinstance(calculator_obj, cryspy.common.cl_fitable.Fitable):
            return
        calculator_obj.value = project_dict['value']
        calculator_obj.refinement = project_dict['refine']


    def setCryspyObjFromPhases(self):
        """Set phases (sample model tab in GUI)"""

        for calculator_phase in self._cryspy_obj.crystals:
            calculator_phase_name = calculator_phase.data_name
            project_phase = self._phases_dict[calculator_phase_name]

            # Unit cell parameters
            calculator_cell = calculator_phase.cell
            project_cell = project_phase['cell']
            self._setCalculatorObjFromProjectDict(calculator_cell.length_a, project_cell['length_a'])
            self._setCalculatorObjFromProjectDict(calculator_cell.length_b, project_cell['length_b'])
            self._setCalculatorObjFromProjectDict(calculator_cell.length_c, project_cell['length_c'])
            self._setCalculatorObjFromProjectDict(calculator_cell.angle_alpha, project_cell['angle_alpha'])
            self._setCalculatorObjFromProjectDict(calculator_cell.angle_beta, project_cell['angle_beta'])
            self._setCalculatorObjFromProjectDict(calculator_cell.angle_gamma, project_cell['angle_gamma'])

            # Atom sites
            for i, label in enumerate(calculator_phase.atom_site.label):
                calculator_atom_site = calculator_phase.atom_site
                project_atom_site = project_phase['atom_site'][label]

                # Atom site coordinates
                self._setCalculatorObjFromProjectDict(calculator_atom_site.fract_x[i], project_atom_site['fract_x'])
                self._setCalculatorObjFromProjectDict(calculator_atom_site.fract_y[i], project_atom_site['fract_y'])
                self._setCalculatorObjFromProjectDict(calculator_atom_site.fract_z[i], project_atom_site['fract_z'])

                # Atom site occupancy
                self._setCalculatorObjFromProjectDict(calculator_atom_site.occupancy[i], project_atom_site['occupancy'])

                # Atom site isotropic ADP
                self._setCalculatorObjFromProjectDict(calculator_atom_site.u_iso_or_equiv[i], project_atom_site['U_iso_or_equiv'])

            # Atom site anisotropic ADP
            if calculator_phase.atom_site_aniso is not None:
                for i, label in enumerate(calculator_phase.atom_site_aniso.label):
                    calculator_atom_site = calculator_phase.atom_site_aniso
                    project_atom_site = project_phase['atom_site'][label]
                    self._setCalculatorObjFromProjectDict(calculator_atom_site.u_11[i], project_atom_site['u_11'])
                    self._setCalculatorObjFromProjectDict(calculator_atom_site.u_22[i], project_atom_site['u_22'])
                    self._setCalculatorObjFromProjectDict(calculator_atom_site.u_33[i], project_atom_site['u_33'])
                    self._setCalculatorObjFromProjectDict(calculator_atom_site.u_12[i], project_atom_site['u_12'])
                    self._setCalculatorObjFromProjectDict(calculator_atom_site.u_13[i], project_atom_site['u_13'])
                    self._setCalculatorObjFromProjectDict(calculator_atom_site.u_23[i], project_atom_site['u_23'])

            # Atom site MSP
            if calculator_phase.atom_site_susceptibility is not None:
                for i, label in enumerate(calculator_phase.atom_site_susceptibility.label):
                    calculator_atom_site = calculator_phase.atom_site_susceptibility
                    project_atom_site = project_phase['atom_site'][label]
                    self._setCalculatorObjFromProjectDict(calculator_atom_site.chi_type[i], project_atom_site['chi_type'])
                    self._setCalculatorObjFromProjectDict(calculator_atom_site.chi_11[i], project_atom_site['chi_11'])
                    self._setCalculatorObjFromProjectDict(calculator_atom_site.chi_22[i], project_atom_site['chi_22'])
                    self._setCalculatorObjFromProjectDict(calculator_atom_site.chi_33[i], project_atom_site['chi_33'])
                    self._setCalculatorObjFromProjectDict(calculator_atom_site.chi_12[i], project_atom_site['chi_12'])
                    self._setCalculatorObjFromProjectDict(calculator_atom_site.chi_13[i], project_atom_site['chi_13'])
                    self._setCalculatorObjFromProjectDict(calculator_atom_site.chi_23[i], project_atom_site['chi_23'])


    def setCryspyObjFromExperiments(self):
        """Set experiments (Experimental data tab in GUI)"""

        for calculator_experiment in self._cryspy_obj.experiments:
            calculator_experiment_name = calculator_experiment.data_name
            project_experiment = self._experiments_dict[calculator_experiment_name]

            # Experimental setup
            calculator_setup = calculator_experiment.setup
            self._setCalculatorObjFromProjectDict(calculator_setup.wavelength, project_experiment['wavelength'])
            self._setCalculatorObjFromProjectDict(calculator_setup.offset_ttheta, project_experiment['offset'])

            # Scale
            self._setCalculatorObjFromProjectDict(calculator_experiment.phase.scale[0], project_experiment['phase']['scale']) # ONLY 1st scale parameter is currently taken into account!!!

            # Background
            calculator_background = calculator_experiment.background
            project_background = project_experiment['background']
            for ttheta, intensity in zip(calculator_background.ttheta, calculator_background.intensity):
                index = str(ttheta)
                self._setCalculatorObjFromProjectDict(intensity, project_background[index]['intensity'])

            # Instrument resolution
            project_resolution = project_experiment['resolution']
            calculator_resolution = calculator_experiment.resolution
            self._setCalculatorObjFromProjectDict(calculator_resolution.u, project_resolution['u'])
            self._setCalculatorObjFromProjectDict(calculator_resolution.v, project_resolution['v'])
            self._setCalculatorObjFromProjectDict(calculator_resolution.w, project_resolution['w'])
            self._setCalculatorObjFromProjectDict(calculator_resolution.x, project_resolution['x'])
            self._setCalculatorObjFromProjectDict(calculator_resolution.y, project_resolution['y'])


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
        experiments = ""
        calculations = ""
        phases = ""
        if len(self._cryspy_obj.experiments) > 0:
            #experiments = "data_" + self._cryspy_obj.experiments[0].data_name + "\n" + self._cryspy_obj.experiments[0].params_to_cif + "\n" + self._cryspy_obj.experiments[0].data_to_cif # maybe meas_to_cif
            #calculations = self._cryspy_obj.experiments[0].calc_to_cif
            experiments = '' # temporarily disable, because not implemented yet in cryspy 0.2.0
            calculations = '' # temporarily disable, because not implemented yet in cryspy 0.2.0
        if len(self._cryspy_obj.crystals) > 0:
            phases = self._cryspy_obj.crystals[0].to_cif()
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
