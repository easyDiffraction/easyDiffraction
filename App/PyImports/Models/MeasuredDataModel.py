import logging

from PySide2.QtCore import Qt, QObject, QPointF, Signal, Slot, Property
from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtCharts import QtCharts

class MeasuredDataSeries(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self._upperSeries = []
        self._lowerSeries = []

    def initSeries(self, calculator):
        logging.info("+++++++++++++++++++++++++ start") # profiling
        project_dict = calculator.asDict()
        for experiment_id, experiment_dict in project_dict['experiments'].items():
            x_list = experiment_dict['measured_pattern']['x']
            y_obs_lower_list = experiment_dict['measured_pattern']['y_obs_lower']
            y_obs_upper_list = experiment_dict['measured_pattern']['y_obs_upper']
            for x, y_obs_lower, y_obs_upper in zip(x_list, y_obs_lower_list, y_obs_upper_list):
                self._lowerSeries.append(QPointF(x, y_obs_lower))
                self._upperSeries.append(QPointF(x, y_obs_upper))
        logging.info("+++++++++++++++++++++++++ end") # profiling

    @Slot(QtCharts.QXYSeries)
    def updateQmlLowerSeries(self, series):
        series.replace(self._lowerSeries)

    @Slot(QtCharts.QXYSeries)
    def updateQmlUpperSeries(self, series):
        series.replace(self._upperSeries)

class MeasuredDataModel(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._headers_model = QStandardItemModel()
        self._data_model = QStandardItemModel()

    def _setModelsFromProjectDict(self, project_dict):
        """Create the model needed for GUI measured data table and chart."""
        logging.info("+++++++++++++++++++++++++ setData start") # profiling
        for experiment_id, experiment_dict in project_dict['experiments'].items():
            self._data_model.blockSignals(True)
            self._headers_model.blockSignals(True)
            #
            column_count = len(experiment_dict['measured_pattern'].items())
            row_count = len(list(experiment_dict['measured_pattern'].items())[0][1])
            self._data_model.setColumnCount(column_count)
            self._data_model.setRowCount(row_count)
            self._headers_model.setColumnCount(column_count)
            self._headers_model.setRowCount(1)
            #
            for colum_index, (data_id, data_list) in enumerate(experiment_dict['measured_pattern'].items()):
                index = self._headers_model.index(0, colum_index)
                self._headers_model.setData(index, data_id, Qt.DisplayRole)
                for row_index, value in enumerate(data_list):
                    index = self._data_model.index(row_index, colum_index)
                    self._data_model.setData(index, value, Qt.DisplayRole)
            #
            self._data_model.blockSignals(False)
            self._headers_model.blockSignals(False)
            #
            self._data_model.layoutChanged.emit()
            self._headers_model.layoutChanged.emit()
        logging.info("+++++++++++++++++++++++++ setData end") # profiling

    def asHeadersModel(self):
        """Return headers model."""
        return self._headers_model

    def asDataModel(self):
        """Return data model."""
        return self._data_model

    def setCalculator(self, calculator):
        self._setModelsFromProjectDict(calculator.asDict())
