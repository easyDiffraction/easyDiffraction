import QtQuick 2.12
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons
import easyDiffraction 1.0 as Specific

GenericAppElements.GroupBox {
    collapsible: false
    showBorder: false
    content: GenericAppElements.RowLayout {

        GenericAppElements.RowLayout {
            id: container
            Layout.fillWidth: true
            height: helpButton.height
        }

        GenericAppContentAreaButtons.SaveState {
            id: saveStateButton
            onClicked: proxy.updateProjectSave()
            enabled: projectManager.validSaveState
        }
        GenericAppContentAreaButtons.Help {
            id: helpButton
            onClicked: Qt.openUrlExternally(currentUrl)
        }
        GenericAppContentAreaButtons.Bug {
            onClicked: Qt.openUrlExternally("https://easydiffraction.org/contact.html")
        }
    }

     //"__" means private by QML convention
    function __insertContents() {
        // move the contents into the placeholder...
        if (typeof contentsPrevious != "undefined") {
            contentsPrevious.parent = container
            contentsPrevious.Layout.alignment.fill = container
        }
        if (typeof contentsNext != "undefined") {
            contentsNext.parent = container
            contentsNext.Layout.alignment.fill = container
        }
    }

    Component.onCompleted: {
        __insertContents()
    }
}