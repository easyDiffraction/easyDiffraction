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
                model: Specific.Variables.projectOpened ? proxy.fitables : null
                GenericAppElements.GuideWindow {
                    message: "Here you can see all the refinable parameters.\n\nYou can change their starting values manually\nor using the slider below."
                    position: "left"
                    guideCurrentIndex: 0
                    toolbarCurrentIndex: Generic.Variables.AnalysisIndex
                    guidesCount: Generic.Variables.AnalysisGuidesCount
                }
            }

            // Buttons
            GenericAppElements.GridLayout {
                columns: 2

                GenericAppContentAreaButtons.PausePlay {
                    id: pausePlayButton
                    onClicked: {
                        proxy.refine()
                    }
                    GenericAppElements.GuideWindow {
                        message: "Click here to start or stop fitting."
                        position: "left"
                        guideCurrentIndex: 3
                        toolbarCurrentIndex: Generic.Variables.AnalysisIndex
                        guidesCount: Generic.Variables.AnalysisGuidesCount
                    }
                }
                CheckBox { enabled: false; checked: false; text: "Auto-update" }

                GenericAppContentAreaButtons.Accept {
                    enabled: false
                    text: "Accept refined parameters"
                }
                CheckBox { enabled: false; checked: true; text: "Auto-accept" }

            }
        }
    }

    // Spacer

    Item { Layout.fillHeight: true }

    // Groupbox

    GenericAppElements.FlowButtons {
        documentationUrl: "https://easydiffraction.org/umanual_use.html#3.2.5.-analysis"
        goPreviousButton: GenericAppContentAreaButtons.GoPrevious {
            text: "Experimental Data"
            ToolTip.text: qsTr("Go to the previous step: Experimental data")
            onClicked: {
                Generic.Variables.toolbarCurrentIndex = Generic.Variables.ExperimentalDataIndex
            }
            GenericAppElements.GuideWindow {
                message: "Click here to go to the previous step: Experimental data.\n\nAlternatively, you can click on the 'Experimental data' button in toolbar."
                position: "top"
                guideCurrentIndex: 4
                toolbarCurrentIndex: Generic.Variables.AnalysisIndex
                guidesCount: Generic.Variables.AnalysisGuidesCount
            }
        }
        goNextButton: GenericAppContentAreaButtons.GoNext {
            text: "Summary"
            enabled: proxy.refinementDone
            highlighted: proxy.refinementDone
            ToolTip.text: qsTr("Go to the next step: Summary")
            onClicked: {
                //Generic.Variables.analysisPageFinished = true
                Generic.Variables.toolbarCurrentIndex = Generic.Variables.SummaryIndex
            }
            GenericAppElements.GuideWindow {
                message: "Click here to go to the next step: Summary.\n\nThis button will be enabled after fitting is done."
                position: "top"
                guideCurrentIndex: 5
                toolbarCurrentIndex: Generic.Variables.AnalysisIndex
                guidesCount: Generic.Variables.AnalysisGuidesCount
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
                Generic.Variables.chiSquared = res.final_chi_sq ? res.final_chi_sq.toFixed(2) : Generic.Variables.chiSquared
                Generic.Variables.numRefinedPars = res.num_refined_parameters ? res.num_refined_parameters : Generic.Variables.numRefinedPars
                let s = `${res.refinement_message}`
                s += res.final_chi_sq ? `\n\nGoodness-of-fit (\u03c7\u00b2): ${(res.final_chi_sq).toFixed(2)}` : ""
                s += res.num_refined_parameters ? `\nNum. refined parameters: ${res.num_refined_parameters}` : ""
                //s += res.nfev ? `\nNumber of evaluations of the objective functions: ${res.nfev}` : ""
                //s += res.nit ? `\nNumber of iterations performed by the optimizer: ${res.nit}` : ""
                //s += res.started_chi_sq ? `\nStarted goodness-of-fit (\u03c7\u00b2): ${(res.started_chi_sq).toFixed(2)}` : ""
                //s += res.refinement_time ? `\nRefinement time in seconds: ${(res.refinement_time).toFixed(2)}` : ""
                return s
            }
        }
    }
}

