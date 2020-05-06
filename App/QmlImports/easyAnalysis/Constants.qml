pragma Singleton
import QtQuick 2.12

QtObject {

    // Proxy
    readonly property var proxy: proxyPyQmlObj ? proxyPyQmlObj._proxy : null

}
