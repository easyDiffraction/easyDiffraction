pragma Singleton
import QtQuick 2.12

QtObject {

    property bool projectOpened: false

    // Main
    property var projectControl: pyQmlProxy.projectControl ? pyQmlProxy.projectControl : ""
    property var projectManager: pyQmlProxy.projectManager ? pyQmlProxy.projectManager : ""
    property var project: projectOpened ? pyQmlProxy.project : null
    property var cif: projectOpened ? pyQmlProxy.fileStructure : null
    property var phaseCif: projectOpened ? pyQmlProxy.phaseCif : null
    property var experimentCif: projectOpened ? pyQmlProxy.experimentCif : null
    property var calculationCif: projectOpened ? pyQmlProxy.calculationCif : null
    property var needToSave: projectOpened ? pyQmlProxy.needToSave : false

    // Measured and calculated data
    property var measuredData: pyQmlProxy.measuredData
    property var measuredDataHeaderModel: projectOpened ? pyQmlProxy.measuredData.asHeadersModel() : null
    property var measuredDataModel: projectOpened ? pyQmlProxy.measuredData.asModel() : null
    property var calculatedData: pyQmlProxy.calculatedData
    property var braggPeaks: pyQmlProxy.braggPeaks

    // Models
    property var fitables: projectOpened ? pyQmlProxy.fitables : null
    property var cellParameters: projectOpened ? pyQmlProxy.cellParameters : null
    property var cellBox: projectOpened ? pyQmlProxy.cellBox : null
    property var atomSites: projectOpened ? pyQmlProxy.atomSites : null
    property var atomAdps: projectOpened ? pyQmlProxy.atomAdps : null
    property var atomMsps: projectOpened ? pyQmlProxy.atomMsps : null
    property var statusInfo: projectOpened ? pyQmlProxy.statusInfo : null

    // Refinement
    property var refinementRunning: pyQmlProxy.refinementRunning
    property var refinementDone: pyQmlProxy.refinementDone
    property var refinementResult: pyQmlProxy.refinementResult

    // Undo-Redo
    property var calculatorInterface: projectOpened ? pyQmlProxy.calculatorInterface : null
    property var undoText: calculatorInterface ? pyQmlProxy.undoText : ""
    property var redoText: calculatorInterface ? pyQmlProxy.redoText : ""
    property var canUndo: calculatorInterface ? pyQmlProxy.canUndo : false
    property var canRedo: calculatorInterface ? pyQmlProxy.canRedo : false

}
