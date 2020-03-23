pragma Singleton

import QtQuick 2.12

QtObject {

    property bool projectOpened: false

    // Main
    property var projectControl: proxyPyQmlObj.projectControl ? proxyPyQmlObj.projectControl : null
    property var projectDict: projectOpened ? proxyPyQmlObj.projectDict : null
    property var cif: projectOpened ? proxyPyQmlObj.fileStructure : null
    property var phaseCif: projectOpened ? proxyPyQmlObj.phaseCif : null
    property var phaseIds: projectOpened ? proxyPyQmlObj.projectDict.info.phase_ids: {}
    property var experimentCif: projectOpened ? proxyPyQmlObj.experimentCif : null
    property var experimentIds: projectOpened ? proxyPyQmlObj.projectDict.info.experiment_ids: {}
    property var calculationCif: projectOpened ? proxyPyQmlObj.calculationCif : null
    property var needToSave: projectOpened ? proxyPyQmlObj.needToSave : false
    property var projectFilePathSelected: proxyPyQmlObj.projectFilePathSelected

    property var projectName: projectOpened ? proxyPyQmlObj.projectManager.projectName : null
    property var projectKeywords: projectOpened ? proxyPyQmlObj.projectManager.projectKeywords : null
    property var projectModifiedDate: projectOpened ? proxyPyQmlObj.projectManager.projectModified : null

    property var projectChangedTime: projectOpened ? proxyPyQmlObj.projectChangedTime : ""

    // Measured and calculated data
    property var measuredData: proxyPyQmlObj.measuredData
    property var measuredDataHeaderModel: projectOpened ? proxyPyQmlObj.measuredData.asHeadersModel(
                                                              ) : null
    property var measuredDataModel: projectOpened ? proxyPyQmlObj.measuredData.asModel(
                                                        ) : null
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
    property var refinementRunning: proxyPyQmlObj.refinementStatus[0]
    property var refinementDone: proxyPyQmlObj.refinementStatus[1]
    property var refinementResult: proxyPyQmlObj.refinementStatus[2]

    // Undo-Redo
    property var calculatorInterface: projectOpened ? proxyPyQmlObj.calculatorInterface : null
    property var undoText: calculatorInterface ? proxyPyQmlObj.undoText : ""
    property var redoText: calculatorInterface ? proxyPyQmlObj.redoText : ""
    property var canUndo: calculatorInterface ? proxyPyQmlObj.canUndo : false
    property var canRedo: calculatorInterface ? proxyPyQmlObj.canRedo : false

    // Logging
    property var loggerPyQml: _loggerPyQml

    // Dummy Phase
    function jsPhase() {
        this.sites = {
            fract_x: [],
            fract_y: [],
            fract_z: [],
            scat_length_neutron: [],
        }

        this.cell = {
            length_a: 0,
            length_b: 0,
            length_c: 0,
        }
    }
    // Get Phase
    function phaseList(phase_index) {
        let this_phase = new jsPhase()
        if (!!phaseIds.length) {
            let phase = proxyPyQmlObj.projectDict.phases[phase_index]
            console.log(phase)
            this_phase.sites.fract_x = phase.sites.fract_x
            this_phase.sites.fract_y = phase.sites.fract_y
            this_phase.sites.fract_z = phase.sites.fract_z
            this_phase.sites.scat_length_neutron = phase.sites.scat_length_neutron
            this_phase.cell.length_a = phase.cell.length_a.store.value
            this_phase.cell.length_b = phase.cell.length_b.store.value
            this_phase.cell.length_c = phase.cell.length_c.store.value
        }
        console.log(this_phase)
        return this_phase
    }
}
