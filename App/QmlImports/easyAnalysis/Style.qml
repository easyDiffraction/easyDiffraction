pragma Singleton
import QtQuick 2.12

QtObject {

    // Application
    readonly property color appBkgColor: "#f5f5f5"
    readonly property color appBorderColor: "gainsboro"
    readonly property int appBorderThickness: 1
    readonly property int buttonHeight: 34
    readonly property int buttonRadius: 4

    // Content Area
    readonly property int contentAreaTabbarHeight: 34

    // Main Area
    //readonly property int mainAreaWidth: appWindowWidth - appBorderThickness - sidebarWidth
    readonly property color mainAreaTabBorderColor: "#ccc"

    // Colors
    // https://www.google.com/search?q=rgb+to+hex&oq=rgb+to+hex&aqs=chrome..69i57j69i60j0l4.3070j0j7&sourceid=chrome&ie=UTF-8
    readonly property string blueColor: "#2a99d9"//"#0099ff"//"#2293de"//"#1c8fdc" // ESS #3e93c5 or #0094ca ?
    readonly property string redColor: "#ed6a5e"//"coral"
    readonly property string greenColor: "#7ab03c"
    readonly property string ultraLightGreenColor: "#daebc7"
    readonly property string darkGreenColor: "#669431"
    readonly property var atomColorList: [redColor, greenColor, blueColor, "orange", "grey"]

    // StatusBar
    readonly property int statusBarHeight: 28

    // Sidebar
    readonly property int sidebarWidth: 605//554//518
    readonly property int sidebarGroupInnerSpacing: 10
    readonly property int sidebarGroupIndicatorIconSize: 10
    readonly property color sidebarGroupTitleColor: blueColor
    readonly property color sidebarGroupTitleDisabledColor: "#999"
    readonly property color sidebarGroupIconDisabledColor: "#aaa"
    readonly property color sidebarLabelColor: "#555"

    // Table
    readonly property int tableRowHeight: 32
    readonly property int tableColumnSpacing: 16
    readonly property int maxVisibleRowsCount: 5

    readonly property color tableRowColor: "white"
    readonly property color tableAlternateRowColor: "#f7f7f7"
    readonly property color tableHighlightRowColor: blueColor //Qt.lighter("dodgerblue", 1.7)
    readonly property color tableHeaderRowColor: "#eee"
    readonly property color tableColumnBorderColor: "#e8e8e8"

    readonly property color tableTextColor: "black"
    readonly property color tableDisabledTextColor: "#888"
    readonly property color tableHighlightTextColor: "white"
    readonly property color tableHighlightBorderColor: Qt.lighter(tableHighlightRowColor, 1.2)

    // Toolbar
    readonly property int toolbarButtonWidth: 150
    readonly property int toolbarButtonHeight: 40
    readonly property int toolbarButtonRadius: 4
    readonly property int toolbarSpacerSize: 10
    readonly property int toolbarSpacing: 10
    readonly property int toolbarHeight: toolbarButtonHeight + 2*toolbarSpacing
    readonly property color toolbarSpacerColor: appBorderColor//"#addButton"
    //readonly property color toolbarBkgColor: "transparent"
    readonly property color toolbarBkgColor: "#cdcdcd"
    readonly property color toolbarBottomBorderColor: "#c5c5c5"

    readonly property color toolbarButtonBkgDisabledColor: appBkgColor
    readonly property color toolbarButtonBkgEnabledColor: "#fff"
    readonly property color toolbarButtonBkgBlendColor: "#e1e1e1"

    readonly property color buttonBkgDisabledColor: "#e1e1e1"
    readonly property color buttonBkgEnabledColor: "#e1e1e1"//"#666"
    readonly property color buttonBkgAttentionColor: redColor //"coral"
    readonly property color buttonBkgHighlightedColor: blueColor
    readonly property color buttonBkgFinishedColor: Qt.lighter(blueColor, 2) //Qt.lighter(blueColor, 1.4) //Qt.lighter(blueColor, 1.9) //!!!!
    readonly property color buttonBkgBlendColor: "white"
    readonly property real buttonBkgBlendAlpha: 0.25

    readonly property color buttonTextDisabledColor: "#777"
    readonly property color buttonTextEnabledColor: "#222"//"white"
    readonly property color buttonTextHighlightedColor: "white"
    readonly property color buttonTextFinishedColor: Qt.darker(blueColor, 1.6) //"white" //Qt.darker(blueColor, 1.5) //!!!!

    readonly property color buttonIconDisabledColor: "#aaa"
    readonly property color buttonIconEnabledColor: "#555"//"white"
    readonly property color buttonIconHighlightedColor: "white"
    readonly property color buttonIconFinishedColor: Qt.darker(blueColor, 1.2) //"white" //Qt.darker(blueColor, 1.2) //!!!!

    readonly property color buttonBorderDisabledColor: appBorderColor
    readonly property color buttonBorderEnabledColor: appBorderColor
    readonly property color buttonBorderHighlightedColor: buttonBkgHighlightedColor
    readonly property color buttonBorderFinishedColor: Qt.lighter(blueColor, 1.85) //Qt.lighter(blueColor, 1.3) //Qt.lighter(blueColor, 1.7) //!!!!

    // Icons
    readonly property string dummyIconPath: "dummy.svg"

    // Fonts
    readonly property string introCondencedThinFontFamily: encodeSansCondensedExtraLight.name
    readonly property string introCondencedRegularFontFamily: encodeSansCondensedRegular.name
    readonly property string introThinFontFamily: encodeSansExtraLight.name
    readonly property string introExpandedThinFontFamily: encodeSansExpandedExtraLight.name
    readonly property string fontFamily: ptSansWebRegular.name
    readonly property string monoFontFamily: ptMono.name
    property FontLoader encodeSansCondensedExtraLight: FontLoader { source: "Resources/Fonts/EncodeSansCondensed/EncodeSansCondensed-ExtraLight.ttf" }
    property FontLoader encodeSansCondensedRegular: FontLoader { source: "Resources/Fonts/EncodeSansCondensed/EncodeSansCondensed-Regular.ttf" }
    property FontLoader encodeSansExtraLight: FontLoader { source: "Resources/Fonts/EncodeSans/EncodeSans-ExtraLight.ttf" }
    property FontLoader encodeSansExpandedExtraLight: FontLoader { source: "Resources/Fonts/EncodeSansExpanded/EncodeSansExpanded-ExtraLight.ttf" }
    property FontLoader ptSansWebRegular: FontLoader { source: "Resources/Fonts/PtSans/PT_Sans-Web-Regular.ttf" }
    property FontLoader ptSansWebBold: FontLoader { source: "Resources/Fonts/PtSans/PT_Sans-Web-Bold.ttf" } // font.bold: true
    property FontLoader ptMono: FontLoader { source: "Resources/Fonts/PtMono/PTM55FT.ttf" }

    // Text
    readonly property string systemFontFamily: text.font.family
    readonly property int systemFontPointSize: text.font.pointSize
    readonly property int fontPointSize: systemFontPointSize + 1
    property Text text: Text {}

}

