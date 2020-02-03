import QtQuick 2.12
import QtQuick.Controls 2.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar

GenericAppToolbar.Button {
    icon.source: Generic.Variables.thirdPartyIconsPath + "cog.svg"
    ToolTip.text: qsTr("Application preferences")

    onClicked: Generic.Variables.showPreferences = 1
}
