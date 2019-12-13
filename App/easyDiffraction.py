import os
import sys
import logging

from PySide2.QtCore import QUrl, Qt, QCoreApplication
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine

from PyImports.Proxy import Proxy

current_dir = os.path.dirname(sys.argv[0])

def installationPath():
    if sys.platform.startswith('win'):
        return os.path.realpath(os.path.join(current_dir, '..'))
    elif sys.platform.startswith('darwin'):
        return os.path.realpath(os.path.join(current_dir, '..', '..', '..'))
    return os.path.join(current_dir)

def logFilePath(log_name):
    return os.path.join(installationPath(), log_name)

logging.basicConfig(
    format = "%(asctime)-15s [%(levelname)s] %(filename)s %(funcName)s [%(lineno)d]: %(message)s",
    level = logging.INFO,
    #filename = logFilePath('easyDiffraction.log'),
    #filemode = 'w'
    )
logger = logging.getLogger()
logger.disabled = True # App crashes on Windows if log to file is enabled. Permissions?

if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)

    app.setOrganizationName("easyDiffraction")
    app.setOrganizationDomain("easyDiffraction.org")
    app.setApplicationName("easyDiffraction")
    app.setWindowIcon(QIcon(os.path.join(current_dir, 'QmlImports', 'easyDiffraction', 'Resources', 'Icons', 'LogoWithPaddings.png')))

    proxy = Proxy()

    examples_dir_path = str(QUrl.fromLocalFile(os.path.join(installationPath(), 'Examples')).toString())
    qml_imports_dir_path = str(QUrl.fromLocalFile(os.path.join(current_dir, "QmlImports")).toString())
    qnl_gui_file_path = os.path.join(current_dir, "Gui.qml")

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("proxy", proxy)
    engine.rootContext().setContextProperty("projectControl", proxy.project_control)
    engine.rootContext().setContextProperty("projectManager", proxy.project_control.manager)
    engine.rootContext().setContextProperty("examplesDir", examples_dir_path)
    engine.rootContext().setContextProperty("qmlImportsDir", qml_imports_dir_path)

    engine.addImportPath(qml_imports_dir_path)
    engine.load(qnl_gui_file_path)
    #engine.addImportPath(":/QmlImports")
    #engine.load(":/Gui.qml")

    if engine.rootObjects():
        sys.exit(app.exec_())
