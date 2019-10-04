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


    // Groupbox

    GenericAppElements.GroupBox {
        title: "Data Explorer"
        collapsible: false
        content: GenericAppElements.ColumnLayout {

            // Table
            GenericAppElements.ExperimentsTableView {
                Layout.fillWidth: true
            }

            // Buttons
            GenericAppElements.GridLayout {
                columns: 2

                GenericAppContentAreaButtons.Import { id: importButton; enabled: false; text: "Import data from local drive"; }
                GenericAppContentAreaButtons.Link { enabled: false; text: "Link to data on local drive"; }
                GenericAppContentAreaButtons.Cloud { enabled: false; id: cloudButton; text: "Import data from SciCat" }
                GenericAppContentAreaButtons.RemoveAll { enabled: false; text: "Remove all data" }

                GenericAppElements.GuideWindow {
                    id: guidWindow
                    //message: "Click here to add or import new data.\n\nSkip this step, if only simulations are needed."
                    message: "Click here to add or import new data."
                    toY: (importButton.y + importButton.height + cloudButton.y) / 2

                    visible: Generic.Variables.showGuide && Generic.Variables.toolbarCurrentIndex === Generic.Variables.ExperimentalDataIndex ? true : false

                    GenericAppContentAreaButtons.Import { id: importButtonClone }
                    GenericAppContentAreaButtons.Cloud { id: cloudButtonClone }
                    Component.onCompleted: {
                        GenericLogic.Copy.copyButton(importButton, importButtonClone)
                        GenericLogic.Copy.copyButton(cloudButton, cloudButtonClone)
                    }
                }
            }
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
                GenericAppElements.TextField { text: Specific.Variables.projectOpened ? Specific.Variables.project.experiments[Specific.Variables.project.info.experiment_ids[0]].resolution.u.value.toFixed(4) : "" }
                Text {}
                Text { text: qsTr("V") }
                GenericAppElements.TextField { text: Specific.Variables.projectOpened ? Specific.Variables.project.experiments[Specific.Variables.project.info.experiment_ids[0]].resolution.v.value.toFixed(4) : "" }
                Text {}
                Text { text: qsTr("W") }
                GenericAppElements.TextField { text: Specific.Variables.projectOpened ? Specific.Variables.project.experiments[Specific.Variables.project.info.experiment_ids[0]].resolution.w.value.toFixed(4) : "" }
                // Row
                Text { text: qsTr("X") }
                GenericAppElements.TextField { text: Specific.Variables.projectOpened ? Specific.Variables.project.experiments[Specific.Variables.project.info.experiment_ids[0]].resolution.x.value.toFixed(4) : "" }
                Text {}
                Text { text: qsTr("Y") }
                GenericAppElements.TextField { text: Specific.Variables.projectOpened ? Specific.Variables.project.experiments[Specific.Variables.project.info.experiment_ids[0]].resolution.y.value.toFixed(4) : "" }
            }
        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Misc"//"Instrument parameters"
        content: GridLayout {
            columns: 5
            columnSpacing: 15
            rowSpacing: 10
            enabled: false
            Text { text: qsTr("Wavelength") }
            GenericAppElements.TextField {
                text: Specific.Variables.projectOpened ? Specific.Variables.project.experiments[Specific.Variables.project.info.experiment_ids[0]].wavelength.value.toFixed(4) : ""
                units: "\u212B"
            }
            Text {}
            Text { text: qsTr("Zero shift") }
            GenericAppElements.TextField {
                text: Specific.Variables.projectOpened ? Specific.Variables.project.experiments[Specific.Variables.project.info.experiment_ids[0]].offset.value.toFixed(4) : ""
                units: "\u00B0"
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
                text: "Home"
                ToolTip.text: qsTr("Go to the previous step: Home")
                onClicked: {
                    Generic.Variables.toolbarCurrentIndex = Generic.Variables.HomeIndex
                }
            }
            GenericAppContentAreaButtons.GoNext {
                text: "Sample Model"
                ToolTip.text: qsTr("Go to the next step: Sample model")
                onClicked: {
                    Generic.Variables.dataPageFinished = true
                    Generic.Variables.toolbarCurrentIndex = Generic.Variables.SampleModelIndex
                }
            }
            GenericAppContentAreaButtons.SaveState {
            }
            GenericAppContentAreaButtons.Help {
                onClicked: Qt.openUrlExternally("https://easydiffraction.github.io/documentation_use.html#3.2.2.-experimental-data")
            }
            GenericAppContentAreaButtons.Bug {
                onClicked: Qt.openUrlExternally("https://easydiffraction.github.io/contact.html")
            }
        }
    }

}

