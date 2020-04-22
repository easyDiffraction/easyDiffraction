import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtQuick.Layouts 1.4

import easyAnalysis 1.0 as Generic
import easyAnalysis.Controls 1.0 as GenericControls

TabButton {
    id: button

    property bool blinking: false
    property int blinkingAnimationDuration: 500
    property int colorAnimationDuration: 250
    property string buttonBorderDisabledColor: Generic.Style.buttonBorderDisabledColor

    property alias toolTipText: toolTip.text

    GenericControls.ToolTip {
        id: toolTip
        visible: text !== "" ? hovered : false
    }

    autoExclusive: true

    width: Generic.Style.toolbarButtonWidth
    font.bold: checked ? true : false

    icon.width: Generic.Style.toolbarButtonHeight / 2
    icon.height: Generic.Style.toolbarButtonHeight / 2
    icon.color: iconColor()
    Behavior on icon.color { ColorAnimation { duration: colorAnimationDuration } }

    ToolTip.visible: ToolTip.text !== "" ? hovered : false

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
        Layout.fillWidth: true
        implicitHeight: Generic.Style.toolbarButtonHeight
        radius: Generic.Style.toolbarButtonRadius
        color: backgroundColor()
        border.color: borderColor()
        Behavior on color { ColorAnimation { duration: colorAnimationDuration } }
        Behavior on border.color { ColorAnimation { duration: colorAnimationDuration } }
    }

    ParallelAnimation {
        running: blinking
        loops: Animation.Infinite
        SequentialAnimation {
            PropertyAnimation { easing.type: Easing.InOutExpo; target: buttonBackground; property: "color"; to: "salmon"; duration: blinkingAnimationDuration }
            PropertyAnimation { easing.type: Easing.InOutExpo; target: buttonBackground; property: "color"; to: backgroundColor(); duration: blinkingAnimationDuration }
        }
        SequentialAnimation {
            PropertyAnimation { easing.type: Easing.InOutExpo; target: buttonBackground; property: "border.color"; to: "salmon"; duration: blinkingAnimationDuration }
            PropertyAnimation { easing.type: Easing.InOutExpo; target: buttonBackground; property: "border.color"; to: borderColor(); duration: blinkingAnimationDuration }
        }
        onFinished: restoreAnimation.restart()
    }

    ParallelAnimation {
        id: restoreAnimation
        running: false
        alwaysRunToEnd: true
        PropertyAnimation { easing.type: Easing.InOutExpo; target: buttonBackground; property: "color"; to: backgroundColor(); duration: blinkingAnimationDuration }
        PropertyAnimation { easing.type: Easing.InOutExpo; target: buttonBackground; property: "border.color"; to: borderColor(); duration: blinkingAnimationDuration }
        PropertyAnimation { easing.type: Easing.InOutExpo; target: buttonIcon; property: "color"; to: textColor(); duration: blinkingAnimationDuration }
        PropertyAnimation { easing.type: Easing.InOutExpo; target: button; property: "icon.color"; to: iconColor(); duration: blinkingAnimationDuration }
    }

    function backgroundColor() {
        const alpha = button.hovered ? (button.down ? 0.25 : 0.15) : 0.0
        if (button.checked) {
            const color1 = Generic.Style.buttonBkgHighlightedColor
            const color2 = Generic.Style.buttonBkgBlendColor
            return Color.blend(color1, color2, alpha)
        }
        if (!button.enabled)
            return Generic.Style.toolbarButtonBkgDisabledColor
        const color1 = Generic.Style.buttonBkgFinishedColor
        const color2 = Generic.Style.buttonBkgBlendColor
        return Color.blend(color1, color2, alpha)
    }

    function borderColor() {
        const alpha = button.hovered ? (button.down ? 0.25 : 0.15) : 0.0
        if (button.checked) {
            const color = Generic.Style.buttonBorderHighlightedColor
            return Color.blend(color, color, alpha)
        }
        if (!button.enabled)
            return Generic.Style.buttonBorderDisabledColor
        const color = Generic.Style.buttonBorderFinishedColor
        return Color.blend(color, color, alpha)
    }

    function iconColor() {
        if (blinking)
            return Generic.Style.buttonIconHighlightedColor
        if (button.checked)
            return Generic.Style.buttonIconHighlightedColor
        if (!button.enabled)
            return Generic.Style.buttonIconDisabledColor
        return Generic.Style.buttonIconFinishedColor
    }

    function textColor() {
        if (blinking)
            return Generic.Style.buttonTextHighlightedColor
        if (button.checked)
            return Generic.Style.buttonTextHighlightedColor
        if (!button.enabled)
            return Generic.Style.buttonTextDisabledColor
        return Generic.Style.buttonTextFinishedColor
    }

}
