import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtQuick.Templates 2.12 as T

T.ToolTip {
    id: control

    property color textColor: control.palette.toolTipText
    property color backgroundColor: control.palette.toolTipBase
    property color borderColor: control.palette.dark
    property real backgroundOpacity: 1.0

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
        text: control.text
        font: control.font
        wrapMode: Text.Wrap
        color: textColor
    }

    background: Rectangle {
        border.color: borderColor
        color: backgroundColor
    }
}
