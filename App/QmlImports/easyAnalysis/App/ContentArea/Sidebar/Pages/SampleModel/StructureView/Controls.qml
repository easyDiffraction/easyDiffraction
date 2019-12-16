import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Dialogs 1.3 as Dialogs1
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons
import easyAnalysis.Logic 1.0 as GenericLogic
import easyDiffraction 1.0 as Specific

ColumnLayout {
    spacing: 0

    property var type_symbol_dict: ({})

    ////////////////////////
    // Check if data changed
    ////////////////////////

    Text {
        visible: false
        text: Specific.Variables.projectOpened ? Specific.Variables.project.info.refinement_datetime : ""
        onTextChanged: {
            //print("--------------------------------------------------------- Time stamp: ", text)
            if (Specific.Variables.projectOpened) {
                const atom_site_dict = Specific.Variables.project.phases[Specific.Variables.project.info.phase_ids[0]].atom_site
                let type_symbol_list = []
                for (let atom_id in atom_site_dict) {
                    type_symbol_list.push(atom_site_dict[atom_id].type_symbol.value)
                }
                type_symbol_list = Array.from(new Set(type_symbol_list))
                for (let i = 0; i < type_symbol_list.length; i++) {
                    type_symbol_dict[type_symbol_list[i]] = Generic.Style.atomColorList[i]
                }
            }
        }
    }

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
                    toolbarCurrentIndex: Generic.Variables.SampleModelIndex
                    guidesCount: Generic.Variables.SampleModelGuidesCount
                }
            }

            // Buttons
            GenericAppElements.GridLayout {
                columns: 2
                GenericAppContentAreaButtons.Add {
                    enabled: false;
                    text: "Add new phase manually"
                    }
                GenericAppContentAreaButtons.RemoveAll {
                    id: removeButton;
                    enabled: false;
                    text: "Remove all phases" }
                GenericAppContentAreaButtons.Import {
                    text: "Import new phase from CIF"
                    enabled: !proxy.refinementRunning
                    onClicked: fileDialogLoadPhase.open()
                    }
                GenericAppContentAreaButtons.Export {
                    enabled: false;
                    text: "Export selected phase to CIF"
                    }
            }
            // Open project dialog
            Dialogs1.FileDialog{
                id: fileDialogLoadPhase
                nameFilters: [ "CIF files (*.cif)"]
                folder: settings.value("lastOpenedProjectFolder", examplesDir)
                onAccepted: {
                    settings.setValue("lastOpenedProjectFolder", folder)
                    projectControl.loadPhases(fileUrl)
                    fileDialogLoadPhase.close()
                    var old_analysis_state = Generic.Variables.analysisPageFinished
                    var old_summary_state = Generic.Variables.summaryPageFinished
                    //if (projectControl.validCif) {
                    proxy.loadPhasesFromFile()
                    Specific.Variables.projectOpened = true
                    Generic.Variables.homePageFinished = true
                    Generic.Variables.dataPageFinished = true
                    Generic.Variables.samplePageFinished = false
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
        content: GenericAppElements.ColumnLayout {
            GenericAppElements.GridLayout {
                columns: 3
                rowSpacing: 2
                enabled: false

                Text { text: "Crystal system"; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }
                Text { text: "Space Group    "; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }
                Text { text: "Setting             "; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }

                GenericAppElements.ComboBox { model: [Specific.Variables.projectOpened ? Specific.Variables.project.phases[Specific.Variables.project.info.phase_ids[0]].space_group.crystal_system.value : ""] }
                GenericAppElements.ComboBox { model: [Specific.Variables.projectOpened ? Specific.Variables.project.phases[Specific.Variables.project.info.phase_ids[0]].space_group.space_group_IT_number.value + '.  ' + Specific.Variables.project.phases[Specific.Variables.project.info.phase_ids[0]].space_group['space_group_name_H-M_alt'].value : ""] }
                GenericAppElements.ComboBox { model: [Specific.Variables.projectOpened ? Specific.Variables.project.phases[Specific.Variables.project.info.phase_ids[0]].space_group.origin_choice.value : ""] }
            }

            GenericAppElements.GridLayout {
                columns: 1
                rowSpacing: 2
                Text { text: "Cell parameters"; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }

                // Table
                GenericAppElements.CellParametersTableView {
                    Layout.fillWidth: true
                    model: Specific.Variables.projectOpened ? proxy.cellParameters : null
                }
            }
        }
        GenericAppElements.GuideWindow {
            message: "The sidebar groups contain details related to the sample model.\n\nClick on the group name to unfold the group."
            position: "left"
            guideCurrentIndex: 3
            toolbarCurrentIndex: Generic.Variables.SampleModelIndex
            guidesCount: Generic.Variables.SampleModelGuidesCount
        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Atoms, atomic coordinates and occupations"
        content: GenericAppElements.ColumnLayout {

            // Table
            GenericAppElements.AtomsTableView {
                Layout.fillWidth: true
                model: Specific.Variables.projectOpened ? proxy.atomSites : null
            }

            // Buttons
            GenericAppElements.GridLayout {
                columns: 2
                GenericAppContentAreaButtons.Add { enabled: false; text: "Add new atom"; }
                GenericAppContentAreaButtons.RemoveAll { enabled: false; text: "Remove all atoms" }
            }
        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Atomic displacement parameters" //(\u200A\u00D7\u200A10\u2075\u200A)"
        content: GenericAppElements.ColumnLayout {

            // Table
            GenericAppElements.AtomAdpsTableView {
                Layout.fillWidth: true
                model: Specific.Variables.projectOpened ? proxy.atomAdps : null
            }
        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Magnetic susceptibility parameters"
        content: GenericAppElements.ColumnLayout {

            // Table
            GenericAppElements.AtomMspsTableView {
                Layout.fillWidth: true
                model: Specific.Variables.projectOpened ? proxy.atomMsps : null
            }
        }
    }

    // Spacer

    Item { Layout.fillHeight: true }

    // Groupbox

    GenericAppElements.FlowButtons {
        documentationUrl: "https://easydiffraction.org/umanual_use.html#3.2.4.-sample-model"
        goPreviousButton: GenericAppContentAreaButtons.GoPrevious {
            text: "Home"
            ToolTip.text: qsTr("Go to the previous step: Home")
            onClicked: {
                Generic.Variables.toolbarCurrentIndex = Generic.Variables.HomeIndex
            }
            GenericAppElements.GuideWindow {
                message: "Click here to go to the previous step: Home.\n\nAlternatively, you can click on the 'Home' button in toolbar."
                position: "top"
                guideCurrentIndex: 4
                toolbarCurrentIndex: Generic.Variables.SampleModelIndex
                guidesCount: Generic.Variables.SampleModelGuidesCount
            }
        }
        goNextButton: GenericAppContentAreaButtons.GoNext {
            text: "Experimental Data"
            ToolTip.text: qsTr("Go to the next step: Experimental data")
            highlighted: Specific.Variables.projectOpened
            onClicked: {
                Generic.Variables.samplePageFinished = true
                Generic.Variables.toolbarCurrentIndex = Generic.Variables.ExperimentalDataIndex
            }
            GenericAppElements.GuideWindow {
                message: "Click here to go to the next step: Experimental data."
                position: "top"
                guideCurrentIndex: 5
                toolbarCurrentIndex: Generic.Variables.SampleModelIndex
                guidesCount: Generic.Variables.SampleModelGuidesCount
            }
        }
    }
}

