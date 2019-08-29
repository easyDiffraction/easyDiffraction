pragma Singleton
import QtQuick 2.12

QtObject {

    readonly property string appLeftName: "easy"
    readonly property string appRightName: "Diffraction"
    readonly property string appName: appLeftName + appRightName
    readonly property string appVersion: "0.3.2"
    readonly property string appDate: "29 Aug 2019"
    readonly property string appUrl: "https://easydiffraction.github.io"

}
