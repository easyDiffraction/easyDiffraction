import os

import logging

from typing import Union, List
from datetime import datetime

import numpy as np

from .ObjectClasses.Utils.DictTools import UndoableDict
#from .ObjectClasses.DataObj import *
#from .ObjectClasses.PhaseObj import *
from .ObjectClasses.PhaseObj.Atom import *
from .ObjectClasses.PhaseObj.Cell import *
from .ObjectClasses.PhaseObj.Phase import *
from .ObjectClasses.PhaseObj.SpaceGroup import *
from .ObjectClasses.DataObj.Calculation import *
from .ObjectClasses.DataObj.Experiment import *

from .ObjectClasses.Utils.InfoObjs import App, Calculator, Info
from .Calculators.CryspyCalculator import CryspyCalculator

from PySide2.QtCore import QObject, Signal


class ProjectDict(UndoableDict):
    """
    This class deals with the creation and modification of the main project dictionary
    """
    def __init__(self, app: App, calculator: Calculator, info: Info, phases: Phases, experiments: Experiments, calculations: Calculations):
        """
        Create the main project dictionary from base classes
        :param app: Details of the EasyDiffraction app
        :param calculator: Details of the Calculator to be used
        :param info: Store of ID's and some fit information
        :param phases: Crystolographic phases in the system
        :param experiments: Experimental data store in the system
        """
        super().__init__(app=app, calculator=calculator, info=info, phases=phases, experiments=experiments, calculations=calculations)

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


class CalculatorInterface(QObject):
    def __init__(self, calculator: Union[CryspyCalculator], parent=None):
        super().__init__(parent)
        logging.info("---")
        self.project_dict = ProjectDict.default()
        self.calculator = calculator
        logging.info("self.calculator:")
        logging.info(type(self.calculator))
        logging.info(self.calculator)
        self.setProjectFromCalculator()

    projectDictChanged = Signal()

    def setProjectFromCalculator(self):
        #TODO initiate buld update here
        self.updatePhases(emit=False)
        self.updateExperiments(emit=False)
        self.updateCalculations(emit=False)
        self.project_dict.setItemByPath(['info', 'modified_datetime'],
                                        datetime.fromtimestamp(os.path.getmtime(self.calculator._main_rcif_path)).strftime('%d %b %Y, %H:%M:%S'))
        self.project_dict.setItemByPath(['info', 'refinement_datetime'], str(np.datetime64('now')))

        _, n_res = self.calculator.getChiSq()
        final_chi_square = self.final_chi_square

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

    def writeMainCif(self, saveDir: str):
        self.calculator.writeMainCif(saveDir)

    def writePhaseCif(self, saveDir: str):
        self.calculator.writePhaseCif(saveDir)

    def writeExpCif(self, saveDir: str):
        self.calculator.writeExpCif(saveDir)

    def saveCifs(self, saveDir: str):
        self.writeMainCif(saveDir)
        self.writePhaseCif(saveDir)
        self.writeExpCif(saveDir)

    def updatePhases(self, emit: bool = True):
        phases = self.calculator.getPhases()

        #for key, val in phases.items():
        #    logging.info(key)
        #    logging.info(dict(val))

        k, v = self.project_dict['phases'].dictComparison(phases)
        #logging.info(k)

        #k = [key.insert(0, 'phases') for key in k]
        for key in k:
            key.insert(0, 'phases')
        #logging.info(k)

        self.project_dict.bulkUpdate(k, v, 'Bulk update of phases')
        self.projectDictChanged.emit()

        #logging.info(k)
        #logging.info(v)

        # This will notify the GUI models changed
        if emit:
            self.projectDictChanged.emit()

    def updateExperiments(self, emit: bool = True):
        experiments = self.calculator.getExperiments()

        k, v = self.project_dict['experiments'].dictComparison(experiments)
        k = [key.insert(0, 'experiments') for key in k]
        self.project_dict.bulkUpdate(k, v, 'Bulk update of experiments')

        # This will notify the GUI models changed
        if emit:
            self.projectDictChanged.emit()

    def updateCalculations(self, emit: bool = True):
        calculations = self.calculator.getCalculations()

        k, v = self.project_dict['calculations'].dictComparison(calculations)
        k = [key.insert(0, 'calculations') for key in k]
        self.project_dict.bulkUpdate(k, v, 'Bulk update of calculations')

        # This will notify the GUI models changed
        if emit:
            self.projectDictChanged.emit()

    def setPhases(self):
        """Set phases (sample model tab in GUI)"""
        self.calculator.setPhases(self.project_dict['phases'])

    def setExperiments(self):
        """Set experiments (Experimental data tab in GUI)"""
        self.calculator.setExperiments(self.project_dict['experiments'])

    def setCalculatorFromProject(self):
        self.calculator.setObjFromProjectDict(self.project_dict['phases'], self.project_dict['experiments'])

    def getByPath(self, keys: list):
        return self.project_dict.getItemByPath(keys)

    def setByPath(self, keys: list, value):
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

