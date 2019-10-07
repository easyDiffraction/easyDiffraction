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
        title: "Export as..."
        collapsible: false
        content: GenericAppElements.ColumnLayout {
            GenericAppElements.RowLayout {
                GenericAppContentAreaButtons.Export {
                    id: exportButton
                    implicitWidth: 60
                    text: "Export"
                    onClicked: proxy.save_report(exportFileName.text, exportFileExt.currentText)
                    GenericAppElements.GuideWindow {
                        message: "Here you can export the report."
                        position: "left"
                        guideCurrentIndex: 0
                        toolbarCurrentIndex: Generic.Variables.SummaryIndex
                        guidesCount: Generic.Variables.SummaryGuidesCount
                    }
                }
                TextField {
                    id: exportFileName
                    Layout.fillWidth: true
                    implicitHeight: 32
                    placeholderText: "Report File Name"
                    horizontalAlignment: Text.AlignRight
                }
                GenericAppElements.ComboBox {
                    id: exportFileExt
                    implicitWidth: 60
                    model: [".HTML"]
                }
            }
        }
    }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Export elements"
        content: GenericAppElements.GridLayout {
            enabled: false
            columns: 3
            GenericAppElements.CheckBox { checked:true;  text:qsTr("Project info") }
            GenericAppElements.CheckBox { checked:true;  text:qsTr("Parameters table") }
            GenericAppElements.CheckBox { checked:true;  text:qsTr("Fitting figure") }
            GenericAppElements.CheckBox { checked:true;  text:qsTr("Structure plot") }
            GenericAppElements.CheckBox { checked:false; text:qsTr("Reliability factors") }
            GenericAppElements.CheckBox { checked:false; text:qsTr("Constraints table") }
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

