import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar
import easyAnalysis.App.Toolbar.Buttons 1.0 as GenericAppToolbarButtons

ColumnLayout{
    id: main
    spacing: 0
    Layout.fillWidth: true
    Layout.preferredHeight: Generic.Style.toolbarHeight

    TabBar {
        id: tabBar
        spacing: Generic.Style.toolbarSpacing
        Layout.fillWidth: true
        Layout.leftMargin: Generic.Style.toolbarSpacing
        Layout.rightMargin: Generic.Style.toolbarSpacing
        background: Rectangle { color: "transparent" }

        currentIndex: Generic.Variables.toolbarCurrentIndex

        onCurrentIndexChanged: Generic.Variables.guideCurrentIndex = 0

        GenericAppToolbarButtons.Home {
            onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.HomeIndex
        }

        // -------
        ///GenericAppToolbar.Spacer { }
        // -------

        GenericAppToolbarButtons.ExperimentalData {
            enabled: Generic.Variables.homePageFinished
            onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.ExperimentalDataIndex
            GenericAppElements.GuideWindow {
                message: "This is a toolbar button of the tab with\ninformation about experimental data."
                position: "bottom"
                guideCurrentIndex: 6
                toolbarCurrentIndex: Generic.Variables.HomeIndex
                guidesCount: Generic.Variables.HomeGuidesCount
            }
        }
        //GenericAppToolbarButtons.InstrumentModel {
        //    enabled: Generic.Variables.dataPageFinished
        //    onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.InstrumentModelIndex
        //}
        GenericAppToolbarButtons.SampleModel {
            enabled: Generic.Variables.dataPageFinished
            onClicked: Generic.Variables.toolbarCurrentIndex  = Generic.Variables.SampleModelIndex
        }

        // -------
        ///GenericAppToolbar.Spacer {}
        // -------

        //GenericAppToolbarButtons.Linking {
        //    enabled: Generic.Variables.samplePageFinished
        //    onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.LinkingIndex
        //}

        // -------
        ///GenericAppToolbar.Spacer {}
        // -------

        GenericAppToolbarButtons.Analysis {
            enabled: Generic.Variables.samplePageFinished
            onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.AnalysisIndex
        }

        // -------
        ///GenericAppToolbar.Spacer {}
        // -------

        GenericAppToolbarButtons.Summary {
            enabled: proxy.refinementDone || Generic.Variables.isDebug//Generic.Variables.analysisPageFinished
            onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.SummaryIndex
        }
    }

    GenericAppElements.HorizontalBorder {}
}
