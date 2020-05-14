import QtQuick 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyDiffraction 1.0 as Specific

Rectangle {
    property int globalSpacing: 20

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
            font.family: Generic.Style.secondFontFamily
            font.pixelSize: 42
            font.weight: Font.Light
            color: "lightgrey"
        }

        GenericAppElements.GuideWindow {
            message: "Brief project details will be shown in the main area."
            position: "right"
            guideCurrentIndex: 3
            toolbarCurrentIndex: Generic.Variables.ProjectIndex
            guidesCount: Generic.Variables.ProjectGuidesCount
        }
    }

    // State 2: Project Created/Opened

    Column {
        visible: Specific.Variables.projectOpened

        anchors.left: parent.left
        anchors.leftMargin: globalSpacing
        anchors.top: parent.top
        anchors.topMargin: globalSpacing * 0.5
        spacing: globalSpacing

        Text {
            //lineHeight: 0.5
            font.pixelSize: 42
            font.family: Generic.Style.secondFontFamily
            font.weight: Font.Light
            text: Specific.Variables.projectName
        }

        Grid {
            columns: 2
            rowSpacing: 0
            columnSpacing: globalSpacing

            Text {
                font.pixelSize: Generic.Style.fontPixelSize
                font.family: Generic.Style.fontFamily
                text: "Keywords:"
            }
            Text {
                width: mainRectangle.width * 0.5

                font.pixelSize: Generic.Style.fontPixelSize
                font.family: Generic.Style.fontFamily
                color: Generic.Style.buttonBkgHighlightedColor
                text: Specific.Variables.projectKeywords
                wrapMode: Text.WordWrap
            }

            Text {
                font.pixelSize: Generic.Style.fontPixelSize
                font.family: Generic.Style.fontFamily
                text: "Phases:"
            }
            Text {
                font.pixelSize: Generic.Style.fontPixelSize
                font.family: Generic.Style.fontFamily
                color: Specific.Variables.phaseIds().length ? Generic.Style.buttonBkgHighlightedColor : Generic.Style.buttonBkgAttentionColor
                text: Specific.Variables.phaseIds().length ? `phases.cif (labels: ${Specific.Variables.phaseIds().join(", ")})` : "None loaded"
            }

            Text {
                font.pixelSize: Generic.Style.fontPixelSize
                font.family: Generic.Style.fontFamily
                text: "Experiments:"
            }
            Text {
                font.pixelSize: Generic.Style.fontPixelSize
                font.family: Generic.Style.fontFamily
                color: Specific.Variables.experimentIds().length ? Generic.Style.buttonBkgHighlightedColor : Generic.Style.buttonBkgAttentionColor
                text: Specific.Variables.experimentIds().length ? `experiments.cif (labels: ${Specific.Variables.experimentIds().join(", ")})` : "None loaded"
            }

            Text {
                font.pixelSize: Generic.Style.fontPixelSize
                font.family: Generic.Style.fontFamily
                text: "Calculations:"
            }
            Text {
                font.pixelSize: Generic.Style.fontPixelSize
                font.family: Generic.Style.fontFamily
                color: Generic.Style.buttonBkgHighlightedColor
                text: "calculations.cif"
            }

            Text {
                font.pixelSize: Generic.Style.fontPixelSize
                font.family: Generic.Style.fontFamily
                text: "Modified:"
            }
            Text {
                font.pixelSize: Generic.Style.fontPixelSize
                font.family: Generic.Style.fontFamily
                color: Generic.Style.buttonBkgHighlightedColor
                text: Specific.Variables.projectModifiedDate
            }

        }

        // Temporary hide images
        Row {
            spacing: globalSpacing

            Repeater {
                model: ["structure.png", "refinement.png"]

                Rectangle {
                    visible: image.progress
                    height: (mainRectangle.width - 3*globalSpacing) / 2
                    width: height
                    color: "white"
                    border.color: Generic.Style.appBorderColor
                    Image {
                        id: image
                        anchors.fill: parent
                        anchors.margins: globalSpacing * 0.5
                        fillMode: Image.PreserveAspectFit
                        clip: true
                        antialiasing: true
                        smooth: true
                        source: Specific.Variables.projectName && Specific.Variables.projectControl ? Specific.Variables.projectControl.fullFilePath(modelData) : ""
                    }
                }
            }
        }

        Item { height: 42; width: 1 }
    }

}



