import QtQuick 2.12
import QtCharts 2.3
import easyAnalysis 1.0 as Generic

Column {
    property int extraPadding: 12
    property int ratio: 0

    property bool showObs: false
    property bool showCalc: false

    padding: -extraPadding
    spacing: -2*extraPadding

    ChartView {
        width: parent.width + 2*extraPadding
        height: parent.height + 2*extraPadding

        legend.visible: false
        antialiasing: true // conflicts with useOpenGL: true in ScatterSeries
        //smooth: true

        titleFont: Qt.font({ family: Generic.Style.fontFamily, pointSize: Generic.Style.fontPointSize })

        ValueAxis {
            id: axisX
            min: 15000
            max: 19000
            tickInterval: 1000
            minorTickCount: 1
            tickType: ValueAxis.TicksDynamic
            //tickInterval: 1.5
            //tickCount: 5
            labelFormat: "%.0f"
            titleText: "TOF"
            labelsFont: Qt.font({ family: Generic.Style.fontFamily, pointSize: Generic.Style.fontPointSize })
            titleFont: Qt.font({ family: Generic.Style.fontFamily, pointSize: Generic.Style.fontPointSize })
        }

        ValueAxis {
            id: axisY
            min: 0 //-2e+4
            max: 1e+6 //+ 2e+4
            tickInterval: 200000
            minorTickCount: 1
            tickType: ValueAxis.TicksDynamic
            //tickInterval: 1e+2
            labelFormat: "%.0e"
            titleText: "Yobs"
            labelsFont: Qt.font({ family: Generic.Style.fontFamily, pointSize: Generic.Style.fontPointSize })
            titleFont: Qt.font({ family: Generic.Style.fontFamily, pointSize: Generic.Style.fontPointSize })
        }

        AreaSeries {
            id: obsArea
            visible: showObs
            axisX: axisX
            axisY: axisY
            color: Qt.lighter("dodgerblue", 1.4)
            borderColor: color
            borderWidth: 2
            upperSeries: LineSeries { id: obsSeriesUpper }
            lowerSeries: LineSeries { id: obsSeriesLower }
            //useOpenGL: true
        }

        LineSeries {
            id: calcSeries
            visible: showCalc
            axisX: axisX
            axisY: axisY
            color: "coral"
            width: 2
            //useOpenGL: true
        }

    }

    Component.onCompleted: {
        // Populate global Chart Series
        for (let i = 0; i < Generic.Variables.xObs.length; i++) {
            const xObs = parseFloat(Generic.Variables.xObs[i])
            const yObs = parseFloat(Generic.Variables.yObs[i])
            const syObs = parseFloat(Generic.Variables.syObs[i])
            const yCalc = parseFloat(Generic.Variables.yCalc[i])
            //const yPreCalc = parseFloat(Generic.Variables.yPreCalc[i])
            //console.log(xObs, yObs, syObs, yObs + syObs, yObs - syObs, yCalc, yPreCalc)
            obsSeriesUpper.append(xObs, yObs + syObs)
            obsSeriesLower.append(xObs, yObs - syObs)
            calcSeries.append(xObs, yCalc)
            //preCalcSeries.append(xObs, yPreCalc)
        }
    }



}
