import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3 as Dialogs1
import Qt.labs.settings 1.1
import Qt.labs.platform 1.1 as QtLabsPlatform
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons
import easyAnalysis.Logic 1.0 as GenericLogic
import easyDiffraction 1.0 as Specific

ColumnLayout {
    spacing: 0

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Get Started"
        collapsible: false
        content: GenericAppElements.GridLayout {
            columns: 2

            // Buttons
            GenericAppContentAreaButtons.Create {
                enabled: true
                text: qsTr("Create a new project")

                onClicked: fileDialogCreateProject.open()

                GenericAppElements.GuideWindow {
                    message: "Create a new project."
                    position: "left"
                    guideCurrentIndex: 2
                    toolbarCurrentIndex: Generic.Variables.HomeIndex
                    guidesCount: Generic.Variables.HomeGuidesCount
                }
            }

            GenericAppContentAreaButtons.Open {
                id: openButton
                text: qsTr("Open another project")
                enabled: !proxy.refinementRunning

                onClicked: fileDialogLoadProject.open()

                GenericAppElements.GuideWindow {
                    message: "Click here to open existing project."
                    position: "left"
                    guideCurrentIndex: 0
                    toolbarCurrentIndex: Generic.Variables.HomeIndex
                    guidesCount: Generic.Variables.HomeGuidesCount
                }
            }

            GenericAppContentAreaButtons.Clone {
                enabled: false
                text: qsTr("Clone an existing project")
            }

            GenericAppContentAreaButtons.Save {
                id: saveButton
                enabled: false
                text: qsTr("Save project as...")

                onClicked: fileDialogSaveProject.open()

                GenericAppElements.GuideWindow {
                    message: "Click here to save a project."
                    position: "left"
                    guideCurrentIndex: 0
                    toolbarCurrentIndex: Generic.Variables.HomeIndex
                    guidesCount: Generic.Variables.HomeGuidesCount
                }

            }

            // Persistent settings
            Settings { id: settings }
            //settings.setValue("appWindowWidth", window.width)

            // Open project dialog
            Dialogs1.FileDialog{
                id: fileDialogLoadProject
                nameFilters: [ "CIF files (*.cif)", "Project files (*.zip)"]
                folder: settings.value("lastOpenedProjectFolder", examplesDir) //QtLabsPlatform.StandardPaths.writableLocation(QtLabsPlatform.StandardPaths.HomeLocation)
                onAccepted: {
                    settings.setValue("lastOpenedProjectFolder", folder)
                    projectControl.loadProject(fileUrl)
                    fileDialogLoadProject.close()
                    if (proxy.validCif == true) {
                        proxy.initialize()
//                        if (proxy.validPojectZip) {
//                            saveStateButton.enabled = true
//                        } else {
//                            saveStateButton.enabled = false
//                        }
                        Specific.Variables.projectOpened = true
                        Generic.Variables.homePageFinished = Generic.Variables.isDebug ? true : false
                        Generic.Variables.dataPageFinished = Generic.Variables.isDebug ? true : false
                        Generic.Variables.samplePageFinished = Generic.Variables.isDebug ? true : false
                        Generic.Variables.analysisPageFinished = Generic.Variables.isDebug ? true : false
                        Generic.Variables.summaryPageFinished = Generic.Variables.isDebug ? true : false
                        saveButton.enabled = true
                    } else {
                        failOpenDialog.visible = true
                        Specific.Variables.projectOpened = false
                        Generic.Variables.homePageFinished = Generic.Variables.isDebug ? true : false
                        Generic.Variables.dataPageFinished = Generic.Variables.isDebug ? true : false
                        Generic.Variables.samplePageFinished = Generic.Variables.isDebug ? true : false
                        Generic.Variables.analysisPageFinished = Generic.Variables.isDebug ? true : false
                        Generic.Variables.summaryPageFinished = Generic.Variables.isDebug ? true : false
                    }
                }
            }

            Dialogs1.FileDialog{
                id: fileDialogSaveProject
                selectExisting: false
                nameFilters: ["Project files (*.zip)"]
                folder: settings.value("lastOpenedProjectFolder", examplesDir) //QtLabsPlatform.StandardPaths.writableLocation(QtLabsPlatform.StandardPaths.HomeLocation)
                onAccepted: {
                    proxy.saveProject(fileUrl)
                    fileDialogSaveProject.close()
                    if (proxy.savedProject == false) {
                        failSaveDialog.visible = true
                    } else {
                        saveStateButton.enabled = true
                    }
                }
            }

            Dialogs1.FileDialog{
                id: fileDialogCreateProject
                selectExisting: false
                nameFilters: ["Project files (*.zip)"]
                folder: settings.value("lastOpenedProjectFolder", examplesDir) //QtLabsPlatform.StandardPaths.writableLocation(QtLabsPlatform.StandardPaths.HomeLocation)
                onAccepted: {
                    fileDialogCreateProject.close()
                    projectControl.createProject(fileUrl)
                    getProjectInfoDialog.visible = true
                }
            }

            Dialog {
                id: failOpenDialog
                parent: Overlay.overlay
                anchors.centerIn: parent
                modal: true
                opacity: 0.9
                visible: false
                Label {
                    id: infoLabel
                    anchors.centerIn: parent
                    text: 'Warning: File was not a valid main `cif` file.'
                    color: "black"
                    font.family: Generic.Style.introThinFontFamily
                    font.pointSize: Generic.Style.systemFontPointSize + 1
                }
            }

             Dialog {
                id: failSaveDialog
                parent: Overlay.overlay
                anchors.centerIn: parent
                modal: true
                opacity: 0.9
                visible: false
                Label {
                    id: infoLabel2
                    anchors.centerIn: parent
                    text: 'Error: The project file was not saved.'
                    color: "black"
                    font.family: Generic.Style.introThinFontFamily
                    font.pointSize: Generic.Style.systemFontPointSize + 1
                }
            }

            Dialog {
                id: getProjectInfoDialog
                visible: false
                parent: Overlay.overlay
                anchors.centerIn: parent
                modal: true
                title: "Project description"
                GenericAppElements.ColumnLayout {
                    GenericAppElements.RowLayout {
                        Label {
                            text: "Project Title:"
                        }
                        TextInput {
                            id: titleInput
                            text: "Undefined"
                            cursorVisible: true
                        }
                    }
                    GenericAppElements.RowLayout {
                        Label {
                            text: "Project keywords:"
                        }
                        TextInput {
                            id: keywordsInput
                            text: "\'neutron diffraction, powder, 1d\'"
                            cursorVisible: true
                        }
                    }
                }
                standardButtons: Dialog.Ok
                onAccepted: {
                    projectControl.writeMain(titleInput.text, keywordsInput.text)
                    proxy.initialize()
                    saveStateButton.enabled = true
                    Specific.Variables.projectOpened = true
                    saveButton.enabled = true
                }
            }

        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Recent Projects"
        enabled: false
        content: GenericAppElements.ColumnLayout {
            spacing: 0

            GenericAppElements.ParametersTable {
                Layout.fillWidth: true
                model: ListModel {
                    ListElement { number:"1"; name:"SiO_experiment";  path:"~/Exp/ESS/2019-03/";  cdate:"11.04.2019" }
                    ListElement { number:"2"; name:"Simulation_test"; path:"~/Exp/ESS/2019-02/";  cdate:"02.04.2019" }
                    ListElement { number:"3"; name:"Fitting_test";    path:"~/Exp/ESS/2018-11/";  cdate:"15.03.2019" }
                    ListElement { number:"4"; name:"Neutron_custom";  path:"~/Exp/ILL/2018-10/";  cdate:"08.03.2019" }
                    ListElement { number:"5"; name:"SiO_test";        path:"~/Exp/ESS/2018-07/";  cdate:"07.02.2019" }
                    ListElement { number:"6"; name:"First_test";      path:"~/Exp/ESS/2018-07/";  cdate:"03.02.2019" }
                    ListElement { number:"7"; name:"X-ray_custom";    path:"~/Exp/ESRF/2016-03/"; cdate:"01.02.2019" }
                }
                Controls1.TableViewColumn { title:"No.";            role:"number";  resizable: false }
                Controls1.TableViewColumn { title:"Name";           role:"name" }
                Controls1.TableViewColumn { title:"Path";           role:"path" }
                Controls1.TableViewColumn { title:"Creation date";  role:"cdate";   resizable: false }
                Controls1.TableViewColumn { role:"remove";          title:"Remove"; resizable: false }
            }
        }

        GenericAppElements.GuideWindow {
            message: "The sidebar groups can be folded and unfolded.\n\nClick on the group name to unfold the group.\n\nDisabled groups are not implemented yet."
            position: "left"
            guideCurrentIndex: 3
            toolbarCurrentIndex: Generic.Variables.HomeIndex
            guidesCount: Generic.Variables.HomeGuidesCount
        }
    }


    // Groupbox

    GenericAppElements.GroupBox {
        title: "Examples"
        enabled: false
        content: GenericAppElements.ColumnLayout {
            spacing: 0

            GenericAppElements.ParametersTable {
                Layout.fillWidth: true
                model: ListModel {
                    ListElement { number:"1"; name:"SiO_experiment";    description:"Neutron powder diffraction" }
                    ListElement { number:"2"; name:"Simulation_test";   description:"Neutron powder diffraction" }
                    ListElement { number:"3"; name:"Fitting_test";      description:"Neutron powder diffraction" }
                    ListElement { number:"4"; name:"Neutron_custom";    description:"Neutron powder diffraction" }
                    ListElement { number:"5"; name:"SiO_test";          description:"Neutron powder diffraction" }
                }
                Controls1.TableViewColumn { title:"No.";                role:"number";  resizable: false }
                Controls1.TableViewColumn { title:"Name";               role:"name" }
                Controls1.TableViewColumn { title:"Short description";  role:"description" }
            }
        }
    }


    // Groupbox

    GenericAppElements.GroupBox {
        title: "Program Preferences"
        content: GenericAppElements.ColumnLayout {

            GenericAppElements.CheckBox {
                text: qsTr("Show Animated Intro")
                checked: Generic.Variables.showIntro
                onCheckedChanged: Generic.Variables.showIntro = checked
            }

            GenericAppElements.CheckBox {
                text: qsTr("Show User Guides")
                checked: Generic.Variables.showGuide
                onCheckStateChanged: Generic.Variables.showGuide = checked
            }
        }
        GenericAppElements.GuideWindow {
            message: "Application user guides and animated intro\ncan be disabled or enabled here."
            position: "left"
            guideCurrentIndex: 4
            toolbarCurrentIndex: Generic.Variables.HomeIndex
            guidesCount: Generic.Variables.HomeGuidesCount
        }
    }

    // Spacer

    Item { Layout.fillHeight: true }

    // Groupbox

    GenericAppElements.FlowButtons {
        property url currentUrl: "https://easydiffraction.org/umanual_use.html#3.2.2.-project"
        property Item contentsNext: GenericAppContentAreaButtons.GoNext {
            text: "Experimental Data"
            ToolTip.text: qsTr("Go to the next step: Experimental data")
            enabled: Specific.Variables.projectOpened
            highlighted: Specific.Variables.projectOpened
            onClicked: {
                Generic.Variables.homePageFinished = true
                Generic.Variables.toolbarCurrentIndex = Generic.Variables.ExperimentalDataIndex
            }
            GenericAppElements.GuideWindow {
                message: "Click here to go to the next step: Experimental data."
                position: "top"
                guideCurrentIndex: 5
                toolbarCurrentIndex: Generic.Variables.HomeIndex
                guidesCount: Generic.Variables.HomeGuidesCount
            }
        }
    }
}

