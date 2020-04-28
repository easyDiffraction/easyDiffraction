import QtQuick 2.12
import QtQuick.Controls 2.12

import easyAnalysis 1.0 as Generic
import easyDiffraction 1.0 as Specific
import easyAnalysis.App.Elements 1.0 as GenericAppElements


Column {
    property alias model: contentListView.model

    property int borderWidth: 1
    property int cellHeight: 34
    property int rowCountToDisplayWithoutHeader: 12

    property real scrollBarPosition: 0

    property bool isRefined: false

    property string rowBackgroundColor: 'white'
    property string alternateRowBackgroundColor: '#f7f7f7'
    property string highlightedRowBackgroundColor: Generic.Style.tableHighlightRowColor//"#2a99d9"
    property string rowForegroundColor: "black"
    property string highlightedRowForegroundColor: Generic.Style.tableHighlightTextColor//"white"
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
        const typeColumnWidth = 30
        const refineColumnWidth = cellHeight * 1.5
        const flexibleColumnsWidth = allColumnWidth - numberColumnWidth - typeColumnWidth - refineColumnWidth
        const flexibleColumnsCount = 4
        if (column === 1)       // No.
            return numberColumnWidth
        else if (column === 2)  // Type
            return typeColumnWidth
        else if (column === 3)  // Label
            return 2.6 * flexibleColumnsWidth / flexibleColumnsCount
        else if (column === 4)  // Value
            return 0.5 * flexibleColumnsWidth / flexibleColumnsCount
        else if (column === 5)  // Units
            return 0.4 * flexibleColumnsWidth / flexibleColumnsCount
        else if (column === 6)  // Error
            return 0.5 * flexibleColumnsWidth / flexibleColumnsCount
        else if (column === 7)  // Fit
            return refineColumnWidth
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
                            leftPadding: Generic.Style.fontPixelSize
                            rightPadding: Generic.Style.fontPixelSize
                            font.pointSize: Generic.Style.fontPointSize
                            font.family: Generic.Style.fontFamily
                            text: "No."
                        }
                        Text {
                            width: cellWidthProvider(2) + cellWidthProvider(3)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignLeft
                            leftPadding: 0
                            rightPadding: Generic.Style.fontPixelSize
                            font.pointSize: Generic.Style.fontPointSize
                            font.family: Generic.Style.fontFamily
                            text: "Label"
                        }
                        Text {
                            width: cellWidthProvider(4)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: Generic.Style.fontPixelSize
                            rightPadding: 0
                            font.pointSize: Generic.Style.fontPointSize
                            font.family: Generic.Style.fontFamily
                            text: "Value"
                        }
                        Text {
                            width: cellWidthProvider(5)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignLeft
                            leftPadding: Generic.Style.fontPixelSize * 0.5
                            rightPadding: Generic.Style.fontPixelSize
                            font.pointSize: Generic.Style.fontPointSize
                            font.family: Generic.Style.fontFamily
                            text: ""
                        }
                        Text {
                            width: cellWidthProvider(6)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: Generic.Style.fontPixelSize
                            rightPadding: Generic.Style.fontPixelSize
                            font.pointSize: Generic.Style.fontPointSize
                            font.family: Generic.Style.fontFamily
                            text: "Error"
                        }
                        Text {
                            width: cellWidthProvider(7)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            font.pointSize: Generic.Style.fontPointSize
                            font.family: Generic.Style.fontFamily
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

                ScrollBar.horizontal: ScrollBar {
                    policy: ScrollBar.AlwaysOff
                }
                ScrollBar.vertical: ScrollBar {
                    id: verticalScrollBar
                    policy: ScrollBar.AsNeeded
                    minimumSize: 1 / rowCountToDisplayWithoutHeader
                }



                // Content row
                delegate: Rectangle {
                    id: contentRow
                    width: parent.width
                    height: cellHeight
                    color: {
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
                            leftPadding: Generic.Style.fontPixelSize
                            rightPadding: Generic.Style.fontPixelSize
                            font.pointSize: Generic.Style.fontPointSize
                            font.family: Generic.Style.fontFamily
                            text: index + 1
                            //color: foregroundColor()
                            color: rowForegroundColor
                        }

                        Text {
                            width: cellWidthProvider(2)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignLeft
                            leftPadding: 0
                            rightPadding: 0
                            font.pixelSize: Generic.Style.fontPixelSize + 2
                            font.family: Generic.Style.fitablesFontFamily
                            //text: labelList[0] === "phases" ? "\u0041" : "\u0042"
                            //color: blockColor(index)
                            textFormat: Text.RichText
                            text: {
                                var arr = labelList
                                if (typeof arr === 'undefined' || arr === null) {
                                    return ""
                                }

                                // Chose icon according to the text
                                let txt = ""
                                if (arr[0] === "phases") {
                                    txt = "\u0041"
                                } else if (arr[0] === "experiments") {
                                    txt = "\u0042"
                                }

                                // Half-hide if previous element is the same
                                const labelListRole = 265
                                const modelIndex = contentListView.model.index(index, 0)
                                const previousModelIndex = contentListView.model.index(index-1, 0)
                                const previousLabelList = getModelData(labelListRole, previousModelIndex)
                                if (typeof previousLabelList !== "undefined" && labelList[0] === previousLabelList[0]) {
                                    txt = `<font color=#b3b3b3>${txt}</font>`
                                }

                                return txt
                            }
                        }

                        Text {
                            width: cellWidthProvider(3)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignLeft
                            leftPadding: 0
                            rightPadding: Generic.Style.fontPixelSize
                            font.pixelSize: Generic.Style.fontPixelSize
                            font.family: Generic.Style.fontFamily
                            //text: label
                            //color: foregroundColor()
                            textFormat: Text.RichText
                            text: {
                                var arr = labelList
                                if (typeof arr === 'undefined' || arr === null) {
                                    return ""
                                }

                                // Hightlight the last element
                                arr[arr.length-1] = `<font color=${Generic.Style.buttonIconFinishedColor}><b>${arr[arr.length-1]}</b></font>`

                                // Half-hide if previous element is the same
                                const labelListRole = 265
                                const modelIndex = contentListView.model.index(index, 0)
                                const previousModelIndex = contentListView.model.index(index-1, 0)
                                const previousLabelList = getModelData(labelListRole, previousModelIndex)
                                for (let i = 1; i < labelList.length; ++i) {
                                    if (typeof previousLabelList !== "undefined" && labelList[i] === previousLabelList[i]) {
                                        arr[i] = `<font color=#777>${arr[i]}</font>`
                                    } else {
                                        if (i === labelList.length - 2 || i === labelList.length - 3 || i === labelList.length - 4) {
                                            arr[i] = `<font color=#000><b>${arr[i]}</b></font>`
                                        }
                                    }
                                }

                                // Skip 1st element and convert to string
                                return arr.slice(1).join(" ")
                            }
                        }
                        TextInput {
                            width: cellWidthProvider(4)
                            height: parent.height
                            enabled: !Specific.Variables.refinementRunning
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: Generic.Style.fontPixelSize
                            rightPadding: 0
                            validator: DoubleValidator {}
                            maximumLength: 8
                            //color: foregroundColor()
                            color: rowForegroundColor
                            font.pointSize: Generic.Style.fontPointSize
                            font.family: Generic.Style.fontFamily
                            text: toFixed(value)
                            onTextChanged: updateSlider()
                            onEditingFinished: {
                                if (valueEdit !== text) {
                                    scrollBarPosition = verticalScrollBar.position
                                    valueEdit = parseFloat(text)
                                }
                            }

                        }
                        Text {
                            width: cellWidthProvider(5)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignLeft
                            leftPadding: Generic.Style.fontPixelSize * 0.5
                            rightPadding: Generic.Style.fontPixelSize
                            font.pointSize: Generic.Style.fontPointSize
                            font.family: Generic.Style.fontFamily
                            //text: thisUnit()
                            //color: foregroundColor2()
                            textFormat: Text.RichText
                            text: {
                                if (typeof(unit) === 'undefined' || unit === null) {
                                    return ""
                                }
                                return unit.replace("^2", "<sup>2</sup>").replace("^-1", "<sup>\uff0d1</sup>")
                            }
                            color: "#999"
                        }
                        Text {
                            width: cellWidthProvider(6)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: Generic.Style.fontPixelSize
                            rightPadding: Generic.Style.fontPixelSize
                            font.pointSize: Generic.Style.fontPointSize
                            font.family: Generic.Style.fontFamily
                            text: error ? error.toFixed(4) : ""
                            //color: foregroundColor()
                            color: rowForegroundColor
                        }
                        CheckBox {
                            width: cellWidthProvider(7)
                            height: parent.height
                            enabled: !Specific.Variables.refinementRunning
                            checked: {
                                if (typeof(refine) !== 'undefined' && refine !== null) {
                                    return refine
                                }
                            }
                            onToggled: {
                                // proper, but slow update of the checkbox
                                // It waits until python updates project, etc.
                                // because of the sequential execution
                                //refineEdit = checked

                                // temporary fix, but imediate update of the checkbox
                                // because of the parallel call of python updates via
                                // Timer (with small delay) using global boolean: isRefined
                                isRefined = checked
                                updateCheckBoxTimer.start()
                            }
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

        // Min edit area
        TextInput {
            id: sliderFromLabel
            width: 80
            height: parent.height
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignLeft
            leftPadding: font.pixelSize
            rightPadding: leftPadding
            selectByMouse: true
            selectedTextColor: "white"
            selectionColor: Generic.Style.tableHighlightRowColor
            validator: DoubleValidator {}
            maximumLength: 8
            font.pointSize: Generic.Style.fontPointSize
            font.family: Generic.Style.fontFamily
            text: toFixed(slider.from)
            onEditingFinished: {
                if (text === toFixed(slider.from))
                    return
                if (parseFloat(text) > parseFloat(sliderToLabel.text))
                    return
                const editValue = parseFloat(text)
                const editRole = 361 // -> minEdit role in FitablesModel.py
                setModelData(editValue, editRole)
            }
            Rectangle {
                z: parent.z - 1
                anchors.fill: parent
                border.width: borderWidth
                border.color: headerBorderColor
            }
        }

        // Slider
        Slider {
            id: slider
            width: parent.width - parent.spacing * 2 - sliderFromLabel.width - sliderToLabel.width
            height: parent.height
            //wheelEnabled: false
            //touchDragThreshold: 10000
            //focus: false
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
                    const editValue = value
                    const editRole = 359 // -> valueEdit role in FitablesModel.py
                    setModelData(editValue, editRole)
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

        // Max edit area
        TextInput {
            id: sliderToLabel
            width: sliderFromLabel.width
            height: parent.height
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignLeft
            leftPadding: font.pixelSize
            rightPadding: leftPadding
            selectByMouse: true
            selectedTextColor: "white"
            selectionColor: Generic.Style.tableHighlightRowColor
            validator: DoubleValidator {}
            maximumLength: 8
            font.pointSize: Generic.Style.fontPointSize
            font.family: Generic.Style.fontFamily
            text: toFixed(slider.to)
            onEditingFinished: {
                if (text === toFixed(slider.to))
                    return
                if (parseFloat(text) < parseFloat(sliderFromLabel.text))
                    return
                const editValue = parseFloat(text)
                const editRole = 362 // -> maxEdit role in FitablesModel.py
                setModelData(editValue, editRole)
            }
            Rectangle {
                z: parent.z - 1
                anchors.fill: parent
                border.width: borderWidth
                border.color: headerBorderColor
            }
        }
    }

    Timer {
        id: updateCheckBoxTimer
        interval: 10
        onTriggered: {
            const editValue = isRefined
            const editRole = 363 // -> refineEdit role in FitablesModel.py
            scrollBarPosition = verticalScrollBar.position
            setModelData(editValue, editRole)
            verticalScrollBar.position = scrollBarPosition
        }
    }

    // LOGIC

    function currentModelIndex() {
        if (contentListView.model !== null)
            return contentListView.model.index(contentListView.currentIndex, 0)
    }

    function getModelData(displayRole, modelIndex = currentModelIndex()) {
        if (contentListView.model !== null)
            return contentListView.model.data(modelIndex, displayRole)
    }

    function setModelData(editValue, editRole, modelIndex = currentModelIndex()) {
        contentListView.model.setData(modelIndex, editValue, editRole)
    }

    function updateSlider() {
        if (!Specific.Variables.projectOpened)
            return
        const from = getModelData(261)  // -> min role in FitablesModel.py
        const to = getModelData(262)    // -> max role in FitablesModel.py
        const value = getModelData(259) // -> value role in FitablesModel.py
        if (typeof from !== "undefined" && slider.from !== from) {
            slider.from = from
        }
        if (typeof to !== "undefined" && slider.to !== to) {
            slider.to = to
        }
        if (typeof value !== "undefined" && slider.value !== value) {
            slider.value = value

        }

            //print("slide")
    }

}
