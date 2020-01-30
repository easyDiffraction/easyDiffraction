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
        spacing: 30

        // Application icon, name, version container
        Row {
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 10

            // Application icon
            Image {
                //id: appIcon
                y: 10
                width: 75
                height: width
                //anchors.horizontalCenter: parent.horizontalCenter
                source: Specific.Settings.appIconPath
            }

            // Application name and version
            Column {

                // Application name
                Row {
                    //anchors.horizontalCenter: parent.horizontalCenter
                    spacing: 3

                    Text {
                        text: "easy"
                        font.family: Generic.Style.introCondencedThinFontFamily
                        font.pointSize: appNameFontSize
                        color: "#444"
                    }
                    Text {
                        text: "Diffraction"
                        font.family: Generic.Style.introCondencedRegularFontFamily
                        font.pointSize: appNameFontSize
                        color: "#444"
                    }
                }
                // Application version
                Text {
                    anchors.right: parent.right
                    font.family: Generic.Style.introExpandedThinFontFamily
                    font.pointSize: appVersionFontSize
                    text: "Version %1 (%2)".arg(Specific.Settings.appVersion).arg(Specific.Settings.appDate)
                }
            }
        }

        // Eula and licences container
        Column {
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 5

            // EULA
            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                font.family: Generic.Style.fontFamily
                font.pointSize: Generic.Style.fontPointSize
                text: "End User Licence Agreement"
                color: Generic.Style.blueColor

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Qt.openUrlExternally(Specific.Settings.eulaUrl)
                }
            }

            // Licences
            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                font.family: Generic.Style.fontFamily
                font.pointSize: Generic.Style.fontPointSize
                text: "Dependent Open Source Licenses"
                color: Generic.Style.blueColor

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Qt.openUrlExternally(Specific.Settings.oslUrl)
                }
            }
        }

        // Description container
        Column {
            id: descriptionContainer
            width: 350
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 5

            Text {
                width: parent.width
                anchors.horizontalCenter: parent.horizontalCenter
                horizontalAlignment: Text.AlignHCenter
                wrapMode: TextEdit.WordWrap
                font.family: Generic.Style.fontFamily
                font.pointSize: Generic.Style.fontPointSize
                color: "#222"
                text: "easyDiffraction is a scientific software for\n modelling and analysis of neutron diffraction data."
            }


            Text {
                width: parent.width
                anchors.horizontalCenter: parent.horizontalCenter
                horizontalAlignment: Text.AlignHCenter
                wrapMode: TextEdit.WordWrap
                font.family: Generic.Style.fontFamily
                font.pointSize: Generic.Style.fontPointSize
                color: "#222"
                text: "easyDiffraction is build by ESS DMSC in\n Copenhagen, Denmark."
            }

            // ESS icon
            Image {
                anchors.horizontalCenter: parent.horizontalCenter
                width: 0.75*sourceSize.width
                height: 0.75*sourceSize.height
                source: Specific.Settings.essIconPath

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Qt.openUrlExternally(Specific.Settings.essUrl)
                }
            }
        }

        // Footer
        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            font.family: Generic.Style.fontFamily
            font.pointSize: Generic.Style.fontPointSize
            color: "#222"
            text: "© 2019-2020 • All rights reserved"
        }
    }
}
