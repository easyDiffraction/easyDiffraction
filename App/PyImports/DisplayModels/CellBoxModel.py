from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItemModel
from easyInterface import logger

from PyImports.DisplayModels.BaseModel import BaseModel


class CellBoxModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._project_dict = None
        self._model = QStandardItemModel()
        # set roles
        self._x_role, self._y_role, self._z_role = [Qt.UserRole + 1 + i for i in range(3)]
        self._model.setItemRoleNames({self._x_role: b'xPos', self._y_role: b'yPos', self._z_role: b'zPos'})
        self._log = logger.getLogger(self.__class__.__module__)

    def _setModelsFromProjectDict(self):
        """Create the model needed for GUI structure chart (unit cell box)."""
        self._log.info("Starting to set Model from Project Dict")
        for phase_id, phase_dict in self._project_dict['phases'].items():
            # block model signals
            self._model.blockSignals(True)
            # get lattice parameters
            a = phase_dict.getItemByPath(['cell', 'length_a']).value
            b = phase_dict.getItemByPath(['cell', 'length_b']).value
            c = phase_dict.getItemByPath(['cell', 'length_c']).value
            # get number of dots along different axes
            dots_per_angstrom = 30
            dots_along_a = int(a * dots_per_angstrom)
            dots_along_b = int(b * dots_per_angstrom)
            dots_along_c = int(c * dots_per_angstrom)
            # set data array for different axes
            data = []
            for i in range(dots_along_a):
                data.append({self._x_role: i * a / dots_along_a, self._y_role: 0, self._z_role: 0})
                data.append({self._x_role: i * a / dots_along_a, self._y_role: b, self._z_role: 0})
                data.append({self._x_role: i * a / dots_along_a, self._y_role: 0, self._z_role: c})
                data.append({self._x_role: i * a / dots_along_a, self._y_role: b, self._z_role: c})
            for i in range(dots_along_b):
                data.append({self._x_role: 0, self._y_role: i * b / dots_along_b, self._z_role: 0})
                data.append({self._x_role: a, self._y_role: i * b / dots_along_b, self._z_role: 0})
                data.append({self._x_role: 0, self._y_role: i * b / dots_along_b, self._z_role: c})
                data.append({self._x_role: a, self._y_role: i * b / dots_along_b, self._z_role: c})
            for i in range(dots_along_c):
                data.append({self._x_role: 0, self._y_role: 0, self._z_role: i * c / dots_along_c})
                data.append({self._x_role: a, self._y_role: 0, self._z_role: i * c / dots_along_c})
                data.append({self._x_role: 0, self._y_role: b, self._z_role: i * c / dots_along_c})
                data.append({self._x_role: a, self._y_role: b, self._z_role: i * c / dots_along_c})
            # set model size
            self._model.setColumnCount(1)
            self._model.setRowCount(len(data))
            # set model from data array created above
            for row_index, dict in enumerate(data):
                index = self._model.index(row_index, 0)
                for role, value in dict.items():
                    self._model.setData(index, value, role)
            # unblock signals and emit model layout changed
            self._model.blockSignals(False)
            self._model.layoutChanged.emit()
        self._log.info("Finished setting Model from Project Dict")
