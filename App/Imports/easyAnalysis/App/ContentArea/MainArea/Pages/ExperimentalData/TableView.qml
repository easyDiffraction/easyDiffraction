import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons

Rectangle {
    //anchors.fill: parent

    color: "white"

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

    Component.onCompleted: {
        for (let i = 0; i < Generic.Variables.xObs.length; i++) {
            const x = parseFloat(Generic.Variables.xObs[i]).toFixed(3)
            const y = parseFloat(Generic.Variables.yObs[i]).toFixed(3)
            const sy = parseFloat(Generic.Variables.syObs[i]).toFixed(3)
            listModel.append( { x: x, y: y, sy: sy } )
        }
    }

}
