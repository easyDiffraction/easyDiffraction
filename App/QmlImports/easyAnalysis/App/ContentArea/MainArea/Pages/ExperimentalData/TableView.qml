import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons
import easyDiffraction 1.0 as Specific

Rectangle {
    //property alias headerModel: headerTableView.model
    //property alias dataModel: contentTableView.model

    property bool editable: false

    property int borderWidth: 0
    property int cellWidth: 130
    property int cellHeight: 30
    property int rowCountToDisplayWithoutHeader: 3

    property string rowBackgroundColor: 'white'
    property string alternateRowBackgroundColor: '#f7f7f7'
    property string headerBackgroundColor: '#eee'
    property string headerBorderColor: '#dedede'

    width: parent.width
    height: parent.height
    border.color: headerBorderColor
    border.width: borderWidth

    Column {
        width: parent.width
        height: parent.height
        x: borderWidth
        y: borderWidth
        spacing: 0
        clip: true

        // Header
        TableView {
            id: headerTableView
            width: parent.width//cellWidth * columns
            height: cellHeight
            enabled: false

            model: Specific.Variables.projectOpened ? proxy.measuredDataHeader : null

            delegate: Rectangle {
                implicitWidth: cellWidth
                implicitHeight: cellHeight
                color: headerBackgroundColor

                Text {
                    anchors.fill: parent
                    leftPadding: font.pixelSize
                    rightPadding: leftPadding
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignRight
                    enabled: false
                    text: display
                }
            }
        }

        // Main content
        TableView {
            id: contentTableView
            width: parent.width//cellWidth * columns
            height: parent.height - headerTableView.height
            clip: true
            boundsBehavior: Flickable.StopAtBounds

            ScrollBar.horizontal: ScrollBar { policy: ScrollBar.AlwaysOff }
            //ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded; minimumSize: 1 / contentTableView.columns }
            ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }

            model: Specific.Variables.projectOpened ? proxy.measuredData : null

            delegate: Rectangle {
                implicitWidth: cellWidth
                implicitHeight: cellHeight
                color: row % 2 ? alternateRowBackgroundColor : rowBackgroundColor

                TextInput {
                    anchors.fill: parent
                    leftPadding: font.pixelSize
                    rightPadding: leftPadding
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignRight
                    enabled: editable
                    text: display.toFixed(4)
                    onEditingFinished: edit = text
                }
            }
        }
    }
}
