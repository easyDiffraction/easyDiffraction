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


    spacing: 0

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

                /*
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
                }*/
            }

            //////////////////////////
            // Top chart (Iobs, Icalc)
            //////////////////////////

            ChartView {
                id: topChart
                visible: Specific.Variables.experimentIds().length? true: false
                //enabled: false
                anchors.fill: parent
                anchors.margins: -extraPadding
                anchors.topMargin: Specific.Variables.isPolarized ? 18 : -extraPadding
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
                    titleText: showCalc ? "Iobs, Icalc" : "Iobs"
                    labelsFont: commonFont
                    titleFont: commonFont
                    min: Specific.Variables.measuredData ? Specific.Variables.measuredData.yMin : 0 //Specific.Variables.calculationByIndex(0).limits.main.y_min
                    max: Specific.Variables.measuredData ? Specific.Variables.measuredData.yMax : 1 //Specific.Variables.calculationByIndex(0).limits.main.y_max
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
                        infoToolTip.text = text
                        infoToolTip.backgroundColor = obsArea.color
                        infoToolTip.borderColor = Qt.darker(obsArea.color, 1.1)
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
                    //adjustLeftAxesAnchor()
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
                    //adjustLeftAxesAnchor()
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
            font.family: Generic.Style.secondFontFamily
            font.weight: Font.Light
            font.pointSize: Generic.Style.fontPointSize
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

    // Set animation timers to skip animation once, when you see chart for the 1st time.
    // TO DO: find a better way to do that
    Timer {
        interval: 100
        running: topChart.visible
        repeat: false
        onTriggered: topChart.animationOptions = globalAnimationOptions
    }

}



