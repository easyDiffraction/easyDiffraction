import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.XmlListModel 2.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.Controls 1.0 as GenericControls
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyDiffraction 1.0 as Specific

GenericControls.Dialog {
    visible: Generic.Variables.showPreferences
    title: "Preferences"

    Column {
        padding: 20
        spacing: 15

        // General preferences

        Text {
            font.pointSize: Generic.Style.fontPointSize + 3
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

        Item { height: 10; width: 1 }

        // Update preferences

        Text {
            font.pointSize: Generic.Style.fontPointSize + 3
            font.family: Generic.Style.fontFamily
            color: "#444"
            text: "Update"
        }

        GenericAppElements.CheckBox {
            text: qsTr("Automatically check for updates")
            checked: false
            GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
        }

        /*
        // Spacer

        Item { height: 10; width: 1 }

        // Language preferences

        Text {
            font.pointSize: Generic.Style.fontPointSize + 3
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

        Item { height: 10; width: 1 }

        // Theme preferences

        Text {
            font.pointSize: Generic.Style.fontPointSize + 3
            font.family: Generic.Style.fontFamily
            color: "#444"
            text: "Theme"
        }

        GenericAppElements.ComboBox {
            width: 250
            enabled: false
            model: ["Light", "Dark"]
        }
        */

        // Spacer

        Item { height: 10; width: 1 }

        // Debugging

        Text {
            font.pointSize: Generic.Style.fontPointSize + 3
            font.family: Generic.Style.fontFamily
            color: "#444"
            text: "Logging"
        }

        GenericAppElements.ComboBox {
            width: 250
            model: XmlListModel {
                xml: ((typeof(Specific.Variables.loggerPyQml) !== 'undefined') && (Specific.Variables.loggerPyQml !== null)) ? Specific.Variables.loggerPyQml.levelsAsXml() : ''
                query: "/root/level"
                XmlRole { name: "name"; query: "name/string()" }
            }
            onActivated: Specific.Variables.loggerPyQml.setLevel(currentIndex)
            onCurrentIndexChanged: Specific.Variables.loggerPyQml.setLevel(currentIndex)
            Component.onCompleted: currentIndex = Specific.Variables.loggerPyQml.defaultLevelIndex()
        }
    }
}



