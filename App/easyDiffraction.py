import os
import sys
import argparse

from PySide2.QtCore import QUrl
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine

from PyImports.ProxyPyQml import ProxyPyQml
from easyInterface import logger, logging
from PyImports.Utils.QtLogging import QtLogger

defaultDebugLevel = logging.WARNING

if __name__ == '__main__':

    description = 'easyDiffraction is a scientific software for modelling and analysis of the neutron diffraction data.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--debug", "-d", help="set the debugging level, 10=DEBUG, 20=INFO, 30=WARNING")
    args = parser.parse_args()

    # Global logging settings
    if args.debug:
        try:
            logger.setLevel(int(args.debug))
        except ValueError:
            logger.setLevel(defaultDebugLevel)
            logger.logger.warning('Debug level %s could no be parsed. Setting to WARNING (30)', args.debug)
    else:
        logger.setLevel(defaultDebugLevel)
    logger.addSysOutput()
    # logger.addNameBlacklistFilter('easyInterface.Diffraction.Calculators', 'easyInterface.Diffraction.DataClasses')
    # logger.addNameFilter('easyDiffraction')
    # logging.getLogger().addFilter(logging.Filter(name='easyInterface'))
    logger_py_qml = QtLogger(logger, level=defaultDebugLevel)

    # The following way to enable HighDpi support doesn't work.
    # Add 'NSHighResolutionCapable = YES' to 'easyDiffraction.app/Contents/Info.plist'
    # using python script 'FreezeApp.py' after PyInstaller
    #QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    #QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Set paths
    current_dir_path = os.path.dirname(sys.argv[0])
    installation_path = current_dir_path
    if sys.platform.startswith('win'):
        installation_path = os.path.realpath(os.path.join(current_dir_path, '..'))
    elif sys.platform.startswith('darwin'):
        installation_path = os.path.realpath(os.path.join(current_dir_path, '..', '..', '..'))

    window_icon_path = os.path.join(current_dir_path, 'QmlImports', 'easyDiffraction', 'Resources', 'Icons', 'LogoWithPaddings.png')
    qml_gui_file_path = os.path.join(current_dir_path, "Gui.qml")
    release_config_file_path = os.path.join(current_dir_path, "Release.yml")
    qml_imports_dir_url = str(QUrl.fromLocalFile(os.path.join(current_dir_path, "QmlImports")).toString())
    qml_imports_dir_path = os.path.abspath(os.path.join(current_dir_path, "QmlImports"))
    examples_dir_url = str(QUrl.fromLocalFile(os.path.join(installation_path, 'Examples')).toString())
    examples_rc_dir_url = str(QUrl.fromLocalFile(os.path.join(current_dir_path, "Resources", "Examples")).toString())
    examples_rc_dir_path = os.path.abspath(os.path.join(current_dir_path, "Resources", "Examples"))
    #print("examples_rc_dir_url", examples_rc_dir_url)
    #print("examples_rc_dir_path", examples_rc_dir_path)

    # Create an application
    app = QApplication(sys.argv)

    app.setOrganizationName("easyDiffraction")
    app.setOrganizationDomain("easyDiffraction.org")
    app.setApplicationName("easyDiffraction")
    app.setWindowIcon(QIcon(window_icon_path))

    # Create a proxy object between python logic and QML GUI
    proxy_py_qml_obj = ProxyPyQml(release_config_file_path)

    # Create GUI from QML
    engine = QQmlApplicationEngine()

    engine.rootContext().setContextProperty("_loggerPyQml", logger_py_qml)
    engine.rootContext().setContextProperty("proxyPyQmlObj", proxy_py_qml_obj)
    engine.rootContext().setContextProperty("examplesDirUrl", examples_dir_url)
    engine.rootContext().setContextProperty("examplesRcDirUrl", examples_rc_dir_url)
    engine.rootContext().setContextProperty("examplesRcDirPath", examples_rc_dir_path)
    engine.rootContext().setContextProperty("qmlImportsDirUrl", qml_imports_dir_url)
    engine.rootContext().setContextProperty("qmlImportsDirPath", qml_imports_dir_path)

    engine.addImportPath(qml_imports_dir_url)
    engine.load(qml_gui_file_path)
    #engine.addImportPath(":/QmlImports")
    #engine.load(":/Gui.qml")

    if engine.rootObjects():
        sys.exit(app.exec_())
