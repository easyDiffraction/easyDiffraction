import QtQuick 2.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.Controls 1.0 as GenericControls
import easyDiffraction 1.0 as Specific

Column {
    property alias model: contentListView.model

    property int borderWidth: 1
    property int cellHeight: 34
    property int rowCountToDisplayWithoutHeader: 1

    property string rowBackgroundColor: 'white'
    property string alternateRowBackgroundColor: '#f7f7f7'
    property string highlightedRowBackgroundColor: "#2a99d9"
    property string rowForegroundColor: "black"
    property string highlightedRowForegroundColor: "white"
    property string headerBackgroundColor: '#eee'
    property string headerBorderColor: '#dedede'

    //property string colorCell: "black"

    height: childrenRect.height
    spacing: 12

    function toFixed(value, precision = 4) {
        if (typeof value === 'number')
            return value.toFixed(precision)
        else if (typeof value === 'string')
            return value
        else
            return ""
    }

    function cellWidthProvider() {
        const allColumnWidth = width - borderWidth * 2
        const flexibleColumnsCount = 6
        return allColumnWidth / flexibleColumnsCount
    }

    ////////////////////////
    // Check if data changed
    ////////////////////////

    Rectangle {
        id: listViewWrapper
        width: parent.width
        height: childrenRect.height
        border.color: headerBorderColor
        border.width: borderWidth

        Column {
            width: parent.width - parent.border.width * 2
            height: childrenRect.height + parent.border.width * 2
            spacing: 0
            padding: parent.border.width

            // Header
            ListView {
                id: headerListView
                width: parent.width
                height: cellHeight
                enabled: false

                header: Rectangle {
                    width: parent.width
                    height: cellHeight
                    color: headerBackgroundColor

                    Row {
                        anchors.fill: parent

                        Text {
                            width: cellWidthProvider()
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pixelSize: Generic.Style.fontPixelSize
                            text: "a (\u212B)"
                        }
                        Text {
                            width: cellWidthProvider()
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pixelSize: Generic.Style.fontPixelSize
                            text: "b (\u212B)"
                        }
                        Text {
                            width: cellWidthProvider()
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pixelSize: Generic.Style.fontPixelSize
                            text: "c (\u212B)"
                        }
                        Text {
                            width: cellWidthProvider()
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pixelSize: Generic.Style.fontPixelSize
                            text: "alpha (°)"
                        }
                        Text {
                            width: cellWidthProvider()
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pixelSize: Generic.Style.fontPixelSize
                            text: "beta (°)"
                        }
                        Text {
                            width: cellWidthProvider()
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pixelSize: Generic.Style.fontPixelSize
                            text: "gamma (°)"
                        }
                    }
                }
            }

            // Main content
            ListView {
                id: contentListView
                width: parent.width
                height: cellHeight * rowCountToDisplayWithoutHeader
                clip: true
                boundsBehavior: Flickable.StopAtBounds

                ScrollBar.horizontal: ScrollBar { policy: ScrollBar.AlwaysOff }
                ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded; minimumSize: 1 / rowCountToDisplayWithoutHeader }

                // Content row
                delegate: Rectangle {
                    id: contentRow
                    width: parent.width
                    height: cellHeight
                    color: backgroundColor()

                    function foregroundColor() {
                        return rowForegroundColor
                    }
                    function backgroundColor() {
                        return index % 2 ? alternateRowBackgroundColor : rowBackgroundColor
                    }

                    Row {
                        anchors.fill: parent

                        Text {
                            width: cellWidthProvider()
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pixelSize: Generic.Style.fontPixelSize
                            text: toFixed(length_a)
                            color: foregroundColor()
                            GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.OnAnalysisPage }
                        }
                        Text {
                            width: cellWidthProvider()
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pixelSize: Generic.Style.fontPixelSize
                            text: toFixed(length_b)
                            color: foregroundColor()
                            GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.OnAnalysisPage }
                        }
                        Text {
                            width: cellWidthProvider()
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pixelSize: Generic.Style.fontPixelSize
                            text: toFixed(length_c)
                            color: foregroundColor()
                            GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.OnAnalysisPage }
                        }
                        Text {
                            width: cellWidthProvider()
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pixelSize: Generic.Style.fontPixelSize
                            text: toFixed(angle_alpha)
                            color: foregroundColor()
                            GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.OnAnalysisPage }
                        }
                        Text {
                            width: cellWidthProvider()
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pixelSize: Generic.Style.fontPixelSize
                            text: toFixed(angle_beta)
                            color: foregroundColor()
                            GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.OnAnalysisPage }
                        }
                        Text {
                            width: cellWidthProvider()
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pixelSize: Generic.Style.fontPixelSize
                            text: toFixed(angle_gamma)
                            color: foregroundColor()
                            GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.OnAnalysisPage }
                        }
                    }


                }

            }
        }
    }

}
