import logging

from PySide2.QtCore import Qt, QObject, Signal
from PySide2.QtGui import QStandardItemModel, QStandardItem

from PyImports.Models.BaseModel import BaseModel

class FileStructureModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        # set roles
        self._phase_role = Qt.UserRole + 2
        self._experiment_role = Qt.UserRole + 3
        self._data_model.setItemRoleNames({
            self._phase_role: b'phasesRole',
            self._experiment_role: b'experimentsRole',
            })

    def _setModelsFromProjectDict(self):
        """
        Create the model needed for GUI representation of structure.
        """

        cif_dict = self._calculator.asCifDict()
        # Important - clear the model, so subsequent calls deal with empty
        self._data_model.clear()

        self._data_model.blockSignals(True)
        self._headers_model.blockSignals(True)

        phases_cif = cif_dict['phases']
        exp_cif = cif_dict['experiments']

        # Currently only one phase/experiment, so assigning
        # explicitly. With more components, we need a proper loop
        # as shown below
        item1 = QStandardItem()
        item1.setData(phases_cif, self._phase_role)
        self._data_model.appendRow(item1)
        item2 = QStandardItem()
        item2.setData(exp_cif, self._experiment_role)
        self._data_model.appendRow(item2)

        #for data_str cif_dict.items():
        #    item = QStandardItem()
        #    item.setData(phases_cif, <self._some_role>)
        #    self._data_model.appendRow(item)

        self._data_model.blockSignals(False)
        self._headers_model.blockSignals(False)
        self._data_model.layoutChanged.emit()
        self._headers_model.layoutChanged.emit()

