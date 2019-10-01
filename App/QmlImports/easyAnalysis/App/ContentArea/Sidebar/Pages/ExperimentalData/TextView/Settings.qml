import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis.App.Elements 1.0 as GenericAppElements

ColumnLayout {
    spacing: 0

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "View settings"
        content: GenericAppElements.GridLayout {
            columns: 2
            GenericAppElements.CheckBox { checked:false; text:qsTr("Highlight syntax") }
            GenericAppElements.CheckBox { checked:false; text:qsTr("Wrap text") }
        }
    }

    /////////
    // Spacer
    /////////
    Item { Layout.fillHeight: true }

}
