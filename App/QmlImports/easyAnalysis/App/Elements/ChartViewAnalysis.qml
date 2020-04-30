import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtCharts 2.3

import easyAnalysis 1.0 as Generic
import easyAnalysis.Controls 1.0 as GenericControls
import easyAnalysis.App.Elements 1.0 as GenericAppElements

import easyDiffraction 1.0 as Specific

ColumnLayout {
    property bool showObs: false
    property bool showCalc: false
    property bool showDiff: false
    property bool showBragg: false
    property bool showInfo: true

    property int extraPadding: 12
    property int borderWidth: 2
    property int infoPadding: 10
    property int xScaleZoom: 0
    property int yScaleZoom: 0

    property font commonFont: Qt.font({ family: Generic.Style.fontFamily, pointSize: Generic.Style.fontPointSize })

    property int globalAnimationDuration: 1000
    property var globalAnimationOptions: ChartView.SeriesAnimations //ChartView.AllAnimations //ChartView.NoAnimation

    property var tthHklDict: ({})

    spacing: 0

    ////////////////////////
    // Check if data changed
    ////////////////////////

    Timer {
        id: projectChangedTimer
        interval: 100
        repeat: false
        onTriggered: adjustLeftAxesAnchor()
    }

    Text {
        visible: false
        text: JSON.stringify(Specific.Variables.projectDict)
        onTextChanged: projectChangedTimer.restart()
    }

    ///////////////////////
    // Full chart container
    ///////////////////////

    ColumnLayout {
        id: chartContainer
        spacing: 0

        //////////////////////
        // Top chart container
        //////////////////////
        Rectangle {
            id: topChartContainer
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "transparent"
            clip: true

            // Data selector
            Row {
                visible: Specific.Variables.isPolarized
                height: Specific.Variables.isPolarized ? implicitHeight : 0
                z: 1000
                anchors.top: topChart.top
                anchors.topMargin: -7
                anchors.horizontalCenter: parent.horizontalCenter

                spacing: 10

                RadioButton {
                    text: qsTr("Up \uff0b Down")
                    checked: Specific.Variables.dataType === "Sum"
                    onClicked: Specific.Variables.dataType = "Sum"
                }
                RadioButton {
                    text: qsTr("Up \uff0d Down")
                    checked: Specific.Variables.dataType === "Difference"
                    onClicked: Specific.Variables.dataType = "Difference"
                }
                RadioButton {
                    text: qsTr("Up")
                    checked: Specific.Variables.dataType === "Up"
                    onClicked: Specific.Variables.dataType = "Up"
                }
                RadioButton {
                    text: qsTr("Down")
                    checked: Specific.Variables.dataType === "Down"
                    onClicked: Specific.Variables.dataType = "Down"
                }
            }

            //////////////////////////
            // Top chart (Iobs, Icalc)
            //////////////////////////

            ChartView {
                id: topChart
                //enabled: false
                anchors.fill: parent
                anchors.margins: -extraPadding
                anchors.topMargin: Specific.Variables.isPolarized ? 18 : -extraPadding
                anchors.bottomMargin: showDiff ? -4*extraPadding : -extraPadding
                antialiasing: true // conflicts with useOpenGL: true in ScatterSeries
                backgroundRoundness: 0
                backgroundColor: "transparent"
                titleFont: commonFont
                legend.visible: false

                // Custom Legend
                Item {
                    opacity: Generic.Variables.showLegend ? 1 : 0
                    Behavior on opacity {
                        NumberAnimation {
                            duration: 500
                        }
                    }

                    y: topChart.plotArea.top + 10
                    x: topChart.plotArea.right - width - 10
                    width: childrenRect.width
                    height: childrenRect.height

                    // Background
                    Rectangle {
                        width: parent.width
                        height: parent.height
                        opacity: 0.75
                        color: Generic.Style.tableHeaderRowColor //"white"
                        border.color: Generic.Style.mainAreaTabBorderColor //"#ddd"
                        border.width: Generic.Style.appBorderThickness //1
                    }

                    // Info
                    Grid {
                        padding: 10
                        columnSpacing: 10
                        rowSpacing: 5
                        columns: 2
                        Text { text: "■"; color: obsArea.color; font.family: Generic.Style.fontFamily; font.pointSize: Generic.Style.fontPointSize * 2; lineHeightMode: Text.FixedHeight; lineHeight: Generic.Style.fontPointSize; verticalAlignment: Text.AlignVCenter; height: Generic.Style.fontPointSize }
                        Text { text: obsArea.name; font: commonFont}
                        Text { text: "–"; color: calcSeries.color; font.family: Generic.Style.fontFamily; font.pointSize: Generic.Style.fontPointSize * 2; font.bold: true; lineHeightMode: Text.FixedHeight; lineHeight: Generic.Style.fontPointSize; verticalAlignment: Text.AlignVCenter; height: Generic.Style.fontPointSize }
                        Text { text: calcSeries.name; font: commonFont}
                        Text { text: "--"; color: calcBkgSeries.color; font.family: Generic.Style.fontFamily; font.pointSize: Generic.Style.fontPointSize * 2; font.bold: true; lineHeightMode: Text.FixedHeight; lineHeight: Generic.Style.fontPointSize; verticalAlignment: Text.AlignVCenter; height: Generic.Style.fontPointSize }
                        Text { text: calcBkgSeries.name; font: commonFont}
                    }
                }

                // Plot Info (after refinement)
                Item {
                    visible: Generic.Variables.numRefinedPars !== " " && Generic.Variables.chiSquared !==  " "

                    opacity: Generic.Variables.showRefinemetResults ? 1 : 0
                    Behavior on opacity {
                        NumberAnimation {
                            duration: 500
                        }
                    }

                    y: topChart.plotArea.top + 10
                    x: topChart.plotArea.left + 10
                    width: childrenRect.width
                    height: childrenRect.height

                    // Background
                    Rectangle {
                        width: parent.width
                        height: parent.height
                        opacity: 0.75
                        color: Generic.Style.tableHeaderRowColor //"white"
                        border.color: Generic.Style.mainAreaTabBorderColor //"#ddd"
                        border.width: Generic.Style.appBorderThickness //1
                    }

                    // Info
                    Grid {
                        padding: 10
                        columnSpacing: 10
                        rowSpacing: 5
                        columns: 2
                        Text { text: 'Goodness-of-fit (\u03c7\u00b2):'; font: commonFont }
                        Text { text: Generic.Variables.chiSquared; font: commonFont } // Generic.Variables.chiSquared
                        Text { text: 'Fit parameters:'; font: commonFont }
                        Text { text: Generic.Variables.numRefinedPars; font: commonFont } // Generic.Variables.numRefinedPars
                    }
                }

                animationDuration: globalAnimationDuration

                // X-axis for measured and calculated data

                ValueAxis {
                    id: axisX
                    lineVisible: false
                    tickType: ValueAxis.TicksFixed
                    tickCount: 5
                    minorTickCount: 1
                    labelFormat: "%.0f"
                    titleVisible: !showDiff
                    titleText: "2\u03B8 (deg)"
                    labelsVisible: !showDiff
                    labelsFont: commonFont
                    titleFont: commonFont
                    min: Specific.Variables.calculationByIndex(0).limits.main.x_min
                    max: Specific.Variables.calculationByIndex(0).limits.main.x_max
                }

                // Y-axis for measured and calculated data

                ValueAxis {
                    id: axisY
                    lineVisible: false
                    tickType: ValueAxis.TicksFixed
                    tickCount: 5
                    minorTickCount: 1
                    labelFormat: "%.0f" //"%.0e"
                    titleText: showCalc ? "Iobs, Icalc, Ibkg" : "Iobs"
                    labelsFont: commonFont
                    titleFont: commonFont
                    min: {
                        if (!Specific.Variables.calculatedData || !Specific.Variables.measuredData) {
                            return 1
                        }
                        const max = Math.max(Specific.Variables.measuredData.yMax, Specific.Variables.calculatedData.yMax)
                        const min = Math.min(Specific.Variables.measuredData.yMin, Specific.Variables.calculatedData.yMin)
                        return min - 0.075*max
                    }
                    max: {
                        if (!Specific.Variables.calculatedData || !Specific.Variables.measuredData) {
                            return 1
                        }
                        const max = Math.max(Specific.Variables.measuredData.yMax, Specific.Variables.calculatedData.yMax)
                        return max + 0.075*max
                    }
                }

                // Measured curve

                AreaSeries {
                    id: obsArea
                    visible: showObs
                    axisX: axisX
                    axisY: axisY
                    color: Generic.Style.blueColor
                    opacity: 0.4
                    borderColor: Qt.darker(Generic.Style.blueColor, 1.1)
                    borderWidth: 1.5
                    name: "Measured (Iobs)"
                    //useOpenGL: true

                    lowerSeries: LineSeries {
                        id: lowerLineSeries
                        // New approach (fast): pass a reference to LineSeries to python for updating
                        Component.onCompleted: Specific.Variables.measuredData.setLowerSeries(lowerLineSeries)
                    }

                    upperSeries: LineSeries {
                        id: upperLineSeries
                        // New approach (fast): pass a reference to LineSeries to python for updating
                        Component.onCompleted: Specific.Variables.measuredData.setUpperSeries(upperLineSeries)
                    }

                    onHovered: {
                        const p = topChart.mapToPosition(point)
                        const text = qsTr("x: %1\ny: %2").arg(point.x).arg(point.y)
                        infoToolTip.parent = topChart
                        infoToolTip.x = p.x
                        infoToolTip.y = p.y - infoToolTip.height
                        infoToolTip.visible = state
                        infoToolTip.text = text
                        infoToolTip.backgroundColor = obsArea.color
                        infoToolTip.borderColor = Qt.darker(obsArea.color, 1.1)
                    }
                }

                // Calculated background curve

                LineSeries {
                    id: calcBkgSeries
                    visible: showCalc
                    axisX: axisX
                    axisY: axisY
                    color: Generic.Style.greyColor
                    width: 2
                    style: Qt.DotLine
                    name: "Background (Ibkg)"
                    //useOpenGL: true

                    // New approach (fast): pass a reference to LineSeries to python for updating
                    Component.onCompleted: Specific.Variables.calculatedData.setCalcBkgSeries(calcBkgSeries)

                    onHovered: {
                        const p = topChart.mapToPosition(point)
                        const text = qsTr("x: %1\ny: %2").arg(point.x).arg(point.y)
                        infoToolTip.parent = topChart
                        infoToolTip.x = p.x
                        infoToolTip.y = p.y - infoToolTip.height
                        infoToolTip.visible = state
                        infoToolTip.text = text
                        infoToolTip.backgroundColor = calcBkgSeries.color
                        infoToolTip.borderColor = Qt.darker(calcBkgSeries.color, 1.1)
                    }
                }

                // Calculated curve

                LineSeries {
                    id: calcSeries
                    visible: showCalc
                    axisX: axisX
                    axisY: axisY
                    color: Generic.Style.redColor
                    width: 2
                    name: "Calculated (Icalc)"
                    //useOpenGL: true

                    // New approach (fast): pass a reference to LineSeries to python for updating
                    Component.onCompleted: Specific.Variables.calculatedData.setCalcSeries(calcSeries)

                    onHovered: {
                        const p = topChart.mapToPosition(point)
                        const text = qsTr("x: %1\ny: %2").arg(point.x).arg(point.y)
                        infoToolTip.parent = topChart
                        infoToolTip.x = p.x
                        infoToolTip.y = p.y - infoToolTip.height
                        infoToolTip.visible = state
                        infoToolTip.text = text
                        infoToolTip.backgroundColor = calcSeries.color
                        infoToolTip.borderColor = Qt.darker(calcSeries.color, 1.1)
                    }
                }
            }

            //////////////////////////
            // Zoom area for top chart
            //////////////////////////

            // Zoom rectangle

            Rectangle{
                id: recZoom
                visible: false
                border.color: Generic.Style.blueColor
                border.width: 1
                color: Generic.Style.blueColor
                opacity: 0.2
                transform: Scale { origin.x: 0; origin.y: 0; xScale: xScaleZoom; yScale: yScaleZoom}
            }

            // Left mouse button events

            MouseArea {
                anchors.fill: topChartContainer
                acceptedButtons: Qt.LeftButton
                onPressed: {
                    recZoom.x = mouseX
                    recZoom.y = mouseY
                    recZoom.visible = true
                }
                onMouseXChanged: {
                    if (mouseX > recZoom.x) {
                        xScaleZoom = 1
                        recZoom.width = Math.min(mouseX, topChartContainer.width) - recZoom.x
                    } else {
                        xScaleZoom = -1
                        recZoom.width = recZoom.x - Math.max(mouseX, 0)
                    }
                }
                onMouseYChanged: {
                    if (mouseY > recZoom.y) {
                        yScaleZoom = 1
                        recZoom.height = Math.min(mouseY, topChartContainer.height) - recZoom.y
                    } else {
                        yScaleZoom = -1
                        recZoom.height = recZoom.y - Math.max(mouseY, 0)
                    }
                }
                onReleased: {
                    recZoom.visible = false
                    const x = Math.min(recZoom.x, mouseX) - topChart.anchors.leftMargin
                    const y = Math.min(recZoom.y, mouseY) - topChart.anchors.topMargin
                    const width = recZoom.width
                    const height = recZoom.height
                    topChart.zoomIn(Qt.rect(x, y, width, height))
                    //setAxesNiceNumbers()
                    adjustLeftAxesAnchor()
                }
            }

            // Right mouse button events

            MouseArea {
                anchors.fill: topChartContainer
                acceptedButtons: Qt.RightButton
                onClicked: {
                    infoToolTip.visible = false
                    topChart.zoomReset()
                    //setAxesNiceNumbers()
                    adjustLeftAxesAnchor()
                }
            }

        }

        /////////////////////////////
        // Middle chart (Bragg peaks)
        /////////////////////////////

        Rectangle {
            id: middleChartContainer
            visible: showBragg
            Layout.fillWidth: true
            height: 2*extraPadding
            color: "transparent"
            clip: true

            ChartView {
                id: middleChart
                anchors.fill: parent
                anchors.margins: -extraPadding
                anchors.topMargin: -3*extraPadding
                anchors.bottomMargin: -3*extraPadding
                //antialiasing: true // conflicts with useOpenGL: true in ScatterSeries
                legend.visible: false
                backgroundRoundness: 0
                backgroundColor: "transparent"
                titleFont: commonFont

                animationDuration: globalAnimationDuration

                ValueAxis {
                    id: axisXbragg
                    lineVisible: false
                    labelsVisible: false
                    gridVisible:false
                    min: axisX.min
                    max: axisX.max
                    labelFormat: "%.0f"
                    labelsFont: commonFont
                }

                ValueAxis {
                    id: axisYbragg
                    lineVisible: false
                    labelsVisible: false
                    gridVisible:false
                    //tickCount: 0
                    tickType: ValueAxis.TicksDynamic
                    tickAnchor: -2
                    tickInterval: 4
                    min: -1
                    max: 1
                    ///labelFormat: "%.0f"
                    ///labelsFont: commonFont
                }

                /*
                SpecificExample.BraggScatterSeries {
                    //https://forum.qt.io/topic/81484/scatterseries-marker-shapes-brushfilename-seems-to-be-ignored/3
                    axisX: axisXbragg
                    axisY: axisYbragg
                    markerShape: ScatterSeries.MarkerShapeRectangle
                    markerSize: 20
                    borderColor: "transparent"
                    color: "transparent"
                    brushFilename: Generic.Variables.originalIconsPath.replace("file:", "") + "bragg.svg"
                    onClicked: console.log("!!!!!!!!!!!!!!! ")
                    //onClicked: console.log("onClicked: " + point.x + ", " + point.y);
                }
                */

                ScatterSeries {
                    id: braggSeries
                    visible: showBragg
                    axisX: axisXbragg
                    axisY: axisYbragg

                    useOpenGL: false

                    markerShape: ScatterSeries.MarkerShapeRectangle
                    markerSize: 10

                    borderWidth: 0.0001
                    borderColor: "transparent"

                    brushFilename: Generic.Variables.originalIconsPath.replace("file:", "") + "bragg.svg"

                    /*
                    markerSize: 1
                    borderWidth: 0.0001
                    borderColor: "transparent"
                    color: "#333"
                    */
                    /*
                    markerSize: 1
                    borderWidth: 0.00000001
                    borderColor: color
                    color: "#333"
                    */

                    // New approach (fast): pass a reference to LineSeries to python for updating
                    Component.onCompleted: Specific.Variables.braggPeaks.setSeries(braggSeries)

                    /*
                    onHovered: {
                        const phase1 = Specific.Variables.projectDict.phasesIds()[0]
                        const braggPeaks = Specific.Variables.projectDict[phase1].bragg_peaks


                        const position = middleChart.mapToPosition(point)
                        const tth = point.x - parseFloat(Generic.Constants.proxy.tmp_setup_zero_shift())
                        const hklList = tthHklDict[tth]
                        let text = "x: %1\nhkl:".arg(point.x)
                        for (let i = 0; i < hklList.length; i++) {
                            const h = hklList[i]["h"]
                            const k = hklList[i]["k"]
                            const l = hklList[i]["l"]
                            text += " (%2 %3 %4),".arg(h).arg(k).arg(l)
                        }
                        text = text.substring(0, text.length - 1)

                        infoToolTip.parent = middleChart
                        infoToolTip.x = position.x
                        infoToolTip.y = position.y - infoToolTip.height
                        infoToolTip.visible = state
                        infoToolTip.contentItem.text = text
                        infoToolTip.contentItem.color = "grey"
                        infoToolTip.background.border.color = Qt.lighter("grey", 1.75)
                    }
                    */
                }
            }
        }

        //////////////////////////////
        // Bottom chart (Iobs - Icalc)
        //////////////////////////////

        Rectangle {
            id: bottomChartContainer
            visible: showDiff
            Layout.fillWidth: true
            height: 150
            color: "transparent"
            clip: true

            ChartView {
                id: bottomChart
                anchors.fill: parent
                anchors.margins: -extraPadding
                anchors.topMargin: -3*extraPadding
                //anchors.topMargin: -extraPadding// - 20
                antialiasing: true // conflicts with useOpenGL: true in ScatterSeries
                legend.visible: false
                backgroundRoundness: 0
                backgroundColor: "transparent"
                titleFont: commonFont

                animationDuration: globalAnimationDuration

                ValueAxis {
                    id: axisXdiff
                    lineVisible: false
                    tickType: ValueAxis.TicksFixed
                    tickCount: 5
                    minorTickCount: 1
                    min: axisX.min
                    max: axisX.max
                    labelFormat: "%.0f"
                    titleText: "2\u03B8 (deg)"
                    labelsFont: commonFont
                    titleFont: commonFont
                }

                ValueAxis {
                    id: axisYdiff
                    lineVisible: false
                    tickType: ValueAxis.TicksFixed
                    tickCount: 3
                    labelFormat: "%.0f" //"%.0e"
                    titleText: "Iobs - Icalc"
                    labelsFont: commonFont
                    titleFont: commonFont
                    min: {
                        if (!Specific.Variables.calculatedData) {
                            return 1
                        }
                        const min = Specific.Variables.calculatedData.yDiffMin
                        const max = Specific.Variables.calculatedData.yDiffMax
                        const MAX = Math.max(Math.abs(min), Math.abs(max))
                        return Math.sign(min) * MAX - 0.35*MAX
                    }
                    max: {
                        if (!Specific.Variables.calculatedData) {
                            return 1
                        }
                        const min = Specific.Variables.calculatedData.yDiffMin
                        const max = Specific.Variables.calculatedData.yDiffMax
                        const MAX = Math.max(Math.abs(min), Math.abs(max))
                        return Math.sign(max) * MAX + 0.35*MAX
                    }
                }

                AreaSeries {
                    id: diffArea
                    axisX: axisXdiff
                    axisY: axisYdiff
                    color: Generic.Style.greenColor
                    opacity: 0.4
                    borderColor: Generic.Style.darkGreenColor
                    borderWidth: 1.5

                    upperSeries: LineSeries {
                        id: upperDiffSeries
                        // New approach (fast): pass a reference to LineSeries to python for updating
                        Component.onCompleted: Specific.Variables.calculatedData.setUpperDiffSeries(upperDiffSeries)
                    }

                    lowerSeries: LineSeries {
                        id: lowerDiffSeries
                        // New approach (fast): pass a reference to LineSeries to python for updating
                        Component.onCompleted: Specific.Variables.calculatedData.setLowerDiffSeries(lowerDiffSeries)
                    }

                    onHovered: {
                        const p = bottomChart.mapToPosition(point)
                        const text = qsTr("x: %1\ny: %2").arg(point.x).arg(point.y)
                        infoToolTip.parent = bottomChart
                        infoToolTip.x = p.x
                        infoToolTip.y = p.y - infoToolTip.height
                        infoToolTip.visible = state
                        infoToolTip.text = text
                        infoToolTip.backgroundColor = diffArea.color
                        infoToolTip.borderColor = Qt.darker(diffArea.color, 1.1)
                    }
                }
            }
        }
    }

    ////////////
    // Info area
    ////////////

    Rectangle {
        id: infoAreaContainer
        visible: showInfo
        Layout.fillWidth: true
        height: Generic.Style.buttonHeight + 3
        color: "transparent"

        Label {
            id: infoArea
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            height: Generic.Style.buttonHeight
            leftPadding: font.pointSize
            rightPadding: font.pointSize
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("Show coordinates: Hover mouse pointer") + "  •  " + qsTr("Zoom in: Left mouse button") + "  •  " + qsTr("Reset: Right mouse button")
            font.family: Generic.Style.introThinFontFamily
            font.pointSize: Generic.Style.systemFontPointSize + 1
            color: "grey"
            background: Rectangle { color: "white"; opacity: 0.9; border.width: 0; radius: Generic.Style.toolbarButtonRadius }
        }
    }

    //////////
    // Helpers
    //////////

    Text {
        id: dummyText
        visible: false
        font: commonFont
    }

    GenericControls.ToolTip {
        id: infoToolTip
        textColor: "white"
        backgroundOpacity: 0.95
    }

    // Save chart onRefinementDone
    Timer {
        interval: 250
        running: Specific.Variables.refinementDone
        repeat: false
        onTriggered: {
            if (showDiff) {
                //print("save chart")
                const reduced_width = chartContainer.width - 10
                const reduced_height =  chartContainer.height / chartContainer.width * reduced_width
                chartContainer.grabToImage(
                            function(result) {
                                result.saveToFile(Specific.Variables.projectControl.project_dir_absolute_path + "/saved_refinement.png")
                            },
                            Qt.size(reduced_width, reduced_height)
                            )
            }
        }
    }

    // Set animation timers to skip animation once, when you see chart for the 1st time.
    // TO DO: find a better way to do that
    Timer {
        interval: 100
        running: topChart.visible
        repeat: false
        onTriggered: topChart.animationOptions = globalAnimationOptions
    }
    Timer {
        interval: 100
        running: middleChart.visible
        repeat: false
        onTriggered: middleChart.animationOptions = globalAnimationOptions
    }
    Timer {
        interval: 100
        running: bottomChart.visible
        repeat: false
        onTriggered: bottomChart.animationOptions = globalAnimationOptions
    }

    ////////////////
    // On completed
    ////////////////

    //Component.onCompleted: {
        //setAxesNiceNumbers()
        //adjustLeftAxesAnchor()
    //}


    ////////
    // Logic
    ////////

    function setAxesNiceNumbers() {
        axisX.applyNiceNumbers()
        axisY.applyNiceNumbers()
        axisXdiff.applyNiceNumbers()
    }

    function adjustLeftAxesAnchor() {
        let topChartTickMaxWidth = 0.0
        let bottomChartTickMaxWidth = 0.0
        let textHeight = 0.0
        const lineHeight = 1.5
        const extraXShift = 2

        dummyText.text = axisY.max.toFixed(0) // follow axisY.labelFormat
        topChartTickMaxWidth = dummyText.width
        textHeight = dummyText.height / lineHeight

        dummyText.text = axisY.min.toFixed(0) // follow axisY.labelFormat
        if (dummyText.width > topChartTickMaxWidth)
            topChartTickMaxWidth = dummyText.width

        dummyText.text = axisYdiff.min.toFixed(0) // follow axisY.labelFormat
        bottomChartTickMaxWidth = dummyText.width

        const leftMargin = topChartTickMaxWidth - bottomChartTickMaxWidth
        const leftBraggMargin = Math.max(topChartTickMaxWidth, bottomChartTickMaxWidth)

        if (leftMargin > 0) {
            bottomChart.anchors.leftMargin = leftMargin - extraPadding
            topChart.anchors.leftMargin = -extraPadding
        } else {
            topChart.anchors.leftMargin = -leftMargin - extraPadding
            bottomChart.anchors.leftMargin = -extraPadding
        }
        middleChart.anchors.leftMargin = leftBraggMargin - extraPadding + textHeight + extraXShift

        //print(topChart.x, topChart.y, topChart.width, topChart.height)

        //plotInfoRec.anchors.right = topChart.right
        //plotInfoRec.anchors.top = topChart.top
    }

}



