import QtQuick 2.12
import QtQuick.Controls 2.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.Controls 1.0 as GenericControls
import easyAnalysis.App.Dialog 1.0 as GenericAppDialog
import easyDiffraction 1.0 as Specific

GenericControls.Dialog {
    id: dialog
    title: "Save Changes"

    Column {
        padding: 20
        spacing: 30

        Text {
            font.pointSize: Generic.Style.fontPointSize
            font.family: Generic.Style.fontFamily
            color: "#444"
            anchors.horizontalCenter: parent.horizontalCenter
            text: "The project has not been saved. Do you want to load another one?"
        }

        Row {
            spacing: 15
            anchors.horizontalCenter: parent.horizontalCenter

            GenericAppDialog.Button {
                text: "Cancel"
                onClicked: dialog.reject()
            }

            GenericAppDialog.Button {
                text: "Load without saving"
                onClicked: dialog.accept()
            }
        }
    }
}
