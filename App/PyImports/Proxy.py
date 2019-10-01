from PySide2.QtCore import Qt, QObject, Signal, Slot, Property
from PySide2.QtGui import QStandardItemModel

import numpy as np

import logging
logging.basicConfig(format="%(asctime)-15s [%(levelname)s] %(filename)s %(funcName)s [%(lineno)d]: %(message)s", level=logging.INFO)

from PyImports.Calculators.CryspyCalculator import *
from PyImports.Models.MeasuredDataModel import *
from PyImports.Models.CalculatedDataModel import *
from PyImports.Models.BraggPeaksModel import *
from PyImports.Models.CellBoxModel import *
from PyImports.Models.AtomSitesModel import *
from PyImports.Models.AtomAdpsModel import *
from PyImports.Models.AtomMspsModel import *
from PyImports.Models.FitablesModel import *

class Proxy(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        logging.info("")
        self._project_model = None
        self._measured_data_model = None
        self._calculated_data_model = None
        self._bragg_peaks_model = None
        self._cell_box_model = None
        self._atom_sites_model = None
        self._atom_adps_model = None
        self._atom_msps_model = None
        self._fitables_model = None

    # Load rcif
    @Slot(str)
    def init(self, main_rcif_path):
        logging.info("")
        self._project_model = CryspyCalculator(main_rcif_path)
        ##print(self._project_model.asDict())
        self._measured_data_model = MeasuredDataModel(self._project_model)
        self._calculated_data_model = CalculatedDataModel(self._project_model)
        self._calculated_data_model.modelChanged.connect(self.projectChanged)
        self._bragg_peaks_model = BraggPeaksModel(self._project_model)
        self._cell_box_model = CellBoxModel(self._project_model)
        self._atom_sites_model = AtomSitesModel(self._project_model)
        self._atom_adps_model = AtomAdpsModel(self._project_model)
        self._atom_msps_model = AtomMspsModel(self._project_model)
        self._fitables_model = FitablesModel(self._project_model)
        #self._fitables_model.modelChanged.connect(self.projectChanged)
        self.projectChanged.emit()
        self.measuredDataHeaderChanged.emit()
        self.measuredDataChanged.emit()
        self.calculatedDataHeaderChanged.emit()
        self.calculatedDataChanged.emit()
        self.braggPeaksChanged.emit()
        self.cellBoxChanged.emit()
        self.atomSitesChanged.emit()
        self.atomAdpsChanged.emit()
        self.atomMspsChanged.emit()
        self.fitablesChanged.emit()

    # Project model for QML
    projectChanged = Signal()
    def getProject(self):
        logging.info("")
        #logging.info("********************************** GET PROJECT *******************************")
        if self._project_model is None:
            return ""
        return self._project_model.asDict()
    project = Property('QVariant', getProject, notify=projectChanged)

    # CIF model for QML
    def getCif(self):
        logging.info("")
        #logging.info("********************************** GET CIF *******************************")
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
        logging.info("")
        if self._fitables_model is None:
            return QStandardItemModel()
        return self._fitables_model.asModel()
    fitables = Property('QVariant', getFitables, notify=fitablesChanged)

    # Time stamp of changes
    timeStamp = Property(str, lambda self: str(np.datetime64('now')), notify=projectChanged)

    @Slot(result='QVariant')
    def refine(self):
        """refinement ..."""
        logging.info("")
        res = self._project_model.refine()
        logging.info("")
        return res

