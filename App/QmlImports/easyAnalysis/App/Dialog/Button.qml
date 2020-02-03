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

    property string buttonBorderDisabledColor: Generic.Style.buttonBorderDisabledColor

    autoExclusive: true

    icon.width: Generic.Style.toolbarButtonHeight / 2
    icon.height: Generic.Style.toolbarButtonHeight / 2
    icon.color: Generic.Style.buttonIconHighlightedColor

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
        color: Generic.Style.buttonTextHighlightedColor
    }

    background: Rectangle {
        id: buttonBackground
        Layout.fillWidth: true
        implicitHeight: Generic.Style.toolbarButtonHeight
        radius: Generic.Style.toolbarButtonRadius
        color: Generic.Style.buttonBkgHighlightedColor
        border.color: Generic.Style.buttonBorderHighlightedColor
    }
}
