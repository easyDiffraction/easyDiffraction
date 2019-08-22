import QtQuick 2.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyDiffraction 1.0 as Specific

Rectangle {
    color: "white"

    Text {
        id: dataChanged
        visible: false
        text: proxy.time_stamp
        onTextChanged: {
            print("Time stamp: ", proxy.time_stamp)

            // Set data
            textArea.text = proxy.rcif_as_string()
        }
    }

    ScrollView {
        anchors.fill: parent
        clip: true

        TextArea {
            id: textArea
            //anchors.fill: parent
            padding: 10
            readOnly: true
            font.family: Generic.Style.monoFontFamily
            antialiasing: true
            wrapMode: Text.WordWrap
            //text: fileContent()
        }
    }

    function fileContent () {
        const xhr = new XMLHttpRequest
        xhr.open("GET", Specific.Variables.resourcesPath + "Examples/CeCuAl3_POLARIS/cecual_vesta.cif", false)
        xhr.send()
        return xhr.responseText
    }

}



