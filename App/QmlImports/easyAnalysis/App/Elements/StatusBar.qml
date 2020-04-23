import QtQuick 2.12
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyDiffraction 1.0 as Specific

ColumnLayout {
    visible: !Generic.Variables.HomeIndex
    spacing: 0

    GenericAppElements.HorizontalBorder {}

    ListView {
        height: Generic.Style.statusBarHeight
        Layout.fillWidth: true
        Layout.leftMargin: Generic.Style.toolbarSpacing
        Layout.rightMargin: Generic.Style.toolbarSpacing
        interactive: false

        orientation: ListView.Horizontal
        spacing: 20

        model: Specific.Variables.statusInfo

        visible: model !== null

        delegate: Rectangle {
            width: childrenRect.width
            height: parent.height
            color: 'transparent'

            Row {
                height: parent.height
                spacing: 5

                Text {
                    height: parent.height
                    verticalAlignment: Text.AlignVCenter
                    font.family: Generic.Style.fontFamily
                    font.pointSize: Generic.Style.fontPointSize - 1
                    color: Generic.Style.buttonTextDisabledColor
                    text: label + ":"
                }
                Text {
                    height: parent.height
                    verticalAlignment: Text.AlignVCenter
                    font.family: Generic.Style.fontFamily
                    font.pointSize: Generic.Style.fontPointSize - 1
                    color: Generic.Style.buttonTextDisabledColor
                    text: value
                }
            }
        }
    }
}
