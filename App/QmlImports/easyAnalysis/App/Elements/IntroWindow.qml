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

    property int toY: 0
    property int arrowWidth: 10
    property int arrowHeight: 20
    property int canvasMargins: 20

    property int animationDuration: 300

    id: dialog

    //visible: true
    modal: true
    padding: 0

    // Redefine background below
    background: Rectangle {
        color: "transparent"
    }

    // Not faded area
    Overlay.modal: Rectangle {
        id: fadeOut
        property real transparency: 0
        color: Color.transparent("black", transparency)
        // Animation
        NumberAnimation on transparency { from: 0; to: 0.5; duration: animationDuration }
    }

    // Animation
    NumberAnimation on opacity { from: 0; to: 1; duration: animationDuration }

    // Custom background
    Canvas {
        id: canvas

        width: layout.width + arrowWidth
        height: layout.height

        x: -(width + canvasMargins/2)
        y: toY - height/2

        onPaint:{
            let ctx = canvas.getContext('2d');
            ctx.fillStyle = Qt.rgba(0.9, 0.9, 0.9, 1)
            ctx.strokeStyle = "#999"
            ctx.lineWidth = 1.5

            // background
            ctx.beginPath()
            ctx.moveTo(0, 0)
            ctx.lineTo(0, height)
            ctx.lineTo(width - arrowWidth, height)
            ctx.lineTo(width - arrowWidth, height/2 + arrowHeight/2)
            ctx.lineTo(width, height/2 )
            ctx.lineTo(width - arrowWidth, height/2 - arrowHeight/2)
            ctx.lineTo(width - arrowWidth, 0)
            ctx.fill()

            // cross
            ctx.beginPath()
            ctx.moveTo(10, 10)
            ctx.lineTo(20, 20)
            ctx.moveTo(20, 10)
            ctx.lineTo(10, 20)
            ctx.stroke()


        }

        ColumnLayout {
            id: layout
            spacing: 0

            // Upper circles
            RowLayout {
                Layout.margins: canvasMargins/2
                spacing: 5
                Item { Layout.fillWidth: true }
                Text { color: "#888"; font.pointSize: 8; text: "\u25CF" }
                Text { color: "#bfbfbf"; font.pointSize: 8; text: "\u25CF" }
                Text { color: "#bfbfbf"; font.pointSize: 8; text: "\u25CF" }
                Text { color: "#bfbfbf"; font.pointSize: 8; text: "\u25CF" }
                Item { Layout.fillWidth: true }
            }

            // Main text
            Text {
                id: messageItem
                Layout.margins: canvasMargins
            }

            // Additional spacing
            Item { height: canvasMargins }

            // Horisontal line
            GenericAppElements.HorizontalBorder { color: "#ccc" }

            // Bottom buttons
            RowLayout {
                Layout.margins: canvasMargins/2
                spacing: 20
                Item { Layout.fillWidth: true }
                Text { color: "#999"; text: qsTr("Prev") }
                Text { color: "#666"; text: qsTr("Next") }
                Item { Layout.fillWidth: true }
            }
        }
    }
}

