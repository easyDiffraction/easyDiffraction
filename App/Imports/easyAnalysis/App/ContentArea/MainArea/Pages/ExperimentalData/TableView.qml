import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons

Rectangle {
    //anchors.fill: parent

    color: "white"

    ////////////////////////
    // Check if data changed
    ////////////////////////

    Text {
        id: dataChanged
        visible: false
        text: proxy.time_stamp
        onTextChanged: {
            print("Time stamp: ", proxy.time_stamp)

            // remove old data points
            listModel.clear()

            for (let i = 0, len = proxy.tmp_tth_list().length; i < len; i++ ) {
                const x = proxy.tmp_tth_list()[i]
                const yobs = proxy.tmp_int_u_list()[i]
                const syobs = proxy.tmp_sint_u_list()[i]

                listModel.append( { x: x, y: yobs, sy: syobs } )
            }
        }
    }

    ListModel {
        id: listModel
    }

    GenericAppElements.ParametersTable {
        customFrameVisible: false
        anchors.fill: parent
        model: listModel
        Controls1.TableViewColumn { role:"x";  title:"TOF";   resizable: false; width: Generic.Variables.mainAreaWidth / 4 - 1 }
        Controls1.TableViewColumn { role:"y";  title:"Yobs";  resizable: false; width: Generic.Variables.mainAreaWidth / 4 - 1 }
        Controls1.TableViewColumn { role:"sy"; title:"sYobs"; resizable: false; width: Generic.Variables.mainAreaWidth / 4 - 1 }
        Controls1.TableViewColumn { }
    }
}
