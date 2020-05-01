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
    readonly property string greyColor: "#aaa"
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
    readonly property color tableHighlightRowColor: "#302a99d9"//buttonBkgFinishedColor//blueColor //Qt.lighter("dodgerblue", 1.7)
    readonly property color tableHeaderRowColor: "#eee"
    readonly property color tableColumnBorderColor: "#e8e8e8"

    readonly property color tableTextColor: "black"
    readonly property color tableDisabledTextColor: "#888"
    readonly property color tableHighlightTextColor: "black"//"white"
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
    readonly property color toolbarBkgColor: "#dfdfdf"//"#cdcdcd"
    readonly property color toolbarBottomBorderColor: "#d7d7d7"//"#c5c5c5"

    readonly property color toolbarButtonBkgDisabledColor: appBkgColor
    readonly property color toolbarButtonBkgEnabledColor: "#fff"
    readonly property color toolbarButtonBkgBlendColor: "#e1e1e1"

    readonly property color buttonBkgDisabledColor: "#e1e1e1"
    readonly property color buttonBkgEnabledColor: "#e9e9e9"//"#e1e1e1"//"#666"
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
    property FontLoader ptSansRegular: FontLoader { source: "Resources/Fonts/PT_Sans/PTSans-Regular.ttf" } // default
    property FontLoader ptSansBold: FontLoader { source: "Resources/Fonts/PT_Sans/PTSans-Bold.ttf" } // font.bold: true
    property FontLoader ptMono: FontLoader { source: "Resources/Fonts/PT_Mono/PTMono-Regular.ttf" }
    property FontLoader encodeSansRegular: FontLoader { source: "Resources/Fonts/Encode_Sans/EncodeSans-Regular.ttf" } // default
    property FontLoader encodeSansLight: FontLoader { source: "Resources/Fonts/Encode_Sans/EncodeSans-Light.ttf" } // font.weight: Font.Light
    property FontLoader encodeSansCondensedRegular: FontLoader { source: "Resources/Fonts/Encode_Sans_Condensed/EncodeSansCondensed-Regular.ttf" } // default
    property FontLoader encodeSansCondensedExtraLight: FontLoader { source: "Resources/Fonts/Encode_Sans_Condensed/EncodeSansCondensed-ExtraLight.ttf" } // font.weight: Font.ExtraLight
    property FontLoader encodeSansExpandedRegular: FontLoader { source: "Resources/Fonts/Encode_Sans_Expanded/EncodeSansExpanded-Regular.ttf" } // default
    property FontLoader encodeSansExpandedLight: FontLoader { source: "Resources/Fonts/Encode_Sans_Expanded/EncodeSansExpanded-Light.ttf" } // font.weight: Font.Light
    property FontLoader icons: FontLoader { source: "Resources/Fonts/Icons/icons.ttf" }
    readonly property string fontFamily: ptSansRegular.name
    readonly property string monoFontFamily: ptMono.name
    readonly property string secondFontFamily: encodeSansRegular.name
    readonly property string secondCondensedFontFamily: encodeSansCondensedRegular.name
    readonly property string secondExpandedFontFamily: encodeSansExpandedRegular.name
    readonly property string iconsFontFamily: icons.name

    // Text
    //property Text text: Text { font.pointSize: Qt.platform.os === "osx" ? Qt.application.font.pointSize + 1 : Qt.application.font.pointSize }
    property Text text: Text { font.pixelSize: 14 }
    //readonly property string systemFontFamily: text.font.family
    readonly property int fontPointSize: text.font.pointSize
    readonly property int fontPixelSize: text.font.pixelSize

    //onSystemFontFamilyChanged: print("systemFontFamily", systemFontFamily)
    //onFontPointSizeChanged: print("fontPointSize", fontPointSize)
    //onFontPixelSizeChanged: print("fontPixelSize", fontPixelSize)

}

