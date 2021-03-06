import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Dialogs 1.3 as Dialogs1
import QtQuick.Layouts 1.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.Controls 1.0 as GenericControls
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
                 GenericControls.EditingToolTip {
                     visible: Specific.Variables.experimentIds().length
                     type: GenericControls.EditingToolTip.Custom
                     text: qsTr("Multiple experiments are not supported yet.")
                 }
                }
                GenericAppContentAreaButtons.Link {
                    //enabled: false
                    text: "Link to data on local drive"
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
                }
                GenericAppContentAreaButtons.Cloud {
                    id: cloudButton
                    //enabled: false
                    text: "Import data from SciCat"
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
                }
                GenericAppContentAreaButtons.RemoveAll {
                    //enabled: false
                    text: "Remove all data"
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
                }
            }
        }
    }

    // Loader
    Dialogs1.FileDialog{
        id: fileDialogLoadExps
        nameFilters: [ "CIF or ASCII data files (*.cif *.xye *.dat)"]
        folder: settings.value("lastOpenedProjectFolder", examplesDirUrl)
        onAccepted: {
            settings.setValue("lastOpenedProjectFolder", folder)
            Specific.Variables.projectControl.loadExperiment(fileUrl)
            fileDialogLoadExps.close()
            var old_analysis_state = Generic.Variables.analysisPageFinished
            var old_summary_state = Generic.Variables.summaryPageFinished
            //if (projectControl.validCif) {
            Generic.Constants.proxy.loadExperiment()
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
        title: "Instrument and experiment type"//"Diffractometer"
        enabled: Specific.Variables.experimentIds().length
        content: GenericAppElements.ColumnLayout {
            GenericAppElements.GridLayout {
                //enabled: false
                columns: 3
                rowSpacing: 2

                Text { text: "Facility            "; color: Generic.Style.sidebarLabelColor; font.family: Generic.Style.fontFamily; font.pixelSize: Generic.Style.fontPixelSize - 1 }
                Text { text: "Instrument      "; color: Generic.Style.sidebarLabelColor; font.family: Generic.Style.fontFamily; font.pixelSize: Generic.Style.fontPixelSize - 1 }
                Text { text: "Configuration"; color: Generic.Style.sidebarLabelColor; font.family: Generic.Style.fontFamily; font.pixelSize: Generic.Style.fontPixelSize - 1 }

                GenericAppElements.ComboBox {
                    implicitWidth: 1
                    currentIndex: 0
                    model: ["Unknown", "ESS", "ISIS", "SNS", "ILL", "MLZ", "LLB", "Custom"]
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
                }
                GenericAppElements.ComboBox {
                    implicitWidth: 1
                    currentIndex: 0
                    model: ["Unknown", "6T2", "Custom"]
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
                }
                GenericAppElements.ComboBox {
                    implicitWidth: 1
                    currentIndex: 0
                    model: ["Standard"]
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
                }

                Item { height: 5 }
                Item { height: 5 }
                Item { height: 5 }

                Text { text: "Radiation"; color: Generic.Style.sidebarLabelColor; font.family: Generic.Style.fontFamily; font.pixelSize: Generic.Style.fontPixelSize - 1 }
                Text { text: "Mode"; color: Generic.Style.sidebarLabelColor; font.family: Generic.Style.fontFamily; font.pixelSize: Generic.Style.fontPixelSize - 1 } //Technique/Data
                Text { text: "Method"; color: Generic.Style.sidebarLabelColor; font.family: Generic.Style.fontFamily; font.pixelSize: Generic.Style.fontPixelSize - 1 } //Method/Sample

                GenericAppElements.ComboBox {
                    currentIndex: 0
                    model: ["Neutron", "X-ray", "Electron"]
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
                }
                GenericAppElements.ComboBox {
                    currentIndex: 0
                    model: ["Constant wavelength", "Time-of-flight"]
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
                }
                GenericAppElements.ComboBox {
                    currentIndex: 0
                    model: ["Powder", "Single crystal"]
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
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
        visible: Specific.Variables.isPolarized
        title: "Diffraction radiation"
        enabled: Specific.Variables.experimentIds().length
        content: GenericAppElements.ColumnLayout {
            GenericAppElements.GridLayout {
                columns: 5
                columnSpacing: 5
                //rowSpacing: 10

                Text {
                    font.pixelSize: Generic.Style.fontPixelSize
                    font.family: Generic.Style.fontFamily
                    text: qsTr("Polarization:")
                }
                GenericAppElements.TextField {
                    text: 100 * Specific.Variables.experimentByIndex(0).polarization.polarization.toFixed(3)
                    units: "%"
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.OnAnalysisPage }
                }
                Text { width: 5 }
                Text {
                    font.pixelSize: Generic.Style.fontPixelSize
                    font.family: Generic.Style.fontFamily
                    text: qsTr("Polarising efficiency:")
                }
                GenericAppElements.TextField {
                    text: 100 * Specific.Variables.experimentByIndex(0).polarization.efficiency.toFixed(3)
                    units: "%"
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.OnAnalysisPage }
                }
            }
        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Setup parameters"
        enabled: Specific.Variables.experimentIds().length
        content: GenericAppElements.ColumnLayout {
            GenericAppElements.GridLayout {
                columns: 8
                columnSpacing: 5
                //rowSpacing: 10

                Text {
                    font.pixelSize: Generic.Style.fontPixelSize
                    font.family: Generic.Style.fontFamily
                    text: qsTr("Zero shift:")
                }
                GenericAppElements.TextField {
                    text: Specific.Variables.experimentByIndex(0).offset.toFixed(4)
                    units: "\u00B0"
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.OnAnalysisPage }
                }
                Text { width: 5 }
                Text {
                    font.pixelSize: Generic.Style.fontPixelSize
                    font.family: Generic.Style.fontFamily
                    text: qsTr("Wavelength:")
                }
                GenericAppElements.TextField {
                    text: Specific.Variables.experimentByIndex(0).wavelength.toFixed(4)
                    units: "\u212B"
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.OnAnalysisPage }
                }
                Text { width: 5 }
                Text {
                    font.pixelSize: Generic.Style.fontPixelSize
                    font.family: Generic.Style.fontFamily
                    text: qsTr("Magnetic field:")
                }
                GenericAppElements.TextField {
                    text: Specific.Variables.experimentByIndex(0).magnetic_field.toFixed(4)
                    units: "T"
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.OnAnalysisPage }
                }
            }
        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Peak profile" // https://wiki-ext.aps.anl.gov/ug11bm/index.php/GSAS_Profile_Terms
        enabled: Specific.Variables.experimentIds().length

        content: GenericAppElements.ColumnLayout {
            spacing: 12
            //enabled: false
            ColumnLayout {
                spacing: 2
                Text { text: "Instrument resolution function"; color: Generic.Style.sidebarLabelColor; font.family: Generic.Style.fontFamily; font.pixelSize: Generic.Style.fontPixelSize - 1 }
                ///GenericAppElements.ComboBox { currentIndex: 3; model: ["Gaussian", "Lorentz", "Pseudo-Voigt", "Thompson-Cox-Hastings pseudo-Voigt"] }
                GenericAppElements.ComboBox {
                    currentIndex: 2
                    model: ["Gaussian", "Lorentz", "Pseudo-Voigt"]
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NoEditingYet }
                }
            }
            GridLayout {
                columns: 8
                columnSpacing: 5
                rowSpacing: 10
                //enabled: false

                // Row
                Text {
                    text: "U:"
                    font.pixelSize: Generic.Style.fontPixelSize
                    font.family: Generic.Style.fontFamily
                }
                GenericAppElements.TextField {
                    text: Specific.Variables.experimentByIndex(0).resolution.u.toFixed(4)
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.OnAnalysisPage }
                }
                Text { width: 5 }

                Text {
                    text: "V:"
                    font.pixelSize: Generic.Style.fontPixelSize
                    font.family: Generic.Style.fontFamily
                }
                GenericAppElements.TextField {
                    text: Specific.Variables.experimentByIndex(0).resolution.v.toFixed(4)
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.OnAnalysisPage }
                }
                Text { width: 5 }

                Text {
                    text: "W:"
                    font.pixelSize: Generic.Style.fontPixelSize
                    font.family: Generic.Style.fontFamily
                }
                GenericAppElements.TextField {
                    text: Specific.Variables.experimentByIndex(0).resolution.w.toFixed(4)
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.OnAnalysisPage }
                }

                // Row
                Text {
                    text: "X:"
                    font.pixelSize: Generic.Style.fontPixelSize
                    font.family: Generic.Style.fontFamily
                }
                GenericAppElements.TextField {
                    text: Specific.Variables.experimentByIndex(0).resolution.x.toFixed(4)
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.OnAnalysisPage }
                }
                Text { width: 5 }

                Text {
                    text: "Y:"
                    font.pixelSize: Generic.Style.fontPixelSize
                    font.family: Generic.Style.fontFamily
                }
                GenericAppElements.TextField {
                    text: Specific.Variables.experimentByIndex(0).resolution.y.toFixed(4)
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.OnAnalysisPage }
                }
            }
        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Background"
        enabled: Specific.Variables.experimentIds().length
        content: GenericAppElements.ColumnLayout {

            // Table
            GenericAppElements.BackgroundTableView {
                Layout.fillWidth: true
                model: Specific.Variables.experimentByIndex(0).background
            }
        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Structural phases"//"Instrument parameters"
        enabled: Specific.Variables.experimentIds().length

        content: GenericAppElements.ColumnLayout {

            // Table
            GenericAppElements.PhasesTableScaleView {
                Layout.fillWidth: true
            }
        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Refinement"
        visible: Specific.Variables.isPolarized
        enabled: Specific.Variables.experimentIds().length
        content: GenericAppElements.ColumnLayout {
            GenericAppElements.RowLayout {
                spacing: 10

                GenericAppElements.CheckBox {
                    text: "Up \uff0b Down"
                    checked: Specific.Variables.refineSum
                    onClicked: Specific.Variables.refineSum = checked
                }

                GenericAppElements.CheckBox {
                    text: "Up \uff0d Down"
                    checked: Specific.Variables.refineDiff
                    onClicked: Specific.Variables.refineDiff = checked
                }
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

