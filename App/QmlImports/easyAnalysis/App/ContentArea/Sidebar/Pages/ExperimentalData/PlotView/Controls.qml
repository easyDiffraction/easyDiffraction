import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Dialogs 1.3 as Dialogs1
import QtQuick.Layouts 1.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons
import easyDiffraction 1.0 as Specific

ColumnLayout {
    spacing: 0
    // Groupbox

    GenericAppElements.GroupBox {
        title: "Data Explorer"
        collapsible: false
        content: GenericAppElements.ColumnLayout {

            // Table
            GenericAppElements.ExperimentsTableView {
                Layout.fillWidth: true

                GenericAppElements.GuideWindow {
                    message: "Here you can see labels of the experimental data."
                    position: "left"
                    guideCurrentIndex: 0
                    toolbarCurrentIndex: Generic.Variables.ExperimentIndex
                    guidesCount: Generic.Variables.ExperimentGuidesCount
                }
            }

            // Buttons
            GenericAppElements.GridLayout {
                columns: 2

                GenericAppContentAreaButtons.Import {
                 enabled: !Specific.Variables.refinementRunning
                 text: "Import data from local drive";
                 onClicked: fileDialogLoadExps.open()
                }
                GenericAppContentAreaButtons.Link { enabled: false; text: "Link to data on local drive"; }
                GenericAppContentAreaButtons.Cloud { enabled: false; id: cloudButton; text: "Import data from SciCat" }
                GenericAppContentAreaButtons.RemoveAll { enabled: false; text: "Remove all data" }
            }
        }
    }

    // Loader
    Dialogs1.FileDialog{
        id: fileDialogLoadExps
        nameFilters: [ "CIF files (*.cif)"]
        folder: settings.value("lastOpenedProjectFolder", examplesDir)
        onAccepted: {
            settings.setValue("lastOpenedProjectFolder", folder)
            Specific.Variables.projectControl.loadExperiment(fileUrl)
            fileDialogLoadExps.close()
            var old_analysis_state = Generic.Variables.analysisPageFinished
            var old_summary_state = Generic.Variables.summaryPageFinished
            //if (projectControl.validCif) {
            Generic.Constants.proxy.loadExperimentFromFile()
            Specific.Variables.projectOpened = true
            //Generic.Variables.projectPageFinished = true
            //Generic.Variables.samplePageFinished = true
            Generic.Variables.dataPageFinished = true
            Generic.Variables.analysisPageFinished = Generic.Variables.isDebug ? true : false
            Generic.Variables.summaryPageFinished = Generic.Variables.isDebug ? true : false
            // The remove button will have to be enabled once we start actually adding phases
            //removeButton.enabled = true
            //}
        }
    }


    // Groupbox

    GenericAppElements.GroupBox {
        title: "Instrument"//"Diffractometer"
        content: GenericAppElements.ColumnLayout {
            GenericAppElements.GridLayout {
                enabled: false
                columns: 3
                rowSpacing: 2

                Text { text: "Facility           "; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }
                Text { text: "Instrument    "; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }
                Text { text: "Configuration"; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }
                GenericAppElements.ComboBox { currentIndex: 5; model: ["ESS", "ISIS", "SNS", "ILL", "MLZ", "LLB", "Custom"] }
                GenericAppElements.ComboBox { currentIndex: 0; model: ["6T2", "Custom"] }
                GenericAppElements.ComboBox { currentIndex: 0; model: ["Standard"] }

                Item { height: 5 }
                Item { height: 5 }
                Item { height: 5 }

                Text { text: "Radiation"; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }
                Text { text: "Mode"; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 } //Technique/Data
                Text { text: "Method"; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 } //Method/Sample
                GenericAppElements.ComboBox { currentIndex: 0; model: ["Neutron", "X-ray", "Electron"] }
                GenericAppElements.ComboBox { currentIndex: 0; model: ["Constant wavelength", "Time-of-flight"] }
                GenericAppElements.ComboBox { currentIndex: 0; model: ["Powder", "Single crystal"] }
            }

            GenericAppElements.GridLayout {
                columns: 6
                columnSpacing: 15
                rowSpacing: 10

                Text { text: qsTr("Wavelength") }
                GenericAppElements.TextField {
                    text: Specific.Variables.projectOpened ? Specific.Variables.projectDict.experiments[Specific.Variables.experimentIds[0]].wavelength.store.value.toFixed(4) : ""
                    units: "\u212B"
                }
                Text {}
                Text { text: qsTr("Zero shift") }
                GenericAppElements.TextField {
                    text: Specific.Variables.projectOpened ? Specific.Variables.projectDict.experiments[Specific.Variables.experimentIds[0]].offset.store.value.toFixed(4) : ""
                    units: "\u00B0"
                }
            }
        }
        GenericAppElements.GuideWindow {
            message: "The sidebar groups contain details related to the experiment.\n\nClick on the group name to unfold the group."
            position: "left"
            guideCurrentIndex: 4
            toolbarCurrentIndex: Generic.Variables.ExperimentIndex
            guidesCount: Generic.Variables.ExperimentGuidesCount
        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Peak profile" // https://wiki-ext.aps.anl.gov/ug11bm/index.php/GSAS_Profile_Terms
        content: GenericAppElements.ColumnLayout {
            spacing: 12
            enabled: false
            ColumnLayout {
                spacing: 2
                Text { text: "Instrument resolution function"; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }
                ///GenericAppElements.ComboBox { currentIndex: 3; model: ["Gaussian", "Lorentz", "Pseudo-Voigt", "Thompson-Cox-Hastings pseudo-Voigt"] }
                GenericAppElements.ComboBox { currentIndex: 2; model: ["Gaussian", "Lorentz", "Pseudo-Voigt"] }
            }
            GridLayout {
                columns: 8
                columnSpacing: 15
                rowSpacing: 10
                enabled: false
                // Row
                Text { text: qsTr("U") }
                GenericAppElements.TextField { text: Specific.Variables.projectOpened ? Specific.Variables.projectDict.experiments[Specific.Variables.experimentIds[0]].resolution.u.store.value.toFixed(4) : "" }
                Text {}
                Text { text: qsTr("V") }
                GenericAppElements.TextField { text: Specific.Variables.projectOpened ? Specific.Variables.projectDict.experiments[Specific.Variables.experimentIds[0]].resolution.v.store.value.toFixed(4) : "" }
                Text {}
                Text { text: qsTr("W") }
                GenericAppElements.TextField { text: Specific.Variables.projectOpened ? Specific.Variables.projectDict.experiments[Specific.Variables.experimentIds[0]].resolution.w.store.value.toFixed(4) : "" }
                // Row
                Text { text: qsTr("X") }
                GenericAppElements.TextField { text: Specific.Variables.projectOpened ? Specific.Variables.projectDict.experiments[Specific.Variables.experimentIds[0]].resolution.x.store.value.toFixed(4) : "" }
                Text {}
                Text { text: qsTr("Y") }
                GenericAppElements.TextField { text: Specific.Variables.projectOpened ? Specific.Variables.projectDict.experiments[Specific.Variables.experimentIds[0]].resolution.y.store.value.toFixed(4) : "" }
            }
        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Associated phases"//"Instrument parameters"
//        content: GridLayout {
//            columns: 4
//            columnSpacing: 15
//            rowSpacing: 10
//            enabled: false
//            Text { text: qsTr("Scale") }
//            GenericAppElements.TextField {
//                text: Specific.Variables.projectOpened ? Specific.Variables.projectDict.experiments[Specific.Variables.projectDict.info.experiment_ids[0]].phase[Specific.Variables.projectDict.info.phase_ids[0]].scale.store.value.toFixed(4) : ""
//                units: ""
//            }
//
//        }
        content:             // Table
        GenericAppElements.PhasesTableScaleView {
            Layout.fillWidth: true
            GenericAppElements.GuideWindow {
                message: "Here you can see labels of the structural phases."
                position: "left"
                guideCurrentIndex: 0
                toolbarCurrentIndex: Generic.Variables.SampleIndex
                guidesCount: Generic.Variables.SampleGuidesCount
            }
        }
    }

    // Spacer

    Item { Layout.fillHeight: true }

    // Groupbox

    GenericAppElements.FlowButtons {
        documentationUrl: "https://easydiffraction.org/umanual_use.html#3.2.3.-experimental-data"
        goPreviousButton: GenericAppContentAreaButtons.GoPrevious {
            text: "Sample"
            ToolTip.text: qsTr("Go to the previous step: Sample")
            onClicked: {
                Generic.Variables.toolbarCurrentIndex = Generic.Variables.SampleIndex
            }
            GenericAppElements.GuideWindow {
                message: "Click here to go to the previous step: Sample.\n\nAlternatively, you can click on the 'Sample' button in toolbar."
                position: "top"
                guideCurrentIndex: 5
                toolbarCurrentIndex: Generic.Variables.ExperimentIndex
                guidesCount: Generic.Variables.ExperimentGuidesCount
            }
        }
        goNextButton: GenericAppContentAreaButtons.GoNext {
            text: "Analysis"
            ToolTip.text: qsTr("Go to the next step: Analysis")
            enabled: Specific.Variables.projectOpened && Generic.Variables.dataPageFinished
            onClicked: {
                Generic.Variables.toolbarCurrentIndex = Generic.Variables.AnalysisIndex
            }
            GenericAppElements.GuideWindow {
                message: "Click here to go to the next step: Structure refinement."
                position: "top"
                guideCurrentIndex: 6
                toolbarCurrentIndex: Generic.Variables.ExperimentIndex
                guidesCount: Generic.Variables.ExperimentGuidesCount
            }
        }
    }

}

