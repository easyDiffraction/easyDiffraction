import logging
import os
from datetime import datetime
from typing import List

from PySide2.QtCore import QObject, Signal, Slot

from .ObjectClasses.DataObj.Calculation import *
from .ObjectClasses.DataObj.Experiment import *
from .ObjectClasses.PhaseObj.Phase import *
from .ObjectClasses.Utils.DictTools import UndoableDict
from .ObjectClasses.Utils.InfoObjs import App, Calculator, Info


class ProjectDict(UndoableDict):
    """
    This class deals with the creation and modification of the main project dictionary
    """

    def __init__(self, app: App, calculator: Calculator, info: Info, phases: Phases, experiments: Experiments,
                 calculations: Calculations):
        """
        Create the main project dictionary from base classes
        :param app: Details of the EasyDiffraction app
        :param calculator: Details of the Calculator to be used
        :param info: Store of ID's and some fit information
        :param phases: Crystolographic phases in the system
        :param experiments: Experimental data store in the system
        """
        super().__init__(app=app, calculator=calculator, info=info, phases=phases, experiments=experiments,
                         calculations=calculations)

    @classmethod
    def default(cls) -> 'ProjectDict':
        """
        Create a default and empty project dictionary
        :return: Default project dictionary with undo/redo
        """
        app = App.default()
        info = Info.default()
        calculator = Calculator.default()
        phases = Phases({})
        experiments = Experiments({})
        calculations = Calculations({})
        return cls(app, calculator, info, phases, experiments, calculations)

    @classmethod
    def fromPars(cls, experiments: Union[Experiments, Experiment, List[Experiment]],
                 phases: Union[Phases, Phase, List[Phase]],
                 calculations: Union[Calculations, Calculation, List[Calculation]]) -> 'ProjectDict':
        """
        Create a main project dictionary from phases and experiments
        :param experiments: A collection of experiments to be compared to calculations
        :param phases: A Collection of crystolographic phases to be calculated
        :return: project dictionary with undo/redo
        """
        app = App.default()
        info = Info.default()
        calculator = Calculator.default()
        if not isinstance(experiments, Experiments):
            experiments = Experiments(experiments)
        if not isinstance(phases, Phases):
            phases = Phases(phases)
        if not isinstance(calculations, Calculations):
            calculations = Calculations(calculations)
        return cls(app, calculator, info, phases, experiments, calculations)

    @Slot(str)
    def atom_site_list(self, in_phase=None):

        def make_list(phase):
            # Atom sites for structure view (all the positions inside unit cell of 1x1x1)
            atom_site_list = [[], [], [], []]
            for x, y, z, scat_length_neutron in zip(self.getItemByPath(['atoms', phase, 'fract_x']).value,
                                                    self.getItemByPath(['atoms', phase, 'fract_y']).value,
                                                    self.getItemByPath(['atoms', phase, 'fract_z']).value,
                                                    self.getItemByPath(['atoms', phase, 'scat_length_neutron']).value):
                x_array, y_array, z_array, _ = self['spacegroup'].calc_xyz_mult(x.value, y.value, z.value)
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
            return dict(fract_x=atom_site_list[0], fract_y=atom_site_list[1], fract_z=atom_site_list[2],
                        scat_length_neutron=atom_site_list[3])

        if in_phase is None:
            atom_store = dict()
            for phase in self['phases'].keys():
                atom_store[phase] = dict() # make_list(phase)
        else:
            atom_store = dict() #make_list(in_phase)
        return atom_store



