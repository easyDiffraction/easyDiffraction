import os
import logging

from PySide2.QtCore import QUrl, QObject, Signal, Slot, Property
from PySide2.QtGui import QStandardItemModel

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
from PyImports.Refinement import Refiner
import PyImports.Helpers as Helpers

class Proxy(QObject):

    def __init__(self, parent=None):
        logging.info("")
        super().__init__(parent)
        #
        self._main_rcif_path = None
        self._calculator = None
        self._tempFolder = None
        #
        self._measured_data_model = None
        self._calculated_data_model = None
        self._calculated_headers_model = None
        self._bragg_peaks_model = None
        self._cell_parameters_model = None
        self._cell_box_model = None
        self._atom_sites_model = None
        self._atom_adps_model = None
        self._atom_msps_model = None
        self._fitables_model = None
        self._status_model = None
        self._refine_thread = None
        self._refinement_running = False
        self._refinement_done = False
        self._refinement_result = None
        self._isValidCif = None

    # Load CIF method, accessible from QML
    @Slot(str)
    def loadCif(self, main_rcif_path):
        logging.info("")
        #
        self._main_rcif_path = QUrl(main_rcif_path).toLocalFile()
        #
        if Helpers.check_if_zip(self._main_rcif_path):
            if Helpers.check_project_file(self._main_rcif_path):
                self._tempFolder = Helpers.temp_project_dir(self._main_rcif_path)
                self._main_rcif_path = os.path.join(self._tempFolder.name, 'main.cif')
                # TODO close self._tempFolder using self._tempFolder.cleanup() on exit.
        #
        self._calculator = CryspyCalculator(self._main_rcif_path)
        self._calculator.projectDictChanged.connect(self.projectChanged)
        #
        if not Helpers.check_project_dict(self._calculator.asCifDict()):
            self._isValidCif = False
            return
        #
        self._measured_data_model = MeasuredDataModel(self._calculator)
        self._calculated_data_model = CalculatedDataModel(self._calculator)
        self._bragg_peaks_model = BraggPeaksModel(self._calculator)
        self._cell_parameters_model = CellParametersModel(self._calculator)
        self._cell_box_model = CellBoxModel(self._calculator)
        self._atom_sites_model = AtomSitesModel(self._calculator)
        self._atom_adps_model = AtomAdpsModel(self._calculator)
        self._atom_msps_model = AtomMspsModel(self._calculator)
        self._fitables_model = FitablesModel(self._calculator)
        self._status_model = StatusModel(self._calculator)
        #
        self._refine_thread = Refiner(self._calculator, 'refine')
        self._refine_thread.finished.connect(self._status_model.onRefinementDone)
        self._isValidCif = True

    @Slot(str)
    def saveCif(self, saveName):
        data_dir = Helpers.make_temp_dir()
        self._calculator.saveCifs(data_dir.name)
        filenames = {
            'original': ['main.rcif', 'pnd_calc.rcif', 'pnd_data.rcif'],
            'new':      ['main.cif', 'phases.cif', 'experiments.cif']
        }
        allOK = Helpers.create_project_zip(data_dir.name, saveName)
        data_dir.cleanup()
        if not allOK:
            raise FileNotFoundError

    # ##############
    # QML Properties
    # ##############

    # Notifications of changes for QML GUI about projectDictChanged,
    # which calls another signal projectChanged
    projectChanged = Signal()
    project = Property('QVariant', lambda self: self._calculator.asDict(), notify=projectChanged)
    cif = Property('QVariant', lambda self: self._calculator.asCifDict(), notify=projectChanged)

    # Notifications of changes for QML GUI are done, when needed, in the
    # respective classes via dataChanged.emit() or layotChanged.emit() signals
    measuredData = Property('QVariant', lambda self: self._measured_data_model.asDataModel(), constant=True)
    measuredDataHeader = Property('QVariant', lambda self: self._measured_data_model.asHeadersModel(), constant=True)
    calculatedData = Property('QVariant', lambda self: self._calculated_data_model.asDataModel(), constant=True)
    calculatedDataHeader = Property('QVariant', lambda self: self._calculated_data_model.asHeadersModel(), constant=True)
    braggPeaks = Property('QVariant', lambda self: self._bragg_peaks_model.asDataModel(), constant=True)
    braggPeaksTicks = Property('QVariant', lambda self: self._bragg_peaks_model.asTickModel(), constant=True)
    cellParameters = Property('QVariant', lambda self: self._cell_parameters_model.asModel(), constant=True)
    cellBox = Property('QVariant', lambda self: self._cell_box_model.asModel(), constant=True)
    atomSites = Property('QVariant', lambda self: self._atom_sites_model.asModel(), constant=True)
    atomAdps = Property('QVariant', lambda self: self._atom_adps_model.asModel(), constant=True)
    atomMsps = Property('QVariant', lambda self: self._atom_msps_model.asModel(), constant=True)
    fitables = Property('QVariant', lambda self: self._fitables_model.asModel(), constant=True)
    statusInfo = Property('QVariant', lambda self: self._status_model.returnStatusBarModel(), constant=True)
    chartInfo = Property('QVariant', lambda self: self._status_model.returnChartModel(), constant=True)

    validCif = Property(bool, lambda self: self._isValidCif, constant=False)

    def _get_working_dir(self):
        if self._tempFolder is None:
            [working_dir, _] = os.path.split(self._main_rcif_path)
        else:
            working_dir = self._tempFolder.name
        return working_dir

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
        furl = os.path.join(self.get_project_url_absolute_path(), fname)
        if os.path.isfile(fpath):
            return furl
        return ""

    def get_project_dir_absolute_path(self):
        if self._main_rcif_path:
            return os.path.dirname(os.path.abspath(self._main_rcif_path))
        return ""
    def get_project_url_absolute_path(self):
        if self._main_rcif_path:
            return str(QUrl.fromLocalFile(os.path.dirname(self._main_rcif_path)).toString())
        return ""
    project_dir_absolute_path = Property(str, get_project_dir_absolute_path, notify=projectChanged)
    project_url_absolute_path = Property(str, get_project_url_absolute_path, notify=projectChanged)

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
            logging.info("No report to save")
            return

        # HTML can contain non-ascii, so need to open with right encoding
        with open(full_filename, 'w', encoding='utf-8') as report_file:
            report_file.write(self.report_html)
            logging.info("Report written")

        # Show the generated report in the default browser
        url = os.path.realpath(full_filename)
        Helpers.open_url(url=url)

