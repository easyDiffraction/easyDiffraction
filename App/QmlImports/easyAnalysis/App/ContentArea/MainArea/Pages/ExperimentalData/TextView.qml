import QtQuick 2.12
import QtQuick.Controls 2.12

import easyAnalysis 1.0 as Generic
import easyDiffraction 1.0 as Specific
import easyDiffraction.Logic 1.0 as Logic

Rectangle {
    width: parent.width
    height: parent.height

    color: "white"

    ScrollView {
        anchors.fill: parent
        clip: true

        TextArea {
            padding: 10
            wrapMode: Text.NoWrap

            color: "#333"
            selectedTextColor: "black"
            selectionColor: Generic.Style.tableHighlightRowColor
            selectByMouse: true

            font.family: Generic.Style.monoFontFamily
            font.pixelSize: Generic.Style.fontPixelSize
            textFormat: TextEdit.RichText

            text: Logic.Helpers.highlightCifSyntax(Specific.Variables.projectCifDict["experiments"].toString())
            onEditingFinished: Generic.Constants.proxy.updateExperimentFromGui(Logic.Helpers.removeHtmlTags(text))
        }
    }
}
