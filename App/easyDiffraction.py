import os
import sys
import logging

from PySide2.QtCore import QUrl, Qt, QCoreApplication
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine

#import QmlResource

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
logger.disabled = True

if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)

    app.setOrganizationName("easyDiffraction")
    app.setOrganizationDomain("easyDiffraction.org")
    app.setApplicationName("easyDiffraction")

    proxy = Proxy()

#    examples_dir = os.path.join(installationPath(), 'Examples')
    qml_gui_path = os.path.join(current_dir, "Gui.qml")
    imports_path = os.path.join(current_dir, "QmlImports")

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("proxy", proxy)
#    engine.rootContext().setContextProperty("examplesDir", examples_dir)
    engine.addImportPath(imports_path)
    engine.load(qml_gui_path)
    #engine.addImportPath(":/QmlImports")
    #engine.load(":/Gui.qml")

    if engine.rootObjects():
        sys.exit(app.exec_())
