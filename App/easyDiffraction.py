import os
import sys

from PySide2.QtCore import QUrl, Qt, QCoreApplication
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine

import RhoChiQml

if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    app.setOrganizationName("easyDiffraction")
    app.setOrganizationDomain("easyDiffraction.org")
    app.setApplicationName("easyDiffraction")

    proxy = RhoChiQml.Proxy()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("proxy", proxy)

    engine.addImportPath(os.path.join(os.path.dirname(sys.argv[0]), "Imports"))
    engine.load(QUrl.fromLocalFile(os.path.join(os.path.dirname(sys.argv[0]), "Gui.qml")))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
