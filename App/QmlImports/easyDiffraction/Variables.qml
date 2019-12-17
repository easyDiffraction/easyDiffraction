pragma Singleton
import QtQuick 2.12

QtObject {

    // Python models
    property bool projectOpened: false
    property var project: projectOpened ? proxy.project : null
    property var cif: projectOpened ? proxy.fileStructure : null
    property var phase_cif: projectOpened ? proxy.phase_cif : null
    property var experiment_cif: projectOpened ? proxy.experiment_cif : null
}
