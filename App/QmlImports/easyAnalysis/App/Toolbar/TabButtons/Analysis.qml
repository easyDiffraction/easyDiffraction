import QtQuick 2.12
import QtQuick.Controls 2.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar
import easyDiffraction 1.0 as Specific


GenericAppToolbar.TabButton {
    icon.source: Generic.Variables.thirdPartyIconsPath + "calculator.svg"
    text: qsTr("Analysis")
    toolTipText: qsTr("Analysis and modelling page")
    //finished: Generic.Variables.analysisPageFinished
    blinking: Specific.Variables.refinementRunning
}
