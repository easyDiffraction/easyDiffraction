import QtQuick 2.12
import Qt.labs.platform 1.0 as QtLabs

import easyAnalysis 1.0 as Generic
import easyDiffraction 1.0 as Specific

QtLabs.MenuBar {

    ////////////
    // File menu
    ////////////

    QtLabs.Menu {
        title: qsTr("&File")

        /*
        QtLabs.MenuItem {
            text: qsTr("&Open")
            onTriggered: messageDialog.show(qsTr("Open action triggered"))
        }
        */

        QtLabs.MenuItem {
            enabled: false // TODO: enable when binded with close dialog if project not changed
            text: qsTr("Exit")
            shortcut: StandardKey.Quit
            onTriggered: Qt.quit()
        }
    }

    ////////////
    // Edit menu
    ////////////

    QtLabs.Menu {
        title: qsTr("&Edit")

        QtLabs.MenuItem {
            enabled: Specific.Variables.canUndo
            text: qsTr("Undo") + " " + Specific.Variables.undoText
            shortcut: StandardKey.Undo
            onTriggered: Specific.Variables.calculatorInterface.undo()
        }
        QtLabs.MenuItem {
            enabled: Specific.Variables.canRedo
            text: qsTr("Redo") + " " + Specific.Variables.redoText
            shortcut: StandardKey.Redo
            onTriggered: Specific.Variables.calculatorInterface.redo()
        }
    }

    ////////////
    // Help menu
    ////////////

    QtLabs.Menu {
        title: qsTr("&Help")

        QtLabs.MenuItem {
            text: qsTr("&About")
            onTriggered: Generic.Variables.showAbout = 1
        }
        QtLabs.MenuItem {
            text: qsTr("Preferences")
            shortcut: StandardKey.Preferences
            onTriggered: Generic.Variables.showPreferences = 1
        }
        QtLabs.MenuItem {
            text: qsTr("Get Started Video Tutorial")
            onTriggered: Qt.openUrlExternally("https://easydiffraction.org/tutorials_start.html")
        }
        QtLabs.MenuItem {
            text: qsTr("Online Documentation")
            onTriggered: Qt.openUrlExternally("https://easydiffraction.org/documentation.html")
        }
        QtLabs.MenuItem {
            text: qsTr("Get in Touch Online")
            onTriggered: Qt.openUrlExternally("https://easydiffraction.org/contact.html")
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
