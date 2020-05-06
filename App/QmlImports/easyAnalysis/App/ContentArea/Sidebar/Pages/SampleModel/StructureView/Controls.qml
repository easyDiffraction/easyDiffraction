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

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Structural phases"
        collapsible: false


        content: GenericAppElements.ColumnLayout {

            // Table
            GenericAppElements.PhasesTableView {
                Layout.fillWidth: true
                GenericAppElements.GuideWindow {
                    message: "Here you can see labels of the structural phases."
                    position: "left"
                    guideCurrentIndex: 0
                    toolbarCurrentIndex: Generic.Variables.SampleIndex
                    guidesCount: Generic.Variables.SampleGuidesCount
                }
            }

            // Buttons
            GenericAppElements.GridLayout {
                columns: 2
                GenericAppContentAreaButtons.Import {
                    text: "Import new phase from CIF"
                    enabled: !Specific.Variables.refinementRunning
                    onClicked: fileDialogLoadPhase.open()
                    GenericControls.EditingToolTip {
                        visible: Specific.Variables.phaseIds().length
                        type: GenericControls.EditingToolTip.Custom
                        text: qsTr("Multiple phases are not supported yet.")
                    }
                }
                GenericAppContentAreaButtons.Export {
                    //enabled: false;
                    text: "Export selected phase to CIF"
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
                }
                GenericAppContentAreaButtons.Add {
                    //enabled: false;
                    text: "Add new phase manually"
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
                }
                GenericAppContentAreaButtons.RemoveAll {
                    id: removeButton;
                    //enabled: false;
                    text: "Remove all phases"
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
                }
            }
            // Open project dialog
            Dialogs1.FileDialog{
                id: fileDialogLoadPhase
                nameFilters: [ "CIF files (*.cif)"]
                folder: settings.value("lastOpenedProjectFolder", examplesDirUrl)
                onAccepted: {
                    settings.setValue("lastOpenedProjectFolder", folder)
                    Specific.Variables.projectControl.loadPhases(fileUrl)
                    fileDialogLoadPhase.close()
                    var old_analysis_state = Generic.Variables.analysisPageFinished
                    var old_summary_state = Generic.Variables.summaryPageFinished
                    //if (projectControl.validCif) {
                    Generic.Constants.proxy.loadPhasesFromFile()
                    Specific.Variables.projectOpened = true
                    //Generic.Variables.projectPageFinished = true
                    Generic.Variables.samplePageFinished = true
                    //Generic.Variables.dataPageFinished = false
                    Generic.Variables.analysisPageFinished = Generic.Variables.isDebug ? true : false
                    Generic.Variables.summaryPageFinished = Generic.Variables.isDebug ? true : false
                    // The remove button will have to be enabled once we start actually adding phases
                    //removeButton.enabled = true
                    //}
                }
            }

        }
    }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        id: group1
        title: "Symmetry and cell parameters"
        enabled: Specific.Variables.phaseIds().length

        content: GenericAppElements.ColumnLayout {
            GenericAppElements.GridLayout {
                columns: 3
                rowSpacing: 2
                //enabled: false

                Text { text: "Crystal system"; color: Generic.Style.sidebarLabelColor; font.family: Generic.Style.fontFamily; font.pixelSize: Generic.Style.fontPixelSize - 1 }
                Text { text: "Space Group    "; color: Generic.Style.sidebarLabelColor; font.family: Generic.Style.fontFamily; font.pixelSize: Generic.Style.fontPixelSize - 1 }
                Text { text: "Setting             "; color: Generic.Style.sidebarLabelColor; font.family: Generic.Style.fontFamily; font.pixelSize: Generic.Style.fontPixelSize - 1 }

                GenericAppElements.ComboBox {
                    model: [Specific.Variables.phaseByIndex(0).spacegroup.crystal_system]
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NoEditingYet }
                }
                GenericAppElements.ComboBox {
                    model: [Specific.Variables.phaseByIndex(0).spacegroup.space_group_with_number]
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NoEditingYet }
                }
                GenericAppElements.ComboBox {
                    model: [Specific.Variables.phaseByIndex(0).spacegroup.origin_choice]
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NoEditingYet }
                }
            }

            GenericAppElements.GridLayout {
                columns: 1
                rowSpacing: 2
                Text { text: "Cell parameters"; color: Generic.Style.sidebarLabelColor; font.family: Generic.Style.fontFamily; font.pixelSize: Generic.Style.fontPixelSize - 1 }

                // Table
                GenericAppElements.CellParametersTableView {
                    Layout.fillWidth: true
                    model: Specific.Variables.cellParameters
                }
            }
        }
        GenericAppElements.GuideWindow {
            message: "The sidebar groups contain details related to the sample model.\n\nClick on the group name to unfold the group."
            position: "left"
            guideCurrentIndex: 3
            toolbarCurrentIndex: Generic.Variables.SampleIndex
            guidesCount: Generic.Variables.SampleGuidesCount
        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Atoms, atomic coordinates and occupations"
        enabled: Specific.Variables.phaseIds().length

        content: GenericAppElements.ColumnLayout {

            // Table
            GenericAppElements.AtomsTableView {
                Layout.fillWidth: true
                model: Specific.Variables.atomSites
            }

            // Buttons
            GenericAppElements.GridLayout {
                columns: 2
                GenericAppContentAreaButtons.Add {
                    //enabled: false
                    text: "Add new atom"
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
                }
                GenericAppContentAreaButtons.RemoveAll {
                    //enabled: false
                    text: "Remove all atoms"
                    GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
                }
            }
        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Atomic displacement parameters" //(\u200A\u00D7\u200A10\u2075\u200A)"
        enabled: Specific.Variables.phaseIds().length
        content: GenericAppElements.ColumnLayout {

            // Table
            GenericAppElements.AtomAdpsTableView {
                Layout.fillWidth: true
                model: Specific.Variables.atomAdps
            }
        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Magnetic susceptibility parameters"
        visible: Specific.Variables.isPolarized
        enabled: Specific.Variables.phaseIds().length

        content: GenericAppElements.ColumnLayout {

            // Table
            GenericAppElements.AtomMspsTableView {
                Layout.fillWidth: true
                model: Specific.Variables.atomMsps
            }
        }
    }

    // Spacer

    Item { Layout.fillHeight: true }

    // Groupbox

    GenericAppElements.FlowButtons {
        documentationUrl: "https://easydiffraction.org/umanual_use.html#3.2.4.-sample-model"
        goPreviousButton: GenericAppContentAreaButtons.GoPrevious {
            text: "Project"
            toolTipText: qsTr("Go to the previous step: Project")
            onClicked: {
                Generic.Variables.toolbarCurrentIndex = Generic.Variables.ProjectIndex
            }
            GenericAppElements.GuideWindow {
                message: "Click here to go to the previous step: Project.\n\nAlternatively, you can click on the 'Project' button in toolbar."
                position: "top"
                guideCurrentIndex: 4
                toolbarCurrentIndex: Generic.Variables.SampleIndex
                guidesCount: Generic.Variables.SampleGuidesCount
            }
        }
        goNextButton: GenericAppContentAreaButtons.GoNext {
            text: "Experiment"
            toolTipText: qsTr("Go to the next step: Experiment")
            enabled: Specific.Variables.projectOpened && Generic.Variables.samplePageFinished
            highlighted: Specific.Variables.projectOpened
            onClicked: {
                Generic.Variables.samplePageFinished = true
                Generic.Variables.toolbarCurrentIndex = Generic.Variables.ExperimentIndex
            }
            GenericAppElements.GuideWindow {
                message: "Click here to go to the next step: Experiment."
                position: "top"
                guideCurrentIndex: 5
                toolbarCurrentIndex: Generic.Variables.SampleIndex
                guidesCount: Generic.Variables.SampleGuidesCount
            }
        }
    }
}
