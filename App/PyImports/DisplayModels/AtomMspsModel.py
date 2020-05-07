from easyInterface import logger

from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItemModel

from PyImports.DisplayModels.BaseModel import BaseModel


class AtomMspsModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._project_dict = None
        self._model = QStandardItemModel()
        # set roles
        self._label_role = Qt.UserRole + 1
        self._type_role = Qt.UserRole + 2
        self._chiiso_role = Qt.UserRole + 3
        self._chi11_role = Qt.UserRole + 4
        self._chi22_role = Qt.UserRole + 5
        self._chi33_role = Qt.UserRole + 6
        self._chi12_role = Qt.UserRole + 7
        self._chi13_role = Qt.UserRole + 8
        self._chi23_role = Qt.UserRole + 9
        self._model.setItemRoleNames({
            self._label_role: b'label',
            self._type_role: b'type',
            self._chiiso_role: b'chiiso',
            self._chi11_role: b'chi11',
            self._chi22_role: b'chi22',
            self._chi33_role: b'chi33',
            self._chi12_role: b'chi12',
            self._chi13_role: b'chi13',
            self._chi23_role: b'chi23'
        })
        self._log = logger.getLogger(self.__class__.__module__)

    def _setModelsFromProjectDict(self):
        """Create the model needed for GUI ..."""
        self._log.info("Starting to set Model from Project Dict")
        for phase_id, phase_dict in self._project_dict['phases'].items():
            # block model signals
            self._model.blockSignals(True)
            # set list of atoms
            data = []
            for atom_id, atom_dict in phase_dict['atoms'].items():
                data.append({
                    self._label_role: atom_id,
                    self._type_role: atom_dict.getItemByPath(['MSP', 'type']).value,
                    self._chiiso_role: "",
                    self._chi11_role: atom_dict.getItemByPath(['MSP', 'chi_11']).value,
                    self._chi22_role: atom_dict.getItemByPath(['MSP', 'chi_22']).value,
                    self._chi33_role: atom_dict.getItemByPath(['MSP', 'chi_33']).value,
                    self._chi12_role: atom_dict.getItemByPath(['MSP', 'chi_12']).value,
                    self._chi13_role: atom_dict.getItemByPath(['MSP', 'chi_13']).value,
                    self._chi23_role: atom_dict.getItemByPath(['MSP', 'chi_23']).value,
                })
            # set model size
            self._model.setColumnCount(1)
            self._model.setRowCount(len(data))
            # set model from data list created above
            for row_index, dict_value in enumerate(data):
                index = self._model.index(row_index, 0)
                for role, value in dict_value.items():
                    self._model.setData(index, value, role)
            # unblock signals and emit model layout changed
            self._model.blockSignals(False)
            self._model.layoutChanged.emit()
        self._log.info("Finished setting Model from Project Dict")
