import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtGraphicalEffects 1.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements

Dialog {
    id: dialog

    property int animationDuration: 200
    property real initialDimmedAreaTransparency: 0.5
    property string dimmedAreaColor: "black"
    property string dialogBackgroundColor: "#efefef"
    property string headerBackgroundColor: "#ddd"
    property string headerBorderColor: "#ccc"

    parent: Overlay.overlay
    anchors.centerIn: parent
    modal: true
    dim: false // dimming is done via 'hiddenPopup'
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    // Background properties
    background: Rectangle {
        color: dialogBackgroundColor
    }

    // Header dialog area
    header: Column {

        // Header area
        TextArea {
            width: parent.width
            height: Generic.Style.toolbarButtonHeight
            leftPadding: font.pixelSize * 0.75
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            readOnly: true
            background: Rectangle { color: headerBackgroundColor }
            font.family: Generic.Style.fontFamily
            font.pixelSize: Generic.Style.fontPixelSize + 1
            text: dialog.title

            // Exit button
            Button {
                width: parent.height
                height: parent.height
                anchors.right: parent.right
                flat: true
                text: "\u2715" // cross
                onClicked: dialog.close()
            }
        }

        // Bottom header border
        Rectangle {
            width: parent.width
            height: Generic.Style.appBorderThickness
            color: headerBorderColor
        }
    }

    // Enter animation
    enter: Transition {
        SequentialAnimation {
            PropertyAction { target: hiddenPopup; property: "visible"; value: true }
            ParallelAnimation {
                NumberAnimation { target: hiddenPopup; easing.type: Easing.OutExpo; property: "dimmedAreaTransparency";
                    from: 0.0; to: initialDimmedAreaTransparency; duration: animationDuration }
                NumberAnimation { target: dialog; easing.type: Easing.OutBack; property: "scale";
                    from: 0.0; to: 1.0; duration: animationDuration }
            }
        }
    }

    // Exit animation
    exit: Transition {
        SequentialAnimation {
            ParallelAnimation {
                NumberAnimation { target: dialog; easing.type: Easing.InBack; property: "scale";
                    from: 1.0; to: 0.0; duration: animationDuration }
                NumberAnimation { target: hiddenPopup; easing.type: Easing.InExpo; property: "dimmedAreaTransparency";
                    from: initialDimmedAreaTransparency; to: 0.0; duration: animationDuration }
            }
            PropertyAction { target: hiddenPopup; property: "visible"; value: false }
        }
    }

    // Exit animation of the out-of-dialog dimmed area transparency is implemented via
    // additional hidden Popup element 'hiddenPopup'. It is needed to sync the scale
    // animation of the main dialog and transparency animation on the out-of-dialog dimmed
    // area created by the hiddenPopup element.
    Popup {
        id: hiddenPopup

        z: -1       // it should be below the main 'dialog'
        width: 0    // and
        height: 0   // invisible

        parent: Overlay.overlay
        modal: true
        closePolicy: Popup.NoAutoClose

        // Out-of-dialog dimmed area
        property real dimmedAreaTransparency
        Overlay.modal: Rectangle {
            anchors.fill: parent
            color: Color.transparent(dimmedAreaColor, dimmedAreaTransparency)
        }

        // Reset show preferences global variable
        onClosed: Generic.Variables.showPreferences = 0
    }
}


