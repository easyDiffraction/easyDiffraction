import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons
import easyAnalysis.Logic 1.0 as GenericLogic

Rectangle {
    width: Generic.Variables.mainAreaWidth // fix
    color: "white"

    GenericAppElements.ParametersTable {
        customFrameVisible: false
        anchors.fill: parent
        model: ListModel {
            ListElement { num:1; leftGroup:0; leftParameter:2; leftSign:"="; multiplier:"1.0"; rightSign:"*"; rightGroup:0; rightParameter:4 }
            ListElement { num:2; leftGroup:0; leftParameter:3; leftSign:"="; multiplier:"1.0"; rightSign:"*"; rightGroup:0; rightParameter:5 }
        }
        Controls1.TableViewColumn { role:"num"; title:"No."; resizable: false }

        Controls1.TableViewColumn { role:"leftGroup"; title:"Group"; delegate: GenericAppElements.CellComboBox { currentIndex: styleData.value;
                model: ["CeCuAl3", "Al", "POLARIS", "DREAM"] } }

        Controls1.TableViewColumn { role:"leftParameter"; title:"Parameter"; delegate: GenericAppElements.CellComboBox { currentIndex: styleData.value;
                model: ["a", "c", "Cu1 z", "Cu2 z", "Al1 z", "Al2 z"] } }

        Controls1.TableViewColumn { role:"leftSign"; title:""; resizable: false }

        Controls1.TableViewColumn { role:"multiplier"; title:"Multiplier"; resizable: false }

        Controls1.TableViewColumn { role:"rightSign"; title:""; resizable: false }

        Controls1.TableViewColumn { role:"rightGroup"; title:"Group"; delegate: GenericAppElements.CellComboBox { currentIndex: styleData.value;
                model: ["CeCuAl3", "Al", "POLARIS", "DREAM"] } }

        Controls1.TableViewColumn { role:"rightParameter"; title:"Parameter"; delegate: GenericAppElements.CellComboBox { currentIndex: styleData.value;
                model: ["a", "c", "Cu1 z", "Cu2 z", "Al1 z", "Al2 z"] } }

        Controls1.TableViewColumn { role:"remove"; title:"Remove"; resizable: false }
    }
}

