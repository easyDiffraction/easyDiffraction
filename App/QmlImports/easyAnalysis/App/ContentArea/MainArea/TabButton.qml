import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.impl 2.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea

GenericAppContentArea.TabButton {
    property int tabbarWidth: Generic.Variables.mainAreaWidth
    width: tabbarWidth / 4 - 1

    // Vertical border on the left
    Rectangle {
        width: parent.checked ? 0 : 1
        height: parent.height
        color: Generic.Style.mainAreaTabBorderColor
    }
}

