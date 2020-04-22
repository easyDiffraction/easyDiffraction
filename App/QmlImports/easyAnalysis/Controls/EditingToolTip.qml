import QtQuick 2.12
import QtQuick.Controls 2.12

import easyAnalysis.Controls 1.0 as GenericControls

MouseArea {
    enum Type {
        NotYet,
        NoEditingYet,
        OnAnalysisPage,
        Custom
    }
    property int type: EditingToolTip.NotYet
    property string text: ""
    readonly property string _text: {
        if (type === EditingToolTip.NotYet) {
            return qsTr("This functionality has not yet been implemented.")
        } else if (type === EditingToolTip.NoEditingYet) {
                return qsTr("Editing here has not yet been implemented.")
        } else if (type === EditingToolTip.OnAnalysisPage) {
            return qsTr("Editing here has not yet been implemented. To do this, please go to the analysis page.")
        } else if (type === EditingToolTip.Custom && text !== "") {
            return text
        } else {
            show = false
            return ""
        }
    }
    property bool show: true
    property bool _show: false

    anchors.fill: parent
    hoverEnabled: true

    onEntered: _show = true
    onExited: _show = false

    /*
    ToolTip.visible: _show && show
    ToolTip.text: _text
    */

    GenericControls.ToolTip {
        text: _text
        visible: _show && show
    }
}
