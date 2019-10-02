import os
import sys

from PySide2.QtCore import QUrl, Qt, QCoreApplication
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine

#import QmlResource

from PyImports.Proxy import *

if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)

    app.setOrganizationName("easyDiffraction")
    app.setOrganizationDomain("easyDiffraction.org")
    app.setApplicationName("easyDiffraction")

    engine = QQmlApplicationEngine()

    proxy = Proxy()
    engine.rootContext().setContextProperty("proxy", proxy)

    current_dir = os.path.dirname(sys.argv[0])
    qml_gui_path = os.path.join(current_dir, "Gui.qml")
    imports_path = os.path.join(current_dir, "QmlImports")

    engine.addImportPath(imports_path)
    engine.load(qml_gui_path)

    #engine.addImportPath(":/QmlImports")
    #engine.load(":/Gui.qml")

    if engine.rootObjects():
        sys.exit(app.exec_())
