import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

CheckBox {
    padding: 0

    // trick to make all the checkboxes equal size in the grid layout...
    Layout.fillWidth: true
    Layout.preferredWidth: 1
}
