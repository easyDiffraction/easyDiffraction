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

    property bool isFitting: true

    ///////////
    // Groupbox
    ///////////
    /*
    GenericAppElements.GroupBox {
        title: "Jobs"
        collapsible: false
        content: GenericAppElements.ColumnLayout {
            // Table
            GenericAppElements.ParametersTable {
                selectable: true
                model: ListModel {
                    ListElement { num:"1"; name: "POLARIS CeCuAl3" }
                    ListElement { num:"2"; name: "POLARIS CeCuAl3 + Al" }
                    ListElement { num:"3"; name: "POLARIS CeCuAl3 + Al & DREAM CeCuAl3" }
                }
                Controls1.TableViewColumn { role:"num";    title:"No.";  resizable: false }
                Controls1.TableViewColumn { role:"name";   title:"Name" }
                Controls1.TableViewColumn { role:"remove"; title:"Remove"; resizable: false }
            }
        }
    }
    */

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Find"
        enabled: false
        content: GenericAppElements.RowLayout {
            TextField { Layout.fillWidth: true; implicitHeight: 29; placeholderText: "Search text"}
            CheckBox { implicitHeight: 32; checked: true; text: qsTr("Ignore case") }
        }
    }

    /////////
    // Spacer
    /////////
    Item { Layout.fillHeight: true }
}

