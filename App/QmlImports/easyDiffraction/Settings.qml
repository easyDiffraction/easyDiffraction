pragma Singleton
import QtQuick 2.12

QtObject {

    // Application
    readonly property string appLeftName: "easy"
    readonly property string appRightName: "Diffraction"
    readonly property string appName: appLeftName + appRightName
    readonly property string appVersion: "0.3.6"
    readonly property string appDate: "23 Oct 2019"
    readonly property string appUrl: "https://easydiffraction.github.io"
    readonly property string appIconPath: qmlImportsDir + "/easyDiffraction/Resources/Icons/App.svg"

}
