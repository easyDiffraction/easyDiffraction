import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Layouts 1.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.Controls 1.0 as GenericControls
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons

import easyDiffraction 1.0 as Specific

ColumnLayout {
    spacing: 0

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Find"
        //enabled: false
        content: GenericAppElements.RowLayout {
            TextField { Layout.fillWidth: true; implicitHeight: 29; placeholderText: "Search text";  GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NoEditingYet }}
            CheckBox { implicitHeight: 32; checked: true; text: qsTr("Ignore case");  GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet } }
        }
    }

    /////////
    // Spacer
    /////////
    Item { Layout.fillHeight: true }
}

