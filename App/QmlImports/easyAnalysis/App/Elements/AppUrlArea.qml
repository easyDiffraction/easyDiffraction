import QtQuick 2.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic

MouseArea {
    cursorShape: Qt.PointingHandCursor
    onClicked: { Qt.openUrlExternally(Generic.Style.appUrl) }
}
