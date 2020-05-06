from easyInterface import logger

from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItemModel

from PyImports.DisplayModels.BaseModel import BaseModel


class CellParametersModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._project_dict = None
        self._model = QStandardItemModel()
        # set roles
        self._a_role, self._b_role, self._c_role, self._alpha_role, self._beta_role, self._gamma_role = [
            Qt.UserRole + 1 + i for i in range(6)]
        self._model.setItemRoleNames({
            self._a_role: b'length_a',
            self._b_role: b'length_b',
            self._c_role: b'length_c',
            self._alpha_role: b'angle_alpha',
            self._beta_role: b'angle_beta',
            self._gamma_role: b'angle_gamma'
        })
        self._log = logger.getLogger(self.__class__.__module__)

    def _setModelsFromProjectDict(self):
        """Create the model needed for GUI ..."""
        self._log.info("Starting to set Model from Project Dict")
        for phase_id, phase_dict in self._project_dict['phases'].items():
            # block model signals
            self._model.blockSignals(True)
            # set helper data list
            data = [{
                self._a_role: phase_dict.getItemByPath(['cell', 'length_a']).value,
                self._b_role: phase_dict.getItemByPath(['cell', 'length_b']).value,
                self._c_role: phase_dict.getItemByPath(['cell', 'length_c']).value,
                self._alpha_role: phase_dict.getItemByPath(['cell', 'angle_alpha']).value,
                self._beta_role: phase_dict.getItemByPath(['cell', 'angle_beta']).value,
                self._gamma_role: phase_dict.getItemByPath(['cell', 'angle_gamma']).value,
            }]
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
        self._log.info("Finished setting Model from Project Dict")
