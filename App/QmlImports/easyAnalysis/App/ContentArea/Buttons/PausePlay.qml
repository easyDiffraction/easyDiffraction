import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea

GenericAppContentArea.Button {
    Layout.fillWidth: true
    text: proxy.refinementRunning ? "Stop fitting" : "Start fitting"
    icon.source: proxy.refinementRunning ? Generic.Variables.thirdPartyIconsPath + "stop-circle.svg" : Generic.Variables.thirdPartyIconsPath + "play-circle.svg"
}



