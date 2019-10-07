import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea.MainArea 1.0 as GenericMainArea
import easyAnalysis.App.ContentArea.MainArea.Pages.ExperimentalData 1.0 as GenericMainAreaSampleModel
import easyAnalysis.App.ContentArea.Sidebar.Pages.ExperimentalData 1.0 as GenericSidebarSampleModel

GenericAppElements.ContentAreaStack {

    tabBarContent: TabBar {
        spacing: 0
        id: tabBar
        GenericMainArea.TabButton { text: qsTr("Plot View"); tabbarWidth: mainArea.width } // fix width
        GenericMainArea.TabButton {
            text: qsTr("Table View")
            tabbarWidth: mainArea.width
            GenericAppElements.GuideWindow {
                message: "This tab displays experimental data as table."
                position: "bottom"
                guideCurrentIndex: 2
                toolbarCurrentIndex: Generic.Variables.ExperimentalDataIndex
                guidesCount: Generic.Variables.ExperimentalDataGuidesCount
            }
        }
        GenericMainArea.TabButton {
            text: qsTr("Text View")
            tabbarWidth: mainArea.width
            GenericAppElements.GuideWindow {
                message: "This tab displays experimental data as text."
                position: "bottom"
                guideCurrentIndex: 3
                toolbarCurrentIndex: Generic.Variables.ExperimentalDataIndex
                guidesCount: Generic.Variables.ExperimentalDataGuidesCount
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

}
