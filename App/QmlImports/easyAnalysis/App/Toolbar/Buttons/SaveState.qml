import QtQuick 2.12
import QtQuick.Controls 2.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar
import easyDiffraction 1.0 as Specific

GenericAppToolbar.ToolButton {
    enabled: Specific.Variables.needToSave
    attention: true
    icon.source: Generic.Variables.thirdPartyIconsPath + "save.svg"
    ToolTip.text: qsTr("Save current state of the project")

    onClicked: {
        Generic.Variables.showSaveDialog = 0
        if (Specific.Variables.projectFilePathSelected) {
            Generic.Constants.proxy.saveProject()
        } else {
            Generic.Variables.showSaveDialog = 1
        }
    }
}
