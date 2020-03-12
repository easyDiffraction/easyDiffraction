__author__ = 'andrewszonov'
__version__ = "2020_03_03"


import logging
from PySide2.QtCore import QObject, Slot
from easyInterface import VERBOSE, Logger
from PyImports.Utils.Helpers import dict2xml


class QtLogger(QObject):
    def __init__(self, logger: Logger, level=None, parent=None):
        super().__init__(parent)
        self.__logger = logger
        self.__initial_level = self.initialLevel(level)
        self.__levels = {
            'levels' : [
                { 'name': 'Disabled', 'code': logging.NOTSET },
                { 'name': 'Verbose',  'code': VERBOSE },
                { 'name': 'Debug',    'code': logging.DEBUG },
                { 'name': 'Info',     'code': logging.INFO },
                { 'name': 'Warning',  'code': logging.WARNING },
                { 'name': 'Error',    'code': logging.ERROR },
                { 'name': 'Critical', 'code': logging.CRITICAL }
            ]
        }

    def initialLevel(self, level):
        """
        Allows to set the initial 'qt logger level (QtLogger)' to be different
        from 'base logger level (Logger)' when creating an object of QtLogger class.
        """
        if level is not None:
            return level
        return self.__logger.logging_level

    @Slot(int)
    def setLevel(self, index: str):
        """
        Set the global logger level

        :param index: Logging level as a string name [Disabled, Verbose, Debug, Info, Warning, Error, Critical]

        """
        level = self.__levels['levels'][index]['code']
        self.__logger.setLevel(level)
        self.__logger.logger.debug('Global debugging level set to: {}'.format(level))

    @Slot(result=str)
    def levelsAsXml(self) -> str:
        """
        Export level lists as an xml string

        :return: XML level string
        """
        xml = dict2xml(self.__levels)
        return xml

    @Slot(result=int)
    def defaultLevelIndex(self):
        """
        Reset the logger to the default level
        """
        for index, level in enumerate(self.__levels['levels']):
            if level['code'] == self.__initial_level:
                return index
        self.__logger.logger.debug('Global debugging has been reset to: {}'.format(self.__initial_level))
        return 0
