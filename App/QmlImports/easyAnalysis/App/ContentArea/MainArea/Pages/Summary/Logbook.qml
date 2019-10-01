import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Layouts 1.12
import QtCharts 2.3
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements

Rectangle {
    property real coeff: 0.7
    property int extraPadding: 12
    property int ratio: 3

    property int commonMargin: 10

    id: wrapper

    //anchors.fill: parent
    Layout.fillWidth: true



    ScrollView {
        anchors.fill: parent
        clip: true


        GenericAppElements.ColumnLayout {


            ///////
            // JOB
            //////

            TextArea {
                Layout.fillWidth: true
                padding: commonMargin
                readOnly: true
                antialiasing: true
                textFormat: Text.RichText
                text:
"
<h1>" + "proxy.project_name" + "</h1>
<p>
<b>Creation date: </b>11.04.2019<br>
<b>Project folder: </b>" + "proxy.tmp_rcif_dir_name()" + "<br>
<b>Project file: </b>" + "proxy.tmp_rcif_file_name()" + "<br>
<b>Experimental data file: </b>" + "proxy.tmp_rcif_file_name()" + "<br>
<b>Instrument: </b>6T2 at LLB<br>
<b>Sample: </b>" + "proxy.project_name" + "<br>
</p>

<h2>Parameters</h2>
"
            }

            /////////////
            // PARAMETERS
            /////////////

            Row {
                // Left margin
                Item { width: 1.5*commonMargin; height: 1 }
                // Table
                GenericAppElements.ParametersTable {
                    id: dataExplorerTable
                    width: Generic.Variables.mainAreaWidth - 3*commonMargin
                    selectable: false
                    enabled: false
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

           }

            /////////////////////
            // OBS VS. CALC title
            /////////////////////

            TextArea {
                Layout.fillWidth: true
                padding: commonMargin
                topPadding: 3*commonMargin
                bottomPadding: 0
                readOnly: true
                antialiasing: true
                textFormat: Text.RichText
                text:
"
<h2>Fitting</h2>
"
            }

            ///////////////////////
            // OBS VS. CALC figures
            ///////////////////////

            Row {
                z: 70
                enabled: false
                GenericAppElements.ChartView {
                    width: wrapper.width
                    height: width
                    showObs: true
                    showCalc: true
                    showDiff: true
                    showBragg: true
                    showInfo: false
                }
            }

            ///////////////////
            // STRUCTURE title
            ///////////////////

            TextArea {
                z: 60
                Layout.fillWidth: true
                padding: commonMargin
                //topPadding: -commonMargin
                bottomPadding: 0
                readOnly: true
                antialiasing: true
                textFormat: Text.RichText
                text:
"
<h2>Structure</h2>
"
            }

            ////////////
            // STRUCTURE
            ////////////

            Column {
                z: 50
                enabled: false
                topPadding: -100
                GenericAppElements.StructureView {
                    width: wrapper.width
                    height: width
                    showInfo: false
                }
            }




        }
    }
}

