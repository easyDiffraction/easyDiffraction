pragma Singleton
import QtQuick 2.12

QtObject {

    // Python models
    property bool projectOpened: false
    property var project: projectOpened ? proxy.project : null
    property var cif: projectOpened ? proxy.fileStructure : null
    property var cif_text: projectOpened ? proxy.cif_text : null
}
