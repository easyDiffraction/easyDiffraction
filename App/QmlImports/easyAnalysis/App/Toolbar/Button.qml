import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtQuick.Layouts 1.4
import easyAnalysis 1.0 as Generic

TabButton {
    //property bool withSeparator: false
    ///property bool finished: false

    property bool blinking: false


    id: button
    //leftPadding: withSeparator ? 20 : 0
    ///rightPadding: withSeparator ? 20 : 0

    checkable: true


    //implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset +  100 ,
    //                        implicitContentWidth + leftPadding + rightPadding +  100 )

    autoExclusive: true


    icon.width: Generic.Style.toolbarButtonHeight / 2
    icon.height: Generic.Style.toolbarButtonHeight / 2
    icon.color: iconColor() //button.enabled ? Generic.Style.buttonIconEnabledColor : Generic.Style.buttonIconDisabledColor

    ToolTip.visible: ToolTip.text !== "" ? hovered : false

    contentItem: /*RowLayout {
        spacing: 10
        Rectangle {
            width: 10; //withSeparator ? 10 : 0
            height: 10
            color: "green"
            visible: withSeparator
        }*/
        IconLabel {
        id: buttonIcon
        spacing: button.spacing
        mirrored: button.mirrored
        display: button.display
        icon: button.icon
        text: button.text
        font: button.font
        color: textColor() //button.enabled ? Generic.Style.buttonTextEnabledColor : Generic.Style.buttonTextDisabledColor
    }
    //}

    background: /*RowLayout {
        id: lay
        //width: rect.implicitWidth + 50
        spacing: 10
        Rectangle {
            width: 10; //withSeparator ? 10 : 0
            height: 10
            color: "blue"
            visible: withSeparator
        }*/
        Rectangle {
            id: buttonBackground
            Layout.fillWidth: true
            implicitHeight: Generic.Style.toolbarButtonHeight
            color: backgroundColor()
            border.color: borderColor()
            radius: Generic.Style.toolbarButtonRadius
        }

        //Component.onCompleted: {
            //lay.width += withSeparator ? 10 : 0
        //}
    //}

    function backgroundColor() {
        if (!button.enabled)
            return Generic.Style.buttonBkgDisabledColor
        var color1 = button.checked ? Generic.Style.buttonBkgHighlightedColor : Generic.Style.buttonBkgFinishedColor
        //var color1 = button.finished ? Generic.Style.buttonBkgFinishedColor : Generic.Style.buttonBkgEnabledColor
        //if (button.checked)
        //    color1 = Generic.Style.buttonBkgHighlightedColor
        var color2 = Generic.Style.buttonBkgBlendColor
        var alpha = button.down ? Generic.Style.buttonBkgBlendAlpha : 0.0
        return Color.blend(color1, color2, alpha)
    }

    function iconColor() {
        if (blinking)
            return Generic.Style.buttonIconHighlightedColor
        if (!button.enabled)
            return Generic.Style.buttonIconDisabledColor
        //if (button.finished)
        //    return Generic.Style.buttonIconFinishedColor
        if (button.checked)
            return Generic.Style.buttonIconHighlightedColor
        return Generic.Style.buttonIconFinishedColor
    }

    function textColor() {
        if (blinking)
            return Generic.Style.buttonTextHighlightedColor
        if (!button.enabled)
            return Generic.Style.buttonTextDisabledColor
        //if (button.finished)
        //    return Generic.Style.buttonTextFinishedColor
        if (button.checked)
            return Generic.Style.buttonTextHighlightedColor
        return Generic.Style.buttonTextFinishedColor
    }

    function borderColor() {
        if (!button.enabled)
            return Generic.Style.buttonBorderDisabledColor
        //if (button.finished)
        //    return Generic.Style.buttonBorderFinishedColor
        if (button.checked)
            return Generic.Style.buttonBorderHighlightedColor
        return Generic.Style.buttonBorderFinishedColor
    }

    ParallelAnimation {
        running: blinking
        loops: Animation.Infinite
        SequentialAnimation {
            PropertyAnimation { target: buttonBackground; property: "color"; to: "#f08c82"; duration: 500 }
            PropertyAnimation { target: buttonBackground; property: "color"; to: backgroundColor(); duration: 500 }
        }
        SequentialAnimation {
            PropertyAnimation { target: buttonBackground; property: "border.color"; to: "#f08c82"; duration: 500 }
            PropertyAnimation { target: buttonBackground; property: "border.color"; to: borderColor(); duration: 500 }
        }
        onFinished: restoreAnimation.restart()
    }

    ParallelAnimation {
        id: restoreAnimation
        alwaysRunToEnd: true
        PropertyAnimation { target: buttonBackground; property: "color"; to: backgroundColor(); duration: 500 }
        PropertyAnimation { target: buttonBackground; property: "border.color"; to: borderColor(); duration: 500 }
        PropertyAnimation { target: buttonIcon; property: "color"; to: textColor(); duration: 500 }
        PropertyAnimation { target: button; property: "icon.color"; to: iconColor(); duration: 500 }
    }
}


