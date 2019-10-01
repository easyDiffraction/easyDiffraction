import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea

Item {
    implicitHeight: Generic.Style.tableRowHeight
    implicitWidth: implicitHeight

    GenericAppContentArea.Button {
        id: button
        anchors.fill: parent
        anchors.margins: 2
        anchors.leftMargin: 3
        anchors.rightMargin: 4
        padding: 0
        icon.source: Generic.Variables.thirdPartyIconsPath + "minus-circle.svg"
        ToolTip.text: qsTr("Remove this row from the table")
    }
}
