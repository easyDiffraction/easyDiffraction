import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea

GenericAppContentArea.Button {
    id: button

    enabled: false // Disable until properly implemented

    Layout.fillWidth: false
    implicitWidth: implicitHeight

    checkable: true
    checked: false

    icon.source: Generic.Variables.thirdPartyIconsPath + "save.svg"
    ToolTip.text: qsTr("Save current state of the project")

    contentItem: IconLabel {
        spacing: button.spacing
        mirrored: button.mirrored
        display: button.display
        icon: button.icon
        text: button.text
        font: button.font
        color: textColor() //button.enabled ? Generic.Style.buttonTextEnabledColor : Generic.Style.buttonTextDisabledColor
    }

    background: Rectangle {
        implicitHeight: Generic.Style.buttonHeight
        color: backgroundColor()
        border.color: borderColor()
        radius: Generic.Style.toolbarButtonRadius
    }

    onClicked: checked = false

    function iconColor() {
        if (!button.enabled)
            return Generic.Style.buttonIconDisabledColor
        return button.checked ? Generic.Style.buttonIconHighlightedColor : Generic.Style.buttonIconEnabledColor
    }

    function borderColor() {
        if (!button.enabled)
            return Generic.Style.appBorderColor
        return button.checked ? "salmon" : Generic.Style.appBorderColor
    }

    function backgroundColor() {
        if (!button.enabled)
            return Generic.Style.buttonBkgDisabledColor
        var color1 = button.checked ? "salmon" : Generic.Style.buttonBkgEnabledColor
        var color2 = Generic.Style.buttonBkgBlendColor
        var alpha = button.down ? Generic.Style.buttonBkgBlendAlpha : 0.0
        return Color.blend(color1, color2, alpha)
    }
}

