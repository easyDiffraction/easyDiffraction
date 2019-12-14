import logging

from PySide2.QtCore import Qt, QObject, Signal, Slot, Property
from PySide2.QtGui import QStandardItem, QStandardItemModel

from PyImports.Models.BaseModel import BaseModel

class MeasuredDataModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._headers_model = QStandardItemModel()
        self._model = QStandardItemModel()
        self._project_dict = None

    #def _setModelsFromProjectDict(self, project_dict):
    def _setModelsFromProjectDict(self):
        """Create the model needed for GUI measured data table and chart."""
        logging.info("+++++++++++++++++++++++++ setData start") # profiling
        for experiment_id, experiment_dict in self._project_dict['experiments'].items():
            self._model.blockSignals(True)
            self._headers_model.blockSignals(True)
            #
            column_count = len(experiment_dict['measured_pattern'].items())
            row_count = len(list(experiment_dict['measured_pattern'].items())[0][1])
            self._model.setColumnCount(column_count)
            self._model.setRowCount(row_count)
            self._headers_model.setColumnCount(column_count)
            self._headers_model.setRowCount(1)
            #
            for colum_index, (data_id, data_list) in enumerate(experiment_dict['measured_pattern'].items()):
                index = self._headers_model.index(0, colum_index)
                self._headers_model.setData(index, data_id, Qt.DisplayRole)
                for row_index, value in enumerate(data_list):
                    index = self._model.index(row_index, colum_index)
                    self._model.setData(index, value, Qt.DisplayRole)
            #
            self._model.blockSignals(False)
            self._headers_model.blockSignals(False)
            #
            self._model.layoutChanged.emit()
            self._headers_model.layoutChanged.emit()
        logging.info("+++++++++++++++++++++++++ setData end") # profiling
