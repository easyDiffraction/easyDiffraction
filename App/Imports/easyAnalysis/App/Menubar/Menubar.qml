import QtQuick 2.12
import Qt.labs.platform 1.0 as QtLabs
import easyAnalysis 1.0 as Generic

QtLabs.MenuBar {

    ////////////
    // File menu
    ////////////

    QtLabs.Menu {
        title: qsTr("&File")

        QtLabs.MenuItem {
            text: qsTr("&Open")
            onTriggered: messageDialog.show(qsTr("Open action triggered"))
        }

        QtLabs.MenuItem {
            text: qsTr("E&xit")
            onTriggered: Qt.quit()
        }
    }

    ////////////
    // Help menu
    ////////////

    QtLabs.Menu {
        title: qsTr("&Help")

        QtLabs.MenuItem {
            text: qsTr("&Help")
            onTriggered: messageDialog.show(qsTr("Open action triggered"))
        }

        QtLabs.MenuItem {
            text: qsTr("Show Application Intro")
            checkable: true
            checked: Generic.Variables.showIntro
            onTriggered: {
                Generic.Variables.showIntro = checked
                //if (checked) {
                    //dialog.close()
                    // reset!
                    //dialog.open()
                    //animo.restart()
                    //if (Generic.Variables.toolbarCurrentIndex !== Generic.Variables.HomeIndex) {
                    //    Generic.Variables.toolbarCurrentIndex = Generic.Variables.HomeIndex
                    //}
                //}
            }
        }

        QtLabs.MenuItem {
            text: qsTr("&Show User Guides")
            checkable: true
            checked: Generic.Variables.showGuide
            onTriggered: Generic.Variables.showGuide = checked
        }

        QtLabs.MenuItem {
            text: qsTr("&About")
            //onTriggered: Qt.quit()
        }
    }
}

/*
Action {
    id: copyAction
    text: qsTr("&Copy")
    icon.name: "edit-copy"
    shortcut: StandardKey.Copy
    onTriggered: window.activeFocusItem.copy()
}

MenuItem {
    id: menuItem
    action: copyAction
    text: qsTr("&Copy selected Text")
}

MenuBar {
    id: menuBar

    Menu {
        id: fileMenu
        title: qsTr("File")
        // ...
    }

    Menu {
        id: editMenu
        title: qsTr("&Edit")
        // ...
    }

    Menu {
        id: viewMenu
        title: qsTr("&View")
        // ...
    }

    Menu {
        id: helpMenu
        title: qsTr("&Help")
        // ...
    }
}
*/
