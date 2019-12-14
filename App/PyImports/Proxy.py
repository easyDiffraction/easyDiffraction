import os
import logging

from PySide2.QtCore import QObject, Signal, Slot, Property

import PyImports.ProjectSentinel
from PyImports.Calculators.CryspyCalculator import CryspyCalculator
from PyImports.Models.MeasuredDataModel import MeasuredDataModel
from PyImports.Models.CalculatedDataModel import CalculatedDataModel
from PyImports.Models.BraggPeaksModel import BraggPeaksModel
from PyImports.Models.CellParametersModel import CellParametersModel
from PyImports.Models.CellBoxModel import CellBoxModel
from PyImports.Models.AtomSitesModel import AtomSitesModel
from PyImports.Models.AtomAdpsModel import AtomAdpsModel
from PyImports.Models.AtomMspsModel import AtomMspsModel
from PyImports.Models.FitablesModel import FitablesModel
from PyImports.Models.StatusModel import StatusModel
from PyImports.Models.FileStructureModel import FileStructureModel
from PyImports.ProjectSentinel import ProjectControl, writeProject, check_project_dict
from PyImports.Refinement import Refiner
import PyImports.Helpers as Helpers


class Proxy(QObject):

    def __init__(self, parent=None):
        logging.info("")
        super().__init__(parent)
        #
        self._main_rcif_path = None
        self._phases_rcif_path = None
        self._experiment_rcif_path = None
        self._calculator = None
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

    @Slot()
    def loadPhasesFromFile(self):
        """
        Replace internal structure models based on requested content from CIF
        """
        self._phases_rcif_path = self.project_control.phases_rcif_path
        self._calculator.updatePhases(self._phases_rcif_path)
        self._file_structure_model.setCalculator(self._calculator)

        pass

    @Slot()
    def loadExperimentFromFile(self):
        """
        Replace internal experiment models based on requested content from CIF
        """
        pass

    # Load CIF method, accessible from QML
    @Slot()
    def initialize(self):
        logging.info("")
        self._main_rcif_path = self.project_control.main_rcif_path
        #
        self._calculator = CryspyCalculator(self._main_rcif_path)
        self._calculator.projectDictChanged.connect(self.projectChanged)
        # This should pick up on non-valid cif files
        if not check_project_dict(self._calculator.asCifDict()):
            # Note that new projects also fall into here, so:
            if not self._calculator.name():
                self.project_control._isValidCif = False
                return
        #
        self._measured_data_model.setCalculator(self._calculator)
        self._calculated_data_model.setCalculator(self._calculator)
        self._bragg_peaks_model.setCalculator(self._calculator)
        self._cell_parameters_model.setCalculator(self._calculator)
        self._cell_box_model.setCalculator(self._calculator)
        self._atom_sites_model.setCalculator(self._calculator)
        self._atom_adps_model.setCalculator(self._calculator)
        self._atom_msps_model.setCalculator(self._calculator)
        self._fitables_model.setCalculator(self._calculator)
        self._status_model.setCalculator(self._calculator)
        self._file_structure_model.setCalculator(self._calculator)
        #
        self._refine_thread = Refiner(self._calculator, 'refine')
        self._refine_thread.finished.connect(self._status_model.onRefinementDone)
        # We can't link signals as the manager signals emitted before the dict is updated :-(
        self.projectChanged.emit()

    @Slot(str)
    def saveProject(self, saveName):
        self._calculator.saveCifs(self.project_control.tempDir.name)
        writeProject(self.project_control, saveName)

    @Slot()
    def updateProjectSave(self):
        self.saveProject(self.project_control._projectFile)

    # ##############
    # QML Properties
    # ##############
    def calculatorAsDict(self):
        return self._calculator.asDict()

    def calculatorAsCifDict(self):
        return self._calculator.asCifDict()

    # Notifications of changes for QML GUI about projectDictChanged,
    # which calls another signal projectChanged
    projectChanged = Signal()
    project = Property('QVariant', lambda self: self.calculatorAsDict(), notify=projectChanged)
    cif = Property('QVariant', lambda self: self.calculatorAsCifDict(), notify=projectChanged)

    # Notifications of changes for QML GUI are done, when needed, in the
    # respective classes via dataChanged.emit() or layotChanged.emit() signals
    measuredData = Property('QVariant', lambda self: self._measured_data_model.asModel(), constant=True)
    measuredDataHeader = Property('QVariant', lambda self: self._measured_data_model.asHeadersModel(), constant=True)
    calculatedData = Property('QVariant', lambda self: self._calculated_data_model.asModel(), constant=True)
    calculatedDataHeader = Property('QVariant', lambda self: self._calculated_data_model.asHeadersModel(),
                                    constant=True)
    braggPeaks = Property('QVariant', lambda self: self._bragg_peaks_model.asModel(), constant=True)
    braggPeaksTicks = Property('QVariant', lambda self: self._bragg_peaks_model.asTickModel(), constant=True)
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

        # HTML can contain non-ascii, so need to open with right encoding
        with open(full_filename, 'w', encoding='utf-8') as report_file:
            report_file.write(self.report_html)
            logging.info("Report written")

        # Show the generated report in the default browser
        url = os.path.realpath(full_filename)
        Helpers.open_url(url=url)
