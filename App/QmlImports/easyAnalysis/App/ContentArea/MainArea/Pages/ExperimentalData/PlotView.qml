import QtQuick 2.12
import QtCharts 2.3
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements

GenericAppElements.ChartView {
    showObs: true
    showCalc: false

    GenericAppElements.GuideWindow {
        message: "Measured data points are plotted in the main area."
        position: "right"
        guideCurrentIndex: 1
        toolbarCurrentIndex: Generic.Variables.ExperimentalDataIndex
        guidesCount: Generic.Variables.ExperimentalDataGuidesCount
    }
}
