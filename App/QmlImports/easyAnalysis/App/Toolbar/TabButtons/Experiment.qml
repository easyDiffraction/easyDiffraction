import QtQuick 2.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar

GenericAppToolbar.TabButton {
    icon.source: Generic.Variables.thirdPartyIconsPath + "microscope.svg"
    text: qsTr("Experiment")
    toolTipText: qsTr("Experimental settings and data page")
    //finished: Generic.Variables.dataPageFinished
}
