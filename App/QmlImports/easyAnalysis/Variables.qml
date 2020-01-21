pragma Singleton
import QtQuick 2.12
import QtQuick.Window 2.12
//import Qt.labs.settings 1.1

import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons

QtObject {

    // Main
    property int showIntro: 1 // bool doesn't work on windows
    property int homepageVisible: 1 // bool doesn't work on windows
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
    property int toolbarCurrentIndex: 0 // Start on project tab
    enum ToolbarIndexEnum {
        HomeIndex = 0,
        ProjectIndex = 1,
        SampleModelIndex = 2,
        ExperimentalDataIndex = 3,
        //InstrumentModelIndex = 2,
        //LinkingIndex = 4,
        AnalysisIndex = 4,
        SummaryIndex = 5
    }

    // User guides
    property int guideCurrentIndex: 0
    enum GuideCountEnum {
        HomeGuidesCount = 0,
        ProjectGuidesCount = 5,
        ExperimentalDataGuidesCount = 7,
        SampleModelGuidesCount = 6,
        AnalysisGuidesCount = 6,
        SummaryGuidesCount = 4
    }

    // States
    property bool projectPageFinished: false
    property bool dataPageFinished: false
    property bool samplePageFinished: false
    property bool analysisPageFinished: false
    property bool summaryPageFinished: false



}
