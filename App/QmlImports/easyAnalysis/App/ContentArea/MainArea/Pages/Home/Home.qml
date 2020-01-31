import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtQuick.Layouts 1.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.Controls 1.0 as GenericControls
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar
import easyDiffraction 1.0 as Specific

Rectangle {
    id: mainRectangle

    property int margin: 20
    property int animationDuration: Generic.Variables.showIntro ? Generic.Variables.introAnimationDuration : 0
    property int appNameFontSize: Generic.Style.systemFontPointSize * 4
    property int appVersionFontSize: Generic.Style.systemFontPointSize + 1
    property int repeatFontSize: Generic.Style.systemFontPointSize + 1

    enabled: false

    Layout.fillWidth: true
    Layout.fillHeight: true

    //color: Generic.Style.appBkgColor
    color: "white"
    
    Component.onCompleted: animo.restart()

    // About dialog
    GenericAppElements.AboutBox{
        id: aboutDialog
    }

    // Content
    Column {
        anchors.centerIn: parent
        width: parent.width
        spacing: 10

        // Application icon
        Image {
            id: appIcon
            opacity: 0
            anchors.horizontalCenter: parent.horizontalCenter
            width: 110
            height: width
            //antialiasing: true
            //fillMode: Image.PreserveAspectFit
            source: Specific.Settings.appIconPath
            sourceSize: Qt.size( img.sourceSize.width, img.sourceSize.height )
            Image {
                id: img
                source: parent.source
                width: 0
                height: 0
            }
            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: Qt.openUrlExternally(Specific.Settings.appUrl)
            }
        }

        // Initial sentence to be transformed to application name
        Item {
            id: container
            anchors.horizontalCenter: parent.horizontalCenter
            height: diffraction.height
            width: making.width + diffraction.width + dam.width + easy.width
            Text { id: making;      text: "Making ";                        opacity: 0; x: 0; font.family: Generic.Style.introCondencedThinFontFamily; font.pointSize: appNameFontSize; color: "#444" }
            Text { id: diffraction; text: "diffraction";                    opacity: 0; x: making.width; font.family: Generic.Style.introCondencedRegularFontFamily; font.pointSize: appNameFontSize; color: "#666" }
            Text { id: dam;         text: " data analysis and modelling ";  opacity: 0; x: making.width + diffraction.width; font.family: Generic.Style.introCondencedThinFontFamily; font.pointSize: appNameFontSize; color: "#444" }
            Text { id: easy;        text: "easy";                           opacity: 0; x: making.width + diffraction.width + dam.width; font.family: Generic.Style.introCondencedRegularFontFamily; font.pointSize: appNameFontSize; color: "#666" }
            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: Qt.openUrlExternally(Specific.Settings.appUrl)
            }
        }

        // Application version
        Text {
            id: appVersion
            opacity: 0
            anchors.horizontalCenter: parent.horizontalCenter
            font.family: Generic.Style.introExpandedThinFontFamily
            font.pointSize: appVersionFontSize
            text: "Version %1 (%2)".arg(Specific.Settings.appVersion).arg(Specific.Settings.appDate)
            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: Qt.openUrlExternally(Specific.Settings.appUrl)
            }
        }

        // Spacer
        Item { height: 10; width: 1 }

        // Analysis & Modelling buttons
        Row {
            id: buttons
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 5
            /*
            GenericAppToolbar.Button {
                id: modellingButton
                opacity: 0
                enabled: false
                checked: true
                autoExclusive: false
                width: 150
                buttonBorderDisabledColor: "#eee"
                //font.bold: true
                text: "Modelling"
                ToolTip.text: "Simulation of diffraction data"
                onClicked: print("Not implemented yet")
            }
            GenericAppToolbar.Button { width: 1; opacity: 0 }
            */
            GenericAppToolbar.Button {
                id: analysisButton
                enabled: true
                opacity: 0
                checked: true
                autoExclusive: false
                width: 230
                font.bold: true
                text: "Start Simulation/Refinement"
                ToolTip.text: "Simulation of the diffraction pattern or structure model refinement"
                onClicked: {
                    //dialog.close() // Only needed in dialog version
                    analysisButton.checked = true
                    Generic.Variables.homepageVisible = 0
                    Generic.Variables.toolbarCurrentIndex = Generic.Variables.ProjectIndex
                    Generic.Variables.homePageFinished = true
                }
            }
        }

        // Spacer
        Item { height: 10; width: 1 }

        // Documentation
        Column {
            id: links
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 5
            //opacity: 0

            Text {
                id: aboutLink
                opacity: 0
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: Generic.Style.fontPointSize
                font.family: Generic.Style.fontFamily
                horizontalAlignment: Text.AlignHCenter
                color: Generic.Style.blueColor
                text: "About easyDiffraction"

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Generic.Variables.showAbout = 1
                }
            }

            Text {
                id: tutorialLink
                opacity: 0
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: Generic.Style.fontPointSize
                font.family: Generic.Style.fontFamily
                horizontalAlignment: Text.AlignHCenter
                color: Generic.Style.blueColor
                text: "Get Started Video Tutorial"

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Qt.openUrlExternally("https://www.easydiffraction.org/tutorials_start.html")
                }
            }

            Text {
                id: documentationLink
                opacity: 0
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: Generic.Style.fontPointSize
                font.family: Generic.Style.fontFamily
                horizontalAlignment: Text.AlignHCenter
                color: Generic.Style.blueColor
                text: "Online Documentation"

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Qt.openUrlExternally("https://www.easydiffraction.org/documentation.html")
                }
            }

            Text {
                id: contactLink
                opacity: 0
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: Generic.Style.fontPointSize
                font.family: Generic.Style.fontFamily
                horizontalAlignment: Text.AlignHCenter
                color: Generic.Style.blueColor
                text: "Get in Touch Online"

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Qt.openUrlExternally("https://www.easydiffraction.org/contact.html")
                }
            }

        }
    }

    // Buttons at the bottom
    Row {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20

        parent: Overlay.overlay

        Button {
            id: skipButton
            visible: Generic.Variables.showIntro
            text: "Skip"
            contentItem: IconLabel {
                text: skipButton.text
                font.family: Generic.Style.introThinFontFamily
                font.pointSize: repeatFontSize
                color: "#666"
            }
            background: Rectangle {
                color: "transparent"
            }
            onClicked: {
                animo.complete()
            }
        }

        Button {
            id: disableButton
            visible: Generic.Variables.showIntro
            text: "Disable"
            contentItem: IconLabel {
                text: disableButton.text
                font.family: Generic.Style.introThinFontFamily
                font.pointSize: repeatFontSize
                color: "#666"
            }
            background: Rectangle {
                color: "transparent"
            }
            onClicked: {
                animo.complete()
                Generic.Variables.showIntro = false
            }
        }
    }

    ////////////
    // Animation
    ////////////

    SequentialAnimation {
        id: animo
        //running: true
        PauseAnimation {
            duration: 1*Generic.Variables.introAnimationDuration
        }
        ParallelAnimation {
            // appearing
            NumberAnimation { easing.type: Easing.Linear; target: making;      property: "opacity"; to: 1; duration: 2*animationDuration }
            NumberAnimation { easing.type: Easing.Linear; target: diffraction; property: "opacity"; to: 1; duration: 2*animationDuration }
            NumberAnimation { easing.type: Easing.Linear; target: dam;         property: "opacity"; to: 1; duration: 2*animationDuration }
            NumberAnimation { easing.type: Easing.Linear; target: easy;        property: "opacity"; to: 1; duration: 2*animationDuration }
        }
        ParallelAnimation {
            // highlighting
            PropertyAnimation { easing.type: Easing.Linear; target: easy;        property: "color"; to: "#444"; duration: animationDuration }
            PropertyAnimation { easing.type: Easing.Linear; target: diffraction; property: "color"; to: "#444"; duration: animationDuration }
            // hidding
            NumberAnimation { easing.type: Easing.Linear; target: making; property: "opacity"; to: 0; duration: animationDuration }
            NumberAnimation { easing.type: Easing.Linear; target: dam;    property: "opacity"; to: 0; duration: animationDuration }
        }
        ParallelAnimation {
            // font change
            PropertyAnimation { target: easy; property: "font.family"; to: Generic.Style.introCondencedThinFontFamily; duration: animationDuration*0.1 }
            // text change
            PropertyAnimation { target: diffraction; property: "text"; to: "Diffraction"; duration: animationDuration*0.1 }
            // mooving
            NumberAnimation { easing.type: Easing.OutExpo; target: easy;         property: "x"; to: container.width/2 - easy.width - (diffraction.width - easy.width)/2; duration: animationDuration }
            NumberAnimation { easing.type: Easing.OutExpo; target: diffraction;  property: "x"; to: container.width/2 - (diffraction.width - easy.width)/2;              duration: animationDuration }
        }
        // easyDiffraction opacity
        ParallelAnimation {
            NumberAnimation { easing.type: Easing.Linear; target: easy;         property: "opacity"; from: 0 ; to: 1; duration: Generic.Variables.showIntro ? 0 : Generic.Variables.introAnimationDuration }
            NumberAnimation { easing.type: Easing.Linear; target: diffraction;  property: "opacity"; from: 0 ; to: 1; duration: Generic.Variables.showIntro ? 0 : Generic.Variables.introAnimationDuration }
        }
        ParallelAnimation {
            // show app icon, version, links: opacity
            PropertyAnimation { easing.type: Easing.OutExpo; target: appIcon;           property: "opacity"; to: 1; duration: Generic.Variables.introAnimationDuration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: appVersion;        property: "opacity"; to: 1; duration: Generic.Variables.introAnimationDuration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: analysisButton;    property: "opacity"; to: 1; duration: Generic.Variables.introAnimationDuration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: aboutLink;         property: "opacity"; to: 1; duration: Generic.Variables.introAnimationDuration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: tutorialLink;      property: "opacity"; to: 1; duration: Generic.Variables.introAnimationDuration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: documentationLink; property: "opacity"; to: 1; duration: Generic.Variables.introAnimationDuration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: contactLink;       property: "opacity"; to: 1; duration: Generic.Variables.introAnimationDuration }
            // show app icon, version, links: moving
            PropertyAnimation { easing.type: Easing.OutExpo; target: appIcon;           property: "y"; from: -appIcon.height; to: appIcon.y;           duration: Generic.Variables.introAnimationDuration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: appVersion;        property: "y"; from: window.height;   to: appVersion.y;        duration: Generic.Variables.introAnimationDuration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: analysisButton;    property: "y"; from: window.height;   to: analysisButton.y;    duration: Generic.Variables.introAnimationDuration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: aboutLink;         property: "y"; from: window.height;   to: aboutLink.y;         duration: Generic.Variables.introAnimationDuration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: tutorialLink;      property: "y"; from: window.height;   to: tutorialLink.y;      duration: Generic.Variables.introAnimationDuration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: documentationLink; property: "y"; from: window.height;   to: documentationLink.y; duration: Generic.Variables.introAnimationDuration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: contactLink;       property: "y"; from: window.height;   to: contactLink.y;       duration: Generic.Variables.introAnimationDuration }
            // bottom buttons
            PropertyAnimation { easing.type: Easing.InExpo; target: disableButton; property: "opacity"; to: 0; duration: Generic.Variables.introAnimationDuration }
            PropertyAnimation { easing.type: Easing.InExpo; target: skipButton;    property: "opacity"; to: 0; duration: Generic.Variables.introAnimationDuration }
            // display toolbar
            NumberAnimation { easing.type: Easing.OutExpo; target: window; property: "toolBarOpacity";                                     to: 1; duration: Generic.Variables.introAnimationDuration }
            NumberAnimation { easing.type: Easing.OutExpo; target: window; property: "toolBarY";       from: -Generic.Style.toolbarHeight; to: 0; duration: Generic.Variables.introAnimationDuration }
            // change app window flags
            NumberAnimation { target: window; property: "flags"; to: Qt.Window; duration: 0 }
        }
        // change background color
        PropertyAction { target: window; property: "color"; value: Generic.Style.appBkgColor }
        // activate links and tooltips
        PropertyAction { target: mainRectangle; property: "enabled"; value: true }
    }

}



