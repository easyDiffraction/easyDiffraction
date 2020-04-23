import QtQuick 2.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar

GenericAppToolbar.TabButton {
    icon.source: Generic.Variables.thirdPartyIconsPath + "clipboard-list.svg"
    text: qsTr("Summary")
    toolTipText: qsTr("Summary page of the work done")
}
