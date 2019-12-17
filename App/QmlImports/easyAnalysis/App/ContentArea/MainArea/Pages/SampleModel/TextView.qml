import QtQuick 2.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyDiffraction 1.0 as Specific

//https://forum.qt.io/topic/90101/textarea-does-not-automatically-scroll/5
Rectangle {
    property bool showContent: false

    color: "white"

    ScrollView {
        anchors.fill: parent
        clip: true

        TextArea {
            //anchors.fill: parent
            padding: 10
            readOnly: true
            color: "#333"
            font.family: Generic.Style.monoFontFamily
            font.pointSize: Generic.Style.fontPointSize
            //antialiasing: true
            wrapMode: Text.NoWrap
            text: showContent ? Specific.Variables.phase_cif : ""
        }
    }

}
