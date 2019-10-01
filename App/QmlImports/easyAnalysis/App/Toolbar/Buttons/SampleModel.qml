import QtQuick 2.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar

GenericAppToolbar.Button {
    icon.source: Generic.Variables.thirdPartyIconsPath + "gem.svg"
    text: qsTr("Sample Model")
    ToolTip.text: qsTr("Sample model description page")
    //finished: Generic.Variables.samplePageFinished
}
