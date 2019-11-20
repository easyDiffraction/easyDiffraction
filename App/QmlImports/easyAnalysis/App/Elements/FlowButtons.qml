import QtQuick 2.12
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons
import easyDiffraction 1.0 as Specific

GenericAppElements.GroupBox {
    property string documentationUrl: "https://easydiffraction.org/umanual_use.html"
    property string contactlUrl: "https://easydiffraction.org/contact.html"

    property alias goPreviousButton: goPreviousButtonContainer.children
    property alias goNextButton: goNextButtonContainer.children

    collapsible: false
    showBorder: false

    content: GenericAppElements.RowLayout {
        Layout.fillWidth: true

        // go previous button
        RowLayout {
            id: goPreviousButtonContainer
            visible: children.length
            spacing: 0
        }

        // go next button
        RowLayout {
            id: goNextButtonContainer
            visible: children.length
            spacing: 0
        }

        // save state button
        GenericAppContentAreaButtons.SaveState {
            onClicked: proxy.updateProjectSave()
            enabled: projectManager.validSaveState
        }

        // help button
        GenericAppContentAreaButtons.Help {
            onClicked: Qt.openUrlExternally(documentationUrl)
        }

        // contact button
        GenericAppContentAreaButtons.Bug {
            onClicked: Qt.openUrlExternally(contactlUrl)
        }

    }

}

