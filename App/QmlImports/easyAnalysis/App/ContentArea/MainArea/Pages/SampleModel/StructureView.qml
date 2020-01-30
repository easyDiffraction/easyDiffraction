import QtQuick 2.12
import QtCharts 2.3
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements

GenericAppElements.StructureView {

    GenericAppElements.GuideWindow {
        message: "Crystal structure is shown in the main area."
        position: "right"
        guideCurrentIndex: 1
        toolbarCurrentIndex: Generic.Variables.SampleIndex
        guidesCount: Generic.Variables.SampleGuidesCount
    }
}


