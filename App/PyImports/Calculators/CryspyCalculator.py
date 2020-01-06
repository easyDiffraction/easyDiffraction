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

    def setPhasesDictFromCryspyObj(self):
        """Set phases (sample model tab in GUI)"""
        self._phases_dict.clear()

        for phase in self._cryspy_obj.crystals:

            # Phase label
            self._phases_dict[phase.data_name] = {}

            # Unit cell parameters
            self._phases_dict[phase.data_name]['cell'] = {}
            self._phases_dict[phase.data_name]['cell']['length_a'] = {
                'header': 'a (Å)',
                'tooltip': 'Unit-cell length of the selected structure in angstroms.',
                'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Icell_length_.html',
                'value': phase.cell.length_a.value,
                'error': phase.cell.length_a.sigma,
                'min': phase.cell.length_a.value * 0.8,
                'max': phase.cell.length_a.value * 1.2,
                'constraint': phase.cell.length_a.constraint,
                'hide': phase.cell.length_a.constraint_flag,
                'refine': phase.cell.length_a.refinement }
            self._phases_dict[phase.data_name]['cell']['length_b'] = {
                'header': 'b (Å)',
                'tooltip': 'Unit-cell length of the selected structure in angstroms.',
                'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Icell_length_.html',
                'value': phase.cell.length_b.value,
                'error': phase.cell.length_b.sigma,
                'min': phase.cell.length_b.value * 0.8,
                'max': phase.cell.length_b.value * 1.2,
                'constraint': phase.cell.length_b.constraint,
                'hide': phase.cell.length_b.constraint_flag,
                'refine': phase.cell.length_b.refinement }
            self._phases_dict[phase.data_name]['cell']['length_c'] = {
                'header': 'c (Å)',
                'tooltip': 'Unit-cell length of the selected structure in angstroms.',
                'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Icell_length_.html',
                'value': phase.cell.length_c.value,
                'error': phase.cell.length_c.sigma,
                'min': phase.cell.length_c.value * 0.8,
                'max': phase.cell.length_c.value * 1.2,
                'constraint': phase.cell.length_c.constraint,
                'hide': phase.cell.length_c.constraint_flag,
                'refine': phase.cell.length_c.refinement }
            self._phases_dict[phase.data_name]['cell']['angle_alpha'] = {
                'header': 'alpha (°)',
                'tooltip': 'Unit-cell angle of the selected structure in degrees.',
                'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Icell_angle_.html',
                'value': phase.cell.angle_alpha.value,
                'error': phase.cell.angle_alpha.sigma,
                'min': phase.cell.angle_alpha.value * 0.8,
                'max': phase.cell.angle_alpha.value * 1.2,
                'constraint': phase.cell.angle_alpha.constraint,
                'hide': phase.cell.angle_alpha.constraint_flag,
                'refine': phase.cell.angle_alpha.refinement }
            self._phases_dict[phase.data_name]['cell']['angle_beta'] = {
                'header': 'beta (°)',
                'tooltip': 'Unit-cell angle of the selected structure in degrees.',
                'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Icell_angle_.html',
                'value': phase.cell.angle_beta.value,
                'error': phase.cell.angle_beta.sigma,
                'min': phase.cell.angle_beta.value * 0.8,
                'max': phase.cell.angle_beta.value * 1.2,
                'constraint': phase.cell.angle_beta.constraint,
                'hide': phase.cell.angle_beta.constraint_flag,
                'refine': phase.cell.angle_beta.refinement }
            self._phases_dict[phase.data_name]['cell']['angle_gamma'] = {
                'header': 'gamma (°)',
                'tooltip': 'Unit-cell angle of the selected structure in degrees.',
                'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Icell_angle_.html',
                'value': phase.cell.angle_gamma.value,
                'error': phase.cell.angle_gamma.sigma,
                'min': phase.cell.angle_gamma.value * 0.8,
                'max': phase.cell.angle_gamma.value * 1.2,
                'constraint': phase.cell.angle_gamma.constraint,
                'hide': phase.cell.angle_gamma.constraint_flag,
                'refine': phase.cell.angle_gamma.refinement }

            # Space group
            self._phases_dict[phase.data_name]['space_group'] = {}
            self._phases_dict[phase.data_name]['space_group']['crystal_system'] = {
                'header': 'Crystal system',
                'tooltip': 'The name of the system of geometric crystal classes of space groups (crystal system) to which the space group belongs.',
                'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Ispace_group_crystal_system.html',
                'value': phase.space_group.crystal_system }
            self._phases_dict[phase.data_name]['space_group']['space_group_name_H-M_alt'] = {
                'header': 'Symbol',
                'tooltip': 'The Hermann-Mauguin symbol of space group.',
                'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Ispace_group_name_H-M_alt.html',
                'value': phase.space_group.name_hm_alt }
            self._phases_dict[phase.data_name]['space_group']['space_group_IT_number'] = {
                'header': 'Number',
                'tooltip': 'The number as assigned in International Tables for Crystallography Vol. A.',
                'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Ispace_group_crystal_system.html',
                'value': phase.space_group.it_number }
            self._phases_dict[phase.data_name]['space_group']['origin_choice'] = {
                'header': 'Setting',
                'tooltip': '',
                'url': '',
                'value': phase.space_group.it_coordinate_system_code }

            # Atom sites label
            self._phases_dict[phase.data_name]['atom_site'] = {}
            for label in phase.atom_site.label:
                self._phases_dict[phase.data_name]['atom_site'][label] = {}
                #phases_dict[phase.data_name]['atom_site'][label]['label'] = {
                #'header': 'Label',
                #'tooltip': 'A unique identifier for a particular site in the crystal.',
                #'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_label.html',
                #}

            # Atom site type symbol
            for label, type_symbol in zip(phase.atom_site.label, phase.atom_site.type_symbol):
                self._phases_dict[phase.data_name]['atom_site'][label]['type_symbol'] = {
                    'header': 'Atom',
                    'tooltip': 'A code to identify the atom species occupying this site.',
                    'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_type_symbol.html',
                    'value': type_symbol }

            # Atom site coordinates
            for label, x, y, z in zip(phase.atom_site.label, phase.atom_site.fract_x, phase.atom_site.fract_y, phase.atom_site.fract_z):
                self._phases_dict[phase.data_name]['atom_site'][label]['fract_x'] = {
                    'header': 'x',
                    'tooltip': 'Atom-site coordinate as fractions of the unit cell length.',
                    'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html',
                    'value': x.value,
                    'error': x.sigma,
                    'min': x.value * 0.8,
                    'max': x.value * 1.2,
                    'constraint': x.constraint,
                    'hide': x.constraint_flag,
                    'refine': x.refinement }
                self._phases_dict[phase.data_name]['atom_site'][label]['fract_y'] = {
                    'header': 'y',
                    'tooltip': 'Atom-site coordinate as fractions of the unit cell length.',
                    'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html',
                    'value': y.value,
                    'error': y.sigma,
                    'min': y.value * 0.8,
                    'max': y.value * 1.2,
                    'constraint': y.constraint,
                    'hide': y.constraint_flag,
                    'refine': y.refinement }
                self._phases_dict[phase.data_name]['atom_site'][label]['fract_z'] = {
                    'header': 'z',
                    'tooltip': 'Atom-site coordinate as fractions of the unit cell length.',
                    'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html',
                    'value': z.value,
                    'error': z.sigma,
                    'min': z.value * 0.8,
                    'max': z.value * 1.2,
                    'constraint': z.constraint,
                    'hide': z.constraint_flag,
                    'refine': z.refinement }

            # Atom site neutron scattering length
            for label, scat_length_neutron in zip(phase.atom_site.label, phase.atom_site.scat_length_neutron):
                self._phases_dict[phase.data_name]['atom_site'][label]['scat_length_neutron'] = {
                    'header': '',
                    'tooltip': '',
                    'url': '',
                    'value': scat_length_neutron }

            # Atom sites for structure view (all the positions inside unit cell of 1x1x1)
            atom_site_list = [[], [], [], []]
            for x, y, z, scat_length_neutron in zip(phase.atom_site.fract_x, phase.atom_site.fract_y, phase.atom_site.fract_z, phase.atom_site.scat_length_neutron):
                x_array, y_array, z_array, _ = phase.space_group.calc_xyz_mult(x.value, y.value, z.value)
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
            self._phases_dict[phase.data_name]['atom_site_list'] = {}
            self._phases_dict[phase.data_name]['atom_site_list']['fract_x'] = atom_site_list[0]
            self._phases_dict[phase.data_name]['atom_site_list']['fract_y'] = atom_site_list[1]
            self._phases_dict[phase.data_name]['atom_site_list']['fract_z'] = atom_site_list[2]
            self._phases_dict[phase.data_name]['atom_site_list']['scat_length_neutron'] = atom_site_list[3]

            # Atom site occupancy
            for label, occupancy in zip(phase.atom_site.label, phase.atom_site.occupancy):
                self._phases_dict[phase.data_name]['atom_site'][label]['occupancy'] = {
                    'header': 'Occupancy',
                    'tooltip': 'The fraction of the atom type present at this site.',
                    'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_occupancy.html',
                    'value': occupancy.value,
                    'error': occupancy.sigma,
                    'min': occupancy.value * 0.8,
                    'max': occupancy.value * 1.2,
                    'constraint': occupancy.constraint,
                    'hide': occupancy.constraint_flag,
                    'refine': occupancy.refinement }

            # Atom site ADP type
            for label, adp_type in zip(phase.atom_site.label, phase.atom_site.adp_type):
                self._phases_dict[phase.data_name]['atom_site'][label]['adp_type'] = {
                    'header': 'Type',
                    'tooltip': 'A standard code used to describe the type of atomic displacement parameters used for the site.',
                    'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_adp_type.html',
                    'value': adp_type }

            # Isotropic ADP
            for label, b_iso in zip(phase.atom_site.label, phase.atom_site.b_iso_or_equiv):
                self._phases_dict[phase.data_name]['atom_site'][label]['B_iso_or_equiv'] = {
                    'header': 'Biso',
                    'tooltip': 'Isotropic atomic displacement parameter, or equivalent isotropic atomic displacement parameter, B(equiv), in angstroms squared.',
                    'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_B_iso_or_equiv.html',
                    'value': b_iso.value,
                    'error': b_iso.sigma,
                    'min': b_iso.value * 0.8,
                    'max': b_iso.value * 1.2,
                    'constraint': b_iso.constraint,
                    'hide': b_iso.constraint_flag,
                    'refine': b_iso.refinement }

            # Anisotropic ADP
            if phase.atom_site_aniso is not None:
                for label, u_11, u_22, u_33, u_12, u_13, u_23 in zip(phase.atom_site_aniso.label,
                    phase.atom_site_aniso.u_11, phase.atom_site_aniso.u_22, phase.atom_site_aniso.u_33,
                    phase.atom_site_aniso.u_12, phase.atom_site_aniso.u_13, phase.atom_site_aniso.u_23):
                    self._phases_dict[phase.data_name]['atom_site'][label]['u_11'] = {
                        'header': 'U11',
                        'tooltip': 'Anisotropic atomic displacement component in angstroms squared.',
                        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_aniso_U_.html',
                        'value': u_11.value,
                        'error': u_11.sigma,
                        'min': u_11.value * 0.8,
                        'max': u_11.value * 1.2,
                        'constraint': u_11.constraint,
                        'hide': u_11.constraint_flag,
                        'refine': u_11.refinement }
                    self._phases_dict[phase.data_name]['atom_site'][label]['u_22'] = {
                        'header': 'U22',
                        'tooltip': 'Anisotropic atomic displacement component in angstroms squared.',
                        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_aniso_U_.html',
                        'value': u_22.value,
                        'error': u_22.sigma,
                        'min': u_22.value * 0.8,
                        'max': u_22.value * 1.2,
                        'constraint': u_22.constraint,
                        'hide': u_22.constraint_flag,
                        'refine': u_22.refinement }
                    self._phases_dict[phase.data_name]['atom_site'][label]['u_33'] = {
                        'header': 'U33',
                        'tooltip': 'Anisotropic atomic displacement component in angstroms squared.',
                        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_aniso_U_.html',
                        'value': u_33.value,
                        'error': u_33.sigma,
                        'min': u_33.value * 0.8,
                        'max': u_33.value * 1.2,
                        'constraint': u_33.constraint,
                        'hide': u_33.constraint_flag,
                        'refine': u_33.refinement }
                    self._phases_dict[phase.data_name]['atom_site'][label]['u_12'] = {
                        'header': 'U12',
                        'tooltip': 'Anisotropic atomic displacement component in angstroms squared.',
                        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_aniso_U_.html',
                        'value': u_12.value,
                        'error': u_12.sigma,
                        'min': u_12.value * 0.8,
                        'max': u_12.value * 1.2,
                        'constraint': u_12.constraint,
                        'hide': u_12.constraint_flag,
                        'refine': u_12.refinement }
                    self._phases_dict[phase.data_name]['atom_site'][label]['u_13'] = {
                        'header': 'U13',
                        'tooltip': 'Anisotropic atomic displacement component in angstroms squared.',
                        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_aniso_U_.html',
                        'value': u_13.value,
                        'error': u_13.sigma,
                        'min': u_13.value * 0.8,
                        'max': u_13.value * 1.2,
                        'constraint': u_13.constraint,
                        'hide': u_13.constraint_flag,
                        'refine': u_13.refinement }
                    self._phases_dict[phase.data_name]['atom_site'][label]['u_23'] = {
                        'header': 'U23',
                        'tooltip': 'Anisotropic atomic displacement component in angstroms squared.',
                        'url': 'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_aniso_U_.html',
                        'value': u_23.value,
                        'error': u_23.sigma,
                        'min': u_23.value * 0.8,
                        'max': u_23.value * 1.2,
                        'constraint': u_23.constraint,
                        'hide': u_23.constraint_flag,
                        'refine': u_23.refinement }

            # Anisotropic MSP
            if phase.atom_site_susceptibility is not None:
                for label, chi_type, chi_11, chi_22, chi_33, chi_12, chi_13, chi_23 in zip(phase.atom_site_susceptibility.label, phase.atom_site_susceptibility.chi_type,
                    phase.atom_site_susceptibility.chi_11, phase.atom_site_susceptibility.chi_22, phase.atom_site_susceptibility.chi_33,
                    phase.atom_site_susceptibility.chi_12, phase.atom_site_susceptibility.chi_13, phase.atom_site_susceptibility.chi_23):
                    self._phases_dict[phase.data_name]['atom_site'][label]['chi_type'] = {
                       'header': 'Type',
                       'tooltip': '',
                       'url': '',
                       'value': chi_type }
                    self._phases_dict[phase.data_name]['atom_site'][label]['chi_11'] = {
                        'header': 'Chi11',
                        'tooltip': '',
                        'url': '',
                        'value': chi_11.value,
                        'error': chi_11.sigma,
                        'min': chi_11.value * 0.8,
                        'max': chi_11.value * 1.2,
                        'constraint': chi_11.constraint,
                        'hide': chi_11.constraint_flag,
                        'refine': chi_11.refinement }
                    self._phases_dict[phase.data_name]['atom_site'][label]['chi_22'] = {
                        'header': 'Chi22',
                        'tooltip': '',
                        'url': '',
                        'value': chi_22.value,
                        'error': chi_22.sigma,
                        'min': chi_22.value * 0.8,
                        'max': chi_22.value * 1.2,
                        'constraint': chi_22.constraint,
                        'hide': chi_22.constraint_flag,
                        'refine': chi_22.refinement }
                    self._phases_dict[phase.data_name]['atom_site'][label]['chi_33'] = {
                        'header': 'Chi33',
                        'tooltip': '',
                        'url': '',
                        'value': chi_33.value,
                        'error': chi_33.sigma,
                        'min': chi_33.value * 0.8,
                        'max': chi_33.value * 1.2,
                        'constraint': chi_33.constraint,
                        'hide': chi_33.constraint_flag,
                        'refine': chi_33.refinement }
                    self._phases_dict[phase.data_name]['atom_site'][label]['chi_12'] = {
                        'header': 'Chi12',
                        'tooltip': '',
                        'url': '',
                        'value': chi_12.value,
                        'error': chi_12.sigma,
                        'min': chi_12.value * 0.8,
                        'max': chi_12.value * 1.2,
                        'constraint': chi_12.constraint,
                        'hide': chi_12.constraint_flag,
                        'refine': chi_12.refinement }
                    self._phases_dict[phase.data_name]['atom_site'][label]['chi_13'] = {
                        'header': 'Chi13',
                        'tooltip': '',
                        'url': '',
                        'value': chi_13.value,
                        'error': chi_13.sigma,
                        'min': chi_13.value * 0.8,
                        'max': chi_13.value * 1.2,
                        'constraint': chi_13.constraint,
                        'hide': chi_13.constraint_flag,
                        'refine': chi_13.refinement }
                    self._phases_dict[phase.data_name]['atom_site'][label]['chi_23'] = {
                        'header': 'Chi23',
                        'tooltip': '',
                        'url': '',
                        'value': chi_23.value,
                        'error': chi_23.sigma,
                        'min': chi_23.value * 0.8,
                        'max': chi_23.value * 1.2,
                        'constraint': chi_23.constraint,
                        'hide': chi_23.constraint_flag,
                        'refine': chi_23.refinement }

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
                'value': experiment.setup.wavelength }
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
                occupancy.refine = self._phases_dict[phase.data_name]['atom_site'][label]['occupancy']['refine']

            # Isotropic ADP
            for label, b_iso in zip(phase.atom_site.label, phase.atom_site.b_iso):
                b_iso.value = self._phases_dict[phase.data_name]['atom_site'][label]['B_iso_or_equiv']['value']
                b_iso.refine = self._phases_dict[phase.data_name]['atom_site'][label]['B_iso_or_equiv']['refine']

            #
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
                        u_11.refine = self._phases_dict[phase.data_name]['atom_site'][label]['u_11']['refine']
                        u_22.refine = self._phases_dict[phase.data_name]['atom_site'][label]['u_22']['refine']
                        u_33.refine = self._phases_dict[phase.data_name]['atom_site'][label]['u_33']['refine']
                        u_12.refine = self._phases_dict[phase.data_name]['atom_site'][label]['u_12']['refine']
                        u_13.refine = self._phases_dict[phase.data_name]['atom_site'][label]['u_13']['refine']
                        u_23.refine = self._phases_dict[phase.data_name]['atom_site'][label]['u_23']['refine']

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
            experiment.offset.value = self._experiments_dict[experiment.data_name]['offset']['value']
            experiment.offset.refinement = self._experiments_dict[experiment.data_name]['offset']['refine']

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
