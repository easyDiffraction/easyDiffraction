import QtQuick 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyDiffraction 1.0 as Specific

Rectangle {
    property int margin: 20

    id: parentRectangle

    Layout.fillWidth: true
    Layout.fillHeight: true

    color: Generic.Style.appBkgColor

    Column {
        visible: !proxy.project_opened

        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter

        Text {
            text: "No Project Created/Opened"
            font.pointSize: Generic.Style.fontPointSize * 3
            font.family: Generic.Style.fontFamily
            color: "lightgrey"
        }
    }

    Column {
        visible: proxy.project_opened

        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: margin
        spacing: 10

        Text {
            text: proxy.project_opened ? proxy.project_name : ""
            /*
            onTextChanged: {
                print("typeof proxy.cell_length_a", typeof proxy.cell_length_a)
                print("typeof text", typeof text)
                print("proxy.cell_length_a", proxy.cell_length_a)
                print("text", text)
                proxy.cell_length_a = text
            }
            */
            font.pointSize: Generic.Style.fontPointSize * 3
            font.family: Generic.Style.fontFamily
        }

        Text {
            text: proxy.project_opened ? "Keywords: " + proxy.project_info : ""
            font.pointSize: Generic.Style.fontPointSize + 1
            font.family: Generic.Style.fontFamily
        }

        Item { height: 1; width: 1 }

        Row {
            spacing: margin

            Repeater {
                model: ["structure", "refinement"]

                Rectangle {
                    height: (parentRectangle.width - 3*margin) / 2
                    width: height
                    color: "white"
                    border.color: Generic.Style.appBorderColor
                    Image {
                        anchors.fill: parent
                        anchors.margins: 10
                        fillMode: Image.PreserveAspectFit
                        clip: true
                        antialiasing: true
                        smooth: true
                        source: proxy.project_opened ? proxy.project_dir_absolute_path + "/" + modelData + ".png" : ""
                    }
                }
            }
        }

        Item { height: Generic.Style.fontPointSize * 3; width: 1 }
    }
}



