import QtQuick 2.12
import QtQuick.Controls 2.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.Controls 1.0 as GenericControls
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar
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
            text: "The project has not been saved. Do you want to exit?"
        }

        Row {
            spacing: 15
            anchors.horizontalCenter: parent.horizontalCenter

            GenericAppToolbar.BasicButton {
                text: "Save and exit"
                onClicked: {
                    Generic.Variables.showSaveDialog = 0
                    Generic.Variables.closeAppAfterSaving = 1
                    if (Specific.Variables.projectFilePathSelected) {
                        Generic.Constants.proxy.saveProject()
                        Qt.quit()
                    } else {
                        Generic.Variables.showSaveDialog = 1
                    }
                    dialog.close()
                }
            }

            GenericAppToolbar.BasicButton {
                text: "Exit without saving"
                onClicked: {
                    dialog.close()
                    Qt.quit()
                }
            }
        }
    }
}
