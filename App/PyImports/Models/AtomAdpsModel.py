import logging

from PySide2.QtCore import Qt, QObject, Signal, Slot, Property
from PySide2.QtGui import QStandardItem, QStandardItemModel

import PyImports.Helpers as Helpers
from PyImports.Models.BaseModel import BaseModel

class AtomAdpsModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._project_dict = None
        self._model = QStandardItemModel()
        # set roles
        self._label_role = Qt.UserRole + 1
        self._type_role = Qt.UserRole + 2
        self._uiso_role = Qt.UserRole + 3
        self._u11_role = Qt.UserRole + 4
        self._u22_role = Qt.UserRole + 5
        self._u33_role = Qt.UserRole + 6
        self._u12_role = Qt.UserRole + 7
        self._u13_role = Qt.UserRole + 8
        self._u23_role = Qt.UserRole + 9
        self._model.setItemRoleNames({
            self._label_role: b'label',
            self._type_role: b'type',
            self._uiso_role: b'uiso',
            self._u11_role: b'u11',
            self._u22_role: b'u22',
            self._u33_role: b'u33',
            self._u12_role: b'u12',
            self._u13_role: b'u13',
            self._u23_role: b'u23'
            })

    def _setModelsFromProjectDict(self):
        """Create the model needed for GUI ..."""
        logging.info("+++++++++++++++++++++++++ setData start") # profiling
        for phase_id, phase_dict in self._project_dict['phases'].items():
            # block model signals
            self._model.blockSignals(True)
            # set list of atoms
            data = []
            for atom_id, atom_dict in phase_dict['atoms'].items():
                data.append({
                    self._label_role: atom_id,
                    self._type_role: atom_dict.getItemByPath(['adp_type', 'store', 'value']),
                    self._uiso_role: atom_dict.getItemByPath(['U_iso_or_equiv', 'store', 'value']),
                    self._u11_role: atom_dict.getItemByPath(['u_11', 'store', 'value']),
                    self._u22_role: atom_dict.getItemByPath(['u_22', 'store', 'value']),
                    self._u33_role: atom_dict.getItemByPath(['u_33', 'store', 'value']),
                    self._u12_role: atom_dict.getItemByPath(['u_12', 'store', 'value']),
                    self._u13_role: atom_dict.getItemByPath(['u_13', 'store', 'value']),
                    self._u23_role: atom_dict.getItemByPath(['u_23', 'store', 'value']),
                    })
            # set model size
            self._model.setColumnCount(1)
            self._model.setRowCount(len(data))
            # set model from data list created above
            for row_index, dict in enumerate(data):
                index = self._model.index(row_index, 0)
                for role, value in dict.items():
                    self._model.setData(index, value, role)
            # unblock signals and emit model layout changed
            self._model.blockSignals(False)
            self._model.layoutChanged.emit()
        logging.info("+++++++++++++++++++++++++ setData end") # profiling
