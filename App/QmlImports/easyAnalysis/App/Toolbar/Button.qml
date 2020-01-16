import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtQuick.Layouts 1.4
import easyAnalysis 1.0 as Generic

TabButton {
    id: button

    property bool blinking: false
    property int blinkingAnimationDuration: 500
    property int colorAnimationDuration: 250

    autoExclusive: true

    icon.width: Generic.Style.toolbarButtonHeight / 2
    icon.height: Generic.Style.toolbarButtonHeight / 2
    icon.color: iconColor()
    Behavior on icon.color { ColorAnimation { duration: colorAnimationDuration } }

    ToolTip.visible: ToolTip.text !== "" ? hovered : false

    width: Generic.Style.toolbarButtonWidth

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
        if (!button.enabled)
            return Generic.Style.toolbarButtonBkgDisabledColor
        var color1 = button.checked ? Generic.Style.buttonBkgHighlightedColor : Generic.Style.buttonBkgFinishedColor
        var color2 = Generic.Style.buttonBkgBlendColor
        var alpha = button.down ? Generic.Style.buttonBkgBlendAlpha : 0.0
        return Color.blend(color1, color2, alpha)
    }

    function borderColor() {
        if (!button.enabled)
            return Generic.Style.buttonBorderDisabledColor
        if (button.checked)
            return Generic.Style.buttonBorderHighlightedColor
        return Generic.Style.buttonBorderFinishedColor
    }

    function iconColor() {
        if (blinking)
            return Generic.Style.buttonIconHighlightedColor
        if (!button.enabled)
            return Generic.Style.buttonIconDisabledColor
        if (button.checked)
            return Generic.Style.buttonIconHighlightedColor
        return Generic.Style.buttonIconFinishedColor
    }

    function textColor() {
        if (blinking)
            return Generic.Style.buttonTextHighlightedColor
        if (!button.enabled)
            return Generic.Style.buttonTextDisabledColor
        if (button.checked)
            return Generic.Style.buttonTextHighlightedColor
        return Generic.Style.buttonTextFinishedColor
    }

}
