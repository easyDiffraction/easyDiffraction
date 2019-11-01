import QtQuick 2.12
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyDiffraction 1.0 as Specific

ColumnLayout {
//    property alias model: contentStatusListView.model

    width: parent.width
    height: Generic.Style.statusBarHeight
    GenericAppElements.HorizontalBorder {}

    ListView {
        id: contentStatusListView

        Layout.fillWidth: true
        height: Generic.Style.statusBarHeight - Generic.Style.appBorderThickness
        Layout.leftMargin: Generic.Style.toolbarSpacing
        Layout.rightMargin: Generic.Style.toolbarSpacing
        Layout.bottomMargin: 4

        model: Specific.Variables.projectOpened ? proxy.statusInfo : null
        orientation: ListView.Horizontal

        // Content row
        delegate: Rectangle {
            id: contentRow
            width: 400 //childrenRect.width
            height: Generic.Style.statusBarHeight - Generic.Style.appBorderThickness - 4
            color: 'white'

            Row {
                width: 200 //childrenRect.width
                height: Generic.Style.statusBarHeight - Generic.Style.appBorderThickness - 4

                Text {
                    //width: 150 //cellWidthProvider(1)
                    width: 100
                    height: parent.height
                    verticalAlignment: Text.AlignVCenter
                    ///horizontalAlignment: Text.AlignRight
//                            leftPadding: font.pixelSize
//                            rightPadding: leftPadding
                    text: {
                        return label
                    }
                }
                Text {
                 width: 100
                    //width: 150 //cellWidthProvider(1)
                    height: parent.height
                    verticalAlignment: Text.AlignVCenter
                    //horizontalAlignment: Text.AlignRight
//                            leftPadding: font.pixelSize
//                            rightPadding: leftPadding
                    text: {
                        return value
                        }
                }
            }

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
