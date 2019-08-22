pragma Singleton
import QtQuick 2.12

QtObject {

    readonly property string appLeftName: "easy"
    readonly property string appRightName: "Diffraction"
    readonly property string appName: appLeftName + appRightName
    readonly property string appVersion: "0.3.1"
    readonly property string appDate: "21 Aug 2019"
    readonly property string appUrl: "https://github.com/easyDiffraction/QmlGuiPrototype"

}
