import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtGraphicalEffects 1.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements

Dialog {
    id: dialog

    property int animationDuration: 500
    property real initialDimmedAreaTransparency: 0.5
    property string dimmedAreaColor: "black"
    property string dialogBackgroundColor: "#efefef"
    property string exitButtonBackgroundColor: "#ddd"
    property string exitButtonBorderColor: "#ccc"
    property string exitButtonIconColor: "#333"

    parent: Overlay.overlay
    anchors.centerIn: parent
    modal: true
    dim: false // dimming is done via 'hiddenPopup'

    // Background properties
    background: Rectangle {
        color: dialogBackgroundColor
    }

    // Header dialog area
    header: Column {

        // Exit button
        Button {
            width: parent.width
            height: Generic.Style.toolbarButtonHeight
            font.pointSize: Generic.Style.fontPointSize + 5
            font.family: Generic.Style.fontFamily
            icon.source: Generic.Variables.thirdPartyIconsPath + "sign-out-alt.svg"
            icon.color: exitButtonIconColor
            text: "Exit " + dialog.title
            background: Rectangle { color: exitButtonBackgroundColor }
            onClicked: dialog.close()
        }

        // Bottom border
        Rectangle {
            width: parent.width
            height: Generic.Style.appBorderThickness
            color: exitButtonBorderColor
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


