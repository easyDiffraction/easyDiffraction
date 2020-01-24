pragma Singleton
import QtQuick 2.12

QtObject {

    // Python models
    property bool projectOpened: false
    property var project: projectOpened ? proxy.project : null
    property var cif: projectOpened ? proxy.fileStructure : null
    property var phase_cif: projectOpened ? proxy.phase_cif : null
    property var measured_data: projectOpened ? proxy.measuredData.asModel() : null
    property var measured_data_header: projectOpened ? proxy.measuredData.asHeadersModel() : null
    property var experiment_cif: projectOpened ? proxy.experiment_cif : null
    property var calculation_cif: projectOpened ? proxy.calculation_cif : null
}
