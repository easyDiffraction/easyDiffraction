pragma Singleton

import QtQuick 2.12

import easyAnalysis 1.0 as Generic

QtObject {

    property bool projectOpened: false

    // Main
    property var projectControl: proxyPyQmlObj.projectControl ? proxyPyQmlObj.projectControl : null
    property var projectDict: projectOpened ? proxyPyQmlObj.projectDict : null
    property var cif: projectOpened ? proxyPyQmlObj.fileStructure : null
    property var phaseCif: projectOpened ? proxyPyQmlObj.phaseCif : null
    function phaseIds(){ return projectOpened ? proxyPyQmlObj.projectDict.info.phase_ids: []}
    property var experimentCif: projectOpened ? proxyPyQmlObj.experimentCif : null
    function experimentIds(){return projectOpened ? proxyPyQmlObj.projectDict.info.experiment_ids: []}
//    property var experimentIds: projectOpened ? proxyPyQmlObj.projectDict.info.experiment_ids: []
    property var calculationCif: projectOpened ? proxyPyQmlObj.calculationCif : null
    function calculationIds(){ return projectOpened ? Object.keys(proxyPyQmlObj.projectDict.calculations): []}
    property var needToSave: projectOpened ? proxyPyQmlObj.needToSave : false
    property var projectFilePathSelected: proxyPyQmlObj.projectFilePathSelected

    property var projectName: projectOpened ? proxyPyQmlObj.projectManager.projectName : null
    property var projectKeywords: projectOpened ? proxyPyQmlObj.projectManager.projectKeywords : null
    property var projectModifiedDate: projectOpened ? proxyPyQmlObj.projectManager.projectModified : null

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

    // Undo-Redo
    property var calculatorInterface: projectOpened ? proxyPyQmlObj.calculatorInterface : null
    property var undoText: calculatorInterface ? proxyPyQmlObj.undoText : ""
    property var redoText: calculatorInterface ? proxyPyQmlObj.redoText : ""
    property var canUndo: calculatorInterface ? proxyPyQmlObj.canUndo : false
    property var canRedo: calculatorInterface ? proxyPyQmlObj.canRedo : false

    // Refinement
    property var refinementRunning: proxyPyQmlObj.refinementStatus[0]
    property var refinementDone: proxyPyQmlObj.refinementStatus[1]
    property var refinementResult: proxyPyQmlObj.refinementStatus[2]

    onRefinementResultChanged: {
        if (Object.entries(refinementResult)) {
            Generic.Variables.refinementMessage = refinementResult.refinement_message ? refinementResult.refinement_message : Generic.Variables.refinementMessage
            Generic.Variables.chiSquared = refinementResult.final_chi_sq ? refinementResult.final_chi_sq.toFixed(2) : Generic.Variables.chiSquared
            Generic.Variables.numRefinedPars = refinementResult.num_refined_parameters ? refinementResult.num_refined_parameters.toFixed(0) : Generic.Variables.numRefinedPars

        }
    }

    // Logging
    property var loggerPyQml: _loggerPyQml
    function debug(obj) {
        const debugLevel = 10
        let currentLevel = 30
        if ((typeof(loggerPyQml) !== 'undefined') && (loggerPyQml !== null)) {
            currentLevel = loggerPyQml.getLevel()
        }
        if (currentLevel > debugLevel) {
            return
        }
        if (typeof obj === 'object') {
            print(JSON.stringify(obj))
        } else {
            print(obj)
        }
    }

    // Phases, Experiments, Calculations

    property var phases: projectDict ? _loadedPhases() : _defaultPhases()
    property var experiments: projectDict ? _loadedExperiments() : _defaultExperiments()
    property var calculations: projectDict ? _loadedCalculations() : _defaultCalculations()

    function _emptyPhase() {
        return {
            "sites": {
                "fract_x": [],
                "fract_y": [],
                "fract_z": [],
                "scat_length_neutron": [],
            },
            "atoms": {},
            "cell": {
                "length_a": 0,
                "length_b": 0,
                "length_c": 0
            },
            "spacegroup": {
                "crystal_system": "",
                "space_group_with_number": "",
                "origin_choice": ""
            }
        }
    }

    function _emptyExperiment() {
        return {
            "resolution": {
                "x": 0,
                "y": 0,
                "u": 0,
                "v": 0,
                "w": 0
            },
            "offset": 0,
            "wavelength": 0,
            "field": 0,
            "polarization": 90.0,
            "efficiency": 95.0,
            "phase": [ { "scale": 0 } ]
        }
    }

    function _emptyCalculation() {
        return {
            "limits": {
                "difference": {
                    "y_min": -1,
                    "y_max": 1
                },
                "main": {
                    "x_min": -1,
                    "x_max": 100,
                    "y_min" : -1,
                    "y_max": 10000
                }
            }
        }
    }

    function _defaultPhases() {
        return { "empty_phase": _emptyPhase() }
    }

    function _defaultExperiments() {
        return { "empty_experiment": _emptyExperiment() }
    }

    function _defaultCalculations() {
        return { "empty_calculation": _emptyCalculation() }
    }

    function _loadedPhases() {
        const those_phases = proxyPyQmlObj.projectDict.phases

        if (!Object.keys(those_phases).length) {
            return _defaultPhases()
        }

        let these_phases = {}

        for (const name in those_phases) {
            debug(`_loadedPhases: ${name}`)

            const this_phase = _emptyPhase()
            const that_phase = those_phases[name]

            this_phase.atoms = that_phase.atoms

            this_phase.sites.fract_x = that_phase.sites.fract_x
            this_phase.sites.fract_y = that_phase.sites.fract_y
            this_phase.sites.fract_z = that_phase.sites.fract_z

            this_phase.sites.scat_length_neutron = that_phase.sites.scat_length_neutron

            this_phase.cell.length_a = that_phase.cell.length_a.store.value
            this_phase.cell.length_b = that_phase.cell.length_b.store.value
            this_phase.cell.length_c = that_phase.cell.length_c.store.value

            this_phase.spacegroup.crystal_system = that_phase.spacegroup.crystal_system.store.value
            this_phase.spacegroup.space_group_with_number = that_phase.spacegroup.space_group_IT_number.store.value + '.  ' + that_phase.spacegroup.space_group_name_HM_alt.store.value
            this_phase.spacegroup.origin_choice = that_phase.spacegroup.crystal_system.store.value

            these_phases[name] = this_phase
        }

        return these_phases
    }

    function _loadedExperiments() {
        const those_experiments = proxyPyQmlObj.projectDict.experiments

        if (!Object.keys(those_experiments).length) {
            return _defaultExperiments()
        }

        let these_experiments = {}

        for (const name in those_experiments) {
            debug(`_loadedExperiments: ${name}`)

            const this_experiment = _emptyExperiment()
            const that_experiment = those_experiments[name]

            this_experiment.resolution.u = that_experiment.resolution.u.store.value
            this_experiment.resolution.v = that_experiment.resolution.v.store.value
            this_experiment.resolution.w = that_experiment.resolution.w.store.value
            this_experiment.resolution.x = that_experiment.resolution.x.store.value
            this_experiment.resolution.y = that_experiment.resolution.y.store.value

            this_experiment.offset = that_experiment.offset.store.value

            this_experiment.wavelength = that_experiment.wavelength.store.value

            this_experiment.phase[0].scale = that_experiment.phase[phaseIds()[0]].scale.store.value

            these_experiments[name] = this_experiment
        }

        return these_experiments
    }

    function _loadedCalculations() {
        const those_calculations = proxyPyQmlObj.projectDict.calculations

        if (!Object.keys(those_calculations).length) {
            return _defaultCalculations()
        }

        let these_calculations = {}

        for (const name in those_calculations) {
            debug(`_loadedCalculations: ${name}`)

            const this_calculation = _emptyCalculation()
            const that_calculation = those_calculations[name]

            this_calculation.limits.main.y_min = that_calculation.limits.main.y_min
            this_calculation.limits.main.y_max = that_calculation.limits.main.y_max
            this_calculation.limits.main.x_min = that_calculation.limits.main.x_min
            this_calculation.limits.main.x_max = that_calculation.limits.main.x_max
            this_calculation.limits.difference.y_min = that_calculation.limits.difference.y_min
            this_calculation.limits.difference.y_max = that_calculation.limits.difference.y_max

            these_calculations[name] = this_calculation
        }

        return these_calculations
    }

    function phaseByIndex(index) {
        const name = Object.keys(phases)[index]
        return phases[name]
    }

    function experimentByIndex(index) {
        const name = Object.keys(experiments)[index]
        return experiments[name]
    }

    function calculationByIndex(index) {
        const name = Object.keys(calculations)[index]
        return calculations[name]
    }

}

