import QtQuick 2.12
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements

ColumnLayout {
    property alias model: contentStatusListView.model

    width: parent.width
    height: 100 // Generic.Style.statusBarHeight
    GenericAppElements.HorizontalBorder {}
//    Rectangle {
//        Layout.fillWidth: true
//        height: Generic.Style.statusBarHeight
//        color: Generic.Style.appBkgColor
//        RowLayout {
//            anchors.fill: parent
//            anchors.leftMargin: Generic.Style.toolbarSpacing
//            anchors.rightMargin: Generic.Style.toolbarSpacing
//            anchors.bottomMargin: 4
//            Rectangle {
//                Layout.fillWidth: true
//                height: parent.height
//                color:  Generic.Style.appBkgColor
//                Text {
//                    id: statusBarText
//                    height: parent.height
//                    color: Generic.Style.sidebarGroupTitleDisabledColor
//                    text: "Placeholder Text"
//                    verticalAlignment: Text.AlignVCenter
//                }
            // Main content
    ListView {
        id: contentStatusListView

//            anchors.fill: parent
//            anchors.leftMargin: Generic.Style.toolbarSpacing
//            anchors.rightMargin: Generic.Style.toolbarSpacing
//            anchors.bottomMargin: 4
        width: 300
        height: 50

        // Content row
        delegate: Rectangle {
            id: contentRow
            width: parent.width
            height: 50 //cellHeight
            color: 'blue'

            //Row {
            //    anchors.fill: parent

                Text {
                    width: 150 //cellWidthProvider(1)
                    height: parent.height
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignRight
//                            leftPadding: font.pixelSize
//                            rightPadding: leftPadding
                    text: {
                        print(label, value)
                        return label
                        }
                    Component.onCompleted: {
                        print('Boo - Text')
                    }
                }
            //}

            Component.onCompleted: {
                print('Boo - Rectangle')
            }
        }
        Component.onCompleted: {
            print('Boo - ListView')
        }
    }
    Component.onCompleted: {
        print('Boo - ColumnLayout ')
    }
}
//        }
//    }
//}
