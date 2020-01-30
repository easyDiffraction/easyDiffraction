import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtQuick.Layouts 1.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.Controls 1.0 as GenericControls
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.Toolbar 1.0 as GenericAppToolbar
import easyDiffraction 1.0 as Specific

GenericControls.Dialog {
    id: aboutDialog
    title: "About"

    Column {
        padding: 20
        spacing: 15
                        // Application icon
        Image {
            id: appIcon
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
            height: easy.height
            width: easy.width
            Text { id: easy;        text: "easyDiffraction"; font.family: Generic.Style.introCondencedRegularFontFamily; font.pointSize: appNameFontSize; color: "#666" }
            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: Qt.openUrlExternally(Specific.Settings.appUrl)
            }
        }
//                // Application version
        Text {
            id: appVersion
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

        Text {
            id: eula
            anchors.horizontalCenter: parent.horizontalCenter
            font.family: Generic.Style.introExpandedThinFontFamily
            font.pointSize: appVersionFontSize
            text: "End User Licence Agreement"
            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: Qt.openUrlExternally(Specific.Settings.eulaUrl)
            }
        }

        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            id: osl
            font.family: Generic.Style.introExpandedThinFontFamily
            font.pointSize: appVersionFontSize
            text: "Dependent Open Source Licenses"
            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: Qt.openUrlExternally(Specific.Settings.oslUrl)
            }
        }

        Text {
            wrapMode: TextEdit.WordWrap
            anchors.horizontalCenter: parent.horizontalCenter
            text: "easyDiffraction is build by ESS - DMSC in Copenhagen Denmark"
        }

         Image {
            id: essIcon
            anchors.horizontalCenter: parent.horizontalCenter
            width: 0.75*img2.sourceSize.width
            height: 0.75*img2.sourceSize.height
            //antialiasing: true
            //fillMode: Image.PreserveAspectFit
            source: Specific.Settings.essIconPath
            sourceSize: Qt.size( img2.sourceSize.width, img2.sourceSize.height )
            Image {
                id: img2
                source: parent.source
                width: 0
                height: 0
            }
            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: Qt.openUrlExternally(Specific.Settings.essUrl)
            }
        }

        Row {
            spacing: 15

            anchors.horizontalCenter: parent.horizontalCenter

            Text{
                text: "© 2019-2020"
            }
             Text{
                text: "All rights reserved"
            }
        }
    }
}