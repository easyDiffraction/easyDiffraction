__author__ = 'andrewszonov'
__version__ = "2020_03_03"


from dicttoxml import dicttoxml
from easyInterface import VERBOSE, Logger
from PySide2.QtCore import QObject, Slot


class QtLogger(QObject):
    def __init__(self, logger: Logger, parent=None):
        super().__init__(parent)
        self.__logger = logger
        self.__initial_level = logger.logging_level
        self.__levels = [
            { 'level': { 'name': 'Disabled', 'code': 0  } },
            {'level':  {'name':  'Verbose',  'code': VERBOSE}},
            { 'level': { 'name': 'Debug',    'code': 10 } },
            { 'level': { 'name': 'Info',     'code': 20 } },
            { 'level': { 'name': 'Warning',  'code': 30 } },
            { 'level': { 'name': 'Error',    'code': 40 } },
            { 'level': { 'name': 'Critical', 'code': 50 } }
        ]

    @Slot(int)
    def setLevel(self, index: str):
        """
        Set the global logger level

        :param index: Logging level as a string name [Disabled, Verbose, Debug, Info, Warning, Error, Critical]

        """
        level = self.__levels[index]['level']['code']
        self.__logger.setLevel(level)
        self.__logger.logger.debug('Global debugging level set to: {}'.format(level))

    @Slot(result=str)
    def levelsAsXml(self) -> str:
        """
        Export level lists as an xml string

        :return: XML level string
        """
        xml = dicttoxml(self.__levels, attr_type=False)
        xml = xml.decode()
        return xml

    @Slot(result=int)
    def defaultLevelIndex(self):
        """
        Reset the logger to the default level 
        """
        for index, level in enumerate(self.__levels):
            if level['level']['code'] == self.__initial_level:
                return index
        self.__logger.logger.debug('Global debugging has been reset to: {}'.format(self.__initial_level))
        return 0