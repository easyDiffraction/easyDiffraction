pragma Singleton
import QtQuick 2.12

QtObject {

    // Python models
    property bool projectOpened: false

    property var project: projectOpened ? proxy.project : null
    property var cif: projectOpened ? proxy.fileStructure : null
    property var phaseCif: projectOpened ? proxy.phaseCif : null
    property var experimentCif: projectOpened ? proxy.experimentCif : null
    property var calculationCif: projectOpened ? proxy.calculationCif : null

    property var measuredData: proxy.measuredData
    property var measuredDataHeaderModel: projectOpened ? proxy.measuredData.asHeadersModel() : null
    property var measuredDataModel: projectOpened ? proxy.measuredData.asModel() : null

    property var calculatedData: proxy.calculatedData
    property var braggPeaks: proxy.braggPeaks

}
