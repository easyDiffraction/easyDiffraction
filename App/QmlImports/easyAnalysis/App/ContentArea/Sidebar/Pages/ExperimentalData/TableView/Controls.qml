import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons
import easyAnalysis.Logic 1.0 as GenericLogic
import easyDiffraction 1.0 as Specific

ColumnLayout {
    spacing: 0

    Item { Layout.fillHeight: true }

    // Groupbox

    GenericAppElements.FlowButtons {
        property url currentUrl: "https://easydiffraction.org/umanual_use.html#3.2.3.-experimental-data"
        property Item contentsPrevious: GenericAppContentAreaButtons.GoPrevious {
            text: "Home"
            ToolTip.text: qsTr("Go to the previous step: Home")
            onClicked: {
                Generic.Variables.toolbarCurrentIndex = Generic.Variables.HomeIndex
            }
            GenericAppElements.GuideWindow {
                message: "Click here to go to the previous step: Home.\n\nAlternatively, you can click on the 'Home' button in toolbar."
                position: "top"
                guideCurrentIndex: 5
                toolbarCurrentIndex: Generic.Variables.ExperimentalDataIndex
                guidesCount: Generic.Variables.ExperimentalDataGuidesCount
            }
        }
        property Item contentsNext: GenericAppContentAreaButtons.GoNext {
            text: "Sample Model"
            ToolTip.text: qsTr("Go to the next step: Sample model")
            onClicked: {
                Generic.Variables.dataPageFinished = true
                Generic.Variables.toolbarCurrentIndex = Generic.Variables.SampleModelIndex
            }
            GenericAppElements.GuideWindow {
                message: "Click here to go to the next step: Sample model."
                position: "top"
                guideCurrentIndex: 6
                toolbarCurrentIndex: Generic.Variables.ExperimentalDataIndex
                guidesCount: Generic.Variables.ExperimentalDataGuidesCount
            }
        }
    }
}

