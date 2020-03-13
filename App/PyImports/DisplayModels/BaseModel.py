from PySide2.QtCore import Qt, QObject, Signal, Slot
from PySide2.QtGui import QStandardItemModel


class BaseModel(QObject):
    """
    ...
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._headers_model = QStandardItemModel()
        self._model = QStandardItemModel()
        self._calculator_interface = None
        self._project_dict = None
        self._log = None

    def _setModelsFromProjectDict(self):
        """
        Pure virtual data setter
        """
        raise NotImplementedError("_setModelFromProjectDict must be implemented in derived class.")

    def onProjectChanged(self):
        """
        Set headers and data models from project dictionary
        """
        self._log.debug("project changed")
        self._setModelsFromProjectDict()

    def setCalculatorInterface(self, calculator_interface):
        """
        ...
        """
        calculator_interface.projectDictChanged.connect(self.onProjectChanged)
        self._calculator_interface = calculator_interface
        self._project_dict = calculator_interface.project_dict
        self._setModelsFromProjectDict()

    @Slot(result='QVariant')
    def asHeadersModel(self):
        """
        Return headers model.
        """
        return self._headers_model

    @Slot(result='QVariant')
    def asModel(self):
        """
        Return data model.
        """
        return self._model
