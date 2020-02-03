import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtQuick.Layouts 1.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea

GenericAppContentArea.Button {
    id: button

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
        color: textColor()
    }

    background: Rectangle {
        implicitHeight: Generic.Style.toolbarButtonHeight
        color: backgroundColor()
        border.color: borderColor()
        radius: Generic.Style.toolbarButtonRadius
    }

    function iconColor() {
        if (!button.enabled)
            return Generic.Style.buttonIconDisabledColor
        return button.checked ? Generic.Style.buttonIconHighlightedColor : Generic.Style.buttonIconEnabledColor
    }

    function borderColor() {
        if (!button.enabled)
            return Generic.Style.appBorderColor
        return Generic.Style.appBorderColor
    }

    function backgroundColor() {
        if (!button.enabled)
            return Generic.Style.toolbarButtonBkgDisabledColor
        var color1 = Generic.Style.toolbarButtonBkgEnabledColor
        var color2 = Generic.Style.toolbarButtonBkgBlendColor
        var alpha = button.down ? Generic.Style.buttonBkgBlendAlpha : 0.0
        return Color.blend(color1, color2, alpha)
    }
}

