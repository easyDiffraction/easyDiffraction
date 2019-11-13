import logging

from PySide2.QtCore import Qt, QObject, Signal
from PySide2.QtGui import QStandardItemModel

class BraggPeaksModel(QObject):
    def __init__(self, calculator, parent=None):
        super().__init__(parent)
        calculator.projectDictChanged.connect(self.onProjectChanged)
        self._project_dict = calculator.asDict()
        self._data_model = QStandardItemModel()
        self._tick_model = QStandardItemModel()
        self._setModelsFromProjectDict()

    def _setModelsFromProjectDict(self):
        """Create the model needed for GUI chart: Bragg peaks."""
        logging.info("+++++++++++++++++++++++++ setData start") # profiling
        for experiment_id, experiment_dict in self._project_dict['calculations'].items():
            for phase_id in self._project_dict['phases'].keys():
                # data model
                column_count = len(experiment_dict['bragg_peaks'][phase_id].items())
                row_count = len(list(experiment_dict['bragg_peaks'][phase_id].items())[0][1])
                self._data_model.blockSignals(True)
                self._data_model.setColumnCount(column_count)
                self._data_model.setRowCount(row_count)
                for colum_index, (data_id, data_list) in enumerate(experiment_dict['bragg_peaks'][phase_id].items()):
                    for row_index, value in enumerate(data_list):
                        index = self._data_model.index(row_index, colum_index)
                        self._data_model.setData(index, value, Qt.DisplayRole)
                self._data_model.blockSignals(False)
                self._data_model.layoutChanged.emit()
                # tick model
                self._tick_model.blockSignals(True)
                vertical_points = 7
                self._tick_model.setColumnCount(2)
                self._tick_model.setRowCount(row_count * vertical_points)
                for row_index in range(row_count):
                    for vertical_index in range(vertical_points):
                        data_x_index = self._data_model.index(row_index, 3)
                        data_x_value = self._data_model.data(data_x_index, Qt.DisplayRole)
                        tick_x_index = self._tick_model.index(row_index * vertical_points + vertical_index, 0)
                        tick_x_value = data_x_value
                        tick_y_index = self._tick_model.index(row_index * vertical_points + vertical_index, 1)
                        tick_y_value = vertical_index
                        self._tick_model.setData(tick_x_index, tick_x_value, Qt.DisplayRole)
                        self._tick_model.setData(tick_y_index, tick_y_value, Qt.DisplayRole)
                self._tick_model.blockSignals(False)
                self._tick_model.layoutChanged.emit()
        logging.info("+++++++++++++++++++++++++ setData end") # profiling

    def onProjectChanged(self):
        """..."""
        self._setModelsFromProjectDict()

    def asTickModel(self):
        """..."""
        return self._tick_model

    def asDataModel(self):
        """Return data model."""
        return self._data_model


