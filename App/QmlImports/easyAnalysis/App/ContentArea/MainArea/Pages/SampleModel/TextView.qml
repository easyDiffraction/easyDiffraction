import QtQuick 2.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyDiffraction 1.0 as Specific

//https://forum.qt.io/topic/90101/textarea-does-not-automatically-scroll/5

Rectangle {
    color: "white"
    property bool showContent: false

    ListView {
        width: parent.width
        height: parent.height
        boundsBehavior: Flickable.StopAtBounds
        model: Specific.Variables.cif
        ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }
        clip: true
        delegate: Text {
                anchors.fill: parent
                leftPadding: font.pixelSize
                rightPadding: leftPadding
                horizontalAlignment: Text.AlignLeft
                text: showContent ? model.phasesRole : ""

        }
    }
}


