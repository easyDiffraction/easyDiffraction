pragma Singleton
import QtQuick 2.12

QtObject {

    property bool projectOpened: false

    // Main
    property var projectControl: proxyPyQml.projectControl ? proxyPyQml.projectControl : ""
    property var projectManager: proxyPyQml.projectManager ? proxyPyQml.projectManager : ""
    property var projectDict: projectOpened ? proxyPyQml.projectDict : null
    property var cif: projectOpened ? proxyPyQml.fileStructure : null
    property var phaseCif: projectOpened ? proxyPyQml.phaseCif : null
    property var experimentCif: projectOpened ? proxyPyQml.experimentCif : null
    property var calculationCif: projectOpened ? proxyPyQml.calculationCif : null
    property var needToSave: projectOpened ? proxyPyQml.needToSave : false

    // Measured and calculated data
    property var measuredData: proxyPyQml.measuredData
    property var measuredDataHeaderModel: projectOpened ? proxyPyQml.measuredData.asHeadersModel() : null
    property var measuredDataModel: projectOpened ? proxyPyQml.measuredData.asModel() : null
    property var calculatedData: proxyPyQml.calculatedData
    property var braggPeaks: proxyPyQml.braggPeaks

    // Models
    property var fitables: projectOpened ? proxyPyQml.fitables : null
    property var cellParameters: projectOpened ? proxyPyQml.cellParameters : null
    property var cellBox: projectOpened ? proxyPyQml.cellBox : null
    property var atomSites: projectOpened ? proxyPyQml.atomSites : null
    property var atomAdps: projectOpened ? proxyPyQml.atomAdps : null
    property var atomMsps: projectOpened ? proxyPyQml.atomMsps : null
    property var statusInfo: projectOpened ? proxyPyQml.statusInfo : null

    // Refinement
    property var refinementRunning: proxyPyQml.refinementRunning
    property var refinementDone: proxyPyQml.refinementDone
    property var refinementResult: proxyPyQml.refinementResult

    // Undo-Redo
    property var calculatorInterface: projectOpened ? proxyPyQml.calculatorInterface : null
    property var undoText: calculatorInterface ? proxyPyQml.undoText : ""
    property var redoText: calculatorInterface ? proxyPyQml.redoText : ""
    property var canUndo: calculatorInterface ? proxyPyQml.canUndo : false
    property var canRedo: calculatorInterface ? proxyPyQml.canRedo : false

}
