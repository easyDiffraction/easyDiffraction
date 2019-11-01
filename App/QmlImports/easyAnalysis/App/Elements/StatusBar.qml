import QtQuick 2.12
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyDiffraction 1.0 as Specific

ColumnLayout {
    width: parent.width
    height: Generic.Style.statusBarHeight

    GenericAppElements.HorizontalBorder {}

    ListView {
        id: contentStatusListView

        height: Generic.Style.statusBarHeight - Generic.Style.appBorderThickness
        Layout.fillWidth: true
        Layout.leftMargin: Generic.Style.toolbarSpacing
        Layout.rightMargin: Generic.Style.toolbarSpacing
        Layout.bottomMargin: 4

        orientation: ListView.Horizontal
        spacing: 20

        model: Specific.Variables.projectOpened ? proxy.statusInfo : null

        delegate: Rectangle {
            id: contentRow
            width: childrenRect.width
            height: parent.height
            color: 'transparent'

            Row {
                height: parent.height
                spacing: 5

                Text {
                    height: parent.height
                    verticalAlignment: Text.AlignVCenter
                    color: Generic.Style.buttonTextDisabledColor
                    text: label
                }
                Text {
                    height: parent.height
                    verticalAlignment: Text.AlignVCenter
                    color: Generic.Style.buttonTextDisabledColor
                    text: value
                }
            }
        }
    }
}
