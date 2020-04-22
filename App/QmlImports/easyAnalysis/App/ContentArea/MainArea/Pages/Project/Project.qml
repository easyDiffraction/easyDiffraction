import QtQuick 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyDiffraction 1.0 as Specific

Rectangle {
    property int margin: 20

    id: mainRectangle

    Layout.fillWidth: true
    Layout.fillHeight: true

    color: Generic.Style.appBkgColor

    // State 1: No Project Created/Opened

    Column {
        visible: !Specific.Variables.projectOpened

        height: parent.height
        width: parent.width

        Text {
            height: parent.height
            width: parent.width
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: "No Project Created/Opened"
            font.pointSize: Generic.Style.fontPointSize * 3
            font.family: Generic.Style.fontFamily
            color: "lightgrey"
        }

        GenericAppElements.GuideWindow {
            message: "Brief project details will be shown in the main area."
            position: "right"
            guideCurrentIndex: 2
            toolbarCurrentIndex: Generic.Variables.ProjectIndex
            guidesCount: Generic.Variables.ProjectGuidesCount
        }
    }

    // State 2: Project Created/Opened

    Column {
        visible: Specific.Variables.projectOpened
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: margin
        spacing: 20

        Text {
            lineHeight: 0.5
            font.pointSize: Generic.Style.fontPointSize * 3
            font.family: Generic.Style.fontFamily
            text: Specific.Variables.projectName
        }

        Grid {
            columns: 2
            rowSpacing: 0
            columnSpacing: 15

            Text {
                font.pointSize: Generic.Style.fontPointSize + 1
                font.family: Generic.Style.fontFamily
                text: "Keywords:"
            }
            Text {
                font.pointSize: Generic.Style.fontPointSize + 1
                font.family: Generic.Style.fontFamily
                color: Generic.Style.buttonBkgHighlightedColor
                text: Specific.Variables.projectKeywords
            }

            Text {
                font.pointSize: Generic.Style.fontPointSize + 1
                font.family: Generic.Style.fontFamily
                text: "Phases:"
            }
            Text {
                font.pointSize: Generic.Style.fontPointSize + 1
                font.family: Generic.Style.fontFamily
                color: Specific.Variables.phaseIds().length ? Generic.Style.buttonBkgHighlightedColor : Generic.Style.buttonBkgAttentionColor
                text: Specific.Variables.phaseIds().length ? Specific.Variables.phaseIds().join(", ") : "None loaded"
            }

            Text {
                font.pointSize: Generic.Style.fontPointSize + 1
                font.family: Generic.Style.fontFamily
                text: "Experiments:"
            }
            Text {
                font.pointSize: Generic.Style.fontPointSize + 1
                font.family: Generic.Style.fontFamily
                color: Specific.Variables.experimentIds().length ? Generic.Style.buttonBkgHighlightedColor : Generic.Style.buttonBkgAttentionColor
                text: Specific.Variables.experimentIds().length ? Specific.Variables.experimentIds().join(", ") : "None loaded"
            }

            Text {
                font.pointSize: Generic.Style.fontPointSize + 1
                font.family: Generic.Style.fontFamily
                text: "Instrument:"
            }
            Text {
                font.pointSize: Generic.Style.fontPointSize + 1
                font.family: Generic.Style.fontFamily
                color: Generic.Style.buttonBkgHighlightedColor
                text: "Unknown"
            }

            Text {
                font.pointSize: Generic.Style.fontPointSize + 1
                font.family: Generic.Style.fontFamily
                text: "Modified:"
            }
            Text {
                font.pointSize: Generic.Style.fontPointSize + 1
                font.family: Generic.Style.fontFamily
                color: Generic.Style.buttonBkgHighlightedColor
                text: Specific.Variables.projectModifiedDate
            }

        }

        // Temporary hide images
        Row {
            spacing: margin

            Repeater {
                model: ["saved_structure.png", "saved_refinement.png"]

                Rectangle {
                    visible: image.progress
                    height: (mainRectangle.width - 3*margin) / 2
                    width: height
                    color: "white"
                    border.color: Generic.Style.appBorderColor
                    Image {
                        id: image
                        anchors.fill: parent
                        anchors.margins: 10
                        fillMode: Image.PreserveAspectFit
                        clip: true
                        antialiasing: true
                        smooth: true
                        source: Specific.Variables.projectName && Specific.Variables.projectControl ? Specific.Variables.projectControl.fullFilePath(modelData) : ""
                    }
                }
            }
        }

        Item { height: Generic.Style.fontPointSize * 3; width: 1 }
    }

}



