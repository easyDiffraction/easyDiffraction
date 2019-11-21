import logging

from PySide2.QtCore import Qt, QObject, Signal, Slot, Property
from PySide2.QtGui import QStandardItem, QStandardItemModel

class CellBoxModel(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._project_dict = None
        self._model = QStandardItemModel()
        # set roles
        self._x_role, self._y_role, self._z_role = [ Qt.UserRole + 1 + i for i in range(3) ]
        self._model.setItemRoleNames({ self._x_role: b'xPos', self._y_role: b'yPos', self._z_role: b'zPos' })

    def _setModelFromProject(self):
        """Create the model needed for GUI structure chart (unit cell box)."""
        logging.info("+++++++++++++++++++++++++ setData start") # profiling
        for phase_id, phase_dict in self._project_dict['phases'].items():
            # block model signals
            self._model.blockSignals(True)
            # get lattice parameters
            a = phase_dict['cell']['length_a']['value']
            b = phase_dict['cell']['length_b']['value']
            c = phase_dict['cell']['length_c']['value']
            # get number of dots along different axes
            dots_per_angstrom = 30
            dots_along_a = int(a * dots_per_angstrom)
            dots_along_b = int(b * dots_per_angstrom)
            dots_along_c = int(c * dots_per_angstrom)
            # set data array for different axes
            data = []
            for i in range(dots_along_a):
                data.append({ self._x_role: i * a / dots_along_a, self._y_role: 0, self._z_role: 0 })
                data.append({ self._x_role: i * a / dots_along_a, self._y_role: b, self._z_role: 0 })
                data.append({ self._x_role: i * a / dots_along_a, self._y_role: 0, self._z_role: c })
                data.append({ self._x_role: i * a / dots_along_a, self._y_role: b, self._z_role: c })
            for i in range(dots_along_b):
                data.append({ self._x_role: 0, self._y_role: i * b / dots_along_b, self._z_role: 0 })
                data.append({ self._x_role: a, self._y_role: i * b / dots_along_b, self._z_role: 0 })
                data.append({ self._x_role: 0, self._y_role: i * b / dots_along_b, self._z_role: c })
                data.append({ self._x_role: a, self._y_role: i * b / dots_along_b, self._z_role: c })
            for i in range(dots_along_c):
                data.append({ self._x_role: 0, self._y_role: 0, self._z_role: i * c / dots_along_c })
                data.append({ self._x_role: a, self._y_role: 0, self._z_role: i * c / dots_along_c })
                data.append({ self._x_role: 0, self._y_role: b, self._z_role: i * c / dots_along_c })
                data.append({ self._x_role: a, self._y_role: b, self._z_role: i * c / dots_along_c })
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
        logging.info("+++++++++++++++++++++++++ setData end") # profiling

    def onProjectChanged(self):
        """Define what to do if project dict is changed, e.g. by external library object."""
        self._setModelFromProject()

    def asModel(self):
        """Return model."""
        return self._model

    def setCalculator(self, calculator):
        calculator.projectDictChanged.connect(self.onProjectChanged)
        self._project_dict = calculator.asDict()
        self._setModelFromProject()
