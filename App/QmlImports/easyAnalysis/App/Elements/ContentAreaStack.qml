import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements

RowLayout {
    property alias mainAreaContent: mainArea.children
    property var tabBarContent: null
    property var sideBarContent: null
    property string notLoadedInfoText: ""

    spacing: 0

    // ContentArea including its TabBar
    ColumnLayout {
        Layout.fillHeight: true
        Layout.fillWidth: true
        spacing: 0

        // ContentArea TabBar
        TabBar {
            visible: !notLoadedInfo.visible
            Layout.alignment: Qt.AlignLeft
            id: tabBar
            height: tabBarContent ? Generic.Style.contentAreaTabbarHeight : 0
            spacing: 0
            children: tabBarContent
        }

        // TabBar bottom border
        GenericAppElements.HorizontalBorder { visible: !notLoadedInfo.visible; height: tabBarContent ? Generic.Style.appBorderThickness : 0 }

        // ContentArea without TabBar
        Rectangle {
            visible: !notLoadedInfo.visible
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "white"

            StackLayout {
                id: mainArea
                anchors.fill: parent
                currentIndex: tabBar.currentIndex
            }
        }

        // Status bar
        GenericAppElements.StatusBar { visible: !notLoadedInfo.visible }

        // Not loaded info container
        Text {
            id: notLoadedInfo
            visible: notLoadedInfoText
            Layout.fillHeight: true
            Layout.fillWidth: true
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: notLoadedInfoText
            font.family: Generic.Style.secondFontFamily
            font.pointSize: 42
            font.weight: Font.Light
            color: "lightgrey"
        }
    }

    // ContentArea right border
    GenericAppElements.VerticalBorder { width: sideBarContent ? Generic.Style.appBorderThickness : 0 }

    // Sidebar
    Rectangle {
        Layout.fillHeight: true
        width: sideBarContent ? Generic.Style.sidebarWidth : 0
        color: "transparent"

        StackLayout {
            id: sideBar
            anchors.fill: parent
            currentIndex: tabBar.currentIndex
            children: sideBarContent
        }
    }

}


