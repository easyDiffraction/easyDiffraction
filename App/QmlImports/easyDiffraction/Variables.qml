pragma Singleton
import QtQuick 2.12

QtObject {

    // Python models
    property bool projectOpened: false

    property var calculatorInterface: projectOpened ? proxy.calculatorInterface : null
    property var undoText: calculatorInterface ? proxy.undoText : ""
    property var redoText: calculatorInterface ? proxy.redoText : ""
    property var canUndo: calculatorInterface ? proxy.canUndo : false
    property var canRedo: calculatorInterface ? proxy.canRedo : false

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
