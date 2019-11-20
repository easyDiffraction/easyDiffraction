import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons
import easyAnalysis.Logic 1.0 as GenericLogic

ColumnLayout {
    spacing: 0

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Find"
        enabled: false
        content: GenericAppElements.RowLayout {
            TextField { Layout.fillWidth: true; implicitHeight: 29; placeholderText: "Search text"}
            CheckBox { implicitHeight: 32; checked: true; text: qsTr("Ignore case") }
        }
    }

    Item { Layout.fillHeight: true }

    // Groupbox

    GenericAppElements.FlowButtons {
        property url currentUrl: "https://easydiffraction.org/umanual_use.html#3.2.4.-sample-model"
        property Item contentsPrevious: GenericAppContentAreaButtons.GoPrevious {
            text: "Experimental Data"
            ToolTip.text: qsTr("Go to the previous step: Experimental data")
            onClicked: {
                Generic.Variables.toolbarCurrentIndex = Generic.Variables.ExperimentalDataIndex
            }
            GenericAppElements.GuideWindow {
                message: "Click here to go to the previous step: Experimental data.\n\nAlternatively, you can click on the 'Experimental data' button in toolbar."
                position: "top"
                guideCurrentIndex: 4
                toolbarCurrentIndex: Generic.Variables.SampleModelIndex
                guidesCount: Generic.Variables.SampleModelGuidesCount
            }
        }
        property Item contentsNext: GenericAppContentAreaButtons.GoNext {
            text: "Analysis"
            ToolTip.text: qsTr("Go to the next step: Analysis")
            onClicked: {
                Generic.Variables.samplePageFinished = true
                Generic.Variables.toolbarCurrentIndex = Generic.Variables.AnalysisIndex
            }
            GenericAppElements.GuideWindow {
                message: "Click here to go to the next step: Structure refinement."
                position: "top"
                guideCurrentIndex: 5
                toolbarCurrentIndex: Generic.Variables.SampleModelIndex
                guidesCount: Generic.Variables.SampleModelGuidesCount
            }
        }
    }
}
