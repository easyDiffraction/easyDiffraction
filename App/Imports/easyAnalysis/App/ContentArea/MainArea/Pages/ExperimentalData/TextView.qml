import QtQuick 2.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyDiffraction 1.0 as Specific

//https://forum.qt.io/topic/90101/textarea-does-not-automatically-scroll/5

Rectangle {
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
            text: fileContent()
        }
		ScrollBar.vertical: ScrollBar {}

    }

    function fileContent () {
        const xhr = new XMLHttpRequest
        xhr.open("GET", Specific.Variables.resourcesPath + "Examples/Fe3O4_6T2_0T_powder_1d/full.dat", false)
        xhr.send()
        return xhr.responseText
    }

}