class CalculatorInterface(QObject):
    def __init__(self, calculator, parent=None):
        super().__init__(parent)
        logging.info("---")
        self.project_dict = ProjectDict.default()
        self.calculator = calculator
        logging.info("self.calculator:")
        logging.info(type(self.calculator))
        logging.info(self.calculator)
        self.setProjectFromCalculator()

        # Set the calculator info
        # TODO this should be a non-logged update
        CALCULATOR_INFO = self.calculator.calculatorInfo()
        for key in CALCULATOR_INFO.keys():
            self.project_dict.setItemByPath(['calculator', key], CALCULATOR_INFO[key])

    projectDictChanged = Signal()

    def __repr__(self) -> str:
        return "EasyDiffraction interface with calculator: {} - {}".format(
            self.project_dict['calculator']['name'],
            self.project_dict['calculator']['version'])

    def setProjectFromCalculator(self):
        #TODO initiate buld update here
        self.updatePhases(emit=False)
        self.updateExperiments(emit=False)
        self.updateCalculations(emit=False)
        self.project_dict.setItemByPath(['info', 'modified_datetime'],
                                        datetime.fromtimestamp(
                                            os.path.getmtime(self.calculator._main_rcif_path)).strftime(
                                            '%d %b %Y, %H:%M:%S'))
        self.project_dict.setItemByPath(['info', 'refinement_datetime'], str(np.datetime64('now')))

        final_chi_square, n_res = self.calculator.getChiSq()
        final_chi_square = final_chi_square/n_res

        self.project_dict.setItemByPath(['info', 'n_res', 'store', 'value'], n_res)
        self.project_dict.setItemByPath(['info', 'chi_squared', 'store', 'value'], final_chi_square)

        self.projectDictChanged.emit()

    #
    def updateExpsDefinition(self, exp_path: str):
        """
        Parse the relevant phases file and update the corresponding model
        """
        self.calculator.updateExpsDefinition(exp_path)
        # This will re-create all local directories
        self.updateExperiments()

    def updatePhaseDefinition(self, phases_path: str):
        """
        Parse the relevant phases file and update the corresponding model
        """
        self.calculator.updatePhaseDefinition(phases_path)
        self.updatePhases()

        # This will notify the GUI models changed
        self.projectDictChanged.emit()

    def writeMainCif(self, save_dir: str):
        self.calculator.writeMainCif(save_dir)

    def writePhaseCif(self, save_dir: str):
        self.calculator.writePhaseCif(save_dir)

    def writeExpCif(self, save_dir: str):
        self.calculator.writeExpCif(save_dir)

    def saveCifs(self, save_dir: str):
        self.writeMainCif(save_dir)
        self.writePhaseCif(save_dir)
        self.writeExpCif(save_dir)

    def updatePhases(self, emit: bool = True):
        phases = self.calculator.getPhases()

        #for key, val in phases.items():
        #    logging.info(key)
        #    logging.info(dict(val))

        k, v = self.project_dict['phases'].dictComparison(phases, ignore=set(['calc_xyz_mult']))

        if not k:
            return

        #logging.info(k)

        #k = [key.insert(0, 'phases') for key in k]
        k = [['phases', *key] for key in k]
        #logging.info(k)

        k.append(['info', 'phase_ids'])
        v.append(list(phases.keys()))

        self.project_dict.bulkUpdate(k, v, 'Bulk update of phases')

        #logging.info(k)
        #logging.info(v)

        # This will notify the GUI models changed
        if emit:
            self.projectDictChanged.emit()

    def updateExperiments(self, emit: bool = True):
        experiments = self.calculator.getExperiments()

        k, v = self.project_dict['experiments'].dictComparison(experiments)

        if not k:
            return
        k = [['experiments', *key] for key in k]

        k.append(['info', 'experiment_ids'])
        v.append(list(experiments.keys()))

        self.project_dict.bulkUpdate(k, v, 'Bulk update of experiments')

        # This will notify the GUI models changed
        if emit:
            self.projectDictChanged.emit()

    def updateCalculations(self, emit: bool = True):
        calculations = self.calculator.getCalculations()

        k, v = self.project_dict['calculations'].dictComparison(calculations)

        if not k:
            return

        k = [['calculations', *key] for key in k]
        self.project_dict.bulkUpdate(k, v, 'Bulk update of calculations')

        # This will notify the GUI models changed
        if emit:
            self.projectDictChanged.emit()

    def setPhases(self, phases=None):
        """Set phases (sample model tab in GUI)"""
        if isinstance(phases, Phase):
            new_phase_name = phases['name']
            self.project_dict.setItemByPath(['phases', new_phase_name], phases)
        elif isinstance(phases, Phases):
            self.project_dict.bulkUpdate([['phases', item] for item in list(phases.keys())],
                                         [phases[key] for key in phases.keys()],
                                         "Setting new phases")
        self.calculator.setPhases(self.project_dict['phases'])

    def setExperiments(self, experiments=None):
        """Set experiments (Experimental data tab in GUI)"""
        if isinstance(experiments, Experiment):
            new_exp_name = experiments['name']
            self.project_dict.setItemByPath(['experiments', new_exp_name], experiments)
        elif isinstance(experiments, Experiments):
            self.project_dict.bulkUpdate([['experiments', item] for item in list(experiments.keys())],
                                         [experiments[key] for key in experiments.keys()],
                                         "Setting new experiments")
        self.calculator.setExperiments(self.project_dict['experiments'])

    def setCalculatorFromProject(self):
        self.calculator.setObjFromProjectDicts(self.project_dict['phases'], self.project_dict['experiments'])

    def getDictByPath(self, keys: list):
        return self.project_dict.getItemByPath(keys)

    def setDictByPath(self, keys: list, value):
        self.project_dict.setItemByPath(keys, value)
        self.setCalculatorFromProject()
        self.projectDictChanged.emit()

    def phasesCount(self) -> int:
        """Returns number of phases in the project."""
        return len(self.project_dict['phases'])

    def experimentsCount(self) -> int:
        """Returns number of experiments in the project."""
        return len(self.project_dict['experiments'])

    def phasesIds(self) -> list:
        """Returns labels of the phases in the project."""
        return list(self.project_dict['phases'].keys())

    def experimentsIds(self) -> list:
        """Returns labels of the experiments in the project."""
        return list(self.project_dict['experiments'].keys())

    def asDict(self) -> dict:
        """Return data dict."""
        return self.project_dict.asDict()

    def name(self) -> str:
        return self.project_dict["info"]["name"]

    def asCifDict(self) -> dict:
        """..."""
        return self.calculator.asCifDict()

    def refine(self):
        """refinement ..."""
        refinement_res, scipy_refinement_res = self.calculator.refine()

        self.setProjectFromCalculator()
        self.projectDictChanged.emit()
        try:
            return {
                "num_refined_parameters": len(scipy_refinement_res.x),
                "refinement_message": scipy_refinement_res.message,
                "nfev": scipy_refinement_res.nfev,
                "nit": scipy_refinement_res.nit,
                "njev": scipy_refinement_res.njev,
                "final_chi_sq": float(self.final_chi_square)
            }
        except:
            if scipy_refinement_res is None:
                return {
                    "refinement_message": "No parameters selected for refinement"
                }
            else:
                return {
                    "refinement_message": "Unknown problems during refinement"
                }

    @property
    def final_chi_square(self) -> float:
        return self.calculator.final_chi_square

