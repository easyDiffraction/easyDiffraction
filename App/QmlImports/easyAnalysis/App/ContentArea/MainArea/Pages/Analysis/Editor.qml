import QtQuick 2.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyDiffraction 1.0 as Specific

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
            font.pointSize: Generic.Style.fontPointSize
            //antialiasing: true
            wrapMode: Text.NoWrap
            text: showContent ? Specific.Variables.cif.calculations : ""
        }
    }
}



