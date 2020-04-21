import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtQuick.Layouts 1.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea

GenericAppContentArea.Button {
    id: button

    property bool attention: false

    Layout.fillWidth: false
    implicitWidth: implicitHeight

    checkable: false

    contentItem: IconLabel {
        spacing: button.spacing
        mirrored: button.mirrored
        display: button.display
        icon: button.icon
        text: button.text
        font: button.font
        color: iconColor()
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

