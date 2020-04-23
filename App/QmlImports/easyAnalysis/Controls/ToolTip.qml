import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtQuick.Templates 2.12 as T

T.ToolTip {
    id: control

    property color textColor: Qt.darker("grey", 1.95)//control.palette.toolTipText
    property color backgroundColor: Qt.lighter("grey", 1.95)//control.palette.toolTipBase
    property color borderColor: Qt.lighter("grey", 1.65)//control.palette.dark
    property real backgroundOpacity: 0.95

    x: parent ? (parent.width - implicitWidth) / 2 : 0
    y: -implicitHeight - 3

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset,
                            contentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             contentHeight + topPadding + bottomPadding)

    margins: 6
    padding: 6

    closePolicy: T.Popup.CloseOnEscape | T.Popup.CloseOnPressOutsideParent | T.Popup.CloseOnReleaseOutsideParent

    contentItem: TextEdit {
        readOnly: true
        text: control.text
        font: control.font
        wrapMode: Text.Wrap
        color: textColor
    }

    background: Rectangle {
        border.color: borderColor
        color: backgroundColor
        opacity: backgroundOpacity
    }

    enter: Transition {
        // toast_enter
        NumberAnimation { property: "opacity"; from: 0.0; to: 1.0; easing.type: Easing.OutQuad; duration: 500 }
    }

    exit: Transition {
        // toast_exit
        NumberAnimation { property: "opacity"; from: 1.0; to: 0.0; easing.type: Easing.InQuad; duration: 500 }
    }
}
