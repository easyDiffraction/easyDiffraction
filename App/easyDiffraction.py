import os
import sys
import logging

from PySide2.QtCore import QUrl, Qt, QCoreApplication
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine

from PyImports.Proxy import Proxy

if __name__ == '__main__':
    # Global logging settings
    logging.basicConfig(level=logging.INFO, format="\033[1;32;49m%(asctime)s  |  %(lineno)-4d %(filename)-30s  |  %(funcName)-35s  |  %(message)s\033[0m")
    logging.getLogger().disabled = False

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
    qml_imports_dir_path = str(QUrl.fromLocalFile(os.path.join(current_dir_path, "QmlImports")).toString())
    examples_dir_path = str(QUrl.fromLocalFile(os.path.join(installation_path, 'Examples')).toString())

    # Create an application
    app = QApplication(sys.argv)

    app.setOrganizationName("easyDiffraction")
    app.setOrganizationDomain("easyDiffraction.org")
    app.setApplicationName("easyDiffraction")
    app.setWindowIcon(QIcon(window_icon_path))

    # Create a proxy object between python logic and QML GUI
    py_qml_proxy = Proxy()

    # Create GUI from QML
    engine = QQmlApplicationEngine()

    engine.rootContext().setContextProperty("pyQmlProxy", py_qml_proxy)
    engine.rootContext().setContextProperty("examplesDir", examples_dir_path)
    engine.rootContext().setContextProperty("qmlImportsDir", qml_imports_dir_path)

    engine.addImportPath(qml_imports_dir_path)
    engine.load(qml_gui_file_path)
    #engine.addImportPath(":/QmlImports")
    #engine.load(":/Gui.qml")

    if engine.rootObjects():
        sys.exit(app.exec_())
