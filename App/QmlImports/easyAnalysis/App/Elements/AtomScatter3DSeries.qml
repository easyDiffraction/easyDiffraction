import QtQuick 2.12
import QtDataVisualization 1.3

Scatter3DSeries {
    property real atomSize: 0.5
    property color atomColor: "coral"
    property alias atomModel: dataProxy.itemModel

    itemSize: atomSize
    baseColor: atomColor

    mesh: Abstract3DSeries.MeshSphere

    ItemModelScatterDataProxy {
        id: dataProxy
        xPosRole: "xPos"
        yPosRole: "yPos"
        zPosRole: "zPos"
    }
}

