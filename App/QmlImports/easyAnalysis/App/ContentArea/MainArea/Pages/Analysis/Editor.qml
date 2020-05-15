import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import easyAnalysis 1.0 as Generic
import easyDiffraction 1.0 as Specific
import easyDiffraction.Logic 1.0 as Logic

// Old implementation
/*
Rectangle {
    property bool showContent: false

    color: "white"

	Flickable {
		id: flickable
		anchors.fill: parent
		flickableDirection: Flickable.VerticalFlick
		ScrollBar.vertical: ScrollBar {}
		ScrollBar.horizontal: ScrollBar {}
		clip: true

        boundsBehavior: Flickable.StopAtBounds
        TextArea.flickable: TextArea {
			//anchors.fill: parent
            padding: 10
            readOnly: true
            color: "#333"
            font.family: Generic.Style.monoFontFamily
            font.pixelSize: Generic.Style.fontPixelSize
            //antialiasing: true
            wrapMode: Text.NoWrap
            // this has to be wrapped with the showContent conditional
            // to allow for the iffy view update.
            // Otherwise, one needs to click in the TextView to redraw the content.
            //text: showContent ? Specific.Variables.calculationCif : ""
            text: Specific.Variables.projectCifDict["calculations"].toString()
        }
    }
}
*/

// Same implementation as for Experiment and Sample text viewers
Rectangle {
    width: parent.width
    height: parent.height

    color: "white"

    ScrollView {
        anchors.fill: parent
        clip: true

        TextArea {
            readOnly: true

            padding: 10
            wrapMode: Text.NoWrap

            color: "#333"
            selectedTextColor: "black"
            selectionColor: Generic.Style.tableHighlightRowColor
            selectByMouse: true

            font.family: Generic.Style.monoFontFamily
            font.pixelSize: Generic.Style.fontPixelSize
            textFormat: TextEdit.RichText

            text: Logic.Helpers.highlightCifSyntax(Specific.Variables.projectCifDict["calculations"].toString())
        }
    }
}








