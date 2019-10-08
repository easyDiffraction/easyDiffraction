import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtQuick.Layouts 1.12
//import Qt.labs.settings 1.0
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar
import easyDiffraction 1.0 as Specific

Dialog {
    property int animationDuration: Generic.Variables.showIntro ? Generic.Variables.introAnimationDuration : 0
    property int appNameFontSize: Generic.Style.systemFontPointSize * 4
    property int appVersionFontSize: Generic.Style.systemFontPointSize + 3
    property int repeatFontSize: Generic.Style.systemFontPointSize + 1

    id: dialog
    visible: true
    anchors.centerIn: parent
    width: parent.width
    height: parent.height
    background: Rectangle { color: "white" }

    Component.onCompleted: {
        animo.restart()
        //console.log("systemFontPointSize: ", Generic.Style.systemFontPointSize)
        //console.log("systemFontPointSize: ", Generic.Style.systemFontFamily)
    }

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
            source: Specific.Variables.resourcesPath + "Icons/App.svg"
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
            GenericAppToolbar.Button {
                id: modellingButton
                opacity: 0
                enabled: false
                checked: true
                autoExclusive: false
                width: 150
                font.bold: true
                text: "Modelling"
                ToolTip.text: "Simulation of diffraction data"
                onClicked: {
                    //console.log("3--", proxy.cell_length_a())
                    //text = proxy.cell_length_a()
                    //checked = true
                }
                Component.onCompleted: {
                    //console.log("2--", proxy.cell_length_a())
                }
            }
            GenericAppToolbar.Button { width: 1; opacity: 0 }
            GenericAppToolbar.Button {
                id: analysisButton
                opacity: 0
                checked: true
                autoExclusive: false
                width: 150
                font.bold: true
                text: "Analysis"
                ToolTip.text: "Fitting of diffraction data"
                onClicked: {
                    dialog.close()
                    Generic.Variables.toolbarCurrentIndex = 0
                }
            }
        }
    }

    // Buttons at the bottom
    Row {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
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
        /*
        Button {
            id: repeatButton
            visible: Generic.Variables.showIntro
            text: "Repeat"
            contentItem: IconLabel {
                text: repeatButton.text
                font.family: Generic.Style.introThinFontFamily
                font.pointSize: repeatFontSize
                color: "#666"
            }
            background: Rectangle {
                color: "transparent"
            }
            onClicked: {
                resetIntro()
                animo.restart()
            }
        }
        */
    }

    // Reset intro
    function resetIntro() {
        making.opacity = 0
        diffraction.opacity = 0
        dam.opacity = 0
        easy.opacity = 0

        easy.color = "#666"
        diffraction.color = "#666"

        easy.font.family = Generic.Style.introCondencedRegularFontFamily
        diffraction.text = "diffraction"

        making.x = 0
        diffraction.x = making.width
        dam.x = making.width + diffraction.width
        easy.x = making.width + diffraction.width + dam.width

        //modellingButton.width = 0
        //analysisButton.width = 0
        //modellingButton.text = ""
        //analysisButton.text = ""
        modellingButton.opacity = 0
        analysisButton.opacity = 0

        appIcon.opacity = 0
        appVersion.opacity = 0
    }

    ////////////
    // Animation
    ////////////

    SequentialAnimation {
        id: animo
        //running: true
        PauseAnimation {
            //duration: 2*animationDuration
        }
        ParallelAnimation {
            // appearing
            NumberAnimation { easing.type: Easing.OutCubic; target: making;      property: "opacity"; to: 1; duration: 2*animationDuration }
            NumberAnimation { easing.type: Easing.OutCubic; target: diffraction; property: "opacity"; to: 1; duration: 2*animationDuration }
            NumberAnimation { easing.type: Easing.OutCubic; target: dam;         property: "opacity"; to: 1; duration: 2*animationDuration }
            NumberAnimation { easing.type: Easing.OutCubic; target: easy;        property: "opacity"; to: 1; duration: 2*animationDuration }
        }
        ParallelAnimation {
            // highlighting
            PropertyAnimation { target: easy;        property: "color"; to: "#444"; duration: animationDuration }
            PropertyAnimation { target: diffraction; property: "color"; to: "#444"; duration: animationDuration }
            // hidding
            NumberAnimation { target: making; property: "opacity"; to: 0; duration: animationDuration }
            NumberAnimation { target: dam;    property: "opacity"; to: 0; duration: animationDuration }
        }
        ParallelAnimation {
            // font change
            PropertyAnimation { target: easy; property: "font.family"; to: Generic.Style.introCondencedThinFontFamily; duration: animationDuration*0.1 }
            // text change
            PropertyAnimation { target: diffraction; property: "text"; to: "Diffraction"; duration: animationDuration*0.1 }
            // mooving
            NumberAnimation { easing.type: Easing.OutExpo; target: easy;         property: "x"; to: container.width/2 - easy.width - (diffraction.width - easy.width)/2; duration: animationDuration }
            NumberAnimation { easing.type: Easing.OutExpo; target: diffraction;  property: "x"; to: container.width/2 - (diffraction.width - easy.width)/2; duration: animationDuration }
        }
        ParallelAnimation {
            // show app icon and version
            PropertyAnimation { easing.type: Easing.InExpo; target: appIcon;    property: "opacity"; to: 1; duration: animationDuration }
            PropertyAnimation { easing.type: Easing.InExpo; target: appVersion; property: "opacity"; to: 1; duration: animationDuration }
        //}
        //ParallelAnimation {
            // show buttons
            //PropertyAnimation { target: modellingButton; property: "text"; to: "Modelling"; duration: animationDuration*0.29 }//animationDuration }
            //PropertyAnimation { target: analysisButton;  property: "text"; to: "Analysis"; duration: animationDuration*0.29 } //animationDuration }
            //PropertyAnimation { target: modellingButton; property: "width"; to: 150; duration: animationDuration*0.3 }//animationDuration }
            //PropertyAnimation { target: analysisButton;  property: "width"; to: 150; duration: animationDuration*0.3 } //animationDuration }
            PropertyAnimation { easing.type: Easing.InExpo; target: modellingButton; property: "opacity"; to: 1; duration: animationDuration }
            PropertyAnimation { easing.type: Easing.InExpo; target: analysisButton; property: "opacity"; to: 1; duration: animationDuration }
        }
    }



}










