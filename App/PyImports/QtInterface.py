__author__ = 'simonward'
__version__ = "2020_02_01"

from typing import NoReturn

from PySide2.QtCore import QObject, Signal, Slot

from easyInterface import logger
from easyInterface.Diffraction.Interface import *


class QtCalculatorInterface(CalculatorInterface, QObject):
    def __init__(self, calculator, parent=None):
        QObject.__init__(self, parent)
        CalculatorInterface.__init__(self, calculator)
        self._log = logger.getLogger(__class__.__module__)

    projectDictChanged = Signal()
    canUndoOrRedoChanged = Signal()

    @Slot(result=str)
    def undoText(self):
        return self.project_dict.undoText()

    @Slot(result=str)
    def redoText(self):
        return self.project_dict.redoText()

    @Slot(result=bool)
    def canUndo(self):
        return CalculatorInterface.canUndo(self)

    @Slot(result=bool)
    def canRedo(self):
        return CalculatorInterface.canRedo(self)

    @Slot()
    def clearUndoStack(self):
        CalculatorInterface.clearUndoStack(self)

    @Slot()
    def undo(self):
        CalculatorInterface.undo(self)
        # self.setCalculatorFromProject()
        self.projectDictChanged.emit()

    @Slot()
    def redo(self):
        CalculatorInterface.redo(self)
        # self.setCalculatorFromProject()
        self.projectDictChanged.emit()

    def __repr__(self) -> str:
        return "easyDiffraction QT interface with calculator: {} - {}".format(
            self.project_dict['calculator']['name'],
            self.project_dict['calculator']['version'])

    def setProjectFromCalculator(self):
        #TODO initiate buld update here
        CalculatorInterface.setProjectFromCalculator(self)
        self.projectDictChanged.emit()

    def setPhaseDefinition(self, phases_path: str):
        """
        Parse the relevant phases file and update the corresponding model
        """
        CalculatorInterface.setPhaseDefinition(self, phases_path)
        self.projectDictChanged.emit()

    def addPhaseDefinition(self, phases_path: str):
        """
        Parse the relevant phases file and update the corresponding model
        """
        CalculatorInterface.addPhaseDefinition(self, phases_path)
        self.projectDictChanged.emit()

    def removePhase(self, phase_name):
        CalculatorInterface.removePhase(self, phase_name)
        self.projectDictChanged.emit()

    def setExperimentDefinition(self, experiment_path: str):
        """
        Parse the relevant phases file and update the corresponding model
        """
        CalculatorInterface.setExperimentDefinition(self, experiment_path)
        # self.updateCalculations()
        self.projectDictChanged.emit()

    def setExperimentDefinitionFromString(self, exp_cif_string: str) -> NoReturn:
        """
        Parse the relevant phases file and update the corresponding model
        """
        CalculatorInterface.setExperimentDefinitionFromString(self, exp_cif_string)
        self.updateCalculations()
        self.projectDictChanged.emit()

    def addExperimentDefinition(self, experiment_path: str):
        """
        Parse the relevant phases file and update the corresponding model
        """
        CalculatorInterface.addExperimentDefinition(self, experiment_path)
        self.updateCalculations()
        self.projectDictChanged.emit()

    def removeExperiment(self, experiment_name):
        CalculatorInterface.removeExperiment(self, experiment_name)
        self.projectDictChanged.emit()

    def setDictByPath(self, keys: list, value):
        CalculatorInterface.setDictByPath(self, keys, value)
        self.projectDictChanged.emit()

    def refine(self) -> dict:
        """refinement ..."""
        refinement_res = CalculatorInterface.refine(self)
        self.projectDictChanged.emit()
        return refinement_res
