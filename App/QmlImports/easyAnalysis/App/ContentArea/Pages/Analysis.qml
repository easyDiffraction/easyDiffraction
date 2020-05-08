import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea.MainArea 1.0 as GenericMainArea
import easyAnalysis.App.ContentArea.MainArea.Pages.Analysis 1.0 as GenericMainAreaAnalysis
import easyAnalysis.App.ContentArea.Sidebar.Pages.Analysis 1.0 as GenericSidebarAnalysis
import easyDiffraction 1.0 as Specific

GenericAppElements.ContentAreaStack {

    tabBarContent: TabBar {
        spacing: 0
        id: tabBar
        //GenericMainArea.TabButton { text: qsTr("Simulation"); tabbarWidth: mainArea.width } // fix width
        GenericMainArea.TabButton { text: qsTr("Fitting"); tabbarWidth: mainArea.width } // fix width
        //GenericMainArea.TabButton { text: qsTr("Constraints"); tabbarWidth: mainArea.width } // fix width
        GenericMainArea.TabButton {
            text: qsTr("calculations.cif")
            tabbarWidth: mainArea.width
            GenericAppElements.GuideWindow {
                message: "This tab button allows to see the\ncalcualted data as plain text."
                position: "bottom"
                guideCurrentIndex: 2
                toolbarCurrentIndex: Generic.Variables.AnalysisIndex
                guidesCount: Generic.Variables.AnalysisGuidesCount
            }
        }
    }

    mainAreaContent: StackLayout {
        id: mainArea
        currentIndex: tabBar.currentIndex
        GenericMainAreaAnalysis.Fitting { }
        GenericMainAreaAnalysis.Editor { id: editor }
    }

    sideBarContent: StackLayout {
        currentIndex: tabBar.currentIndex
        GenericSidebarAnalysis.Fitting { }
        GenericSidebarAnalysis.Editor { }
    }

}
