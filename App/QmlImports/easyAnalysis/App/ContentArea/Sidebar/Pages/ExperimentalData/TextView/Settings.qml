import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import easyAnalysis.Controls 1.0 as GenericControls

import easyAnalysis.App.Elements 1.0 as GenericAppElements

ColumnLayout {
    spacing: 0

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "View settings"
        //enabled: false
        content: GenericAppElements.GridLayout {
            columns: 2
            GenericAppElements.CheckBox { checked:false; text:qsTr("Highlight syntax"); GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet } }
            GenericAppElements.CheckBox { checked:false; text:qsTr("Wrap text"); GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet } }
       }
    }

    /////////
    // Spacer
    /////////
    Item { Layout.fillHeight: true }
}
