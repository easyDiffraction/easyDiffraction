import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtQuick.Layouts 1.12
import QtGraphicalEffects 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons

Dialog {
    property alias message: messageItem.text

    property string position: "right"

    property int toolbarCurrentIndex: 0
    property int guideCurrentIndex: 0
    property int guidesCount: 1


    property int toY: 0

    property int arrowThikness: 10
    property int arrowLength: 8
    property int canvasMargins: 20
    property int extraMargin: 2

    property int animationDuration: 300

    id: dialog
    padding: 0

    x: {
        if (position === "right") {
            return -canvas.width - extraMargin }
        else if (position === "top") {
            return (-canvas.width + parent.width ) / 2 }
        else {
            print("Unknown position: " + position)
            return 0 }
    }
    y: {
        if (position === "right") {
            return (-canvas.height + parent.height ) / 2 }
        else if (position === "top") {
            return -canvas.height - extraMargin }
        else {
            print("Unknown position: " + position)
            return 0 }
    }

    visible: Generic.Variables.showGuide &&
             Generic.Variables.toolbarCurrentIndex === toolbarCurrentIndex &&
             Generic.Variables.guideCurrentIndex === guideCurrentIndex ? true : false

    closePolicy: Popup.NoAutoClose
    modal: true
    background: Rectangle { color: "transparent" }
    Overlay.modal: Rectangle { color: Color.transparent("black", 0.1) }

    // Animation on dialog window
    enter: Transition {
        NumberAnimation { property: "opacity"; from: 0.0; to: 1.0 }
    }
    exit: Transition {
        NumberAnimation { property: "opacity"; from: 1.0; to: 0.0 }
    }

    // Custom background
    Canvas {
        id: canvas

        width: {
            if (position === "right") {
                return layout.width + arrowThikness }
            else if (position === "top") {
                return layout.width }
        }
        height: {
            if (position === "right") {
                return layout.height }
            else if (position === "top") {
                return layout.height + arrowLength }
        }

        onPaint:{
            let ctx = canvas.getContext('2d');
            ctx.fillStyle = "coral"//Qt.rgba(0.9, 0.9, 0.9, 1)
            ctx.strokeStyle = "#999"
            ctx.lineWidth = 1.5

            // background
            ctx.beginPath()
            ctx.moveTo(0, 0)
            if (position === "right") {
                ctx.lineTo(0, height)
                ctx.lineTo(width - arrowLength, height)
                ctx.lineTo(width - arrowLength, height/2 + arrowThikness)
                ctx.lineTo(width, height/2 )
                ctx.lineTo(width - arrowLength, height/2 - arrowThikness)
                ctx.lineTo(width - arrowLength, 0) }
            else if (position === "top") {
                ctx.lineTo(0, height - arrowLength)
                ctx.lineTo(width/2 - arrowThikness, height - arrowLength)
                ctx.lineTo(width/2, height)
                ctx.lineTo(width/2 + arrowThikness, height - arrowLength)
                ctx.lineTo(width, height - arrowLength)
                ctx.lineTo(width, 0)

            }
            ctx.fill()
        }

        // Cross (close button)
        Button {
            id: buttonClose
            x: 0
            y: 0
            text: "\u2715"
            background: Rectangle {
                color: "transparent"
            }
            contentItem: Text {
                text: parent.text
                font: parent.font
                opacity: parent.down ? 0.3 : 0.7
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            onPressed: dialog.close()
        }

        // Content
        ColumnLayout {
            id: layout
            spacing: 0

            // Upper circles to show current index
            RowLayout {
                Layout.margins: canvasMargins / 2
                spacing: 5
                Item { Layout.fillWidth: true }
                Repeater {
                    model: guidesCount
                    Text {
                        color: "white"
                        opacity: index === Generic.Variables.guideCurrentIndex ? 0.7 : 0.3
                        font.pointSize: 8
                        text: "\u25CF"
                    }
                }
                Item { Layout.fillWidth: true }
            }

            // Main text
            Text {
                id: messageItem
                Layout.margins: canvasMargins
                horizontalAlignment: Text.AlignHCenter
                color: "white"
            }

            // Additional spacing
            Item { height: canvasMargins }

            // Horisontal line
            GenericAppElements.HorizontalBorder { color: "white"; opacity: 0.3 }

            // Bottom buttons
            RowLayout {
                Layout.margins: canvasMargins / 2
                spacing: 20
                Item { Layout.fillWidth: true }
                Button {
                    id: buttonPrev
                    text: qsTr("Prev")
                    enabled: Generic.Variables.guideCurrentIndex !== 0
                    background: Rectangle {
                        color: "transparent"
                    }
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        opacity: !enabled || parent.down ? 0.3 : 0.7
                        color: "white"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    onClicked: Generic.Variables.guideCurrentIndex -= 1
                }
                Button {
                    id: buttonNext
                    text: qsTr("Next")
                    enabled: Generic.Variables.guideCurrentIndex !== guidesCount - 1
                    background: Rectangle {
                        color: "transparent"
                    }
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        opacity: !enabled || parent.down ? 0.3 : 0.7
                        color: "white"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    onClicked: Generic.Variables.guideCurrentIndex += 1
                }
                Item { Layout.fillWidth: true }
            }
        }
    }
}
