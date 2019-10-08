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
                GenericAppElements.TextField {
                    id: exportFileName
                    implicitWidth: Generic.Style.sidebarWidth - Generic.Style.sidebarGroupIndicatorIconSize - exportFileExt.implicitWidth - exportButton.implicitWidth
                    placeholderText: "Report File Name"
                    horizontalAlignment: Text.AlignRight
                    GenericAppElements.GuideWindow {
                        message: "Here you can export the report."
                        position: "left"
                        guideCurrentIndex: 1
                        toolbarCurrentIndex: Generic.Variables.SummaryIndex
                        guidesCount: Generic.Variables.SummaryGuidesCount
                    }
                }

                GenericAppElements.ComboBox {
                    id: exportFileExt
                    implicitWidth: 100
                    model: [".HTML"]
                }

                GenericAppContentAreaButtons.Export {
                    id: exportButton
                    implicitWidth: 190
                    text: "Export"
                    onClicked: proxy.save_report(exportFileName.text, exportFileExt.currentText)
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
                GenericAppElements.GuideWindow {
                    message: "Click here to go to the previous step: Analysis.\n\nAlternatively, you can click on the 'Analysis' button in toolbar."
                    position: "top"
                    guideCurrentIndex: 2
                    toolbarCurrentIndex: Generic.Variables.SummaryIndex
                    guidesCount: Generic.Variables.SummaryGuidesCount
                }
            }
            GenericAppContentAreaButtons.SaveState {
            }
            GenericAppContentAreaButtons.Help {
                onClicked: Qt.openUrlExternally("https://easydiffraction.github.io/documentation_use.html#3.2.5.-summary")
            }
            GenericAppContentAreaButtons.Bug {
                onClicked: Qt.openUrlExternally("https://easydiffraction.github.io/contact.html")
                GenericAppElements.GuideWindow {
                    message: "Please send us your feedback.\n\nYour opinion matters!"
                    position: "top left"
                    guideCurrentIndex: 3
                    toolbarCurrentIndex: Generic.Variables.SummaryIndex
                    guidesCount: Generic.Variables.SummaryGuidesCount
                }
            }
        }
    }

}

