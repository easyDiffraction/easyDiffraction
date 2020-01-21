import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar
import easyAnalysis.App.Toolbar.Buttons 1.0 as GenericAppToolbarButtons
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons
import easyDiffraction 1.0 as Specific

ColumnLayout{
    id: main
    spacing: 0

    Rectangle {
      Layout.fillWidth: true
      height: Generic.Style.toolbarHeight
      color: "#ddd"

      GenericAppContentAreaButtons.Home {
        anchors.left: parent.left
        anchors.verticalCenter: parent.verticalCenter
        anchors.margins: Generic.Style.toolbarSpacing
      }

      TabBar {
          id: tabBar
          anchors.centerIn: parent
          spacing: Generic.Style.toolbarSpacing
          background: Rectangle { color: "transparent" }

          currentIndex: Generic.Variables.toolbarCurrentIndex

          onCurrentIndexChanged: Generic.Variables.guideCurrentIndex = 0
          
          GenericAppToolbarButtons.Home {
              onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.HomeIndex
          }

          GenericAppToolbarButtons.Project {
              onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.ProjectIndex
          }

          // -------
          ///GenericAppToolbar.Spacer { }
          // -------

          GenericAppToolbarButtons.SampleModel {
              enabled: Specific.Variables.projectOpened && Generic.Variables.projectPageFinished
              onClicked: Generic.Variables.toolbarCurrentIndex  = Generic.Variables.SampleModelIndex
          }
          GenericAppToolbarButtons.ExperimentalData {
              enabled: Specific.Variables.projectOpened && Generic.Variables.samplePageFinished
              onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.ExperimentalDataIndex
              GenericAppElements.GuideWindow {
                  message: "This is a toolbar button of the tab with\ninformation about experimental data."
                  position: "bottom"
                  guideCurrentIndex: 6
                  toolbarCurrentIndex: Generic.Variables.ProjectIndex
                  guidesCount: Generic.Variables.ProjectGuidesCount
              }
          }
          //GenericAppToolbarButtons.InstrumentModel {
          //    enabled: Generic.Variables.dataPageFinished
          //    onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.InstrumentModelIndex
          //}

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
              enabled: Specific.Variables.projectOpened && Generic.Variables.dataPageFinished
              onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.AnalysisIndex
          }

          // -------
          ///GenericAppToolbar.Spacer {}
          // -------

          GenericAppToolbarButtons.Summary {
              enabled: Specific.Variables.projectOpened && Generic.Variables.analysisPageFinished && proxy.refinementDone
              onClicked: Generic.Variables.toolbarCurrentIndex = Generic.Variables.SummaryIndex
          }
      }

      GenericAppContentAreaButtons.SaveState {
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter
        anchors.margins: Generic.Style.toolbarSpacing
      }

    }

    GenericAppElements.HorizontalBorder { color: "#d2d2d2" }
}
