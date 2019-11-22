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
            guideCurrentIndex: 1
            toolbarCurrentIndex: Generic.Variables.HomeIndex
            guidesCount: Generic.Variables.HomeGuidesCount
        }
    }

    // State 2: Project Created/Opened

    Column {
        visible: Specific.Variables.projectOpened

        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: margin
        spacing: 10

        Text {
            text: Specific.Variables.projectOpened ? projectManager.projectName : ""
            font.pointSize: Generic.Style.fontPointSize * 3
            font.family: Generic.Style.fontFamily
        }

        Text {
            text: {
                let s = ""
                if (!Specific.Variables.projectOpened)
                    return s
                s += "Keywords: " + projectManager.projectKeywords + "\n"
                s += "Phases: " + proxy.project.info.phase_ids.join(", ") + "\n"
                s += "Experiments: " + proxy.project.info.experiment_ids.join(", ") + "\n"
                s += "Instrument: 6T2 at LLB\n"
                s += "Modified: " + proxy.project.info.modified_datetime
            }
            font.pointSize: Generic.Style.fontPointSize + 1
            font.family: Generic.Style.fontFamily
        }

        Item { height: 1; width: 1 }

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
                        source: Specific.Variables.projectOpened ? proxy.fullFilePath(modelData) : ""
                    }
                }
            }
        }

        Item { height: Generic.Style.fontPointSize * 3; width: 1 }
    }

}



