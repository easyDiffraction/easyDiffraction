pragma Singleton
import QtQuick 2.12

QtObject {

    // Application
    readonly property string appLeftName: "easy"
    readonly property string appRightName: "Diffraction"
    readonly property string appName: appLeftName + appRightName
    readonly property string appVersion: proxyPyQmlObj ? proxyPyQmlObj._releaseInfo.version : ""
    readonly property string appDate: proxyPyQmlObj ? proxyPyQmlObj._releaseInfo.date : ""
    readonly property string appUrl: "https://easydiffraction.org"
    readonly property string essUrl: "https://ess.eu"
    readonly property string oslUrl: "https://raw.githubusercontent.com/easyDiffraction/easyDiffraction/master/externalLicences.md"
    readonly property string eulaUrl: "https://raw.githubusercontent.com/easyDiffraction/easyDiffraction/master/LICENSE"
    readonly property string appIconPath: qmlImportsDir + "/easyDiffraction/Resources/Icons/App.svg"
    readonly property string essIconPath: qmlImportsDir + "/easyDiffraction/Resources/Icons/ESSlogo.png"
}
