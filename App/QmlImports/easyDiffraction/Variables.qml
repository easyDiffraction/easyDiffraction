pragma Singleton
import QtQuick 2.12

QtObject {
    // Resources
    property string resourcesPath: ""

    // Python models
    property bool projectOpened: false
    property var project: projectOpened ? proxy.project : null
    property var cif: projectOpened ? proxy.cif : null
}
