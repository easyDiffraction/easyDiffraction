import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
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
        text: proxy.timeStamp
        onTextChanged: {
            //print("--------------------------------------------------------- Time stamp: ", text)
            if (Generic.Variables.projectOpened) {
                const atom_site_dict = Specific.Variables.project.phases.Fe3O4.atom_site
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
            GenericAppElements.ParametersTable {
                selectable: false
                enabled: false

                model: ListModel {
                    id: structuralPhasesModel
                    ListElement { num:0; name:""; note:"" }
                }

                Controls1.TableViewColumn { role:"num";     title:"No.";    resizable: false }
                Controls1.TableViewColumn { role:"name";    title:"Name ";   resizable: false }
                Controls1.TableViewColumn { role:"note";    title:"Note" }
                Controls1.TableViewColumn { role:"remove";  title:"Remove"; resizable: false }
            }

            // Buttons
            GenericAppElements.GridLayout {
                columns: 2

                GenericAppContentAreaButtons.Add { id: addButton; enabled: false; text: "Add new phase manually"; }
                GenericAppContentAreaButtons.RemoveAll { enabled: false; text: "Remove all phases" }
                GenericAppContentAreaButtons.Import { id: importButton; enabled: false; text: "Import new phase from CIF" }
                GenericAppContentAreaButtons.Export { enabled: false; text: "Export selected phase to CIF" }

                GenericAppElements.GuideWindow {
                    id: guidWindow
                    message: "Click here to add or import a new proxy."
                    toY: (addButton.y + addButton.height + importButton.y) / 2

                    visible: Generic.Variables.showGuide && Generic.Variables.toolbarCurrentIndex === Generic.Variables.SampleModelIndex ? true : false

                    GenericAppContentAreaButtons.Add { id: addButtonClone }
                    GenericAppContentAreaButtons.Import { id: importButtonClone }
                    Component.onCompleted: {
                        GenericLogic.Copy.copyButton(addButton, addButtonClone)
                        GenericLogic.Copy.copyButton(importButton, importButtonClone)
                    }
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

                GenericAppElements.ComboBox { model: [Generic.Variables.projectOpened ? Specific.Variables.project.phases.Fe3O4.space_group.crystal_system.value : ""] }
                GenericAppElements.ComboBox { model: [Generic.Variables.projectOpened ? Specific.Variables.project.phases.Fe3O4.space_group.space_group_IT_number.value + '.  ' + Specific.Variables.project.phases.Fe3O4.space_group['space_group_name_H-M_alt'].value : ""] }
                GenericAppElements.ComboBox { model: [Generic.Variables.projectOpened ? Specific.Variables.project.phases.Fe3O4.space_group.origin_choice.value : ""] }
            }

            GenericAppElements.GridLayout {
                columns: 1
                rowSpacing: 2
                Text { text: "Cell parameters"; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }

                // Table
                GenericAppElements.CellParametersTableView {
                    Layout.fillWidth: true
                    model: proxy.cellParameters
                }
            }
        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Atoms, atomic coordinates and occupations"
        content: GenericAppElements.ColumnLayout {

            // Table
            GenericAppElements.AtomsTableView {
                Layout.fillWidth: true
                model: proxy.atomSites
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
                model: proxy.atomAdps
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
                model: proxy.atomMsps
            }
        }
    }

    // Spacer

    Item { Layout.fillHeight: true }

    // Groupbox

    GenericAppElements.GroupBox {
        collapsible: false
        showBorder: false
        content: GenericAppElements.RowLayout {
            GenericAppContentAreaButtons.GoPrevious {
                text: "Experimental Data"
                ToolTip.text: qsTr("Go to the previous step: Experimental data")
                onClicked: {
                    Generic.Variables.toolbarCurrentIndex = Generic.Variables.ExperimentalDataIndex
                }
            }
            GenericAppContentAreaButtons.GoNext {
                text: "Analysis"
                ToolTip.text: qsTr("Go to the next step: Analysis")
                onClicked: {
                    Generic.Variables.samplePageFinished = true
                    Generic.Variables.toolbarCurrentIndex = Generic.Variables.AnalysisIndex
                }
            }

            GenericAppContentAreaButtons.SaveState {
            }
            GenericAppContentAreaButtons.Help {
                onClicked: Qt.openUrlExternally("https://easydiffraction.github.io/documentation_use.html#3.2.3.-sample-model")
            }
            GenericAppContentAreaButtons.Bug {
                onClicked: Qt.openUrlExternally("https://easydiffraction.github.io/contact.html")
            }
        }
    }

}

