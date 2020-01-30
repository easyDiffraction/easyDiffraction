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
    id: window

    property real toolBarOpacity: 0

    visible: true
    minimumWidth: Generic.Variables.appMinWindowWidth
    minimumHeight: Generic.Variables.appMinWindowHeight
    title: Specific.Settings.appName
    color: "white"
    font.family: Generic.Style.fontFamily
    font.pointSize: Generic.Style.fontPointSize
    flags: Qt.FramelessWindowHint | Qt.Dialog

    // Application preferences dialog (disabled by default)
    GenericAppElements.AppPreferences{}

    // Application menubar (not implemented yet)
    //GenericAppMenubar.Menubar {}

    // Application window layout
    ColumnLayout {
        id: content
        //visible: displayContent
        anchors.fill: parent
        spacing: 0
        GenericAppToolbar.Toolbar { opacity: toolBarOpacity }
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
}


