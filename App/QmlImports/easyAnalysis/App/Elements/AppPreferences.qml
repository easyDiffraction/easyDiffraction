import QtQuick 2.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons

Dialog {
    id: dialog

    visible: Generic.Variables.showPreferences
    anchors.centerIn: parent
    modal: true

    background: Rectangle {
        color: "white"
        border.color: "#888"
        radius: 3
    }

    enter: Transition {
        NumberAnimation { easing.type: Easing.OutBack; property: "scale"; from: 0.0; to: 1.0; duration: 500 }
    }
    /*
    exit: Transition {
        SequentialAnimation {
            PropertyAction { property: "dim"; value: true }
            ParallelAnimation {
                NumberAnimation { easing.type: Easing.InBack; property: "scale"; from: 1.0; to: 0.0; duration: 500 }
                NumberAnimation { easing.type: Easing.InOutExpo; property: "opacity"; from: 1.0; to: 0.0; duration: 500 }
            }
            PropertyAction { property: "dim"; value: false }
        }
    }
    */
    SequentialAnimation {
        id: exitAnimation
        running: false
        NumberAnimation { target: dialog; easing.type: Easing.InBack; property: "scale"; from: 1.0; to: 0.0; duration: 500 }
        PropertyAction { target: dialog; property: "visible"; value: false }
    }

    closePolicy: Popup.NoAutoClose

    onClosed: Generic.Variables.showPreferences = 0

    Column {
        anchors.centerIn: parent
        padding: 30
        topPadding: 20
        spacing: 30

        // Exit preferences link

        Text {
            font.pointSize: Generic.Style.fontPointSize
            font.family: Generic.Style.fontFamily
            color: Generic.Style.blueColor
            text: "Exit preferences"

            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: exitAnimation.running = true
            }
        }

        // Preferences

        Column {
            spacing: 15

            // General preferences

            Text {
                font.pointSize: Generic.Style.fontPointSize + 5
                font.family: Generic.Style.fontFamily
                color: "#444"
                text: "General"
            }

            GenericAppElements.CheckBox {
                text: qsTr("Show Animated Intro")
                checked: Generic.Variables.showIntro
                onCheckedChanged: Generic.Variables.showIntro = checked
            }

            GenericAppElements.CheckBox {
                text: qsTr("Show User Guides")
                checked: Generic.Variables.showGuide
                onCheckStateChanged: Generic.Variables.showGuide = checked
            }

            // Spacer

            Item { height: 15; width: 1 }

            // Update

            Text {
                font.pointSize: Generic.Style.fontPointSize + 5
                font.family: Generic.Style.fontFamily
                color: "#444"
                text: "Update"
            }

            GenericAppElements.CheckBox {
                enabled: false
                text: qsTr("Automatically check for updates")
                checked: false
            }

            // Spacer

            Item { height: 15; width: 1 }

            // Language

            Text {
                font.pointSize: Generic.Style.fontPointSize + 5
                font.family: Generic.Style.fontFamily
                color: "#444"
                text: "Language"
            }

            GenericAppElements.ComboBox {
                width: 250
                enabled: false
                model: ["English", "German", "French"]
            }

            // Spacer

            Item { height: 15; width: 1 }

            // Language

            Text {
                font.pointSize: Generic.Style.fontPointSize + 5
                font.family: Generic.Style.fontFamily
                color: "#444"
                text: "Theme"
            }

            GenericAppElements.ComboBox {
                width: 250
                enabled: false
                model: ["Light", "Dark"]
            }

        }
    }
}


