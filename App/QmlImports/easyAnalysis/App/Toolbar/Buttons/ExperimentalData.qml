import QtQuick 2.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar

GenericAppToolbar.Button {
    icon.source: Generic.Variables.thirdPartyIconsPath + "server.svg"
    text: qsTr("Experimental Data") // Measured data?
    ToolTip.text: qsTr("Experimental data page")
    //finished: Generic.Variables.dataPageFinished
}
