import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import QtQuick.Templates 2.12 as T
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic

RowLayout {
    property alias currentIndex: control.currentIndex
    property alias model: control.model

    property bool sizeToContents: true
    property int modelWidth: 0

    id: cellLayout
    anchors.fill: parent
    spacing: 0

    // Vertical border
    Rectangle {
        Layout.fillHeight: true
        width: Generic.Style.appBorderThickness
        ///color: styleData.selected ? Generic.Style.tableHighlightBorderColor : Generic.Style.tableHeaderRowColor
        color: Generic.Style.tableColumnBorderColor
    }

    // Vertical spacer
    Item { width: Generic.Style.tableColumnSpacing/2 }


    // Content
    ComboBox {
        id: control
        leftPadding: 0
        rightPadding: 0
        Layout.fillHeight: true

        indicator: Canvas {
            id: canvas
            x: control.width - width
            y: control.topPadding + (control.availableHeight - height) / 2
            width: 10
            height: 15
            contextType: "2d"

            onPaint: {
                context.reset();

                context.moveTo(0, height / 3)
                context.lineTo(width / 2, 0)
                context.lineTo(width, height / 3)
                context.closePath()

                context.moveTo(0, height * 2 / 3)
                context.lineTo(width / 2, height)
                context.lineTo(width, height * 2 / 3);
                context.closePath();

                context.fillStyle = Generic.Style.buttonIconEnabledColor
                context.fill()
            }
        }

        background: Rectangle {
            implicitWidth: modelWidth + 2*canvas.width
            //implicitHeight: 40
            color: "transparent"
            border.color: control.palette.highlight
            border.width: !control.editable && control.visualFocus ? 2 : 0
            visible: !control.flat || control.down
        }

        TextMetrics {
            id: textMetrics
        }

        Component.onCompleted: {
            textMetrics.font = control.font
            for(var i = 0; i < model.length; i++){
                textMetrics.text = model[i]
                modelWidth = Math.max(textMetrics.width, modelWidth)
                //console.log("modelWidth", modelWidth, model[i])
            }

            contentItem.leftPadding = 0
            popup.width = modelWidth + 30 // ?
        }
    }

    // Vertical spacer
    Item { width: Generic.Style.tableColumnSpacing/2 }


}
