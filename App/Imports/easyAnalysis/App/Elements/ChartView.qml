import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtCharts 2.3
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyDiffraction.Resources.Examples.CeCuAl3_POLARIS 1.0 as SpecificExample

ColumnLayout {
    property bool showObs: false
    property bool showCalc: false
    property bool showDiff: false
    property bool showBragg: false
    property bool showInfo: true

    property int extraPadding: 12

    property int xScaleZoom: 0
    property int yScaleZoom: 0

    property font commonFont: Qt.font({ family: Generic.Style.fontFamily, pointSize: Generic.Style.fontPointSize })

    property var tthHklDict: ({})

    spacing: 0


    ////////////////////////
    // Check if data changed
    ////////////////////////

    Text {
        id: dataChanged
        visible: false
        text: proxy.time_stamp
        onTextChanged: {
            print("Time stamp: ", proxy.time_stamp)

            // set axes min, max
            axisX.min = Math.min(...proxy.tmp_tth_list())
            axisX.max = Math.max(...proxy.tmp_tth_list())
            axisY.min = Math.min(...proxy.tmp_int_u_list(), ...proxy.tmp_int_u_mod_list()) - Math.max(...proxy.tmp_sint_u_list())
            axisY.max = Math.max(...proxy.tmp_int_u_list(), ...proxy.tmp_int_u_mod_list()) + Math.max(...proxy.tmp_sint_u_list())

            // remove old data points
            lowerObsSeries.removePoints(0, lowerObsSeries.count)
            upperObsSeries.removePoints(0, upperObsSeries.count)
            calcSeries.removePoints(0, calcSeries.count)
            braggSeries.removePoints(0, braggSeries.count)
            lowerDiffSeries.removePoints(0, lowerDiffSeries.count)
            upperDiffSeries.removePoints(0, upperDiffSeries.count)

            // append updated data and ...
            let min = Infinity
            let max = -Infinity

            for (let i = 0, len = proxy.tmp_tth_list().length; i < len; i++ ) {
                const x = proxy.tmp_tth_list()[i]
                const yobs = proxy.tmp_int_u_list()[i]
                const syobs = proxy.tmp_sint_u_list()[i]
                const ycalc = proxy.tmp_int_u_mod_list()[i]

                min = Math.min(min, yobs - syobs - ycalc)
                max = Math.max(max, yobs + syobs - ycalc)

                lowerObsSeries.append(x, yobs - syobs)
                upperObsSeries.append(x, yobs + syobs)
                calcSeries.append(x, ycalc)
                lowerDiffSeries.append(x, yobs - syobs - ycalc)
                upperDiffSeries.append(x, yobs + syobs - ycalc)
            }

            //
            for (let i = 0, n = 20, len = proxy.tmp_pos_hkl_list().length; i < len; i++) {
                const x = proxy.tmp_pos_hkl_list()[i]
                for (let k = 0; k < n; k++) {
                    const zero_shift = parseFloat(proxy.tmp_setup_zero_shift())
                    braggSeries.append(x + zero_shift, (axisYbragg.max - axisYbragg.min) / n * k)
                }
            }

            //
            for (let i = 0; i < proxy.tmp_pos_hkl_list().length; i++ ) {
                const newHkl = [{ "h":proxy.tmp_h_list()[i], "k":proxy.tmp_k_list()[i], "l":proxy.tmp_l_list()[i] }]
                const oldHklList = tthHklDict[proxy.tmp_pos_hkl_list()[i]] === undefined ? [] : tthHklDict[proxy.tmp_pos_hkl_list()[i]]
                const updatedHklList = oldHklList.concat(newHkl)
                tthHklDict[proxy.tmp_pos_hkl_list()[i]] = updatedHklList
            }

            axisYdiff.min = Math.sign(min) * Math.max(Math.abs(min), Math.abs(max))
            axisYdiff.max = Math.sign(max) * Math.max(Math.abs(min), Math.abs(max))

            adjustLeftAxesAnchor()
        }
    }



    //////////////////////////
    // Top chart (Iobs, Icalc)
    //////////////////////////

    Rectangle {
        id: topChartContainer
        Layout.fillWidth: true
        Layout.fillHeight: true
        color: "transparent"
        clip: true

        ChartView {
            id: topChart
            anchors.fill: parent
            anchors.margins: -extraPadding
            anchors.bottomMargin: showDiff ? -4*extraPadding : -extraPadding
            antialiasing: true // conflicts with useOpenGL: true in ScatterSeries
            ///smooth: true // conflicts with useOpenGL?
            legend.visible: false
            backgroundRoundness: 0
            backgroundColor: "transparent"
            titleFont: commonFont

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
            }

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
            }

            AreaSeries {
                id: obsArea
                visible: showObs
                axisX: axisX
                axisY: axisY
                color: Generic.Style.blueColor
                opacity: 0.4
                borderColor: Qt.darker(Generic.Style.blueColor, 1.1)
                borderWidth: 1.5
                lowerSeries: LineSeries { id: lowerObsSeries }
                upperSeries: LineSeries { id: upperObsSeries }
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
                /*
                Component.onCompleted: {
                    const len = proxy.tmp_tth_list().length
                    for (let i = 0; i < len; i++ ) {
                        const x = proxy.tmp_tth_list()[i]
                        const y = proxy.tmp_int_u_list()[i]
                        const sy = proxy.tmp_sint_u_list()[i]
                        lowerSeries.append(x, y + sy)
                        upperSeries.append(x, y - sy)
                    }
                }
                */
            }

            SpecificExample.CalcLineSeries {
                id: calcSeriesBorder
                visible: showCalc
                axisX: axisX
                axisY: axisY
                color: "white"
                opacity: 0.4
                width: 6.5
            }

            LineSeries {//tmp_int_u_mod_list
                id: calcSeries
                visible: showCalc
                axisX: axisX
                axisY: axisY
                color: Generic.Style.redColor
                width: 2.5
                //useOpenGL: true
                //onClicked: console.log("onClicked: calcSeries")
                //pointsVisible: true
                //pointLabelsVisible: false
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
                /*
                Component.onCompleted: {
                    const len = proxy.tmp_tth_list().length
                    for (let i = 0; i < len; i++ ) {
                        const x = proxy.tmp_tth_list()[i]
                        const y = proxy.tmp_int_u_mod_list()[i]
                        append(x, y)
                    }
                }
                */
            }
        }

        ////////////
        // Zoom area
        ////////////

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
    // https://doc.qt.io/qt-5/qtcharts-callout-example.html
    // https://stackoverflow.com/questions/51923764/custom-tooltip-tooltip-in-qml-chartview

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
            anchors.topMargin: -3.6*extraPadding
            anchors.bottomMargin: -4*extraPadding
            antialiasing: true // conflicts with useOpenGL: true in ScatterSeries
            ///smooth: true // conflicts with useOpenGL?
            legend.visible: false
            backgroundRoundness: 0
            backgroundColor: "transparent"
            titleFont: commonFont

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
                markerSize: 1
                borderWidth: 0.0001
                borderColor: "transparent"
                color: "grey"
                //onClicked: console.log("onClicked: BraggScatterSeries")
                //onHovered: console.log("onHovered: BraggScatterSeries")
                onHovered: {
                    const position = middleChart.mapToPosition(point)
                    const tth = point.x - parseFloat(proxy.tmp_setup_zero_shift())
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

            }

            /*
            SpecificExample.BraggScatterSeries {
                axisX: axisXbragg
                axisY: axisYbragg
                markerShape: ScatterSeries.MarkerShapeRectangle
                markerSize: 2
                borderWidth: 0.0001
                borderColor: "transparent"
                color: "grey"
                //onClicked: console.log("onClicked: BraggScatterSeries")
                //onHovered: console.log("onHovered: BraggScatterSeries")
                onHovered: {
                    const p = middleChart.mapToPosition(point)
                    const text = qsTr("x: %1\nhkl: 0 4 0").arg(point.x)
                    infoToolTip.parent = middleChart
                    infoToolTip.x = p.x
                    infoToolTip.y = p.y - infoToolTip.height
                    infoToolTip.visible = state
                    infoToolTip.contentItem.text = text
                    infoToolTip.contentItem.color = "grey"
                    infoToolTip.background.border.color = Qt.lighter("grey", 1.75)
                }
            }
            */
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
            ///smooth: true // conflicts with useOpenGL?
            legend.visible: false
            backgroundRoundness: 0
            backgroundColor: "transparent"
            titleFont: commonFont

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
            }

            AreaSeries {
                id: diffArea
                axisX: axisXdiff
                axisY: axisYdiff
                color: Generic.Style.greenColor
                opacity: 0.4
                borderColor: Generic.Style.darkGreenColor
                borderWidth: 1.5
                lowerSeries: LineSeries { id: lowerDiffSeries }
                upperSeries: LineSeries { id: upperDiffSeries }
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
                /*
                Component.onCompleted: {
                    const len = proxy.tmp_tth_list().length
                    let min = Infinity
                    let max = -Infinity
                    for (let i = 0; i < len; i++ ) {
                        const x = proxy.tmp_tth_list()[i]
                        const yobs = proxy.tmp_int_u_list()[i]
                        const syobs = proxy.tmp_sint_u_list()[i]
                        const ycalc = proxy.tmp_int_u_mod_list()[i]
                        const low = yobs - syobs - ycalc
                        const high = yobs + syobs - ycalc
                        lowerSeries.append(x, low)
                        upperSeries.append(x, high)
                        min = Math.min(min, low)
                        max = Math.max(max, high)
                    }
                    axisYdiff.min = Math.sign(min) * Math.max(Math.abs(min), Math.abs(max))
                    axisYdiff.max = Math.sign(max) * Math.max(Math.abs(min), Math.abs(max))
                    adjustLeftAxesAnchor()
                }
                */
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
        height: Generic.Style.buttonHeight + Generic.Style.sidebarGroupInnerSpacing + 2*Generic.Style.appBorderThickness
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

    ////////////////
    // On completed
    ////////////////

    //Component.onCompleted: {
        //setAxesNiceNumbers()
        ///adjustLeftAxesAnchor()
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
    }

}
