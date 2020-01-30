import os
import logging

from PySide2.QtCore import QObject, Signal, Slot, Property
from PySide2.QtGui import QPdfWriter, QTextDocument
from PyImports.DisplayModels.MeasuredDataModel import MeasuredDataModel
from PyImports.DisplayModels.CalculatedDataModel import CalculatedDataModel
from PyImports.DisplayModels.BraggPeaksModel import BraggPeaksModel
from PyImports.DisplayModels.CellParametersModel import CellParametersModel
from PyImports.DisplayModels.CellBoxModel import CellBoxModel
from PyImports.DisplayModels.AtomSitesModel import AtomSitesModel
from PyImports.DisplayModels.AtomAdpsModel import AtomAdpsModel
from PyImports.DisplayModels.AtomMspsModel import AtomMspsModel
from PyImports.DisplayModels.FitablesModel import FitablesModel

from PyImports.DisplayModels.StatusModel import StatusModel
from PyImports.DisplayModels.FileStructureModel import FileStructureModel
from PyImports.ProjectSentinel import ProjectControl, writeProject, check_project_dict, writeEmptyProject
from PyImports.Refinement import Refiner
import easyInterface.Utils.Helpers as Helpers

from easyInterface.Calculators.CryspyCalculator import CryspyCalculator
from easyInterface.QtInterface import QtCalculatorInterface

