import QtQuick 2.12
import QtQuick.Controls 2.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar
import easyDiffraction 1.0 as Specific

GenericAppToolbar.ToolButton {
    enabled: Specific.Variables.canRedo
    icon.source: Generic.Variables.thirdPartyIconsPath + "redo-alt.svg"
    toolTipText: qsTr("Redo") + " " + Specific.Variables.redoText

    onClicked: Specific.Variables.calculatorInterface.redo()
}
