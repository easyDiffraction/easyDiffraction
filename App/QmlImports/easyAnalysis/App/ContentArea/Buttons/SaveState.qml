import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyDiffraction 1.0 as Specific

GenericAppContentArea.Button {
    id: button

    enabled: Specific.Variables.needToSave

    Layout.fillWidth: false
    implicitWidth: implicitHeight

    checkable: false
    checked: true

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
        implicitHeight: Generic.Style.toolbarButtonHeight
        color: backgroundColor()
        border.color: borderColor()
        radius: Generic.Style.toolbarButtonRadius
    }

    onClicked: {
        Generic.Variables.showSaveDialog = 0
        if (Specific.Variables.projectFilePathSelected) {
            Generic.Constants.proxy.saveProject()
        } else {
            Generic.Variables.showSaveDialog = 1
        }
    }

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
            return Generic.Style.toolbarButtonBkgDisabledColor
        var color1 = button.checked ? "salmon" : Generic.Style.toolbarButtonBkgEnabledColor
        var color2 = Generic.Style.toolbarButtonBkgBlendColor
        var alpha = button.down ? Generic.Style.buttonBkgBlendAlpha : 0.0
        return Color.blend(color1, color2, alpha)
    }
}


