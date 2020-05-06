import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea.MainArea 1.0 as GenericMainArea
import easyAnalysis.App.ContentArea.MainArea.Pages.SampleModel 1.0 as GenericMainAreaSampleModel
import easyAnalysis.App.ContentArea.Sidebar.Pages.SampleModel 1.0 as GenericSidebarSampleModel

import easyDiffraction 1.0 as Specific

GenericAppElements.ContentAreaStack {

    tabBarContent: TabBar {
        spacing: 0
        id: tabBar
        GenericMainArea.TabButton { text: qsTr("Structure View"); tabbarWidth: mainArea.width } // fix width
        GenericMainArea.TabButton {
            text: qsTr("Phases.cif Edit")
            tabbarWidth: mainArea.width

            GenericAppElements.GuideWindow {
                message: "This tab button allows to see the phase\ndetails as plain text (CIF)."
                position: "bottom"
                guideCurrentIndex: 2
                toolbarCurrentIndex: Generic.Variables.SampleIndex
                guidesCount: Generic.Variables.SampleGuidesCount
            }
        }
    }

    mainAreaContent: StackLayout {
        id: mainArea
        currentIndex: tabBar.currentIndex
        GenericMainAreaSampleModel.StructureView { }
        GenericMainAreaSampleModel.TextView { id: textView }
        onCurrentIndexChanged: {
            textView.showContent = (currentIndex === 1)
        }
    }

    sideBarContent: StackLayout {
        currentIndex: tabBar.currentIndex
        GenericSidebarSampleModel.StructureView { }
        GenericSidebarSampleModel.TextView { }
    }

    notLoadedInfoText: !Specific.Variables.phaseIds().length ? "No Phases Loaded" : ""

}
