//pragma Singleton
import QtQuick 2.12
import QtCharts 2.3

/*
LineSeries {
    XYPoint { x: 11000; y: 100000 }
    XYPoint { x: 15000; y: 500000 }
    XYPoint { x: 19000; y: 200000 }
}
*/


//Component {
    LineSeries {
        XYPoint { x: 11000; y: 100000 }
        XYPoint { x: 15000; y: 500000 }
        XYPoint { x: 19000; y: 200000 }
    }
//}

/*
AreaSeries {
    axisX: axisX5
    axisY: axisY5
    color: Qt.lighter("red", 1.3)
    borderColor: color
    borderWidth: 1
    upperSeries: Generic.Variables.yObsSeriesUpper
    lowerSeries: Generic.Variables.yObsSeriesLower
    useOpenGL: true
    Component.onCompleted: {
        console.log("obsArea", obsArea5.lowerSeries)
    }
}
*/
