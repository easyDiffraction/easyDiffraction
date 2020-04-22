import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtQuick.Controls.impl 2.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.Controls 1.0 as GenericControls

Button {
    id: button

    property bool fillWidthEqually: false
    property bool blinking: false
    property int colorAnimationDuration: 250
    property alias toolTipText: toolTip.text

    Layout.fillWidth: true
    implicitWidth: 1

    font.bold: enabled && highlighted ? true : false

    icon.width: Generic.Style.buttonHeight / 1.75
    icon.height: Generic.Style.buttonHeight / 1.75
    icon.color: iconColor()
    Behavior on icon.color { ColorAnimation { duration: colorAnimationDuration } }

    //ToolTip.visible: ToolTip.text !== "" ? hovered : false

    GenericControls.ToolTip {
        id: toolTip
        visible: text !== "" ? hovered : false
    }

    contentItem: IconLabel {
        id: buttonIcon
        spacing: button.spacing
        mirrored: button.mirrored
        display: button.display
        icon: button.icon
        text: button.text
        font: button.font
        color: textColor()
        Behavior on color { ColorAnimation { duration: colorAnimationDuration } }
    }

    background: Rectangle {
        id: buttonBackground
        implicitHeight: Generic.Style.buttonHeight
        color: backgroundColor()
        border.color: borderColor()
        radius: Generic.Style.toolbarButtonRadius
        Behavior on color { ColorAnimation { duration: colorAnimationDuration } }
        Behavior on border.color { ColorAnimation { duration: colorAnimationDuration } }
    }

    Component.onCompleted: {
        if (fillWidthEqually) {
            button.Layout.fillWidth = true
            implicitWidth = 1
        }
    }

    function backgroundColor() {
        if (!button.enabled)
            return Generic.Style.buttonBkgDisabledColor
        const color1 = button.highlighted ? Generic.Style.buttonBkgHighlightedColor : Generic.Style.buttonBkgEnabledColor
        const color2 = Generic.Style.buttonBkgBlendColor
        const alpha = button.hovered ? (button.down ? 0.3 : 0.15) : 0.0
        return Color.blend(color1, color2, alpha)
    }

    function borderColor() {
        if (!button.enabled)
            return Generic.Style.appBorderColor
        const color = button.highlighted ? Generic.Style.buttonBkgHighlightedColor : Generic.Style.buttonBorderEnabledColor
        const alpha = button.hovered ? (button.down ? 0.0 : 0.45) : 0.9
        return Color.blend(color, color, alpha)
    }

    function iconColor() {
        if (!button.enabled)
            return Generic.Style.buttonIconDisabledColor
        return button.highlighted ? Generic.Style.buttonIconHighlightedColor : Generic.Style.buttonIconEnabledColor
    }

    function textColor() {
        if (!button.enabled)
            return Generic.Style.buttonTextDisabledColor
        return button.highlighted ? Generic.Style.buttonTextHighlightedColor : Generic.Style.buttonTextEnabledColor
    }

    ParallelAnimation {
        running: blinking
        alwaysRunToEnd: true
        loops: Animation.Infinite
        SequentialAnimation {
            PropertyAnimation { target: buttonBackground; property: "color"; to: "#f08c82"; duration: 500 }
            PropertyAnimation { target: buttonBackground; property: "color"; to: backgroundColor(); duration: 500 }
        }
        SequentialAnimation {
            PropertyAnimation { target: buttonBackground; property: "border.color"; to: "#f08c82"; duration: 500 }
            PropertyAnimation { target: buttonBackground; property: "border.color"; to: borderColor(); duration: 500 }
        }
    }
}
