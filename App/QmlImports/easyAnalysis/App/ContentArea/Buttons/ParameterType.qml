import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea

Item {
    property bool isSample: true
    
    implicitHeight: Generic.Style.tableRowHeight
    implicitWidth: implicitHeight

    RowLayout {
        id: cellLayout
        anchors.fill: parent
        spacing: 0

        // Vertical border
        Rectangle {
            Layout.fillHeight: true
            width: Generic.Style.appBorderThickness
            color: selectable && styleData.selected ? Generic.Style.tableHighlightBorderColor : Generic.Style.tableHeaderRowColor
            //color: Generic.Style.tableColumnBorderColor
        }

        GenericAppContentArea.Button {
            id: button
            anchors.fill: parent
            anchors.margins: 2
            anchors.leftMargin: 3
            anchors.rightMargin: 4
            padding: 0
            icon.source: isSample ? Generic.Variables.thirdPartyIconsPath + "gem.svg" : Generic.Variables.thirdPartyIconsPath + "microscope.svg"

            background: Rectangle {
                color: "transparent"
            }
        }
    }
}
