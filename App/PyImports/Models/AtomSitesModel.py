from PySide2.QtCore import Qt, QObject, Signal, Slot, Property
from PySide2.QtGui import QStandardItem, QStandardItemModel

import logging
logging.basicConfig(format="%(asctime)-15s [%(levelname)s] %(filename)s %(funcName)s [%(lineno)d]: %(message)s", level=logging.INFO)

class AtomSitesModel(QObject):
    def __init__(self, calculator, parent=None):
        super().__init__(parent)
        calculator.projectDictChanged.connect(self.onProjectChanged)
        self._project_dict = calculator.asDict()
        self._model = QStandardItemModel()
        # set roles
        self._label_role = Qt.UserRole + 1
        self._atom_role = Qt.UserRole + 2
        self._color_role = Qt.UserRole + 3
        self._x_role = Qt.UserRole + 4
        self._y_role = Qt.UserRole + 5
        self._z_role = Qt.UserRole + 6
        self._occupancy_role = Qt.UserRole + 7
        self._model.setItemRoleNames({
            self._label_role: b'label',
            self._atom_role: b'atom',
            self._color_role: b'colorStr',
            self._x_role: b'xPos',
            self._y_role: b'yPos',
            self._z_role: b'zPos',
            self._occupancy_role: b'occupancy'
            })
        # set model
        self._setModelFromProject()

    def _setModelFromProject(self):
        """Create the model needed for GUI ..."""
        logging.info("+++++++++++++++++++++++++ setData start") # profiling
        for phase_id, phase_dict in self._project_dict['phases'].items():
            # block model signals
            self._model.blockSignals(True)
            # set list of atoms
            data = []
            for atom_id, atom_dict in phase_dict['atom_site'].items():
                label = atom_id
                atom = atom_dict['type_symbol']['value']
                color = atom_dict['scat_length_neutron']['value']
                x = atom_dict['fract_x']['value']
                y = atom_dict['fract_x']['value']
                z = atom_dict['fract_x']['value']
                occupancy = atom_dict['occupancy']['value']
                data.append({
                    self._label_role: label,
                    self._atom_role: atom,
                    self._color_role: color,
                    self._x_role: x,
                    self._y_role: y,
                    self._z_role: z,
                    self._occupancy_role: occupancy
                    })
            # set model size
            self._model.setColumnCount(1)
            self._model.setRowCount(len(data))
            # set model from data array created above
            for row_index, dict in enumerate(data):
                index = self._model.index(row_index, 0)
                for role, value in dict.items():
                    self._model.setData(index, value, role)
                    #print(index)
            # unblock signals and emit model layout changed
            self._model.blockSignals(False)
            self._model.layoutChanged.emit()
        logging.info("+++++++++++++++++++++++++ setData end") # profiling

    modelChanged = Signal()

    def onProjectChanged(self):
        """Define what to do if project dict is changed, e.g. by external library object."""
        self._setModelFromProject()
        self.modelChanged.emit()

    def asModel(self):
        """Return model."""
        return self._model
