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
            //readOnly: true
            color: "#333"
            font.family: Generic.Style.monoFontFamily
            font.pointSize: Generic.Style.fontPointSize
            //antialiasing: true
            wrapMode: Text.Wrap //Text.NoWrap
            selectByMouse: true
            selectedTextColor: "white"
            selectionColor: Generic.Style.tableHighlightRowColor
            //text: showContent ? Specific.Variables.phaseCif : ""
            textFormat: TextEdit.RichText
            text: Specific.Variables.projectCifDict["phases"]
                .toString()                                                     // convert to string
                .replace(/\n(_[\w,-]+) /ig, "\n<font color=#2380b5>$1</font> ") // colorize individual keys (with space at the end), e.g., "_setup_wavelength"
                .replace(/\n(_[\w,-]+)/ig, "\n<font color=#669431>$1</font>")   // colorize keys inside loops (with new line at the end), e.g., "_phase_label"
                .replace(/loop_/ig, "<font color=#888>loop_</font>")            // colorize "loop_"
                .replace(/data_\w+/ig, "<font color=#b95e39>$&</font>")         // colorize datablock, e.g., "data_Fe3O4"
                .replace(/\n/ig, "<br />")                                      // change newline to html format

            onEditingFinished: Generic.Constants.proxy.updatePhaseFromGui(text
                                                                          .replace(/<br \/>/ig, "\n")     // convert newline from html format
                                                                          .replace(/<\/?[^>]+>/ig, " "))  // remove html format
        }
    }

}
