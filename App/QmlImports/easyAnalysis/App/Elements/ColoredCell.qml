import QtQuick 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic

RowLayout {
    property string cellColor: "transparent"
    anchors.fill: parent
    spacing: 0

    Item {
        Layout.fillWidth: true
        Layout.fillHeight: true

        Rectangle {
            anchors.fill: parent
            anchors.margins: 2
            color: cellColor
        }
    }

    // Vertical border
    Rectangle {
        Layout.fillHeight: true
        width: Generic.Style.appBorderThickness
        ///color: styleData.selected ? Generic.Style.tableHighlightBorderColor : Generic.Style.tableHeaderRowColor
        color: Generic.Style.tableColumnBorderColor
    }
}
