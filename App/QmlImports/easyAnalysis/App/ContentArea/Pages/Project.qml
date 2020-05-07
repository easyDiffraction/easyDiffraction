import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea.MainArea 1.0 as GenericMainArea
import easyAnalysis.App.ContentArea.MainArea.Pages.Project 1.0 as GenericMainAreaSampleModel
import easyAnalysis.App.ContentArea.Sidebar.Pages.Project 1.0 as GenericSidebarSampleModel

import easyDiffraction 1.0 as Specific

GenericAppElements.ContentAreaStack {

    tabBarContent: TabBar {
        spacing: 0
        id: tabBar
        GenericMainArea.TabButton { text: qsTr("Description"); tabbarWidth: mainArea.width } // fix width
        GenericMainArea.TabButton {
            text: qsTr("Main.cif")
            enabled: Specific.Variables.projectOpened
            tabbarWidth: mainArea.width
        }
    }

    mainAreaContent: StackLayout {
        id: mainArea
        currentIndex: tabBar.currentIndex
        GenericMainAreaSampleModel.Project { }
        GenericMainAreaSampleModel.Editor { }
    }

    sideBarContent: StackLayout {
        GenericSidebarSampleModel.Project { }
    }

}
