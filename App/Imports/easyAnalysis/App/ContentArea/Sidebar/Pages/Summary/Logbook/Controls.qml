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
        title: "Export elements"
        content: GenericAppElements.GridLayout {
            enabled: false
            columns: 2
            GenericAppElements.CheckBox { checked:true;  text:qsTr("Parameters table") }
            GenericAppElements.CheckBox { checked:false; text:qsTr("Reliability factors") }
            GenericAppElements.CheckBox { checked:false; text:qsTr("Constraints table") }
            GenericAppElements.CheckBox { checked:true;  text:qsTr("Fitting figure") }
        }
    }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Export as..."
        content: GenericAppElements.ColumnLayout {
            GenericAppElements.RowLayout {
                GenericAppContentAreaButtons.Export { id: exportButton; implicitWidth: 60; text: "Export" }
                TextField { Layout.fillWidth: true; implicitHeight: 32; placeholderText: "Logbook File Name"; horizontalAlignment: Text.AlignRight}
                GenericAppElements.ComboBox { implicitWidth: 60; model: [".PDF", ".HTML"] }

                GenericAppElements.GuideWindow {
                    id: guidWindow
                    message: "Click here to export a logbook."
                    toY: exportButton.y + exportButton.height / 2

                    visible: Generic.Variables.showGuide && Generic.Variables.toolbarCurrentIndex === Generic.Variables.SummaryIndex ? true : false

                    GenericAppContentAreaButtons.Add { id: exportButtonClone }
                    Component.onCompleted: {
                        GenericLogic.Copy.copyButton(exportButton, exportButtonClone)
                    }
                }
            }
        }
    }

    /////////
    // Spacer
    /////////
    Item { Layout.fillHeight: true }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        collapsible: false
        showBorder: false
        content: GenericAppElements.RowLayout {
            GenericAppContentAreaButtons.GoPrevious {
                text: "Analysis"
                ToolTip.text: qsTr("Go to the previous step: Analysis")
                onClicked: {
                    Generic.Variables.toolbarCurrentIndex = Generic.Variables.AnalysisIndex
                }
            }
            GenericAppContentAreaButtons.SaveState {
            }
            GenericAppContentAreaButtons.Help {
                onClicked: Qt.openUrlExternally("https://easydiffraction.github.io/documentation_use.html#3.2.5.-summary")
            }
            GenericAppContentAreaButtons.Bug {
                onClicked: Qt.openUrlExternally("https://easydiffraction.github.io/contact.html")
            }
        }
    }

}

