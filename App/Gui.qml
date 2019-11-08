import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtQuick.Window 2.12
import Qt.labs.settings 1.1

import easyAnalysis 1.0 as Generic
import easyAnalysis.App 1.0 as GenericApp
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.Menubar 1.0 as GenericAppMenubar
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar
import easyAnalysis.Logic 1.0 as GenericLogic
import easyDiffraction 1.0 as Specific

ApplicationWindow {
    id: window

    visible: true
    color: Generic.Style.appBkgColor
    title: Specific.Settings.appName

    minimumWidth: Generic.Variables.appMinWindowWidth
    minimumHeight: Generic.Variables.appMinWindowHeight
    ///x: Generic.Variables.appWindowX
    ///y: Generic.Variables.appWindowY

    font.family: Generic.Style.fontFamily
    font.pointSize: Generic.Style.fontPointSize

    // Introduction animation
    GenericApp.Intro {}

    // Application menubar
    ///GenericAppMenubar.Menubar {}

    // Application window layout
    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        GenericAppToolbar.Toolbar {}
        GenericAppContentArea.ContentArea {}
    }

    // Set paths related to the current file
    Image {
        visible: false
        source: Generic.Style.dummyIconPath
        onSourceChanged: {
            const currentFilePath = GenericLogic.Misc.dirFromPath(source.toString())
            Specific.Variables.resourcesPath = currentFilePath + "QmlImports/easyDiffraction/Resources/"
            Generic.Variables.resourcesPath = currentFilePath + "QmlImports/easyAnalysis/Resources/"
            //Generic.Variables.thirdPartyIconsPath = Generic.Variables.resourcesPath + "Icons/"
            Generic.Variables.originalIconsPath = Generic.Variables.resourcesPath + "Icons/"
            Generic.Variables.thirdPartyIconsPath = Generic.Variables.resourcesPath + "Fonts/Awesome/svgs/"
            Generic.Variables.qmlElementsPath = currentFilePath + "QmlImports/easyAnalysis/App/Elements/"
        }
    }

    // Persistent settings
    Settings {
        id: settings
        property alias x: window.x
        property alias y: window.y
        property alias width: window.width
        property alias height: window.height
    }

    Component.onCompleted: {
        // Load persistent settings
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

    Component.onDestruction: {
        // Save persistent settings
        settings.setValue("showIntro", Generic.Variables.showIntro)
        settings.setValue("showGuide", Generic.Variables.showGuide)
        settings.setValue("appWindowWidth", window.width)
        settings.setValue("appWindowHeight", window.height)
        settings.setValue("appWindowX", window.x)
        settings.setValue("appWindowY", window.y)
    }

    onWidthChanged: Generic.Variables.mainAreaWidth = width - Generic.Style.appBorderThickness - Generic.Style.sidebarWidth
}