class Proxy(QObject):

    def __init__(self, parent=None):
        logging.info("")
        super().__init__(parent)
        #
        self._main_rcif_path = None
        self._phases_rcif_path = None
        self._experiment_rcif_path = None
        self._calculator_interface = None
        #
        self.project_control = ProjectControl()
        self._measured_data_model = MeasuredDataModel()
        self._calculated_data_model = CalculatedDataModel()
        self._bragg_peaks_model = BraggPeaksModel()
        self._cell_parameters_model = CellParametersModel()
        self._cell_box_model = CellBoxModel()
        self._atom_sites_model = AtomSitesModel()
        self._atom_adps_model = AtomAdpsModel()
        self._atom_msps_model = AtomMspsModel()
        self._fitables_model = FitablesModel()
        self._status_model = StatusModel()
        self._file_structure_model = FileStructureModel()

        self._refine_thread = None
        self._refinement_running = False
        self._refinement_done = False
        self._refinement_result = None

        self._needToSave = False

    @Slot()
    def loadPhasesFromFile(self):
        """
        Replace internal structure models based on requested content from CIF
        """
        self._phases_rcif_path = self.project_control.phases_rcif_path
        self._calculator_interface.updatePhaseDefinition(self._phases_rcif_path)
        self._file_structure_model.setCalculatorInterface(self._calculator_interface)
        # explicit emit required for the view to reload the model content
        self.projectChanged.emit()

    @Slot()
    def loadExperimentFromFile(self):
        """
        Replace internal experiment models based on requested content from CIF
        """
        self._experiment_rcif_path = self.project_control.experiment_rcif_path
        self._calculator_interface.updateExpsDefinition(self._experiment_rcif_path)
        self._measured_data_model.setCalculatorInterface(self._calculator_interface)
        self._file_structure_model.setCalculatorInterface(self._calculator_interface)
        # explicit emit required for the view to reload the model content
        self.projectChanged.emit()

    # Load CIF method, accessible from QML
    @Slot()
    def initialize(self):
        logging.info("")
        self._main_rcif_path = self.project_control.main_rcif_path
        #logging.info(self._calculator.asCifDict())
        # TODO This is where you would choose the calculator and import the module
        self._calculator_interface = QtCalculatorInterface(
            CryspyCalculator(self._main_rcif_path)
        )
        self._calculator_interface.projectDictChanged.connect(self.projectChanged)
        self._calculator_interface.canUndoOrRedoChanged.connect(self.canUndoOrRedoChanged)
        self.projectChanged.connect(self.set_SaveState)
        #logging.info(self._calculator_interface.asCifDict())
        ####self.projectChanged.connect(self.updateCalculatedSeries) #---#
        # This should pick up on non-valid cif files
        #if not check_project_dict(self._calculator.asCifDict()):
        #    # Note that new projects also fall into here, so:
        #    if not self._calculator.name():
        #        self.project_control._isValidCif = False
        #        return
        #
        self._measured_data_model.setCalculatorInterface(self._calculator_interface)
        self._calculated_data_model.setCalculatorInterface(self._calculator_interface)
        self._bragg_peaks_model.setCalculatorInterface(self._calculator_interface)
        self._cell_parameters_model.setCalculatorInterface(self._calculator_interface)
        self._cell_box_model.setCalculatorInterface(self._calculator_interface)
        self._atom_sites_model.setCalculatorInterface(self._calculator_interface)
        self._atom_adps_model.setCalculatorInterface(self._calculator_interface)
        self._atom_msps_model.setCalculatorInterface(self._calculator_interface)
        self._fitables_model.setCalculatorInterface(self._calculator_interface)
        self._status_model.setCalculatorInterface(self._calculator_interface)
        self._file_structure_model.setCalculatorInterface(self._calculator_interface)
        #
        self._refine_thread = Refiner(self._calculator_interface, 'refine')
        self._refine_thread.finished.connect(self._status_model.onRefinementDone)

        # We can't link signals as the manager signals emitted before the dict is updated :-(
        # self.projectChanged.emit()

        self._calculator_interface.clearUndoStack()
        self.reset_saveState()

    @Slot()
    def createProjectZip(self):
        self._calculator_interface.writeMainCif(self.project_control.tempDir.name)
        writeEmptyProject(self.project_control, self.project_control._projectFile)
        self.reset_saveState()

    @Slot(str)
    def saveProject(self, saveName):
        self._calculator_interface.saveCifs(self.project_control.tempDir.name)
        writeProject(self.project_control, saveName)
        self.reset_saveState()


    @Slot()
    def updateProjectSave(self):
        self.saveProject(self.project_control._projectFile)
        self.reset_saveState()

    def get_saveState(self):
        return self._needToSave

    def set_SaveState(self):
        self._needToSave = True
        logging.info('save_state - {}'.format(self._needToSave))

    def reset_saveState(self):
        self._needToSave = False
        logging.info('reset_state - {}'.format(self._needToSave))

    # ##############
    # QML Properties
    # ##############

    # Notifications of changes for QML GUI about projectDictChanged,
    # which calls another signal projectChanged

    projectChanged = Signal()
    canUndoOrRedoChanged = Signal()

    # self._projectChanged.connect(self.set_SaveState)

    calculatorInterface = Property('QVariant', lambda self: self._calculator_interface, notify=projectChanged)
    project = Property('QVariant', lambda self: self._calculator_interface.asDict(), notify=projectChanged)
    phaseCif = Property('QVariant', lambda self: self._file_structure_model.asPhaseString(), notify=projectChanged)
    experimentCif = Property('QVariant', lambda self: self._file_structure_model.asExperimentString(), notify=projectChanged)
    calculationCif = Property('QVariant', lambda self: self._file_structure_model.asCalculationString(), notify=projectChanged)

    getSaveState = Property(bool, lambda self: self.get_saveState(), notify=projectChanged)

    canUndo = Property('QVariant', lambda self: self._calculator_interface.canUndo(), notify=canUndoOrRedoChanged)
    canRedo = Property('QVariant', lambda self: self._calculator_interface.canRedo(), notify=canUndoOrRedoChanged)

    # Notifications of changes for QML GUI are done, when needed, in the
    # respective classes via dataChanged.emit() or layotChanged.emit() signals

    measuredData = Property('QVariant', lambda self: self._measured_data_model, constant=True)
    calculatedData = Property('QVariant', lambda self: self._calculated_data_model, constant=True)
    braggPeaks = Property('QVariant', lambda self: self._bragg_peaks_model, constant=True)
    cellParameters = Property('QVariant', lambda self: self._cell_parameters_model.asModel(), constant=True)
    cellBox = Property('QVariant', lambda self: self._cell_box_model.asModel(), constant=True)
    atomSites = Property('QVariant', lambda self: self._atom_sites_model.asModel(), constant=True)
    atomAdps = Property('QVariant', lambda self: self._atom_adps_model.asModel(), constant=True)
    atomMsps = Property('QVariant', lambda self: self._atom_msps_model.asModel(), constant=True)
    fitables = Property('QVariant', lambda self: self._fitables_model.asModel(), constant=True)

    statusInfo = Property('QVariant', lambda self: self._status_model.returnStatusBarModel(), constant=True)
    chartInfo = Property('QVariant', lambda self: self._status_model.returnChartModel(), constant=True)
    fileStructure = Property('QVariant', lambda self: self._file_structure_model.asModel(), constant=True)

    # ##########
    # REFINEMENT
    # ##########

    def _thread_finished(self, res):
        """
        Notfy the listeners about refinement results
        """
        logging.info("")
        self._refinement_running = False
        self._refinement_done = True
        self._refinement_result = res
        self._needToSave = True
        self.refinementChanged.emit()


    def _thread_failed(self, reason):
        """
        Notify the GUI about failure so a message can be shown
        """
        logging.info("Refinement failed: " + str(reason))
        self._refinement_running = False
        self._refinement_done = False
        self.refinementChanged.emit()

    @Slot()
    def refine(self):
        """
        Start refinement as a separate thread
        """
        logging.info("")
        if self._refinement_running:
            logging.info("Fitting stopped")
            # This lacks actual stopping functionality, needs to be added
            self._refinement_running = False
            self._refinement_done = True
            self.refinementChanged.emit()
            return
        self._refinement_running = True
        self._refinement_done = False
        self._refine_thread.finished.connect(self._thread_finished)
        self._refine_thread.failed.connect(self._thread_failed)
        self._refine_thread.start()
        self.refinementChanged.emit()
        logging.info("")

    refinementChanged = Signal()
    refinementRunning = Property(bool, lambda self: self._refinement_running, notify=refinementChanged)
    refinementDone = Property(bool, lambda self: self._refinement_done, notify=refinementChanged)
    refinementResult = Property('QVariant', lambda self: self._refinement_result, notify=refinementChanged)

    # ######
    # REPORT
    # ######

    @Slot(str)
    def store_report(self, report=""):
        """
        Keep the QML generated HTML report for saving
        """
        self.report_html = report

    @Slot(str, str)
    def save_report(self, filename="", extension="html"):
        """
        Save the generated report to the specified file
        Currently only html
        """
        full_filename = filename + extension.lower()
        full_filename = os.path.join(self.project_control.get_project_dir_absolute_path(), full_filename)

        if not self.report_html:
            logging.info("No report to save")
            return

        if extension == '.HTML':
            # HTML can contain non-ascii, so need to open with right encoding
            with open(full_filename, 'w', encoding='utf-8') as report_file:
                report_file.write(self.report_html)
                logging.info("Report written")
        elif extension == '.PDF':
            document = QTextDocument(parent=None)
            document.setHtml(self.report_html)
            printer = QPdfWriter(full_filename)
            printer.setPageSize(printer.A4)
            document.print_(printer)
        else:
            raise NotImplementedError

        # Show the generated report in the default browser
        url = os.path.realpath(full_filename)
        Helpers.open_url(url=url)
