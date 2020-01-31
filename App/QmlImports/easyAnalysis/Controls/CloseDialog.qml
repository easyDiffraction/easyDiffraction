import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtGraphicalEffects 1.12

import QtQuick.Dialogs 1.3 as Dialogs1
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar
import easyDiffraction 1.0 as Specific

Dialog {
    id: dialog

    property int animationDuration: 500
    property real initialDimmedAreaTransparency: 0.5
    property string dimmedAreaColor: "black"
    property string dialogBackgroundColor: "#efefef"
    property string exitButtonBackgroundColor: "#ddd"
    property string exitButtonBorderColor: "#ccc"
    property string exitButtonIconColor: "#333"
    property string mytitle:  "Save Changes"

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

        // Exit button
        Button {
            width: parent.width
            height: Generic.Style.toolbarButtonHeight
            font.pointSize: Generic.Style.fontPointSize + 5
            font.family: Generic.Style.fontFamily
            icon.source: Generic.Variables.thirdPartyIconsPath + "sign-out-alt.svg"
            icon.color: exitButtonIconColor
            text: "Exit " + mytitle
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

    Column {
        padding: 20
        spacing: 30

        Text {
            font.pointSize: Generic.Style.fontPointSize
            font.family: Generic.Style.fontFamily
            color: "#444"
            anchors.horizontalCenter: parent.horizontalCenter
            text: "The project has not been saved. Do you want to exit?"
        }

        Row {
            spacing: 15
            anchors.horizontalCenter: parent.horizontalCenter

            GenericAppToolbar.BasicButton {
                text: "Save and exit"
                onClicked: {
                    fileDialogSaveProject.visible = true
                    closeDialogue.close()
                }
            }

            GenericAppToolbar.BasicButton {
                text: "Exit without saving"
                onClicked: {
                    closeDialogue.close()
                    Qt.exit(0)
                }
            }
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

    Dialogs1.FileDialog{
        id: fileDialogSaveProject
        visible: false
        selectExisting: false
        nameFilters: ["Project files (*.zip)"]
        folder: settings.value("lastOpenedProjectFolder", examplesDir) //QtLabsPlatform.StandardPaths.writableLocation(QtLabsPlatform.StandardPaths.HomeLocation)
        onAccepted: {
            pyQmlProxy.saveProject(fileUrl)
            fileDialogSaveProject.close()
            if (Specific.Variables.projectControl.savedProject === false) {
                failSaveDialog.visible = true
            } else {
                Qt.exit(0)
            }
        }
    }

    Dialog {
        id: failSaveDialog
        parent: Overlay.overlay
        anchors.centerIn: parent
        modal: true
        opacity: 0.9
        visible: false
        Label {
            id: infoLabel2
            anchors.centerIn: parent
            text: 'Error: The project file was not saved.'
            color: "black"
            font.family: Generic.Style.introThinFontFamily
            font.pointSize: Generic.Style.systemFontPointSize + 1
        }
    }
}
