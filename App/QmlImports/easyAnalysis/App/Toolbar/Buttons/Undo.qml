import QtQuick 2.12
import QtQuick.Controls 2.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar
import easyDiffraction 1.0 as Specific

GenericAppToolbar.ToolButton {
    enabled: Specific.Variables.canUndo
    icon.source: Generic.Variables.thirdPartyIconsPath + "undo-alt.svg"
    toolTipText: qsTr("Undo") + " " + Specific.Variables.undoText

    onClicked: Specific.Variables.calculatorInterface.undo()
}
