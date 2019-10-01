import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea.Sidebar 1.0 as GenericSidebar

ColumnLayout {
    //property var controlsContent: null
    //property var settingsContent: null
    property alias controlsContent: controls.children
    property alias settingsContent: settings.children

    id: stackLayout
    spacing: 0

    // Sidebar tabs with bottom border
    ColumnLayout {
        spacing: 0
        visible: settings.children.length

        // Sidebar tabs
        TabBar {
            id: tabbar
            spacing: 0
            GenericSidebar.TabButton { text: qsTr("Basic controls") }
            GenericSidebar.TabButton { text: qsTr("Advanced controls") }
        }

        // tabs bottom border
        GenericAppElements.HorizontalBorder { height: tabBarContent ? Generic.Style.appBorderThickness : 0 }
    }

    // Sidebar area without tabs
    StackLayout {
        id: stack
        // doesn't work with Layout.fillWidth: true; switched to width: parent.width
        //Layout.fillWidth: true
        //Layout.fillHeight: true
        width: parent.width
        height: parent.height
        currentIndex: tabbar.currentIndex

        // Controls Tab
        Item {
            id: controls
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        // Settings Tab
        Item {
            id: settings
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

}
