import logging

from PySide2.QtCore import Qt, QObject, Signal
from PySide2.QtGui import QStandardItemModel

class BaseModel(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._headers_model = QStandardItemModel()
        self._data_model = QStandardItemModel()
        self._project_dict = None

    def _setModelFromProjectDict(self):
        """ Pure virtual data setter """
        raise NotImplementedError("_setModelFromProjectDict must be implemented in derived class.")

    def onProjectChanged(self):
        """Set headers and data models from project dictionary"""
        self._setModelFromProjectDict()

    def asHeadersModel(self):
        """Return headers model."""
        return self._headers_model

    def asModel(self):
        """Return data model."""
        return self._data_model

    def setCalculator(self, calculator):
        calculator.projectDictChanged.connect(self.onProjectChanged)
        self._calculator = calculator
        self._project_dict = calculator.asDict()
        self._setModelsFromProjectDict()


