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
            font.pixelSize: Generic.Style.fontPixelSize
            //antialiasing: true
            wrapMode: Text.NoWrap
            selectByMouse: true
            selectedTextColor: "white"
            selectionColor: Generic.Style.tableHighlightRowColor
            //text: showContent ? Specific.Variables.experimentCif : ""
            textFormat: TextEdit.RichText
            text: Specific.Variables.projectCifDict["experiments"]
                .toString()                                                     // convert to string
                .replace(/\n(_[\w,-]+) /ig, "\n<font color=#2380b5>$1</font> ") // colorize individual keys (with space at the end), e.g., "_setup_wavelength"
                .replace(/\n(_[\w,-]+)/ig, "\n<font color=#669431>$1</font>")   // colorize keys inside loops (with new line at the end), e.g., "_phase_label"
                .replace(/loop_/ig, "<font color=#888>loop_</font>")            // colorize "loop_"
                .replace(/data_\w+/ig, "<font color=#b95e39>$&</font>")         // colorize datablock, e.g., "data_Fe3O4"
                .replace(/\n/ig, "<br />")                                      // change newline to html format

            onEditingFinished: Generic.Constants.proxy.updateExperimentFromGui(text
                                                                               .replace(/<br \/>/ig, "\n")     // convert newline from html format
                                                                               .replace(/<\/?[^>]+>/ig, " "))  // remove html format
        }
    }

}

/*
Rectangle {
    property bool showContent: false

    color: "white"

	Flickable {
		id: flickable
		anchors.fill: parent

		flickableDirection: Flickable.VerticalFlick

        TextArea.flickable: TextArea {
            id: textArea
            anchors.fill: parent
            padding: 10
            readOnly: true
            //font.family: "Monaco"
            font.family: Generic.Style.monoFontFamily
            //antialiasing: true
            //wrapMode: Text.WordWrap
            text: showContent ? Specific.Variables.cif.experiments : ""
        }
        ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded; minimumSize: 0.1 }

    }

}
*/


