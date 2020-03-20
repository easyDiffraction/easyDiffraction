import QtQuick 2.12
import QtQuick.Controls 2.12
import QtGraphicalEffects 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
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

    height: childrenRect.height
    spacing: 12

    function cellWidthProvider(column) {
        const allColumnWidth = width - borderWidth * 2
        const numberColumnWidth = 40
        const iconColumnWidth = cellHeight
        const flexibleColumnsWidth = allColumnWidth - numberColumnWidth - iconColumnWidth
        const flexibleColumnsCount = 1
        if (column === 1)
            return numberColumnWidth
        else if (column === 3)
            return iconColumnWidth
        else
            return flexibleColumnsWidth / flexibleColumnsCount
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
                            width: cellWidthProvider(1)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: "No."
                        }
                        Text {
                            width: cellWidthProvider(2)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignLeft
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: "Label"
                        }
                        Item {
                            width: cellWidthProvider(3)
                            height: width
                            Image {
                                id: headerCellIcon
                                visible: false
                                anchors.fill: parent
                                anchors.margins: 8
                                smooth: true
                                sourceSize.width: parent.width
                                sourceSize.height: parent.height
                                source: Generic.Variables.thirdPartyIconsPath + "trash-alt.svg"
                            }
                            ColorOverlay {
                                source: headerCellIcon
                                anchors.fill: headerCellIcon
                                color: Generic.Style.buttonIconEnabledColor
                            }
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

                model: Specific.Variables.projectOpened ? Specific.Variables.phaseIds : 1

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
                            width: cellWidthProvider(1)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: index + 1
                            color: foregroundColor()
                        }
                        Text {
                            width: cellWidthProvider(2)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignLeft
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: Specific.Variables.projectOpened ? Specific.Variables.phaseIds[index] : ""
                            color: foregroundColor()
                        }
                        GenericAppContentArea.Button {
                            id: button
                            enabled: false
                            ToolTip.visible: hovered
                            ToolTip.text: qsTr("Remove this row from the table")
                            width: cellWidthProvider(3)
                            height: width
                            padding: 3
                            leftPadding: padding
                            rightPadding: padding
                            background: Rectangle {
                                anchors.fill: parent
                                anchors.margins: button.padding
                                anchors.leftMargin: button.leftPadding
                                anchors.rightMargin: button.rightPadding
                                radius: Generic.Style.toolbarButtonRadius
                                border.color: button.highlighted ? Generic.Style.buttonBkgHighlightedColor : Generic.Style.appBorderColor
                                color: {
                                    if (!button.enabled)
                                        return Generic.Style.buttonBkgDisabledColor
                                    var color1 = button.highlighted ? Generic.Style.buttonBkgHighlightedColor : Generic.Style.buttonBkgEnabledColor
                                    var color2 = Generic.Style.buttonBkgBlendColor
                                    var alpha = button.down ? Generic.Style.buttonBkgBlendAlpha : 0.0
                                    return Color.blend(color1, color2, alpha)
                                }
                            }
                            icon.source: Generic.Variables.thirdPartyIconsPath + "minus-circle.svg"
                        }
                    }


                }

            }
        }
    }

}
