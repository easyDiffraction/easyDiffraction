import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtQuick.Layouts 1.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.Controls 1.0 as GenericControls
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea

Button {
    id: button

    property bool attention: false
    property int colorAnimationDuration: 250
    property alias toolTipText: toolTip.text

    Layout.fillWidth: false
    implicitWidth: implicitHeight

    checkable: false

    icon.width: Generic.Style.buttonHeight / 1.75
    icon.height: Generic.Style.buttonHeight / 1.75
    icon.color: iconColor()
    //Behavior on icon.color { ColorAnimation { duration: colorAnimationDuration } } // get wrong color if frequintly changes (e.g. as in canUndo)

    GenericControls.ToolTip {
        id: toolTip
        visible: text !== "" ? hovered : false
    }

    background: Rectangle {
        implicitHeight: Generic.Style.toolbarButtonHeight
        color: backgroundColor()
        border.color: borderColor()
        radius: height * 0.5
    }

    function iconColor() {
        if (!button.enabled)
            return Generic.Style.buttonIconDisabledColor
        return button.attention ? Generic.Style.buttonBkgAttentionColor : Generic.Style.buttonIconEnabledColor
    }

    function borderColor() {
        if (!button.enabled)
            return Generic.Style.toolbarBkgColor
        return Generic.Style.toolbarBkgColor
    }

    function backgroundColor() {
        if (!button.enabled)
            return Generic.Style.toolbarBkgColor
        var color1 = Generic.Style.toolbarBkgColor
        var color2 = "white"
        var alpha = button.hovered ? (button.down ? 0.75 : 0.50) : 0.0
        return Color.blend(color1, color2, alpha)
    }
}

