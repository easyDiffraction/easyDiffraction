pragma Singleton
import QtQuick 2.12

QtObject {

    property bool projectOpened: false

    // Main
    property var projectControl: proxyPyQmlObj.projectControl ? proxyPyQmlObj.projectControl : ""
    property var projectManager: proxyPyQmlObj.projectManager ? proxyPyQmlObj.projectManager : ""
    property var projectDict: projectOpened ? proxyPyQmlObj.projectDict : null
    property var cif: projectOpened ? proxyPyQmlObj.fileStructure : null
    property var phaseCif: projectOpened ? proxyPyQmlObj.phaseCif : null
    property var experimentCif: projectOpened ? proxyPyQmlObj.experimentCif : null
    property var calculationCif: projectOpened ? proxyPyQmlObj.calculationCif : null
    property var needToSave: projectOpened ? proxyPyQmlObj.needToSave : false
    property var projectFilePathSelected: proxyPyQmlObj.projectFilePathSelected

    // Measured and calculated data
    property var measuredData: proxyPyQmlObj.measuredData
    property var measuredDataHeaderModel: projectOpened ? proxyPyQmlObj.measuredData.asHeadersModel() : null
    property var measuredDataModel: projectOpened ? proxyPyQmlObj.measuredData.asModel() : null
    property var calculatedData: proxyPyQmlObj.calculatedData
    property var braggPeaks: proxyPyQmlObj.braggPeaks

    // Models
    property var fitables: projectOpened ? proxyPyQmlObj.fitables : null
    property var cellParameters: projectOpened ? proxyPyQmlObj.cellParameters : null
    property var cellBox: projectOpened ? proxyPyQmlObj.cellBox : null
    property var atomSites: projectOpened ? proxyPyQmlObj.atomSites : null
    property var atomAdps: projectOpened ? proxyPyQmlObj.atomAdps : null
    property var atomMsps: projectOpened ? proxyPyQmlObj.atomMsps : null
    property var statusInfo: projectOpened ? proxyPyQmlObj.statusInfo : null

    // Refinement
    property var refinementRunning: proxyPyQmlObj.refinementRunning
    property var refinementDone: proxyPyQmlObj.refinementDone
    property var refinementResult: proxyPyQmlObj.refinementResult

    // Undo-Redo
    property var calculatorInterface: projectOpened ? proxyPyQmlObj.calculatorInterface : null
    property var undoText: calculatorInterface ? proxyPyQmlObj.undoText : ""
    property var redoText: calculatorInterface ? proxyPyQmlObj.redoText : ""
    property var canUndo: calculatorInterface ? proxyPyQmlObj.canUndo : false
    property var canRedo: calculatorInterface ? proxyPyQmlObj.canRedo : false

}
