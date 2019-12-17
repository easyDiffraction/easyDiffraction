pragma Singleton
import QtQuick 2.12
import QtQuick.Window 2.12
//import Qt.labs.settings 1.1

import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons

QtObject {

    // Main
    property int showIntro: 1 // bool doesn't work on windows
    property int showGuide: 1 // bool doesn't work on windows
    property int appMinWindowWidth: 1280
    property int appMinWindowHeight: 760
    property int appWindowWidth: appMinWindowWidth
    property int appWindowHeight: appMinWindowHeight
    property int appWindowX: 0
    property int appWindowY: 0
    property int mainAreaWidth: appWindowWidth

    // Intro page
    property int introAnimationDuration: 1000

    // Reliability factors
    property string chiSquared: ""
    property int numRefinedPars: 0

    // Paths
    readonly property string originalIconsPath: qmlImportsDir + "/easyAnalysis/Resources/Icons/"
    readonly property string thirdPartyIconsPath: qmlImportsDir + "/easyAnalysis/Resources/Fonts/Awesome/svgs/"
    readonly property string qmlElementsPath: qmlImportsDir + "/easyAnalysis/App/Elements/"

    // Content area
    property int toolbarCurrentIndex: -1
    enum ToolbarIndexEnum {
        HomeIndex = 0,
        SampleModelIndex = 1,
        ExperimentalDataIndex = 2,
        //InstrumentModelIndex = 2,
        //LinkingIndex = 4,
        AnalysisIndex = 3,
        SummaryIndex = 4
    }

    // User guides
    property int guideCurrentIndex: 0
    enum GuideCountEnum {
        HomeGuidesCount = 5,
        ExperimentalDataGuidesCount = 7,
        SampleModelGuidesCount = 6,
        AnalysisGuidesCount = 6,
        SummaryGuidesCount = 4
    }

    // States
    property bool isDebug: false
    property bool homePageFinished: isDebug ? true : false
    property bool dataPageFinished: isDebug ? true : false
    property bool samplePageFinished: isDebug ? true : false
    //property bool instrumentPageFinished: false
    //property bool linkingPageFinished: false
    property bool analysisPageFinished: isDebug ? true : false
    property bool summaryPageFinished: isDebug ? true : false

    // Data arrays
    property var xPeaks: []
    property var xObs: []
    property var yObs: []
    property var syObs: []
    property var yCalc: []
    property var yPreCalc: []

}
