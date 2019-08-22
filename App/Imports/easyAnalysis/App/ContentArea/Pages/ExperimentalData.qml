import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea.MainArea 1.0 as GenericMainArea
import easyAnalysis.App.ContentArea.MainArea.Pages.ExperimentalData 1.0 as GenericMainAreaSampleModel
import easyAnalysis.App.ContentArea.Sidebar.Pages.ExperimentalData 1.0 as GenericSidebarSampleModel

GenericAppElements.ContentAreaStack {

    tabBarContent: TabBar {
        spacing: 0
        id: tabBar
        GenericMainArea.TabButton { text: qsTr("Plot View"); tabbarWidth: mainArea.width } // fix width
        GenericMainArea.TabButton { text: qsTr("Table View"); tabbarWidth: mainArea.width } // fix width
        GenericMainArea.TabButton { text: qsTr("Text View"); tabbarWidth: mainArea.width } // fix width
    }

    mainAreaContent: StackLayout {
        id: mainArea
        currentIndex: tabBar.currentIndex
        GenericMainAreaSampleModel.PlotView { }
        GenericMainAreaSampleModel.TableView { }
        GenericMainAreaSampleModel.TextView { }
    }

    sideBarContent: StackLayout {
        currentIndex: tabBar.currentIndex
        GenericSidebarSampleModel.PlotView { }
        GenericSidebarSampleModel.TableView { }
        GenericSidebarSampleModel.TextView { }
    }

}
