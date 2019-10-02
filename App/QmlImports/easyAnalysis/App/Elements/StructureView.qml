import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtDataVisualization 1.3 // versions above 1.3 are not recognized by PySide2 (Qt for Python)
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyDiffraction 1.0 as Specific

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
        text: Generic.Variables.projectOpened ? Specific.Variables.project.info.last_modified_date : ""
        onTextChanged: {
            //print("--------------------------------------------------------- Time stamp: ", text)
            if (Generic.Variables.projectOpened) {
                // Create dictionary b_scattering:color
                const bscatList = Array.from(new Set(Specific.Variables.project.phases[Specific.Variables.project.info.phase_ids[0]].atom_site_list.scat_length_neutron))

                let bscatColorDict = {}
                for (let i = 0; i < bscatList.length; i++ ) {
                    bscatColorDict[bscatList[i]] = Generic.Style.atomColorList[i]
                }

                // Unit cell parameters
                const a = Specific.Variables.project.phases[Specific.Variables.project.info.phase_ids[0]].cell.length_a.value
                const b = Specific.Variables.project.phases[Specific.Variables.project.info.phase_ids[0]].cell.length_b.value
                const c = Specific.Variables.project.phases[Specific.Variables.project.info.phase_ids[0]].cell.length_c.value

                // Remove old atom scatters, but unit cell box (number 1)
                for (let i = 1, len = chart.seriesList.length; i < len; i++) {
                    chart.removeSeries(chart.seriesList[1])
                }

                // Populate chart with atoms. Every atom is an individual scatter serie
                for (let i = 0, len = Specific.Variables.project.phases[Specific.Variables.project.info.phase_ids[0]].atom_site_list.fract_x.length; i < len; i++ ) {
                    var component = Qt.createComponent(Generic.Variables.qmlElementsPath + "AtomScatter3DSeries.qml");
                    if (component.status === Component.Ready) {
                        var series = component.createObject()
                        if (series === null) {
                            console.log("Error creating object")
                        } else {
                            series.atomSize = Math.abs(Specific.Variables.project.phases[Specific.Variables.project.info.phase_ids[0]].atom_site_list.scat_length_neutron[i]) * 0.4
                            series.atomColor = bscatColorDict[Specific.Variables.project.phases[Specific.Variables.project.info.phase_ids[0]].atom_site_list.scat_length_neutron[i]]
                            series.atomModel.append({
                                x: Specific.Variables.project.phases[Specific.Variables.project.info.phase_ids[0]].atom_site_list.fract_x[i] * a,
                                y: Specific.Variables.project.phases[Specific.Variables.project.info.phase_ids[0]].atom_site_list.fract_y[i] * b,
                                z: Specific.Variables.project.phases[Specific.Variables.project.info.phase_ids[0]].atom_site_list.fract_z[i] * c
                            })
                        }
                        chart.addSeries(series)
                    }
                }

            }
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
