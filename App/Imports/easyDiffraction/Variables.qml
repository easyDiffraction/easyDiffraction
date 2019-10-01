pragma Singleton
import QtQuick 2.12

QtObject {
    // Resources
    property string resourcesPath: ""

    // Python models
    property var project: proxy.project
    property var cif: proxy.cif
}
