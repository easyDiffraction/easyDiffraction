import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyDiffraction 1.0 as Specific

GenericAppContentArea.Button {
    Layout.fillWidth: true
    enabled: !Specific.Variables.refinementRunning
    text: Specific.Variables.refinementRunning ?
              "Stop fitting" :
              "Start fitting"
    icon.source: Specific.Variables.refinementRunning ?
                     Generic.Variables.thirdPartyIconsPath + "stop-circle.svg" :
                     Generic.Variables.thirdPartyIconsPath + "play-circle.svg"
}
