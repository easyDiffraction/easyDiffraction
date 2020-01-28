import QtQuick 2.12
import QtQuick.Controls 2.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.Controls 1.0 as GenericControls
import easyAnalysis.App.Elements 1.0 as GenericAppElements

GenericControls.Dialog {
    visible: Generic.Variables.showPreferences
    title: "Preferences"

    Column {
        padding: 20
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

        // Update preferences

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

        // Language preferences

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

        // Theme preferences

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


