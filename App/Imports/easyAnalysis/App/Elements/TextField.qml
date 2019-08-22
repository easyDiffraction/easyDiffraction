import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic

TextField {
    property string units: ""

    id: control
    Layout.fillWidth: true
    implicitWidth: 1
    rightPadding: placeholder.width
    horizontalAlignment: Text.AlignRight
    color: Generic.Style.buttonTextEnabledColor //enabled ? Generic.Style.buttonTextEnabledColor : Generic.Style.buttonTextDisabledColor

    background: Rectangle {
        anchors.fill: parent
        implicitHeight: Generic.Style.tableRowHeight
        color: "white" //enabled ? "white" : Generic.Style.buttonBkgDisabledColor
        border.color: Generic.Style.appBorderColor
        border.width: Generic.Style.appBorderThickness
    }

    PlaceholderText {
        id: placeholder
        x: control.width - width
        anchors.verticalCenter: control.verticalCenter
        leftPadding: dummyText.width
        rightPadding: control.leftPadding
        color: Generic.Style.buttonTextDisabledColor
        text: units
    }

    Text {
        id: dummyText
        visible: false
        text: " "
    }
}
