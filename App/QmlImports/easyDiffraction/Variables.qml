pragma Singleton

import QtQuick 2.12

QtObject {

    property bool projectOpened: false

    // Main
    property var projectControl: proxyPyQmlObj.projectControl ? proxyPyQmlObj.projectControl : null
    property var projectDict: projectOpened ? proxyPyQmlObj.projectDict : null
    property var cif: projectOpened ? proxyPyQmlObj.fileStructure : null
    property var phaseCif: projectOpened ? proxyPyQmlObj.phaseCif : null
    property var phaseIds: projectOpened ? proxyPyQmlObj.projectDict.info.phase_ids: []
    property var experimentCif: projectOpened ? proxyPyQmlObj.experimentCif : null
    property var experimentIds: projectOpened ? proxyPyQmlObj.projectDict.info.experiment_ids: []
    property var calculationCif: projectOpened ? proxyPyQmlObj.calculationCif : null
    property var calculationIds: projectOpened ? Object.keys(proxyPyQmlObj.projectDict.calculations): []
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

    // Dummy phase
    function _emptyPhase() {
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
        this.spacegroup = {
            crystal_system: "",
            space_group_with_number: "",
            origin_choice: ""
        }
    }

    // Get phase by index
    function phaseByIndex(phase_index) {
        let this_phase = new _emptyPhase()

        if (!!phaseIds.length) {
            loggerPyQml.getLevel() < 20 && console.debug("Phases loaded")
            const phases = proxyPyQmlObj.projectDict.phases
            const phase_name = Object.keys(phases)[phase_index]
            const phase = phases[phase_name]

            this_phase.sites.fract_x = phase.sites.fract_x
            this_phase.sites.fract_y = phase.sites.fract_y
            this_phase.sites.fract_z = phase.sites.fract_z

            this_phase.sites.scat_length_neutron = phase.sites.scat_length_neutron

            this_phase.cell.length_a = phase.cell.length_a.store.value
            this_phase.cell.length_b = phase.cell.length_b.store.value
            this_phase.cell.length_c = phase.cell.length_c.store.value

            this_phase.spacegroup.crystal_system = phase.spacegroup.crystal_system.store.value
            this_phase.spacegroup.space_group_with_number = phase.spacegroup.space_group_IT_number.store.value + '.  ' + phase.spacegroup.space_group_name_HM_alt.store.value
            this_phase.spacegroup.origin_choice = phase.spacegroup.crystal_system.store.value
        }
        else
        {
            loggerPyQml.getLevel() < 20 && console.debug("No phases yet")
        }
        return this_phase
    }

    // Dummy Calculation
    function _emptyCalculation(){
        this.limits = {
            difference: {
                y_min: -1,
                y_max: 1,
            },
            main: {
                x_min: -1,
                x_max: 1,
                y_min : -1,
                y_max: 1,
            },
        }
    }

    // Get Calculation
    function calculationByIndex(calculation_index){
        let this_calculation = new _emptyCalculation()

        if (!!calculationIds.length) {

            loggerPyQml.getLevel() < 20 && console.debug("Calculation loaded")
            const calculations = proxyPyQmlObj.projectDict.calculations
            const calcultion_name = Object.keys(calculations)[calculation_index]
            const calc = calculations[calcultion_name]

            this_calculation.limits.main.y_min = calc.limits.main.y_min
            this_calculation.limits.main.y_max = calc.limits.main.y_max
            this_calculation.limits.main.x_min = calc.limits.main.x_min
            this_calculation.limits.main.x_max = calc.limits.main.x_max
            this_calculation.limits.difference.y_min = calc.limits.difference.y_min
            this_calculation.limits.difference.y_max = calc.limits.difference.y_max
        }
        else
        {
            loggerPyQml.getLevel() < 20 && console.debug("No calculations yet")
        }
        return this_calculation
    }

    //Dummy Experiment
    function _emptyExperiment(){
        this.resolution = {
            x: 0,
            y: 0,
            u: 0,
            v: 0,
            w: 0,
        },
        this.offset = 0
        this.wavelength = 0
        this.phase = [{scale: 0}]
    }

    function experimentByIndex(exp_index){
        let this_exp = new _emptyExperiment()

        if (!!experimentIds.length && !!calculationIds.length){

            loggerPyQml.getLevel() < 20 && console.debug("Experiemnt loaded")
            const experiments = proxyPyQmlObj.projectDict.experiments
            const experiment_name = Object.keys(experiments)[exp_index]
            const exp = experiments[experiment_name]

            this_exp.resolution.u = exp.resolution.u.store.value
            this_exp.resolution.v = exp.resolution.v.store.value
            this_exp.resolution.w = exp.resolution.w.store.value
            this_exp.resolution.x = exp.resolution.x.store.value
            this_exp.resolution.y = exp.resolution.y.store.value

            this_exp.offset = exp.offset.store.value

            this_exp.wavelength = exp.wavelength.store.value

            this_exp.phase[0].scale = exp.phase[phaseIds[0]].scale.store.value
        }
        else
        {
            loggerPyQml.getLevel() < 20 && console.debug("No calculations yet")
        }
        return this_exp
    }
}
