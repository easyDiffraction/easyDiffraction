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

    visible: Generic.Variables.showAbout

    onClosed: Generic.Variables.showAbout = 0

    Column {
        padding: 20
        spacing: 30

        // Application icon, name, version container
        Item {
            id: infoRect
            width: childrenRect.width
            height: childrenRect.height

            Row {
                spacing: 10
                bottomPadding: appIcon.y

                // Application icon
                Image {
                    id: appIcon
                    y: 10
                    width: 75
                    fillMode: Image.PreserveAspectFit
                    source: Specific.Constants.appIconPath
                }

                // Application name and version
                Column {
                    spacing: 0

                    // Application name
                    Row {
                        spacing: 3

                        Text {
                            text: "easy"
                            font.family: Generic.Style.secondCondensedFontFamily
                            font.weight: Font.ExtraLight
                            font.pixelSize: 50
                            color: "#444"
                        }
                        Text {
                            text: "Diffraction"
                            font.family: Generic.Style.secondCondensedFontFamily
                            font.pixelSize: 50
                            color: "#444"
                        }
                    }
                    // Application version
                    Text {
                        id: appVersion
                        anchors.right: parent.right
                        font.family: Generic.Style.secondExpandedFontFamily
                        font.weight: Font.Light
                        font.pixelSize: Generic.Style.fontPixelSize
                        text: "Version %1 (%2)".arg(Specific.Constants.appVersion).arg(Specific.Constants.appDate)
                    }
                }
            }

            // Link to app website
            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: Qt.openUrlExternally(Specific.Constants.appUrl)
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
                font.pixelSize: Generic.Style.fontPixelSize
                text: "End User Licence Agreement"
                color: Generic.Style.blueColor

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Qt.openUrlExternally(Specific.Constants.eulaUrl)
                }
            }

            // Licences
            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                font.family: Generic.Style.fontFamily
                font.pixelSize: Generic.Style.fontPixelSize
                text: "Dependent Open Source Licenses"
                color: Generic.Style.blueColor

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Qt.openUrlExternally(Specific.Constants.oslUrl)
                }
            }
        }

        // Description container
        Column {
            id: descriptionContainer
            width: infoRect.width
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 5

            Text {
                width: parent.width
                anchors.horizontalCenter: parent.horizontalCenter
                horizontalAlignment: Text.AlignHCenter
                wrapMode: TextEdit.WordWrap
                font.family: Generic.Style.fontFamily
                font.pixelSize: Generic.Style.fontPixelSize
                color: "#222"
                text: "easyDiffraction is a scientific software for\n modelling and analysis of neutron diffraction data."
            }

            Text {
                width: parent.width
                anchors.horizontalCenter: parent.horizontalCenter
                horizontalAlignment: Text.AlignHCenter
                wrapMode: TextEdit.WordWrap
                font.family: Generic.Style.fontFamily
                font.pixelSize: Generic.Style.fontPixelSize
                color: "#222"
                text: "easyDiffraction is build by ESS DMSC in\n Copenhagen, Denmark."
            }

            // ESS icon
            Image {
                anchors.horizontalCenter: parent.horizontalCenter
                height: 75
                fillMode: Image.PreserveAspectFit
                source: Specific.Constants.essIconPath

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Qt.openUrlExternally(Specific.Constants.essUrl)
                }
            }
        }

        // Footer
        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            font.family: Generic.Style.fontFamily
            font.pixelSize: Generic.Style.fontPixelSize
            color: "#222"
            text: "© 2019-2020 • All rights reserved"
        }
    }
}
