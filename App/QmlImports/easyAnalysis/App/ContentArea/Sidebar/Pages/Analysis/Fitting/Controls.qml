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
    property bool isFitting: true

    spacing: 0

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Parameters"
        id: dataExplorerTable
        collapsible: false
        content: GenericAppElements.ColumnLayout {
            // Fitables table
            GenericAppElements.FitablesView {
                Layout.fillWidth: true
                model: proxy.fitables
            }

            // Buttons
            GenericAppElements.GridLayout {
                columns: 2

                GenericAppContentAreaButtons.PausePlay {
                    id: pausePlayButton
                    text: proxy.refinementRunning ? "Stop fitting" : "Start fitting"
                    onClicked: {
                        proxy.refine()
                    }
                }
                CheckBox { enabled: false; checked: false; text: "Auto-update"; }

                GenericAppContentAreaButtons.Accept {
                    enabled: false;
                    text: "Accept refined parameters";
                }
                CheckBox { enabled: false; checked: true; text: "Auto-accept"; }

                GenericAppElements.GuideWindow {
                    id: guidWindow
                    message: "Click here to start or stop fitting."
                    toY: pausePlayButton.y + pausePlayButton.height / 2

                    visible: Generic.Variables.showGuide && Generic.Variables.toolbarCurrentIndex === Generic.Variables.AnalysisIndex ? true : false

                    GenericAppContentAreaButtons.Add { id: pausePlayButtonClone }
                    Component.onCompleted: {
                        GenericLogic.Copy.copyButton(pausePlayButton, pausePlayButtonClone)
                    }
                }

            }
        }
    }

    // Spacer

    Item { Layout.fillHeight: true }

    // Groupbox

    GenericAppElements.GroupBox {
        collapsible: false
        showBorder: false
        content: GenericAppElements.RowLayout {
            GenericAppContentAreaButtons.GoPrevious {
                text: "Sample Model"
                ToolTip.text: qsTr("Go to the previous step: Sample model")
                onClicked: {
                    Generic.Variables.toolbarCurrentIndex = Generic.Variables.SampleModelIndex
                }
            }
            GenericAppContentAreaButtons.GoNext {
                text: "Summary"
                enabled: proxy.refinementDone
                highlighted: proxy.refinementDone
                ToolTip.text: qsTr("Go to the next step: Summary")
                onClicked: {
                    Generic.Variables.analysisPageFinished = true
                    Generic.Variables.summaryPageFinished = true
                    Generic.Variables.toolbarCurrentIndex = Generic.Variables.SummaryIndex
                }
            }
            GenericAppContentAreaButtons.SaveState {
                checked: true
            }
            GenericAppContentAreaButtons.Help {
                onClicked: Qt.openUrlExternally("https://easydiffraction.github.io/documentation_use.html#3.2.4.-analysis")
            }
            GenericAppContentAreaButtons.Bug {
                onClicked: Qt.openUrlExternally("https://easydiffraction.github.io/contact.html")
            }
        }
    }

    // Info dialog (after refinement)

    Dialog {
        id: info
        parent: Overlay.overlay
        anchors.centerIn: parent
        modal: true
        visible: proxy.refinementDone

        Label {
            id: infoLabel
            anchors.centerIn: parent
            text: {
                if (!proxy.refinementDone)
                    return ""
                const res = proxy.refinementResult
                Generic.Variables.chiSquared = res.final_chi_sq ? res.final_chi_sq.toFixed(4) : Generic.Variables.chiSquared
                let s = `${res.refinement_message}`
                s += res.num_refined_parameters ? `\nNumber of refined parameters: ${res.num_refined_parameters}` : ""
                s += res.nfev ? `\nnfev: ${res.nfev}` : ""
                s += res.nit ? `\nnfev: ${res.nit}` : ""
                s += res.njev ? `\nnfev: ${res.njev}` : ""
                s += res.started_chi_sq ? `\nStarted goodnes-of-fit (\u03c7\u00b2): ${(res.started_chi_sq).toFixed(3)}` : ""
                s += res.final_chi_sq ? `\nFinal goodnes-of-fit (\u03c7\u00b2): ${(res.final_chi_sq).toFixed(3)}` : ""
                s += res.refinement_time ? `\nRefinement time in seconds: ${(res.refinement_time).toFixed(2)}` : ""
                return s
            }
        }
    }
}

