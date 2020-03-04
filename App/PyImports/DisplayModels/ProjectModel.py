import pprint
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

from PySide2.QtCore import QObject, Slot

from easyInterface import logger


class ProjectModel(QObject):
    """
    ...
    """

    def __init__(self, parent=None):
        """
        ...
        """
        super().__init__(parent)
        self._calculator_interface = None
        self._project_dict = None
        self._log = logger.getLogger(__class__.__module__)

    def setCalculatorInterface(self, calculator_interface):
        """
        ...
        """
        calculator_interface.projectDictChanged.connect(self.onProjectChanged)
        self._calculator_interface = calculator_interface
        self._project_dict = calculator_interface.project_dict
        self.onProjectChanged()

    def onProjectChanged(self):
        """
        ...
        """
        self._log.debug("project is changed!")
        self._log.debug("project as dict:")
        self._log.debug(pprint.pformat(self._project_dict['experiments']['pd']['wavelength'], indent=2, width=200))
        #self._log.debug("project as xml:")
        #self._log.debug(parseString(self.projectDictAsXml()).toprettyxml())

    @Slot(result='QVariant')
    def asDictVariant(self):
        """
        ...
        """
        return self._project_dict.asDict()

    @Slot(result=str)
    def asXmlString(self):
        """
        ...
        """
        xml = dicttoxml(self._project_dict, attr_type=False)
        xml = xml.decode()
        return xml

    @Slot(str, str, float)
    def updateProject(self, path, name, value):
        """
        ...
        """
        self._log.debug(f"{path}, {name}, {value}")
        undo_redo_text = f"Changing '{name}' refine state to '{value}'"
        self._calculator_interface.project_dict.startBulkUpdate(undo_redo_text)
        self._calculator_interface.canUndoOrRedoChanged.emit()
        #self._calculator_interface.setPhaseValue(keys_list[1], keys_list[2:-2], value)
        self._calculator_interface.updateCalculations() # phases also updated ?
        self._calculator_interface.project_dict.endBulkUpdate()
        self._calculator_interface.canUndoOrRedoChanged.emit()

