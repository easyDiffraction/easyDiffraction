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
            GenericAppElements.CheckBox { checked:true;  text:qsTr("Show experimental data"); GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NoEditingYet } }
            GenericAppElements.CheckBox { checked:true;  text:qsTr("Show difference plot"); GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NoEditingYet } }
            //GenericAppElements.CheckBox { checked:false; text:qsTr("Show Bragg positions") }
            GenericAppElements.CheckBox { checked:false; text:qsTr("Show legend"); GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NoEditingYet } }
            //GenericAppElements.CheckBox { Layout.fillWidth:true; checked:true;  text:qsTr("Display coordinate system") }
        }
    }

    /////////
    // Spacer
    /////////
    Item { Layout.fillHeight: true }

}

