import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtCharts 2.3
import easyAnalysis 1.0 as Generic
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
        //running: bottomChart.visible
        repeat: false
        onTriggered: {
            if (Specific.Variables.projectOpened) {
                adjustLeftAxesAnchor()
            }
        }
    }

    Text {
        visible: false
        text: Specific.Variables.projectChangedTime
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

            Rectangle {
                id: plotInfoRect
                z: 100

                anchors.top: topChart.top
                anchors.right: topChart.right
                anchors.topMargin: extraPadding + infoPadding + 30
                anchors.rightMargin: extraPadding + infoPadding + 30

                width: childrenRect.width
                height: childrenRect.height

                color: Generic.Style.tableHeaderRowColor //Generic.Style.buttonBkgFinishedColor
                border.color: Generic.Style.mainAreaTabBorderColor //Generic.Style.buttonBorderFinishedColor
                border.width: Generic.Style.appBorderThickness //1

                opacity: 0.8

                Label {
                    id: plotInfo
                    topPadding: infoPadding/2
                    bottomPadding: topPadding
                    leftPadding: topPadding + font.pixelSize/4
                    rightPadding: leftPadding

                    font.family: Generic.Style.fontFamily
                    font.pointSize: Generic.Style.fontPointSize
                    color: Generic.Style.tableTextColor //Generic.Style.buttonTextFinishedColor

                    text: {
                        const showPars = {
                            'Goodness-of-fit (\u03c7\u00b2)': Generic.Variables.chiSquared,
                            'Num. refined parameters': Generic.Variables.numRefinedPars
                        }
                        let out = ""
                        for (let key in showPars) {
                            if (showPars[key]) {
                                out += "%1: %2\n".arg(key).arg(showPars[key])
                            }
                        }
                        if (out) {
                            plotInfoRect.visible = true
                        } else {
                            plotInfoRect.visible = false
                        }
                        return out.slice(0, -1)
                    }
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
                anchors.bottomMargin: showDiff ? -4*extraPadding : -extraPadding
                antialiasing: true // conflicts with useOpenGL: true in ScatterSeries
                legend.visible: false
                backgroundRoundness: 0
                backgroundColor: "transparent"
                titleFont: commonFont

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
                    min: Specific.Variables.projectOpened ? Specific.Variables.projectDict.calculations[Specific.Variables.experimentIds[0]].limits.main.x_min : 0
                    max: Specific.Variables.projectOpened ? Specific.Variables.projectDict.calculations[Specific.Variables.experimentIds[0]].limits.main.x_max : 1
                }

                // Y-axis for measured and calculated data

                ValueAxis {
                    id: axisY
                    lineVisible: false
                    tickType: ValueAxis.TicksFixed
                    tickCount: 5
                    minorTickCount: 1
                    labelFormat: "%.0f" //"%.0e"
                    titleText: showCalc ? "Iobs, Icalc" : "Iobs"
                    labelsFont: commonFont
                    titleFont: commonFont
                    min: Specific.Variables.projectOpened ? Specific.Variables.projectDict.calculations[Specific.Variables.experimentIds[0]].limits.main.y_min : 0
                    max: Specific.Variables.projectOpened ? Specific.Variables.projectDict.calculations[Specific.Variables.experimentIds[0]].limits.main.y_max : 0
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
                        infoToolTip.contentItem.text = text
                        infoToolTip.contentItem.color = Generic.Style.blueColor
                        infoToolTip.background.border.color = Qt.lighter(Generic.Style.blueColor, 1.9)
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
                        infoToolTip.contentItem.text = text
                        infoToolTip.contentItem.color = Generic.Style.redColor
                        infoToolTip.background.border.color = Qt.lighter(Generic.Style.redColor, 1.5)
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
                    min: 0
                    max: 10
                    labelFormat: "%.0f"
                    labelsFont: commonFont
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
                    markerShape: ScatterSeries.MarkerShapeRectangle
                    /*
                    markerSize: 1
                    borderWidth: 0.0001
                    borderColor: "transparent"
                    color: "#333"
                    */
                    markerSize: 1
                    borderWidth: 0.00000001
                    borderColor: color
                    color: "#333"

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
                        if (Specific.Variables.projectOpened) {
                            let min = Specific.Variables.projectDict.calculations[Specific.Variables.experimentIds[0]].limits.difference.y_min
                            let max = Specific.Variables.projectDict.calculations[Specific.Variables.experimentIds[0]].limits.difference.y_max
                            let MAX = Math.max(Math.abs(min), Math.abs(max))
                            return Math.sign(min) * MAX
                        }
                        return 0
                    }
                    max: {
                        if (Specific.Variables.projectOpened) {
                            let min = Specific.Variables.projectDict.calculations[Specific.Variables.experimentIds[0]].limits.difference.y_min
                            let max = Specific.Variables.projectDict.calculations[Specific.Variables.experimentIds[0]].limits.difference.y_max
                            let MAX = Math.max(Math.abs(min), Math.abs(max))
                            return Math.sign(max) * MAX
                        }
                        return 1
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
                        infoToolTip.contentItem.text = text
                        infoToolTip.contentItem.color = Generic.Style.darkGreenColor
                        infoToolTip.background.border.color = Generic.Style.ultraLightGreenColor
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

    ToolTip {
        id: infoToolTip
        background: Rectangle { color: "white"; opacity: 0.95 }
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
        middleChart.anchors.leftMargin = leftBraggMargin - extraPadding + textHeight

        //print(topChart.x, topChart.y, topChart.width, topChart.height)

        //plotInfoRec.anchors.right = topChart.right
        //plotInfoRec.anchors.top = topChart.top
    }

}



