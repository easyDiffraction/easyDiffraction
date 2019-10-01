import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea.MainArea 1.0 as GenericMainArea
import easyAnalysis.App.ContentArea.MainArea.Pages.Summary 1.0 as GenericMainAreaSummary
import easyAnalysis.App.ContentArea.Sidebar.Pages.Summary 1.0 as GenericSidebarSummary

GenericAppElements.ContentAreaStack {

    tabBarContent: TabBar {
        spacing: 0
        id: tabBar
        GenericMainArea.TabButton { text: qsTr("Report"); tabbarWidth: mainArea.width } // fix width
    }

    mainAreaContent: StackLayout {
        id: mainArea
        currentIndex: tabBar.currentIndex
        GenericMainAreaSummary.Logbook { }
    }

    sideBarContent: StackLayout {
        currentIndex: tabBar.currentIndex
        GenericSidebarSummary.Logbook { }
    }

}
