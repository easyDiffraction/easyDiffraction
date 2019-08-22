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

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Data Explorer"
        collapsible: false
        content: GenericAppElements.ColumnLayout {
            // Table
            GenericAppElements.ParametersTable {
                selectable: true
                selectedRow: 1
                model: ListModel {
                    ListElement { num:"1"; fname: "cecual_polaris.dat"; fpath:"~/Experiments/ISIS/2019-01/cecual/" }
                    ListElement { num:"2"; fname: "cecual_dream.dat";   fpath:"~/Experiments/ESS/2019-03/cecual/" }
                    ListElement { num:"3"; fname: "cecual_d2b.dat";     fpath:"~/Experiments/ILL/2018-11/cecual/" }
                    ListElement { num:"4"; fname: "cecual_01_test.dat"; fpath:"~/Experiments/Test/2018-03/cecual/" }
                    ListElement { num:"5"; fname: "cecual_02_test.dat"; fpath:"~/Experiments/Test/2018-03/cecual/" }
                    ListElement { num:"6"; fname: "cecual_03_test.dat"; fpath:"~/Experiments/Test/2018-03/cecual/" }
                    ListElement { num:"7"; fname: "cecual_04_test.dat"; fpath:"~/Experiments/Test/2018-03/cecual/" }
                }
                Controls1.TableViewColumn { role:"num";    title:"No.";  resizable: false }
                Controls1.TableViewColumn { role:"fname";  title:"Name"; resizable: false }
                Controls1.TableViewColumn { role:"fpath";  title:"Path" }
                Controls1.TableViewColumn { role:"remove"; title:"Remove"; resizable: false }
            }

            // Buttons
            GenericAppElements.GridLayout {
                columns: 2

                GenericAppContentAreaButtons.Import { id: importButton; text: "Import data from local drive"; }
                GenericAppContentAreaButtons.Link { text: "Link to data on local drive"; }
                GenericAppContentAreaButtons.Cloud { id: cloudButton; text: "Import data from SciCat" }
                GenericAppContentAreaButtons.RemoveAll { text: "Remove all data" }
            }
        }
    }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Metadata"
        collapsed: true
        content: GenericAppElements.ColumnLayout {
            Text { text: "To be added" }
        }
    }

    /////////
    // Spacer
    /////////
    Item { Layout.fillHeight: true }

    ///////////
    // Groupbox
    ///////////
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

}

