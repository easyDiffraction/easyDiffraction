import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons
import easyAnalysis.Logic 1.0 as GenericLogic

ColumnLayout {
    spacing: 0


    ////////////////////////
    // Check if data changed
    ////////////////////////

    Text {
        id: dataChanged
        visible: false
        text: proxy.time_stamp
        onTextChanged: {
            print("Time stamp: ", proxy.time_stamp)

            // Update Parameters

            // dataExplorerTable
            dataExplorerTable.model.clear()
            dataExplorerTable.model.append({
                'num':"1",
                'fname':proxy.tmp_rcif_file_name(),
                'fdir':proxy.tmp_rcif_dir_name()
            })

            // instrument parameters
            wavelength.text = proxy.tmp_setup_wavelength()
            u.text = proxy.tmp_setup_resolution_u()
            x.text = proxy.tmp_setup_resolution_x()
            zeroShift.text = proxy.tmp_setup_zero_shift()
            v.text = proxy.tmp_setup_resolution_v()
            y.text = proxy.tmp_setup_resolution_y()
            w.text = proxy.tmp_setup_resolution_w()
        }
    }


    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Data Explorer"
        collapsible: false
        content: GenericAppElements.ColumnLayout {
            // Table
            GenericAppElements.ParametersTable {
                id: dataExplorerTable
                selectable: false
                //selectedRow: 1
                enabled: false

                model: ListModel {
                    ListElement { num:""; fname:"0123456789"; fdir:"" }
                }

                Controls1.TableViewColumn { role:"num";    title:"No.";  resizable: false }
                Controls1.TableViewColumn { role:"fname";  title:"File"; resizable: false }
                Controls1.TableViewColumn { role:"fdir";   title:"Directory" }
                Controls1.TableViewColumn { role:"remove"; title:"Remove"; resizable: false }
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

    ///////////
    // Groupbox
    ///////////
    /*
    GenericAppElements.GroupBox {
        title: "Metadata"
        collapsed: true
        enabled: false
        content: GenericAppElements.ColumnLayout {
            Text { text: "To be added" }
        }
    }
    */

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Instrument"//"Diffractometer"
        content: GenericAppElements.ColumnLayout {
            GenericAppElements.GridLayout {
                //enabled: false
                columns: 3
                rowSpacing: 2

                Text { text: "Facility           "; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }
                Text { text: "Instrument    "; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }
                Text { text: "Configuration"; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }
                GenericAppElements.ComboBox { currentIndex: 5; model: ["ESS", "ISIS", "SNS", "ILL", "MLZ", "LLB", "Custom"] }
                //GenericAppElements.ComboBox { currentIndex: 6; model: ["BEER", "D2B", "DREAM", "HEIMDAL", "MAGiC", "POLARIS", "6T2", "Custom neutron", "Custom X-ray"] }
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

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Peak profile"
        content: GenericAppElements.ColumnLayout {
            spacing: 12
            //enabled: false
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
                Text { text: qsTr("U") } // https://wiki-ext.aps.anl.gov/ug11bm/index.php/GSAS_Profile_Terms
                GenericAppElements.TextField { id: u }
                Text {}
                Text { text: qsTr("V") }
                GenericAppElements.TextField { id: v }
                Text {}
                Text { text: qsTr("W") }
                GenericAppElements.TextField { id: w }
                // Row
                Text { text: qsTr("X") }
                GenericAppElements.TextField { id: x }
                Text {}
                Text { text: qsTr("Y") }
                GenericAppElements.TextField { id: y }
                //Text {}
                //Text { text: qsTr("Z") }
                //GenericAppElements.TextField { id: z }
            }
        }
    }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Misc"//"Instrument parameters"
        content: GridLayout {
            columns: 5
            columnSpacing: 15
            rowSpacing: 10
            enabled: false
            // Row
            Text { text: qsTr("Wavelength") }
            GenericAppElements.TextField { id: wavelength; units: "\u212B" }
            Text {}
            Text { text: qsTr("Zero shift") }
            GenericAppElements.TextField { id: zeroShift; units: "\u00B0" }
        }
    }

    /////////
    // Spacer
    /////////
    Item { Layout.fillHeight: true }

    ///////////
    // Groupbox
    ///////////
    /*
    GenericAppElements.GroupBox {
        collapsible: false
        showBorder: false
        content: GenericAppElements.RowLayout {
            GenericAppContentAreaButtons.GoNext {
                text: "Next step: Instrument Model"
                ToolTip.text: qsTr("Go to the next step: Instrument Model description")
                onClicked: {
                    Generic.Variables.dataPageFinished = true
                    Generic.Variables.toolbarCurrentIndex = Generic.Variables.InstrumentModelIndex
                }
            }
            GenericAppContentAreaButtons.SaveState {}
            GenericAppContentAreaButtons.Help {}
            GenericAppContentAreaButtons.Bug {}
        }
    }
    */

    ///////////
    // Groupbox
    ///////////
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

