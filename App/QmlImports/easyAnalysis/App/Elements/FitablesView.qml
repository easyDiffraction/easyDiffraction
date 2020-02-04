import QtQuick 2.12
import QtQuick.Controls 2.12

import easyDiffraction 1.0 as Specific

Column {
    property alias model: contentListView.model

    property int borderWidth: 1
    property int cellHeight: 34
    property int rowCountToDisplayWithoutHeader: 10

    property string rowBackgroundColor: 'white'
    property string alternateRowBackgroundColor: '#f7f7f7'
    property string highlightedRowBackgroundColor: "#2a99d9"
    property string rowForegroundColor: "black"
    property string highlightedRowForegroundColor: "white"
    property string headerBackgroundColor: '#eee'
    property string headerBorderColor: '#dedede'

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

    function cellWidthProvider(column) {
        const allColumnWidth = width - borderWidth * 2
        const numberColumnWidth = 40
        const refineColumnWidth = cellHeight * 1.5
        const flexibleColumnsWidth = allColumnWidth - numberColumnWidth - refineColumnWidth
        const flexibleColumnsCount = 4
        if (column === 1)
            return numberColumnWidth
        else if (column === 2)
            return 2.6 * flexibleColumnsWidth / flexibleColumnsCount
        else if (column === 3)
            return 0.5 * flexibleColumnsWidth / flexibleColumnsCount
        else if (column === 4)
            return 0.5 * flexibleColumnsWidth / flexibleColumnsCount
        else if (column === 5)
            return refineColumnWidth
        else if (column === 6)
            return 0.4 * flexibleColumnsWidth / flexibleColumnsCount
        else return 0
    }

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
                        spacing: 0

                        Text {
                            width: cellWidthProvider(1)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            text: "No."
                        }
                        Text {
                            width: cellWidthProvider(2)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignLeft
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            text: "Label"
                        }
                        Text {
                            width: cellWidthProvider(3)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: 0
                            text: "Value"
                        }
                        Text {
                            width: cellWidthProvider(6)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignLeft
                            leftPadding: font.pixelSize * 0.5
                            rightPadding: font.pixelSize
                            text: ""
                        }
                        Text {
                            width: cellWidthProvider(4)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            text: "Error"
                        }
                        Text {
                            width: cellWidthProvider(5)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            text: "Fit"
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
                        return index === contentListView.currentIndex ? highlightedRowForegroundColor : rowForegroundColor
                    }
                    function foregroundColor2() {
                        return index === contentListView.currentIndex ? highlightedRowForegroundColor : "#999"
                    }
                    function backgroundColor() {
                        if (index === contentListView.currentIndex)
                            return highlightedRowBackgroundColor
                        else
                            return index % 2 ? alternateRowBackgroundColor : rowBackgroundColor
                    }

                    Row {
                        anchors.fill: parent
                        spacing: 0

                        Text {
                            width: cellWidthProvider(1)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
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
                            text: label
                            color: foregroundColor()
                        }
                        TextInput {
                            width: cellWidthProvider(3)
                            height: parent.height
                            enabled: !Specific.Variables.refinementRunning
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: 0
                            color: foregroundColor()
                            text: toFixed(value)
                            onTextChanged: {
                                updateSlider()
                            }
                            onEditingFinished: {
                                if (valueEdit !== text) {
                                    valueEdit = parseFloat(text)
                                }
                            }
                        }
                        Text {
                            width: cellWidthProvider(6)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignLeft
                            leftPadding: font.pixelSize * 0.5
                            rightPadding: font.pixelSize
                            text: unit
                            color: foregroundColor2()
                        }
                        Text {
                            width: cellWidthProvider(4)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            text: error ? error.toFixed(4) : ""
                            color: foregroundColor()
                        }
                        CheckBox {
                            width: cellWidthProvider(5)
                            height: parent.height
                            enabled: !Specific.Variables.refinementRunning
                            checked: refine
                            onToggled: refineEdit = checked
                        }
                    }

                    // Change current row by mouse click
                    MouseArea {
                        anchors.fill: parent
                        propagateComposedEvents: true
                        acceptedButtons: Qt.LeftButton
                        onPressed: {
                            contentListView.currentIndex = index
                            mouse.accepted = false
                        }
                    }

                }
                // Content row changed
                onCurrentIndexChanged: {
                    updateSlider()
                }

            }
        }
    }

    // Slider
    Row {
        id: slideRow
        enabled: !Specific.Variables.refinementRunning
        width: parent.width
        height: cellHeight
        spacing: 10

        Label {
            id: sliderFromLabel
            width: 80
            height: parent.height
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignRight
            leftPadding: font.pixelSize
            rightPadding: leftPadding
            background: Rectangle { border.width: borderWidth; border.color: headerBorderColor }
            text: slider.from.toFixed(4)
        }

        Slider {
            id: slider
            width: parent.width - parent.spacing * 2 - sliderFromLabel.width - sliderToLabel.width
            height: parent.height
            //wheelEnabled: false
            //touchDragThreshold: 10000
            //focus: false

            /*
            from: Specific.Variables.projectOpened ? contentListView.model.data(contentListView.model.index(contentListView.currentIndex, 0), Qt.UserRole + 5) : 0
            to: Specific.Variables.projectOpened ? contentListView.model.data(contentListView.model.index(contentListView.currentIndex, 0), Qt.UserRole + 6) : 0
            value: Specific.Variables.projectOpened ? contentListView.model.data(contentListView.model.index(contentListView.currentIndex, 0), Qt.UserRole + 3) : 0
            */

            handle: Rectangle {
                id: sliderHandle
                x: slider.leftPadding + slider.visualPosition * (slider.availableWidth - width)
                y: slider.topPadding + slider.availableHeight / 2 - height / 2
                implicitWidth: 26
                implicitHeight: 26
                radius: 13
                color: slider.pressed ? "#f0f0f0" : "#f6f6f6"
                border.color: "#bdbebf"
                ToolTip.visible: slider.pressed
                ToolTip.text: slider.value.toFixed(4)

            }

            onPressedChanged: {
                if (!pressed) {
                    // Change valueEdit in the table model with new value from slider
                    contentListView.model.setData(contentListView.model.index(contentListView.currentIndex, 0), value, Qt.UserRole + 103)
                }
            }

            //onWheelEnabledChanged:

            /*
            MouseArea {
                    anchors.fill: parent
                    onPressed: {
                        mouse.accepted = false
                    }
                    onReleased: {
                        mouse.accepted = false
                    }
                    onWheel: {
                        mouse.accepted = true
                    }
            }
            */

        }

        Label {
            id: sliderToLabel
            width: sliderFromLabel.width
            height: parent.height
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignLeft
            leftPadding: font.pixelSize
            rightPadding: leftPadding
            background: Rectangle { border.width: borderWidth; border.color: headerBorderColor }
            text: slider.to.toFixed(4)
        }
    }

    function updateSlider() {
        if (!Specific.Variables.projectOpened)
            return
        const from = contentListView.model.data(contentListView.model.index(contentListView.currentIndex, 0), Qt.UserRole + 5)
        const to = contentListView.model.data(contentListView.model.index(contentListView.currentIndex, 0), Qt.UserRole + 6)
        const value = contentListView.model.data(contentListView.model.index(contentListView.currentIndex, 0), Qt.UserRole + 3)
        if (typeof from !== "undefined" && slider.from !== from) {
            slider.from = from
        }
        if (typeof to !== "undefined" && slider.to !== to) {
            slider.to = to
        }
        if (typeof value !== "undefined" && slider.value !== value) {
            slider.value = value
        }
    }

}
