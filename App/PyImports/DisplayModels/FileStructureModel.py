from easyInterface import logger

from PySide2.QtCore import Qt, QObject, Signal
from PySide2.QtGui import QStandardItemModel, QStandardItem

from PyImports.DisplayModels.BaseModel import BaseModel

class FileStructureModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        # set roles
        self._phase_role = Qt.UserRole + 1
        self._experiment_role = Qt.UserRole + 2
        self._calculation_role = Qt.UserRole + 3
        self._model.setItemRoleNames({
            self._phase_role: b'phasesRole',
            self._experiment_role: b'experimentsRole',
            self._calculation_role: b'calculationsRole',
            })
        self._log = logger.getLogger(self.__class__.__module__)

    def asPhaseString(self):
        """
        Returns the content of the phase data as string
        """
        content = ""
        if self._model.rowCount() > 0:
            content = str(self._model.item(0).data(role=self._phase_role))
        return content

    def asExperimentString(self):
        """
        Returns the content of the experiment data as string
        """
        content = ""
        if self._model.rowCount() > 0:
            content = str(self._model.item(0).data(role=self._experiment_role))
        return content

    def asCalculationString(self):
        """
        Returns the content of the calculation data as string
        """
        content = ""
        if self._model.rowCount() > 0:
            content = str(self._model.item(0).data(role=self._calculation_role))
        return content

    def _setModelsFromProjectDict(self):
        """
        Create the model needed for GUI representation of structure.
        """

        cif_dict = self._calculator_interface.asCifDict()
        # Important - clear the model, so subsequent calls deal with empty
        self._model.clear()

        self._model.blockSignals(True)
        self._headers_model.blockSignals(True)

        phases_cif = cif_dict['phases']
        exp_cif = cif_dict['experiments']
        calc_cif = cif_dict['calculations']

        # Currently only one phase/experiment, so assigning
        # explicitly. With more components, we need a proper loop
        # as shown below
        item = QStandardItem()
        item.setData(phases_cif, self._phase_role)
        item.setData(exp_cif, self._experiment_role)
        item.setData(calc_cif, self._calculation_role)
        self._model.appendRow(item)

        #for data_str cif_dict.items():
        #    item = QStandardItem()
        #    item.setData(phases_cif, <self._some_role>)
        #    self._model.appendRow(item)

        self._model.blockSignals(False)
        self._headers_model.blockSignals(False)
        self._model.layoutChanged.emit()
        self._headers_model.layoutChanged.emit()

