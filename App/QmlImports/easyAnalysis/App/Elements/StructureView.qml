import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtDataVisualization 1.3 // versions above 1.3 are not recognized by PySide2 (Qt for Python)
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements

Rectangle {
    property bool showInfo: true
    property real xRotationInitial: -50.0
    property real yRotationInitial:  3.0
    property real zoomLevelInitial: 100.0
    property real xTargetInitial: 0.0
    property real yTargetInitial: 0.0
    property real zTargetInitial: 0.0
    property int animationDuration: 1000

    color: "coral"
    clip: true


    ////////////////////////
    // Check if data changed
    ////////////////////////

    Text {
        visible: false
        text: proxy.timeStamp
        onTextChanged: {
            //print("--------------------------------------------------------- Time stamp: ", text)


            /*

            // Create dictionary b_scattering:color
            const bscatList = Array.from(new Set(proxy.atom_site_bscat_list()))
            let bscatColorDict = {}
            for (let i = 0; i < bscatList.length; i++ ) {
                bscatColorDict[bscatList[i]] = Generic.Style.atomColorList[i]
            }

            // Unit cell parameters
            const a = parseFloat(proxy.cell_length_a())
            const b = parseFloat(proxy.cell_length_b())
            const c = parseFloat(proxy.cell_length_c())

            // Remove old atom scatters
            for (let i = 0, len = chart.seriesList.length; i < len; i++) {
                chart.removeSeries(chart.seriesList[1])
            }

            // Populate chart with atoms. Every atom is an individual scatter serie
            for (let i = 0, len = proxy.tmp_no_symmetry_atom_site_fract_x_list().length; i < len; i++ ) {
                var component = Qt.createComponent(Generic.Variables.qmlElementsPath + "AtomScatter3DSeries.qml");
                if (component.status === Component.Ready) {
                    var series = component.createObject()
                    if (series === null) {
                        console.log("Error creating object")
                    } else {
                        series.atomSize = Math.abs(proxy.tmp_no_symmetry_atom_site_bscat_list()[i]) * 0.4
                        series.atomColor = bscatColorDict[proxy.tmp_no_symmetry_atom_site_bscat_list()[i]]
                        series.atomModel.append({
                            x: parseFloat(proxy.tmp_no_symmetry_atom_site_fract_x_list()[i]) * a,
                            y: parseFloat(proxy.tmp_no_symmetry_atom_site_fract_y_list()[i]) * b,
                            z: parseFloat(proxy.tmp_no_symmetry_atom_site_fract_z_list()[i]) * c
                        })
                    }
                    chart.addSeries(series)
                }
            }

            */
        }
    }

    ///////
    // Plot
    ///////

    Scatter3D {
        id: chart
        anchors.fill: parent
        anchors.topMargin: -60
        anchors.leftMargin: -250
        anchors.rightMargin: -250
        clip: true

        // Camera view settings
        orthoProjection: false
        //scene.activeCamera.cameraPreset: Camera3D.CameraPresetIsometricLeftHigh
        scene.activeCamera.xRotation: xRotationInitial
        scene.activeCamera.yRotation: yRotationInitial
        scene.activeCamera.zoomLevel: zoomLevelInitial
        scene.activeCamera.target.x: xTargetInitial
        scene.activeCamera.target.y: yTargetInitial
        scene.activeCamera.target.z: zTargetInitial

        // Geometrical settings
        //horizontalAspectRatio: 0.0
        aspectRatio: 1.0

        // Interactivity
        selectionMode: AbstractGraph3D.SelectionNone // Left mouse button will be used for "reset view" coded below

        // Visualization settings
        theme: Theme3D {
            type: Theme3D.ThemeUserDefined
            ambientLightStrength: 0.5
            lightStrength: 5.0
            windowColor: "white"
            backgroundEnabled: false
            labelBackgroundEnabled: false
            labelBorderEnabled: false
            labelTextColor: "grey"
            gridEnabled: false
            font.pointSize: 60
            font.family: Generic.Style.fontFamily
        }
        shadowQuality: AbstractGraph3D.ShadowQualityNone // AbstractGraph3D.ShadowQualitySoftHigh

        // X axis
        axisX: ValueAxis3D {
            labelFormat: ""
        }

        // Y axis
        axisY: ValueAxis3D {
            labelFormat: ""
        }

        // Z axis
        axisZ: ValueAxis3D {
            labelFormat: ""
        }

        //GenericAppElements.AtomScatter3DSeries {
        //    atomModel: proxy.cellBox
        //}

        // Unit cell chart settings
        Scatter3DSeries {
            mesh: Abstract3DSeries.MeshSphere
            itemSize: 0.03
            baseColor: "grey"
            colorStyle: Theme3D.ColorStyleUniform

            ItemModelScatterDataProxy {
                itemModel: proxy.cellBox
                xPosRole: "xPos"
                yPosRole: "yPos"
                zPosRole: "zPos"
            }
        }
    }

    ///////////
    // Helpers
    ///////////

    // Reset view with animation: Override default left mouse button
    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton
        onClicked: animo.restart()
    }
    ParallelAnimation {
        id: animo
        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.target.x"; to: xTargetInitial; duration: animationDuration }
        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.target.y"; to: yTargetInitial; duration: animationDuration }
        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.target.z"; to: zTargetInitial; duration: animationDuration }
        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.xRotation"; to: xRotationInitial; duration: animationDuration }
        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.yRotation"; to: yRotationInitial; duration: animationDuration }
        NumberAnimation { easing.type: Easing.OutCubic; target: chart; property: "scene.activeCamera.zoomLevel"; to: zoomLevelInitial; duration: animationDuration }
    }

    // Info area
    Label {
        visible: showInfo
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: font.pointSize
        leftPadding: font.pointSize * lineHeight * 0.5
        rightPadding: font.pointSize * lineHeight * 0.5
        lineHeight: 1.5
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        text: qsTr("Rotate: Drag with right mouse button pressed") + "  •  " + qsTr("Zoom in/out: Mouse wheel") + "  •  " + qsTr("Reset: Left mouse button")
        font.family: Generic.Style.introThinFontFamily
        font.pointSize: Generic.Style.systemFontPointSize + 1
        color: "grey"
        background: Rectangle { color: "white"; opacity: 0.9; border.width: 0; radius: Generic.Style.toolbarButtonRadius }
    }



}
