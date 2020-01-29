import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtQuick.Window 2.12
import Qt.labs.settings 1.1

import easyAnalysis 1.0 as Generic
import easyAnalysis.Controls 1.0 as GenericControls
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.Menubar 1.0 as GenericAppMenubar
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar
import easyDiffraction 1.0 as Specific

ApplicationWindow {

    property string exitButtonBackgroundColor: "#ddd"
    property string exitButtonBorderColor: "#ccc"
    property string exitButtonIconColor: "#333"

    id: window

    visible: true
    minimumWidth: Generic.Variables.appMinWindowWidth
    minimumHeight: Generic.Variables.appMinWindowHeight
    title: Specific.Settings.appName
    color: Generic.Style.appBkgColor
    font.family: Generic.Style.fontFamily
    font.pointSize: Generic.Style.fontPointSize

    // Application preferences dialog (disabled by default)
    GenericAppElements.AppPreferences{}

    // Application menubar (not implemented yet)
    //GenericAppMenubar.Menubar {}

    // Application window layout
    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        GenericAppToolbar.Toolbar {}
        GenericAppContentArea.ContentArea {}
    }

    // Persistent settings
    Settings {
        id: settings
        property alias x: window.x
        property alias y: window.y
        property alias width: window.width
        property alias height: window.height
    }

    // Load persistent settings when window is created
    Component.onCompleted: {
        Generic.Variables.showIntro = settings.value("showIntro", Generic.Variables.showIntro)
        Generic.Variables.showGuide = settings.value("showGuide", Generic.Variables.showGuide)
        Generic.Variables.appWindowWidth = settings.value("appWindowWidth", Generic.Variables.appWindowWidth)
        Generic.Variables.appWindowHeight = settings.value("appWindowHeight", Generic.Variables.appWindowHeight)
        Generic.Variables.appWindowX = settings.value("appWindowX", (Screen.width - Generic.Variables.appWindowWidth) / 2)
        Generic.Variables.appWindowY = settings.value("appWindowY", (Screen.height - Generic.Variables.appWindowHeight) / 2)
        window.width = Generic.Variables.appWindowWidth
        window.height = Generic.Variables.appWindowHeight
        window.x = Generic.Variables.appWindowX
        window.y = Generic.Variables.appWindowY
    }

    // Save persistent settings when app window is closed
    Component.onDestruction: {
        settings.setValue("showIntro", Generic.Variables.showIntro)
        settings.setValue("showGuide", Generic.Variables.showGuide)
        settings.setValue("appWindowWidth", window.width)
        settings.setValue("appWindowHeight", window.height)
        settings.setValue("appWindowX", window.x)
        settings.setValue("appWindowY", window.y)
    }

    // Temporary solution to update main area width
    onWidthChanged: Generic.Variables.mainAreaWidth = width - Generic.Style.appBorderThickness - Generic.Style.sidebarWidth

    onClosing: {
        print(projectManager.needToSave)
        //        close.accepted = projectManager.needToSave ? false: true
//        close.accepted = false
        close.accepted = true
//        closeDialogue.visible = true
    }


    GenericControls.Dialog {
        id: closeDialogue
        visible: false
        title: "Save Changes"

        Column {
            padding: 20
            spacing: 20

            Text {
                font.pointSize: Generic.Style.fontPointSize + 1
                font.family: Generic.Style.fontFamily
                color: "#444"
                anchors.horizontalCenter: parent.horizontalCenter
                text: "The project has not been saved. Do you want to exit?"
            }

            Row {
                spacing: 15
                anchors.horizontalCenter: parent.horizontalCenter

                GenericAppToolbar.Button {
                    text: "Save and exit"
                    onClicked: {
                        closeDialogue.close()
                        Qt.exit(0)
                    }
                }

                GenericAppToolbar.Button {
                    text: "Exit without saving"
                    onClicked: {
                        closeDialogue.close()
                        Qt.exit(0)
                    }
                }

                GenericAppToolbar.Button {
                    text: "Cancel"
                    onClicked: {
                        closeDialogue.close()
                    }
                }
            }
        }
    }
}


