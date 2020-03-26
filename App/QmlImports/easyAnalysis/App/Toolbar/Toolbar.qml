import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtGraphicalEffects 1.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar
import easyAnalysis.App.Toolbar.Buttons 1.0 as GenericAppToolbarButtons
import easyAnalysis.App.Toolbar.TabButtons 1.0 as GenericAppToolbarTabButtons
import easyDiffraction 1.0 as Specific

ColumnLayout{
    id: main
    spacing: 0

    /*
    DropShadow {
        z: -1
        anchors.fill: parent
        horizontalOffset: 0
        radius: 7
        samples: 21
        color: "#aaa"
    }
    */

    Rectangle {
        Layout.fillWidth: true
        height: Generic.Style.toolbarHeight
        color: Generic.Style.toolbarBkgColor

        // Preferences and save state buttons on the left side
        Row {
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter
            anchors.margins: Generic.Style.toolbarSpacing
            spacing: Generic.Style.toolbarSpacing

            GenericAppToolbarButtons.Preferences {}
            GenericAppToolbarButtons.SaveState {}
        }

        // Workflow buttons in the middle
        TabBar {
            id: tabBar
            anchors.centerIn: parent
            spacing: Generic.Style.toolbarSpacing
            background: Rectangle { color: "transparent" }

            currentIndex: Generic.Variables.toolbarCurrentIndex

            onCurrentIndexChanged: Generic.Variables.guideCurrentIndex = 0

            GenericAppToolbarTabButtons.Home {
                onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.HomeIndex
            }

            GenericAppToolbarTabButtons.Project {
                enabled: Generic.Variables.homePageFinished
                onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.ProjectIndex
            }

            GenericAppToolbarTabButtons.Sample {
                enabled: Specific.Variables.projectOpened && Generic.Variables.projectPageFinished
                onClicked: Generic.Variables.toolbarCurrentIndex  = Generic.Variables.SampleIndex
            }

            GenericAppToolbarTabButtons.Experiment {
                enabled: Specific.Variables.projectOpened && Generic.Variables.samplePageFinished
                onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.ExperimentIndex
                GenericAppElements.GuideWindow {
                    message: "This is a toolbar button of the tab with\ninformation about experimental data."
                    position: "bottom"
                    guideCurrentIndex: 6
                    toolbarCurrentIndex: Generic.Variables.ProjectIndex
                    guidesCount: Generic.Variables.ProjectGuidesCount
                }
            }

            GenericAppToolbarTabButtons.Analysis {
                enabled: Specific.Variables.projectOpened && Generic.Variables.dataPageFinished
                onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.AnalysisIndex
                GenericAppElements.GuideWindow {
                    message: "This button is blinking during the fitting process."
                    position: "bottom"
                    guideCurrentIndex: 4
                    toolbarCurrentIndex: Generic.Variables.AnalysisIndex
                    guidesCount: Generic.Variables.AnalysisGuidesCount
                }
            }

            GenericAppToolbarTabButtons.Summary {
                enabled: Specific.Variables.projectOpened && Generic.Variables.analysisPageFinished && Specific.Variables.refinementDone
                onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.SummaryIndex
            }
        }

        // Undo-redu buttons on the right side
        Row {
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            anchors.margins: Generic.Style.toolbarSpacing
            spacing: Generic.Style.toolbarSpacing

            GenericAppToolbarButtons.Undo {}
            GenericAppToolbarButtons.Redo {}
        }

    }

    GenericAppElements.HorizontalBorder { color: Generic.Style.toolbarBottomBorderColor }
}
