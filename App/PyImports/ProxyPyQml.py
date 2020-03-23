import os
import time
from copy import deepcopy

from PySide2.QtCore import QObject, Signal, Slot, Property
from PySide2.QtGui import QPdfWriter, QTextDocument

from PyImports.DisplayModels import *
from PyImports.ProjectSentinel import ProjectControl, writeProject, check_project_dict, writeEmptyProject
from PyImports.QtInterface import QtCalculatorInterface
from PyImports.Refinement import Refiner
from PyImports.ReleaseReader import Config

from easyInterface import logger
from easyInterface.Utils.Helpers import open_url
from easyInterface.Diffraction.Calculators.CryspyCalculator import CryspyCalculator


class ProxyPyQml(QObject):

    def __init__(self, release_config_file_path, parent=None):
        self.__log = logger.getLogger(__name__)
        self.__log.info("")
        super().__init__(parent)

        self.info = Config(release_config_file_path)['release']

        self._main_rcif_path = None
        self._phases_rcif_path = None
        self._experiment_rcif_path = None
        self._calculator_interface = None
        self._project_dict_copy = {}

        self._project_control = ProjectControl()
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
        self._refinement_result = {}

        self._needToSave = False

    @Slot()
    def loadPhasesFromFile(self):
        """
        Replace internal structure models based on requested content from CIF
        """
        self._phases_rcif_path = self._project_control.phases_rcif_path
        self._calculator_interface.addPhaseDefinition(self._phases_rcif_path)
        self._file_structure_model.setCalculatorInterface(self._calculator_interface)
        # explicit emit required for the view to reload the model content
        self.projectChanged.emit()
        self.onProjectUnsaved()

    @Slot()
    def loadExperimentFromFile(self):
        """
        Replace internal experiment models based on requested content from CIF
        """
        self._experiment_rcif_path = self._project_control.experiment_rcif_path
        self._calculator_interface.addExperimentDefinition(self._experiment_rcif_path)
        self._measured_data_model.setCalculatorInterface(self._calculator_interface)
        self._file_structure_model.setCalculatorInterface(self._calculator_interface)
        # explicit emit required for the view to reload the model content
        self._calculator_interface.updateCalculations()
        self.projectChanged.emit()
        self.onProjectUnsaved()

    # Load CIF method, accessible from QML
    @Slot()
    def initialize(self):
        self.__log.info("")
        self._main_rcif_path = self._project_control.main_rcif_path
        #logging.info(self._calculator.asCifDict())
        # TODO This is where you would choose the calculator and import the module
        self._calculator_interface = QtCalculatorInterface(
            CryspyCalculator(self._main_rcif_path)
        )
        self._calculator_interface.project_dict['app']['name'] = self.info['name']
        self._calculator_interface.project_dict['app']['version'] = self.info['version']
        self._calculator_interface.project_dict['app']['url'] = self.info['url']
        self._calculator_interface.projectDictChanged.connect(self.projectChanged)
        self._calculator_interface.canUndoOrRedoChanged.connect(self.canUndoOrRedoChanged)
        self._calculator_interface.clearUndoStack()
        self.onProjectSaved()
        self.projectChanged.connect(self.onProjectChanged)

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
        self._refine_thread.failed.connect(self._thread_failed)
        self._refine_thread.finished.connect(self._thread_finished)
        self._refine_thread.finished.connect(self._status_model.onRefinementDone)

        # We can't link signals as the manager signals emitted before the dict is updated :-(
        # self.projectChanged.emit()


    @Slot()
    def createProjectZip(self):
        self._calculator_interface.writeMainCif(self._project_control.tempDir.name)
        writeEmptyProject(self._project_control, self._project_control._project_file)
        self.onProjectSaved()

    @Slot(str)
    def createProject(self, file_path):
        self._project_control.createProject(file_path)
        self.onProjectSaved()

    @Slot(str)
    def saveProjectAs(self, file_path):
        self._project_control._project_file = file_path
        self.saveProject()

    @Slot()
    def saveProject(self):
        self._calculator_interface.saveCifs(self._project_control.tempDir.name)
        writeProject(self._project_control, self._project_control._project_file)
        self.onProjectSaved()

    def onProjectSaved(self):
        if self._calculator_interface is not None:
            self._project_dict_copy = deepcopy(self._calculator_interface.project_dict)
        self._needToSave = False
        self.projectSaveStateChanged.emit()

    def onProjectUnsaved(self):
        self._needToSave = True
        self.projectSaveStateChanged.emit()

    def onProjectChanged(self):
        keys, _ = self._calculator_interface.project_dict.dictComparison(self._project_dict_copy)
        self.__log.debug(f"keys: {keys}")
        self._needToSave = True
        if not keys:
            self._needToSave = False
        self.__log.debug(f"needToSave: {self._needToSave}")
        self.projectSaveStateChanged.emit()

    # ##############
    # QML Properties
    # ##############

    # Notifications of changes for QML GUI about projectDictChanged,
    # which calls another signal projectChanged

    projectChanged = Signal()
    projectSaveStateChanged = Signal()
    canUndoOrRedoChanged = Signal()

    # self._projectChanged.connect(self.set_SaveState)

    projectChangedTime = Property(str, lambda self: str(time.time()), notify=projectChanged)

    projectDict = Property('QVariant', lambda self: self._calculator_interface.asDict(), notify=projectChanged)
    phaseCif = Property('QVariant', lambda self: self._file_structure_model.asPhaseString(), notify=projectChanged)
    experimentCif = Property('QVariant', lambda self: self._file_structure_model.asExperimentString(), notify=projectChanged)
    calculationCif = Property('QVariant', lambda self: self._file_structure_model.asCalculationString(), notify=projectChanged)

    needToSave = Property(bool, lambda self: self._needToSave, notify=projectSaveStateChanged)
    projectFilePathSelected = Property(bool, lambda self: bool(self._project_control._project_file), notify=projectSaveStateChanged)

    calculatorInterface = Property('QVariant', lambda self: self._calculator_interface, notify=projectChanged)
    undoText = Property('QVariant', lambda self: self._calculator_interface.undoText(), notify=canUndoOrRedoChanged)
    redoText = Property('QVariant', lambda self: self._calculator_interface.redoText(), notify=canUndoOrRedoChanged)
    canUndo = Property('QVariant', lambda self: self._calculator_interface.canUndo(), notify=canUndoOrRedoChanged)
    canRedo = Property('QVariant', lambda self: self._calculator_interface.canRedo(), notify=canUndoOrRedoChanged)

    # Notifications of changes for QML GUI are done, when needed, in the
    # respective classes via dataChanged.emit() or layotChanged.emit() signals

    proxy = Property('QVariant', lambda self: self, constant=True)

    projectControl = Property('QVariant', lambda self: self._project_control, constant=True)
    projectManager = Property('QVariant', lambda self: self._project_control.manager, constant=True)

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

    releaseInfo = Property('QVariant', lambda self: self.info, constant=True)

    # ##########
    # REFINEMENT
    # ##########

    def _thread_finished(self, res):
        """
        Notfy the listeners about refinement results
        """
        self._refinement_running = False
        self._refinement_done = True
        self._refinement_result = deepcopy(res)
        self.refinementStatusChanged.emit()

    def _thread_failed(self, reason):
        """
        Notify the GUI about failure so a message can be shown
        """
        self.__log.info("Refinement failed: " + str(reason))
        self._refinement_running = False
        self._refinement_done = False
        self.refinementStatusChanged.emit()

    @Slot()
    def refine(self):
        """
        Start refinement as a separate thread
        """
        self.__log.info("")
        if self._refinement_running:
            self.__log.info("Fitting stopped")
            # This lacks actual stopping functionality, needs to be added
            self._refinement_running = False
            self._refinement_done = True
            self.refinementStatusChanged.emit()
            return
        self._refinement_running = True
        self._refinement_done = False
        self.refinementStatusChanged.emit()
        self._refine_thread.start()

    refinementStatusChanged = Signal()
    refinementStatus = Property('QVariant', lambda self: [self._refinement_running, self._refinement_done, self._refinement_result], notify=refinementStatusChanged)

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
    def save_report(self, filename="", extension=".HTML"):
        """
        Save the generated report to the specified file
        Currently only html
        """
        full_filename = filename + extension.lower()
        full_filename = os.path.join(self._project_control.get_project_dir_absolute_path(), full_filename)

        if not self.report_html:
            self.__log.info("No report to save")
            return

        if extension == '.HTML':
            # HTML can contain non-ascii, so need to open with right encoding
            with open(full_filename, 'w', encoding='utf-8') as report_file:
                report_file.write(self.report_html)
                self.__log.info("Report written")
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
        open_url(url=url)
