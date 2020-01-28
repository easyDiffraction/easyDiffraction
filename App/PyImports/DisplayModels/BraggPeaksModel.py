import logging

from PySide2.QtCore import Qt, QObject, QPointF, Signal, Slot, Property
from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtCharts import QtCharts

from PyImports.DisplayModels.BaseModel import BaseModel

class BraggPeaksSeries(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self._series = []

    def updateSeries(self, calculator):
        logging.info("=====> start")
        project_dict = calculator.asDict()
        self._series.clear()
        for experiment_id, experiment_dict in project_dict['calculations'].items():
            for phase_id in project_dict['phases'].keys():
                x_list = experiment_dict['bragg_peaks'][phase_id]['ttheta']
                for x in x_list:
                    vertical_points = 11
                    for vertical_index in range(vertical_points):
                        self._series.append(QPointF(x, vertical_index))
        logging.info("<===== end")

    @Slot(QtCharts.QXYSeries)
    def updateQmlSeries(self, series):
        series.replace(self._series)

class BraggPeaksModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._project_dict = None
        self._model = QStandardItemModel()
        self._tick_model = QStandardItemModel()

    def _setModelsFromProjectDict(self):
        """Create the model needed for GUI chart: Bragg peaks."""
        logging.info("-> start")
        for experiment_id, experiment_dict in self._project_dict['calculations'].items():
            for phase_id in self._project_dict['phases'].keys():
                # data model
                column_count = len(experiment_dict['bragg_peaks'][phase_id].items())
                row_count = len(list(experiment_dict['bragg_peaks'][phase_id].items())[0][1])
                self._model.blockSignals(True)
                self._model.setColumnCount(column_count)
                self._model.setRowCount(row_count)
                for colum_index, (data_id, data_list) in enumerate(experiment_dict['bragg_peaks'][phase_id].items()):
                    for row_index, value in enumerate(data_list):
                        index = self._model.index(row_index, colum_index)
                        self._model.setData(index, value, Qt.DisplayRole)
                self._model.blockSignals(False)
                self._model.layoutChanged.emit()
                # tick model
                self._tick_model.blockSignals(True)
                vertical_points = 7
                self._tick_model.setColumnCount(2)
                self._tick_model.setRowCount(row_count * vertical_points)
                for row_index in range(row_count):
                    for vertical_index in range(vertical_points):
                        data_x_index = self._model.index(row_index, 3)
                        data_x_value = self._model.data(data_x_index, Qt.DisplayRole)
                        tick_x_index = self._tick_model.index(row_index * vertical_points + vertical_index, 0)
                        tick_x_value = data_x_value
                        tick_y_index = self._tick_model.index(row_index * vertical_points + vertical_index, 1)
                        tick_y_value = vertical_index
                        self._tick_model.setData(tick_x_index, tick_x_value, Qt.DisplayRole)
                        self._tick_model.setData(tick_y_index, tick_y_value, Qt.DisplayRole)
                self._tick_model.blockSignals(False)
                self._tick_model.layoutChanged.emit()
        logging.info("<- end")

    def asTickModel(self):
        """..."""
        return self._tick_model