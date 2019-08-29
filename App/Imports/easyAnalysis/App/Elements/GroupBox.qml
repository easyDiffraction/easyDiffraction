import QtQuick 2.12
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import Qt.labs.settings 1.1
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements

Column {
    property string title: ""
    property bool collapsible: true
    property bool collapsed: collapsible ? true : false
    property bool showBorder: true
    property alias content: layout.children

    id: box

    Layout.fillWidth: true
    //width: parent.width
    Layout.alignment: Qt.AlignTop
    spacing: 0

    /////////////
    // Title area
    /////////////
    Button {
        id: titleArea
        visible: title ? true : false
        leftPadding: Generic.Style.sidebarGroupIndicatorIconSize
        text: title
        font.weight: Font.DemiBold
        icon.width: Generic.Style.sidebarGroupIndicatorIconSize
        icon.height: Generic.Style.sidebarGroupIndicatorIconSize
        icon.source: iconSource()
        icon.color: enabled ? Generic.Style.sidebarGroupTitleColor : Generic.Style.sidebarGroupIconDisabledColor

        contentItem: IconLabel {
            spacing: titleArea.spacing
            mirrored: titleArea.mirrored
            display: titleArea.display
            icon: titleArea.icon
            text: titleArea.text
            font: titleArea.font
            color: enabled ? Generic.Style.sidebarGroupTitleColor : Generic.Style.sidebarGroupTitleDisabledColor
        }

        background: Rectangle {
            implicitHeight: 40
            visible: !titleArea.flat || titleArea.down || titleArea.checked || titleArea.highlighted
            color: "transparent"
        }

        // Click area for collapsion
        MouseArea {
            anchors.fill: parent
            onClicked: {
                if (collapsible) {
                    if (collapsed) {
                        collapsed = false
                        contentArea.height = groupBox.height
                    }
                    else {
                        collapsed = true
                        contentArea.height = 0
                    }
                }
            }
        }
    }

    ///////////////
    // Content area
    ///////////////
    Item {
        id: contentArea
        width: parent.width
        height: collapsed ? 0 : groupBox.height // default: open
        clip: true

        // Groupbox for "content"
        GroupBox {
            id: groupBox
            width: parent.width
            topPadding: 0
            leftPadding: 18

            background: Rectangle {
                y: groupBox.topPadding - groupBox.bottomPadding
                width: groupBox.width
                height: groupBox.height - groupBox.topPadding + groupBox.bottomPadding

                color: "transparent"
                //border.color: control.palette.mid
            }

            GridLayout {
                id: layout
                width: parent.width
            }
        }

        // Collapsion animation
        Behavior on height { NumberAnimation { duration: 150 } }
    }

    ////////////////
    // Bottom border
    ////////////////
    Rectangle {
        width: parent.width
        height: showBorder ? Generic.Style.appBorderThickness : 0
        color: Generic.Style.appBorderColor
    }

    //////////
    // Helpers
    //////////
    function iconSource() {
        if (!collapsible)
            return Generic.Variables.thirdPartyIconsPath + "circle.svg"
        return collapsed ? Generic.Variables.originalIconsPath + "triangle-right.svg" : Generic.Variables.originalIconsPath + "triangle-down.svg"
    }

    //////////////////////
    // Persistent settings
    //////////////////////
    Settings { id: settings }
    Component.onCompleted: {
        if (collapsible && title) {
            collapsed = settings.value(title, true)
        }
    }
    Component.onDestruction: {
        if (collapsible && title) {
            settings.setValue(title, collapsed)
        }
    }

}
