import os
import sys
import logging
import numpy as np

from PySide2.QtCore import QUrl, Qt, QObject, Signal, Slot, Property
from PySide2.QtGui import QStandardItemModel

from PyImports.Calculators.CryspyCalculator import *
from PyImports.Models.MeasuredDataModel import *
from PyImports.Models.CalculatedDataModel import *
from PyImports.Models.BraggPeaksModel import *
from PyImports.Models.CellParametersModel import *
from PyImports.Models.CellBoxModel import *
from PyImports.Models.AtomSitesModel import *
from PyImports.Models.AtomAdpsModel import *
from PyImports.Models.AtomMspsModel import *
from PyImports.Models.FitablesModel import *
from PyImports.Refinement import *

class Proxy(QObject):

    def __init__(self, parent=None):
        logging.info("")
        super().__init__(parent)
        self._main_rcif_path = None
        self._project_model = None
        self._measured_data_model = None
        self._calculated_data_model = None
        self._bragg_peaks_model = None
        self._cell_parameters_model = None
        self._cell_box_model = None
        self._atom_sites_model = None
        self._atom_adps_model = None
        self._atom_msps_model = None
        self._fitables_model = None
        self._refine_thread = None
        self._refinement_running = False
        self._refinement_done = False
        self._refinement_result = None

    # Load rcif
    @Slot(str)
    def init(self, main_rcif_path):
        logging.info("")
        self._main_rcif_path = QUrl(main_rcif_path).toLocalFile()
        self._project_model = CryspyCalculator(self._main_rcif_path)
        ##print(self._project_model.asDict())
        self._measured_data_model = MeasuredDataModel(self._project_model)
        self._calculated_data_model = CalculatedDataModel(self._project_model)
        self._calculated_data_model.modelChanged.connect(self.projectChanged)
        self._bragg_peaks_model = BraggPeaksModel(self._project_model)
        self._cell_parameters_model = CellParametersModel(self._project_model)
        self._cell_box_model = CellBoxModel(self._project_model)
        self._atom_sites_model = AtomSitesModel(self._project_model)
        self._atom_adps_model = AtomAdpsModel(self._project_model)
        self._atom_msps_model = AtomMspsModel(self._project_model)
        self._fitables_model = FitablesModel(self._project_model)
        self._refine_thread = Refiner(self._project_model, 'refine')
        #self._fitables_model.modelChanged.connect(self.projectChanged)
        self.projectChanged.emit()
        self.measuredDataHeaderChanged.emit()
        self.measuredDataChanged.emit()
        self.calculatedDataHeaderChanged.emit()
        self.calculatedDataChanged.emit()
        self.braggPeaksChanged.emit()
        self.cellParametersChanged.emit()
        self.cellBoxChanged.emit()
        self.atomSitesChanged.emit()
        self.atomAdpsChanged.emit()
        self.atomMspsChanged.emit()
        self.fitablesChanged.emit()

    # Project model for QML
    projectChanged = Signal()
    def getProject(self):
        logging.info("")
        if self._project_model is None:
            return ""
        return self._project_model.asDict()
    project = Property('QVariant', getProject, notify=projectChanged)

    # CIF model for QML
    def getCif(self):
        logging.info("")
        if self._project_model is None:
            return ""
        return self._project_model.asCifDict()
    cif = Property('QVariant', getCif, notify=projectChanged)

    # Measured data header model for QML
    measuredDataHeaderChanged = Signal()
    def getMeasuredDataHeader(self):
        logging.info("")
        if self._measured_data_model is None:
            return QStandardItemModel()
        return self._measured_data_model.asHeadersModel()
    measuredDataHeader = Property('QVariant', getMeasuredDataHeader, notify=measuredDataHeaderChanged)

    # Measured data model for QML
    measuredDataChanged = Signal()
    def getMeasuredData(self):
        logging.info("")
        if self._measured_data_model is None:
            return QStandardItemModel()
        return self._measured_data_model.asDataModel()
    measuredData = Property('QVariant', getMeasuredData, notify=measuredDataChanged)

    # Calculated data header model for QML
    calculatedDataHeaderChanged = Signal()
    def getCalculatedDataHeader(self):
        logging.info("")
        if self._calculated_data_model is None:
            return QStandardItemModel()
        return self._calculated_data_model.asHeadersModel()
    calculatedDataHeader = Property('QVariant', getCalculatedDataHeader, notify=calculatedDataHeaderChanged)

    # Calculated data model for QML
    calculatedDataChanged = Signal()
    def getCalculatedData(self):
        logging.info("")
        if self._calculated_data_model is None:
            return QStandardItemModel()
        return self._calculated_data_model.asDataModel()
    calculatedData = Property('QVariant', getCalculatedData, notify=calculatedDataChanged)

    # Bragg peaks model for QML
    braggPeaksChanged = Signal()
    def getBraggPeaks(self):
        logging.info("")
        if self._bragg_peaks_model is None:
            return QStandardItemModel()
        return self._bragg_peaks_model.asDataModel()
    def getBraggPeaksTicks(self):
        logging.info("")
        if self._bragg_peaks_model is None:
            return QStandardItemModel()
        return self._bragg_peaks_model.asTickModel()
    braggPeaks = Property('QVariant', getBraggPeaks, notify=braggPeaksChanged)
    braggPeaksTicks = Property('QVariant', getBraggPeaksTicks, notify=braggPeaksChanged)

    # Cell parameters model for QML
    cellParametersChanged = Signal()
    def getCellParameters(self):
        logging.info("")
        if self._cell_parameters_model is None:
            return QStandardItemModel()
        return self._cell_parameters_model.asModel()
    cellParameters = Property('QVariant', getCellParameters, notify=cellParametersChanged)

    # Cell box model for QML
    cellBoxChanged = Signal()
    def getCellBox(self):
        logging.info("")
        if self._cell_box_model is None:
            return QStandardItemModel()
        return self._cell_box_model.asModel()
    cellBox = Property('QVariant', getCellBox, notify=cellBoxChanged)

    # Atom sites model for QML
    atomSitesChanged = Signal()
    def getAtomSites(self):
        logging.info("")
        if self._atom_sites_model is None:
            return QStandardItemModel()
        return self._atom_sites_model.asModel()
    atomSites = Property('QVariant', getAtomSites, notify=atomSitesChanged)

    # Atom ADPs model for QML
    atomAdpsChanged = Signal()
    def getAtomAdps(self):
        logging.info("")
        if self._atom_adps_model is None:
            return QStandardItemModel()
        return self._atom_adps_model.asModel()
    atomAdps = Property('QVariant', getAtomAdps, notify=atomAdpsChanged)

    # Atom MSPs model for QML
    atomMspsChanged = Signal()
    def getAtomMsps(self):
        logging.info("")
        if self._atom_msps_model is None:
            return QStandardItemModel()
        return self._atom_msps_model.asModel()
    atomMsps = Property('QVariant', getAtomMsps, notify=atomMspsChanged)

    # Fitables model for QML
    fitablesChanged = Signal()
    def getFitables(self):
        ##logging.info("")
        if self._fitables_model is None:
            return QStandardItemModel()
        return self._fitables_model.asModel()
    fitables = Property('QVariant', getFitables, notify=fitablesChanged)

    # Time stamp of changes
    #timeStamp = Property(str, lambda self: str(np.datetime64('now')), notify=projectChanged)

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

    # ####
    # MISC
    # ####

    @Slot(str, result=str)
    def fullFilePath(self, fname):
        fpath = os.path.join(self.get_project_dir_absolute_path(), fname)
        if os.path.isfile(fpath):
            return fpath
        return ""

    def get_project_dir_absolute_path(self):
        if self._main_rcif_path:
            return os.path.dirname(os.path.abspath(self._main_rcif_path))
        return ""
    project_dir_absolute_path = Property(str, get_project_dir_absolute_path, notify=projectChanged)
    #project_url_absolute_path = Property(str, lambda self: str(QUrl.fromLocalFile(os.path.dirname(self._main_rcif_path)).toString()), notify=projectChanged)

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
        full_filename = os.path.join(self.get_project_dir_absolute_path(), full_filename)

        if not self.report_html:
            print("No report to save")
            return

        # HTML can contain non-ascii, so need to open with right encoding
        with open(full_filename, 'w', encoding='utf-8') as report_file:
            report_file.write(self.report_html)
            print("Report written")

        # Show the generated report in the default browser
        # TODO: refactor this part out
        import webbrowser
        try:
            webbrowser.open('file://' + os.path.realpath(full_filename))
        except ex as Exception:
            print("Report viewing failed: "+ str(ex))

    # Not used?
    @Slot(result=str)
    def get_report_html(self):
        return self.report_html

    # Not used?
    @Slot(result=str)
    def get_table_html(self):
        tableHTML = \
        "<h1>" + self.project_name + "</h1><p>" + \
        "<b>Creation date: </b>11.04.2019<br>" + \
        "<b>Project folder: </b>" + self.tmp_rcif_dir_name() + "<br>" + \
        "<b>Project file: </b>" + self.tmp_rcif_file_name() + "<br>" + \
        "<b>Experimental data file: </b>" + self.tmp_rcif_file_name() + "<br>" + \
        "<b>Instrument: </b>6T2 at LLB<br>" + \
        "<b>Sample: </b>" + self.project_name + "<br> </p>" + \
        "<h2>Parameters</h2>"
        return tableHTML


