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

    property bool isFitting: true

    Text {
        id: dataChanged
        visible: false
        text: proxy.time_stamp
        onTextChanged: {
            print("Time stamp: ", proxy.time_stamp)

            // Set data
            const parameters = proxy.get_parameters()
            //print("parameters.length", parameters.length)
            //print("parameters", parameters)
            for (let i = 0; i < parameters.length; i++) {
                for (const key in parameters[i]) {
                    dataExplorerTableModel.set(i, {
                        'num':i+1,
                        'group':parameters[i][key]['group'],
                        'subgroup':parameters[i][key]['subgroup'],
                        'parameter':parameters[i][key]['name'],
                        'started':parameters[i][key]['value'],
                        'min':parameters[i][key]['min'],
                        'max':parameters[i][key]['max'],
                        'fit':parameters[i][key]['fit'],
                        'refined':parameters[i][key]['value'].includes('(') ? parameters[i][key]['value'] : "",
                        'error':parameters[i][key]['esd']
                    })
                }
            }
        }
    }


    ///////////
    // Groupbox
    ///////////
    /*
    GenericAppElements.GroupBox {
        title: "Jobs"
        collapsible: false
        visible: false
        content: GenericAppElements.ColumnLayout {
            // Table
            GenericAppElements.ParametersTable {
                selectable: true
                model: ListModel {
                    ListElement { num:"1"; name: "POLARIS CeCuAl3" }
                    ListElement { num:"2"; name: "POLARIS CeCuAl3 + Al" }
                    ListElement { num:"3"; name: "POLARIS CeCuAl3 + Al & DREAM CeCuAl3" }
                }
                Controls1.TableViewColumn { role:"num";    title:"No.";  resizable: false }
                Controls1.TableViewColumn { role:"name";   title:"Name" }
                Controls1.TableViewColumn { role:"remove"; title:"Remove"; resizable: false }
            }
        }
    }
    */

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Parameters"
        id: dataExplorerTable
        collapsible: false
        content: GenericAppElements.ColumnLayout {
            // Table
            GenericAppElements.ParametersTable {
                selectable: true
                selectedRow: 0
                enabled: true
                model: ListModel {
                    id: dataExplorerTableModel
                    ListElement { num:1; group:"sample";      subgroup:"cell";        parameter:"CeCuAl3 a    "; started:"4.25";  min:"";     max:"";     fit:true;   refined:"4.2598";   error:"0.0001" }
                    ListElement { num:6; group:"instrument";  subgroup:"resolution";  parameter:"POLARIS Sig-2"; started:"0.00";  min:"";     max:"";     fit:false;  refined:"";         error:"" }
                    //ListElement { num:1; type:"sample";      group:"cell";       parameter:"CeCuAl3 a    "; started:"4.25";  min:"4.00";     max:"5.00";     fit:true;   refined:"4.2598";   error:"0.0001" }
                    //ListElement { num:6; type:"instrument";  group:"resolution"; parameter:"POLARIS Sig-2"; started:"0.00";  min:"";         max:"";         fit:false;  refined:"";         error:"" }
                }
                Controls1.TableViewColumn { role:"num";         title:"No.";  resizable: false }
                Controls1.TableViewColumn { role:"group";       title:"Type"; resizable: false }
                Controls1.TableViewColumn { role:"subgroup";    title:"Group" }
                Controls1.TableViewColumn { role:"parameter";   title:"Parameter" }
                Controls1.TableViewColumn { role:"min";         title:"Min"; resizable: false }
                Controls1.TableViewColumn { role:"started";     title:"Started" }
                Controls1.TableViewColumn { role:"max";         title:"Max"; resizable: false }
                Controls1.TableViewColumn { role:"fit";         title:"Fit"; resizable: false }
                Controls1.TableViewColumn { role:"refined";     title:"Refined" }
                //Controls1.TableViewColumn { role:"error";       title:"Error" }
            }

            // Slider
            GenericAppElements.RowLayout {
                Text { enabled: false; text: "-\u221E" }
                Slider {
                    enabled: false
                    Layout.fillWidth: true
                    padding: 0
                    from: 0.00
                    value: 1.00
                    to: 2.00
                }
                Text { enabled: false; text: "+\u221E" }
            }


            // Buttons
            GenericAppElements.GridLayout {
                columns: 2

                GenericAppContentAreaButtons.PausePlay {
                    id: pausePlayButton;
                    text: proxy.fitButtonState;
                    onClicked: {
                        const res = proxy.refine()
                        print(res)
                        pausePlayButton.text = proxy.fitButtonState
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
                text: "Sample Model"
                ToolTip.text: qsTr("Go to the previous step: Sample model")
                onClicked: {
                    Generic.Variables.toolbarCurrentIndex = Generic.Variables.SampleModelIndex
                }
            }
            GenericAppContentAreaButtons.GoNext {
                text: "Summary"
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

}

