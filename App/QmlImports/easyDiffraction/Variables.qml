pragma Singleton

import QtQuick 2.12

import easyAnalysis 1.0 as Generic

QtObject {

    property bool projectOpened: false

    // Main
    property var projectControl: proxyPyQmlObj && proxyPyQmlObj._projectControl ? proxyPyQmlObj._projectControl : null

    property var calculatorInterface: proxyPyQmlObj._calculatorInterface
    //property var calculatorInterface: projectOpened ? proxyPyQmlObj.calculatorInterface : null
    property var projectDict: projectOpened ? calculatorInterface.asDict() : null
    property var projectCifDict: projectOpened ? calculatorInterface.asCifDict() : {"phases": {}, "experiments": {}, "calculations": {}}
    ///property var projectDict: projectOpened ? projectDict : null
    ////property var projectDict: projectOpened ? proxyPyQmlObj.projectDict : null
    ////property var projectCifDict: projectOpened ? proxyPyQmlObj.projectCifDict : {"phases": {}, "experiments": {}, "calculations": {}}

    property var cif: proxyPyQmlObj && projectOpened ? proxyPyQmlObj._fileStructure : null

    //property var phaseCif: projectOpened ? proxyPyQmlObj.phaseCif : null
    //property var phaseIds: projectOpened ? projectDict.info.phases_ids: []
    function phaseIds(){ return projectOpened ? projectDict.info.phase_ids: []}

    //property var experimentCif: projectOpened ? proxyPyQmlObj.experimentCif : null
    //property var experimentIds: projectOpened ? projectDict.info.experiment_ids: []
    function experimentIds(){return projectOpened ? projectDict.info.experiment_ids: []}

    //property var calculationCif: projectOpened ? proxyPyQmlObj.calculationCif : null
    function calculationIds(){ return projectOpened ? Object.keys(projectDict.calculations): []}

    property var needToSave: proxyPyQmlObj && projectOpened ? proxyPyQmlObj._needToSave : false
    property var projectFilePathSelected: projectOpened ? proxyPyQmlObj._projectFilePathSelected : ""

    property var projectName: proxyPyQmlObj && projectOpened ? proxyPyQmlObj._projectManager.projectName : null
    property var projectKeywords: proxyPyQmlObj && projectOpened ? proxyPyQmlObj._projectManager.projectKeywords : null
    property var projectModifiedDate: proxyPyQmlObj && projectOpened ? proxyPyQmlObj._projectManager.projectModified : null

    // Measured and calculated data
    property var measuredData: proxyPyQmlObj._measuredData
    property var measuredDataHeaderModel: proxyPyQmlObj && projectOpened ?
                                              proxyPyQmlObj._measuredData.asHeadersModel() : null
    property var measuredDataModel: proxyPyQmlObj && projectOpened ?
                                        proxyPyQmlObj._measuredData.asModel() : null
    property var calculatedData: proxyPyQmlObj._calculatedData
    property var braggPeaks: proxyPyQmlObj._braggPeaks
    property string dataType: "Sum"
    onDataTypeChanged: {
        measuredData.setDataType(dataType)
        calculatedData.setDataType(dataType)
    }
    property bool isPolarized: projectCifDict["experiments"].toString().includes("_pd_meas_intensity_up")
    property bool refineSum: proxyPyQmlObj && projectOpened ? proxyPyQmlObj._refineSum : false
    property bool refineDiff: proxyPyQmlObj && projectOpened ? proxyPyQmlObj._refineDiff : false
    onRefineSumChanged: proxyPyQmlObj._refineSum = refineSum
    onRefineDiffChanged: proxyPyQmlObj._refineDiff = refineDiff

    // Models
    property var fitables: proxyPyQmlObj && projectOpened ? proxyPyQmlObj._fitables : null
    property var cellParameters: proxyPyQmlObj && projectOpened ? proxyPyQmlObj._cellParameters : null
    property var cellBox: proxyPyQmlObj && projectOpened ? proxyPyQmlObj._cellBox : null
    property var atomSites: proxyPyQmlObj && projectOpened ? proxyPyQmlObj._atomSites : null
    property var atomAdps: proxyPyQmlObj && projectOpened ? proxyPyQmlObj._atomAdps : null
    property var atomMsps: proxyPyQmlObj && projectOpened ? proxyPyQmlObj._atomMsps : null
    property var statusInfo: proxyPyQmlObj && projectOpened ? proxyPyQmlObj._statusInfo : null

    // Examples
    readonly property var examplesList: [
        examplesRcDirUrl.replace("file:", "") + "/Fe3O4_pol-neutron-powder-1d_5T_5C1(LLB)/main.cif",
        examplesRcDirPath + "/PbSO4_unpol-neutron-powder-1d_D1A(ILL)/main.cif"
    ]

    // Undo-Redo
    property var undoText: calculatorInterface ? proxyPyQmlObj._undoText : ""
    property var redoText: calculatorInterface ? proxyPyQmlObj._redoText : ""
    property var canUndo: calculatorInterface ? proxyPyQmlObj._canUndo : false
    property var canRedo: calculatorInterface ? proxyPyQmlObj._canRedo : false

    // Refinement
    property var refinementRunning: proxyPyQmlObj._refinementStatus[0]
    property var refinementDone: proxyPyQmlObj._refinementStatus[1]
    property var refinementResult: proxyPyQmlObj._refinementStatus[2]

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
            "chi2" : {
                "sum": false,
                "diff": false
            },
            "polarization": {
                "polarization": 0.90,
                "efficiency": 0.95
             },
            "phase": [ { "scale": 0 } ],
            "background": [
                { "ttheta":   "0.0", "intensity": 100.0 },
                { "ttheta":  "90.0", "intensity": 100.0 },
                { "ttheta": "180.0", "intensity": 100.0 }
            ]
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
        const those_phases = projectDict.phases

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
        const those_experiments = projectDict.experiments

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
            this_experiment.field = that_experiment.field.store.value
            this_experiment.wavelength = that_experiment.wavelength.store.value

            this_experiment.chi2.sum = that_experiment.chi2._sum
            this_experiment.chi2.diff = that_experiment.chi2._diff
            this_experiment.polarization.polarization = that_experiment.polarization.polarization.store.value
            this_experiment.polarization.efficiency = that_experiment.polarization.efficiency.store.value

            this_experiment.phase[0].scale = that_experiment.phase[phaseIds()[0]].scale.store.value

            this_experiment.background = []
            for (let ttheta in that_experiment.background) {
                const intensity = that_experiment.background[ttheta].intensity.store.value
                this_experiment.background.push({ "ttheta": ttheta, "intensity": intensity })
            }

            these_experiments[name] = this_experiment
        }

        return these_experiments
    }

    function _loadedCalculations() {
        const those_calculations = projectDict.calculations

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

    /*
    Component.onCompleted: {
        print("examplesRcDirUrl", examplesRcDirUrl)
        print("examplesRcDirPath", examplesRcDirPath)
    }
    */

}

