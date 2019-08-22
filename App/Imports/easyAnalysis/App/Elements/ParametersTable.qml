import QtQuick 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtGraphicalEffects 1.12
import QtQuick.Controls.impl 2.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea

Controls1.TableView {
    property bool customFrameVisible: true
    property bool selectable: false
    property int selectedRow: 0
    property int visibleRowsCount: Math.min(model.count, Generic.Style.maxVisibleRowsCount)

    id: tableView
    clip: true
    Layout.fillWidth: true
    implicitHeight: (visibleRowsCount + 1) * Generic.Style.tableRowHeight + Generic.Style.appBorderThickness // add 1 row for header

    horizontalScrollBarPolicy: Qt.ScrollBarAlwaysOff
    verticalScrollBarPolicy: Qt.ScrollBarAsNeeded

    // Model
    model: ListModel {}

    // Custom frame
    frameVisible: false
    Rectangle {
        anchors.fill: parent
        color: "transparent"
        border.color: Generic.Style.appBorderColor
        border.width: customFrameVisible ? 1 : 0
    }

    // Header
    headerDelegate: Rectangle {
        implicitWidth: headerLayout.implicitWidth
        height: Generic.Style.tableRowHeight
        color: Generic.Style.tableHeaderRowColor

        RowLayout {
            id: headerLayout
            anchors.fill: parent
            spacing: 0

            // Vertical border
            Rectangle {
                Layout.fillHeight: true
                width: Generic.Style.appBorderThickness
                color: Generic.Style.appBorderColor
            }

            // Vertical spacer
            Item { width: Generic.Style.tableColumnSpacing/2 }

            // Icon
            Item {
                visible: styleData.value === "Remove"
                Layout.alignment: Qt.AlignCenter
                height: Generic.Style.tableRowHeight * 0.6
                width: height
                Image {
                    id: headerCellIcon
                    visible: false
                    anchors.fill: parent
                    smooth: true
                    sourceSize.width: parent.width
                    sourceSize.height: parent.height
                    source: Generic.Variables.thirdPartyIconsPath + "trash-alt.svg"
                }
                ColorOverlay {
                    source: headerCellIcon
                    anchors.fill: headerCellIcon
                    color: Generic.Style.buttonIconEnabledColor
                }
            }

            // Content
            Text {
                visible: styleData.value !== "Remove"
                Layout.fillWidth: true
                horizontalAlignment: styleData.textAlignment
                font.family: Generic.Style.fontFamily
                font.pointSize: Generic.Style.fontPointSize
                text: styleData.value
            }

            // Vertical spacer
            Item { width: Generic.Style.tableColumnSpacing/2 }
        }
    }

    // Row
    rowDelegate: Rectangle {
        height: Generic.Style.tableRowHeight
        Layout.fillHeight: true
        color: {
            if (selectable && styleData.selected)
                return Generic.Style.tableHighlightRowColor
            return styleData.alternate ? Generic.Style.tableAlternateRowColor : Generic.Style.tableRowColor
        }
    }

    // Cell
    itemDelegate: Rectangle {
        implicitWidth: cellLayout.implicitWidth
        color: "transparent"

        RowLayout {
            id: cellLayout
            anchors.fill: parent
            spacing: 0

            // Vertical border
            Rectangle {
                Layout.fillHeight: true
                width: Generic.Style.appBorderThickness
                color: selectable && styleData.selected ? Generic.Style.tableHighlightBorderColor : Generic.Style.tableHeaderRowColor
            }

            // Vertical spacer
            Item {
                id: leftSpacer
                visible: !(styleData.role === "remove") && !(styleData.role === "color")
                width: Generic.Style.tableColumnSpacing/2
            }


            // Icon
            Item {
                visible: (styleData.value === "sample") || (styleData.value === "instrument")
                Layout.alignment: Qt.AlignCenter
                height: Generic.Style.tableRowHeight * 0.6
                width: height
                Image {
                    id: cellIcon
                    visible: false
                    anchors.fill: parent
                    smooth: true
                    sourceSize.width: parent.width
                    sourceSize.height: parent.height
                    source: {
                        if (styleData.value === "sample") return Generic.Variables.thirdPartyIconsPath + "gem.svg"
                        if (styleData.value === "instrument") return Generic.Variables.thirdPartyIconsPath + "microscope.svg"
                        return ""
                    }
                }
                ColorOverlay {
                    source: cellIcon
                    anchors.fill: cellIcon
                    color: selectable && styleData.selected ? Generic.Style.buttonIconHighlightedColor : Generic.Style.buttonIconEnabledColor
                }
            }

            // TextEdit
            TextEdit {
                Layout.fillWidth: true
                font.family: Generic.Style.fontFamily
                font.pointSize: Generic.Style.fontPointSize
                visible: !(styleData.role === "remove") && !(styleData.role === "color")
                ///enabled: styleData.role === "num" || styleData.value[0] === "&" ? false : true
                enabled: false
                color: {
                    if (!enabled  && styleData.role === "jobName")
                        return Generic.Style.tableDisabledTextColor
                    return selectable && styleData.selected ? Generic.Style.tableHighlightTextColor : Generic.Style.tableTextColor
                }
                text: {
                    if (styleData.value[0] === "&" && styleData.role === "jobName") return styleData.value.substr(1)
                    if (styleData.value === "sample") return ""
                    if (styleData.value === "instrument") return ""
                    if (styleData.role === "fit") return ""
                    if (styleData.role === "color") return ""
                    if (styleData.role === "min" && !styleData.value) return "-\u221E"
                    if (styleData.role === "max" && !styleData.value) return "+\u221E"
                    return styleData.value
                }
            }

            // Remove-button
            GenericAppContentArea.Button {
                id: button
                enabled: false
                visible: styleData.role === "remove" ? true : false
                ToolTip.visible: hovered
                ToolTip.text: qsTr("Remove this row from the table")
                Layout.fillHeight: true
                Layout.fillWidth: true
                padding: 2
                leftPadding: 3
                rightPadding: 4
                background: Rectangle {
                    anchors.fill: parent
                    anchors.margins: button.padding
                    anchors.leftMargin: button.leftPadding
                    anchors.rightMargin: button.rightPadding
                    radius: Generic.Style.toolbarButtonRadius
                    border.color: button.highlighted ? Generic.Style.buttonBkgHighlightedColor : Generic.Style.appBorderColor
                    color: {
                        if (!button.enabled)
                            return Generic.Style.buttonBkgDisabledColor
                        var color1 = button.highlighted ? Generic.Style.buttonBkgHighlightedColor : Generic.Style.buttonBkgEnabledColor
                        var color2 = Generic.Style.buttonBkgBlendColor
                        var alpha = button.down ? Generic.Style.buttonBkgBlendAlpha : 0.0
                        return Color.blend(color1, color2, alpha)
                    }
                }
                icon.source: styleData.role === "remove" ? Generic.Variables.thirdPartyIconsPath + "minus-circle.svg" : ""
            }

            // Color-box
            Button {
                id: colorBox
                visible: styleData.role === "color" ? true : false
                Layout.fillHeight: true
                Layout.fillWidth: true
                contentItem: IconLabel {                }
                background: Rectangle {
                    anchors.fill: parent
                    anchors.margins: 2
                    anchors.rightMargin: 3
                    anchors.leftMargin: anchors.rightMargin
                    color: styleData.role === "color" ? styleData.value : "transparent"
                }
            }

            // CheckBox
            CheckBox {
                visible: styleData.role === "fit"
                Layout.fillWidth: true
                Layout.fillHeight: true
                checked: styleData.value
            }

            // Vertical spacer
            Item {
                id: rightSpacer
                visible: !(styleData.role === "remove") && !(styleData.role === "color")
                width: Generic.Style.tableColumnSpacing/2
            }


        }
    }

    // Adjust columns widths function
    function resizeColumns() {
        // First, resize with default Qt function
        tableView.resizeColumnsToContents()

        // sum column widths and number of resizable columns
        let sumColumnsWidth = 0
        let resizableColumnsCount = 0
        for (let i = 0; i < columnCount; i++){
            sumColumnsWidth += getColumn(i).width
            if (getColumn(i).resizable) {
                resizableColumnsCount += 1
            }
        }

        // increase columns width
        const extenderWidth = Math.round((tableView.width - sumColumnsWidth) / resizableColumnsCount)
        for (let i = 0; i < columnCount; i++){
            if (getColumn(i).resizable) {
                getColumn(i).width += extenderWidth
            }
        }

        // adjust last column width
        const rest = tableView.width - sumColumnsWidth - extenderWidth*resizableColumnsCount
        getColumn(columnCount-1).width += rest

        // select 1st row, if table is selectable
        if (selectable)
            tableView.selection.select(selectedRow)
    }

    // Adjust columns widths on completed
    Component.onCompleted: {
        resizeColumns()
    }

}
