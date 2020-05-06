import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea.MainArea 1.0 as GenericMainArea
import easyAnalysis.App.ContentArea.MainArea.Pages.ExperimentalData 1.0 as GenericMainAreaSampleModel
import easyAnalysis.App.ContentArea.Sidebar.Pages.ExperimentalData 1.0 as GenericSidebarSampleModel

import easyDiffraction 1.0 as Specific

GenericAppElements.ContentAreaStack {

    tabBarContent: TabBar {
        spacing: 0
        id: tabBar
        GenericMainArea.TabButton { text: qsTr("Plot View"); tabbarWidth: mainArea.width } // fix width
        GenericMainArea.TabButton {
            text: qsTr("Table View")
            tabbarWidth: mainArea.width
            GenericAppElements.GuideWindow {
                message: "This tab button switches to the table\nview of the measured data."
                position: "bottom"
                guideCurrentIndex: 2
                toolbarCurrentIndex: Generic.Variables.ExperimentIndex
                guidesCount: Generic.Variables.ExperimentGuidesCount
            }
        }
        GenericMainArea.TabButton {
            text: qsTr("Experiments.cif Edit")
            tabbarWidth: mainArea.width
            GenericAppElements.GuideWindow {
                message: "This tab button allows to see the\nmeasured data as plain text."
                position: "bottom"
                guideCurrentIndex: 3
                toolbarCurrentIndex: Generic.Variables.ExperimentIndex
                guidesCount: Generic.Variables.ExperimentGuidesCount
            }
        }
    }

    mainAreaContent: StackLayout {
        id: mainArea
        currentIndex: tabBar.currentIndex
        GenericMainAreaSampleModel.PlotView { }
        GenericMainAreaSampleModel.TableView { }
        GenericMainAreaSampleModel.TextView { id: textView }
        onCurrentIndexChanged: {
            textView.showContent = (currentIndex === 2)
        }
    }

    sideBarContent: StackLayout {
        currentIndex: tabBar.currentIndex
        GenericSidebarSampleModel.PlotView { }
        GenericSidebarSampleModel.TableView { }
        GenericSidebarSampleModel.TextView { }
    }

    notLoadedInfoText: !Specific.Variables.experimentIds().length ? "No Experiments Loaded" : ""

}
