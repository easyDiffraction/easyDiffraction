import QtQuick 2.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyDiffraction 1.0 as Specific

Column {
    property alias model: contentListView.model

    property int borderWidth: 1
    property int cellHeight: 34
    property int rowCountToDisplayWithoutHeader: 3

    property string rowBackgroundColor: 'white'
    property string alternateRowBackgroundColor: '#f7f7f7'
    property string highlightedRowBackgroundColor: "#2a99d9"
    property string rowForegroundColor: "black"
    property string highlightedRowForegroundColor: "white"
    property string headerBackgroundColor: '#eee'
    property string headerBorderColor: '#dedede'

    //property string colorCell: "black"
    property var type_symbol_dict: ({})

    height: childrenRect.height
    spacing: 12

    function cellWidthProvider(column) {
        const allColumnWidth = width - borderWidth * 2
        const numberColumnWidth = 40
        const colorColumnWidth = 40
        const flexibleColumnsWidth = allColumnWidth - numberColumnWidth - colorColumnWidth
        const flexibleColumnsCount = 6
        if (column === 1)
            return numberColumnWidth
        else if (column === 4)
            return colorColumnWidth
        else
            return flexibleColumnsWidth / flexibleColumnsCount
    }

    ////////////////////////
    // Check if data changed
    ////////////////////////

    Text {
        visible: false
        text: proxy.timeStamp
        onTextChanged: {
            print("--------------------------------------------------------- Time stamp: ", text)
            if (Specific.Variables.projectOpened) {
                const atom_site_dict = Specific.Variables.project.phases.Fe3O4.atom_site
                let type_symbol_list = []
                for (let atom_id in atom_site_dict) {
                    type_symbol_list.push(atom_site_dict[atom_id].type_symbol.value)
                }
                type_symbol_list = Array.from(new Set(type_symbol_list))
                for (let i = 0; i < type_symbol_list.length; i++) {
                    type_symbol_dict[type_symbol_list[i]] = Generic.Style.atomColorList[i]
                }
            }
        }
    }

    Rectangle {
        id: listViewWrapper
        width: parent.width
        height: childrenRect.height
        border.color: headerBorderColor
        border.width: borderWidth

        Column {
            width: parent.width - parent.border.width * 2
            height: childrenRect.height + parent.border.width * 2
            spacing: 0
            padding: parent.border.width

            // Header
            ListView {
                id: headerListView
                width: parent.width
                height: cellHeight
                enabled: false

                header: Rectangle {
                    width: parent.width
                    height: cellHeight
                    color: headerBackgroundColor

                    Row {
                        anchors.fill: parent

                        Text {
                            width: cellWidthProvider(1)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: "No."
                        }
                        Text {
                            width: cellWidthProvider(2)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignLeft
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: "Label"
                        }
                        Text {
                            width: cellWidthProvider(3)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignLeft
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: "Atom"
                        }
                        Text {
                            width: cellWidthProvider(4)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: "Color"
                        }
                        Text {
                            width: cellWidthProvider(5)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: "x"
                        }
                        Text {
                            width: cellWidthProvider(6)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: "y"
                        }
                        Text {
                            width: cellWidthProvider(7)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: "z"
                        }
                        Text {
                            width: cellWidthProvider(8)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: "Occupancy"
                        }
                    }
                }
            }

            // Main content
            ListView {
                id: contentListView
                width: parent.width
                height: cellHeight * rowCountToDisplayWithoutHeader
                clip: true
                boundsBehavior: Flickable.StopAtBounds

                ScrollBar.horizontal: ScrollBar { policy: ScrollBar.AlwaysOff }
                ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded; minimumSize: 1 / rowCountToDisplayWithoutHeader }

                // Content row
                delegate: Rectangle {
                    id: contentRow
                    width: parent.width
                    height: cellHeight
                    color: backgroundColor()

                    function foregroundColor() {
                        return rowForegroundColor
                    }
                    function backgroundColor() {
                        return index % 2 ? alternateRowBackgroundColor : rowBackgroundColor
                    }

                    Row {
                        anchors.fill: parent

                        Text {
                            width: cellWidthProvider(1)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignRight
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: index + 1
                            color: foregroundColor()
                        }
                        Text {
                            width: cellWidthProvider(2)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignLeft
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: label
                            color: foregroundColor()
                        }
                        Text {
                            width: cellWidthProvider(3)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignLeft
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: atom
                            color: foregroundColor()
                        }
                        Rectangle {
                            width: cellWidthProvider(4)
                            height: parent.height - y * 2
                            y: 3
                            color: type_symbol_dict[atom]
                        }
                        Text {
                            width: cellWidthProvider(5)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: typeof xPos === 'number' ? xPos.toFixed(4) : xPos
                            color: foregroundColor()
                        }
                        Text {
                            width: cellWidthProvider(6)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: typeof yPos === 'number' ? yPos.toFixed(4) : yPos
                            color: foregroundColor()
                        }
                        Text {
                            width: cellWidthProvider(7)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: typeof zPos === 'number' ? zPos.toFixed(4) : zPos
                            color: foregroundColor()
                        }
                        Text {
                            width: cellWidthProvider(8)
                            height: parent.height
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            leftPadding: font.pixelSize
                            rightPadding: leftPadding
                            font.family: Generic.Style.fontFamily
                            font.pointSize: Generic.Style.fontPointSize
                            text: typeof occupancy === 'number' ? occupancy.toFixed(4) : occupancy
                            color: foregroundColor()
                        }
                    }


                }

            }
        }
    }

}
