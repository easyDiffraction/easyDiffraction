import QtQuick 2.12
import QtDataVisualization 1.3

Scatter3DSeries {
    property real atomSize: 0.5
    property color atomColor: "#ff7f49" //"coral"
    property alias atomModel: itemModel
    //property var atomPositionList: [{"x":8.7, "y":8.7, "z":8.7}, {"x":8.7*0.5, "y":8.7*0.5, "z":8.7*0.5}, {"x":0, "y":0, "z":0}]

    itemSize: atomSize
    baseColor: atomColor

    mesh: Abstract3DSeries.MeshSphere

    ItemModelScatterDataProxy {
        //id: itemModelScatterDataProxy
        itemModel: ListModel { id: itemModel }

        xPosRole: "x"
        yPosRole: "y"
        zPosRole: "z"
    }

    /*
    Component.onCompleted: {
        for (const atom of atomPositionList) {
            itemModel.append(atom)
        }
    }
    */
}

