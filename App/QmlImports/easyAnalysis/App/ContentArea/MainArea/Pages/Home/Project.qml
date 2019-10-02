import QtQuick 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyDiffraction 1.0 as Specific

Rectangle {
    property int margin: 20

    id: mainRectangle

    Layout.fillWidth: true
    Layout.fillHeight: true

    color: Generic.Style.appBkgColor

    // State 1: No Project Created/Opened

    Column {
        visible: !Generic.Variables.projectOpened

        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter

        Text {
            text: "No Project Created/Opened"
            font.pointSize: Generic.Style.fontPointSize * 3
            font.family: Generic.Style.fontFamily
            color: "lightgrey"
        }
    }

    // State 2: Project Created/Opened

    Column {
        visible: Generic.Variables.projectOpened

        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: margin
        spacing: 10

        Text {
            text: Generic.Variables.projectOpened ? proxy.project.info.name : ""
            font.pointSize: Generic.Style.fontPointSize * 3
            font.family: Generic.Style.fontFamily
        }

        Text {
            text: Generic.Variables.projectOpened ? proxy.project.info.keywords.join(", ") : ""
            font.pointSize: Generic.Style.fontPointSize + 1
            font.family: Generic.Style.fontFamily
        }

        Item { height: 1; width: 1 }

        // Temporary hide images

        Row {
            spacing: margin

            Repeater {
                model: ["saved_structure", "saved_refinement"]

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
                        source: Generic.Variables.projectOpened ? proxy.project_dir_absolute_path + "/" + modelData + ".png" : ""
                    }
                }
            }
        }

        Item { height: Generic.Style.fontPointSize * 3; width: 1 }
    }

}



