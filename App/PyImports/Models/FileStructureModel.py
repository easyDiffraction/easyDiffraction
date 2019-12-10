import logging

from PySide2.QtCore import Qt, QObject, Signal
from PySide2.QtGui import QStandardItemModel

from PyImports.Models.BaseModel import BaseModel

class FileStructureModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def _setModelsFromProjectDict(self):
        """
        Create the model needed for GUI representation of structure.
        """

        cif_dict = self._calculator.asCifDict()

        column_count = len(cif_dict)
        row_count = 1 # currenly just 1 component
        self._data_model.blockSignals(True)
        self._headers_model.blockSignals(True)
        self._data_model.setColumnCount(column_count)
        self._data_model.setRowCount(row_count)

        phases_cif = cif_dict['phases']
        exp_cif = cif_dict['experiments']

        for colum_index, (data_id, data_str) in enumerate(cif_dict.items()):
            index = self._headers_model.index(0, colum_index)
            self._headers_model.setData(index, data_id, Qt.DisplayRole)
            index = self._data_model.index(0, colum_index)
            self._data_model.setData(index, data_str, Qt.DisplayRole)

        self._data_model.blockSignals(False)
        self._headers_model.blockSignals(False)
        self._data_model.layoutChanged.emit()
        self._headers_model.layoutChanged.emit()
