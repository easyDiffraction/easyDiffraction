import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea

GenericAppContentArea.Button {
    Layout.fillWidth: false
    implicitWidth: implicitHeight
    icon.source: Generic.Variables.thirdPartyIconsPath + "undo-alt.svg"
    ToolTip.text: qsTr("Undo parameter changes")
    text: "Undo"
}


