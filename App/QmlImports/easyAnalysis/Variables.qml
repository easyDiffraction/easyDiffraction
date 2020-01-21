pragma Singleton
import QtQuick 2.12

QtObject {

    // Main
    property int showIntro: 1 // bool doesn't work on windows
    property int homepageVisible: 1 // bool doesn't work on windows
    property int showGuide: 1 // bool doesn't work on windows
    property int showPreferences: 0
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
    property int toolbarCurrentIndex: 0 // App starts on home tab
    enum ToolbarIndexEnum {
        HomeIndex = 0,
        ProjectIndex = 1,
        SampleIndex = 2,
        ExperimentIndex = 3,
        AnalysisIndex = 4,
        SummaryIndex = 5
    }

    // User guides
    property int guideCurrentIndex: 0
    enum GuideCountEnum {
        HomeGuidesCount = 0,
        ProjectGuidesCount = 4,
        SampleGuidesCount = 6,
        ExperimentGuidesCount = 7,
        AnalysisGuidesCount = 6,
        SummaryGuidesCount = 4
    }

    // Tolbar tab states
    property bool homePageFinished: false
    property bool projectPageFinished: false
    property bool dataPageFinished: false
    property bool samplePageFinished: false
    property bool analysisPageFinished: false
    property bool summaryPageFinished: false
}
