import QtQuick 2.12
import QtCharts 2.3
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements

GenericAppElements.ChartView {
    showObs: true
    showCalc: true
    showDiff: true
    showBragg: true

    GenericAppElements.GuideWindow {
        message: "Measured (Iobs, blue) and calculate (Icalc, red) data\npoints are shown in the main area.\n\nTheir difference (Iobs-Icalc, green) is given\nin the bottom plot.\n\nVertical ticks between the plots indicate\nBragg peak positions."
        position: "right"
        guideCurrentIndex: 1
        toolbarCurrentIndex: Generic.Variables.AnalysisIndex
        guidesCount: Generic.Variables.AnalysisGuidesCount
    }
}



