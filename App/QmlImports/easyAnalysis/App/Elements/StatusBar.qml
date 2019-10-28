import QtQuick 2.12
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements

ColumnLayout {
    width: parent.width
    height: Generic.Style.statusBarHeight
    GenericAppElements.HorizontalBorder {}
    Rectangle {
        Layout.fillWidth: true
        height: Generic.Style.statusBarHeight
        color: Generic.Style.appBkgColor
        RowLayout {
            anchors.fill: parent
//            height: Generic.Style.statusBarHeight
            anchors.leftMargin: Generic.Style.toolbarSpacing
            anchors.rightMargin: Generic.Style.toolbarSpacing
            anchors.bottomMargin: 4
            Rectangle {
                Layout.fillWidth: true
                height: parent.height
                color:  Generic.Style.appBkgColor
                Text {
                    id: statusBarText
                    height: parent.height
                    color: Generic.Style.sidebarGroupTitleDisabledColor
                    text: "Placeholder Text"
                    verticalAlignment: Text.AlignVCenter
                }
            }
        }
    }
}
