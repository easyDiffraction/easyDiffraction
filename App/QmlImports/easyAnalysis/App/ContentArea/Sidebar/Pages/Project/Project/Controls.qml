import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3 as Dialogs1
import Qt.labs.settings 1.1
import Qt.labs.platform 1.1 as QtLabsPlatform

import easyAnalysis 1.0 as Generic
import easyAnalysis.Controls 1.0 as GenericControls
import easyAnalysis.App.Dialog 1.0 as GenericAppDialog
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons

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

                /*
                GenericAppElements.GuideWindow {
                    message: "Create a new project."
                    position: "left"
                    guideCurrentIndex: 2
                    toolbarCurrentIndex: Generic.Variables.ProjectIndex
                    guidesCount: Generic.Variables.ProjectGuidesCount
                }
                */

                GenericAppElements.GuideWindow {
                    message: "Or here to create a new one."
                    position: "bottom"
                    guideCurrentIndex: 1
                    toolbarCurrentIndex: Generic.Variables.ProjectIndex
                    guidesCount: Generic.Variables.ProjectGuidesCount
                }
            }

            GenericAppContentAreaButtons.Open {
                id: openButton
                text: qsTr("Open an existing project")
                enabled: !Specific.Variables.refinementRunning

                onClicked: fileDialogLoadProject.open()

                GenericAppElements.GuideWindow {
                    message: "Click here to open existing project..."
                    position: "left"
                    guideCurrentIndex: 0
                    toolbarCurrentIndex: Generic.Variables.ProjectIndex
                    guidesCount: Generic.Variables.ProjectGuidesCount
                }
            }

            GenericAppContentAreaButtons.Clone {
                //enabled: false
                text: qsTr("Clone an existing project")
                GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
            }

            GenericAppContentAreaButtons.Save {
                id: saveButton
                enabled: false
                text: qsTr("Save project as...")

                onClicked: Generic.Variables.showSaveDialog = 1
                /*
                GenericAppElements.GuideWindow {
                    message: "Click here to save a project."
                    position: "left"
                    guideCurrentIndex: 0
                    toolbarCurrentIndex: Generic.Variables.ProjectIndex
                    guidesCount: Generic.Variables.ProjectGuidesCount
                }
                */

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
                    Specific.Variables.projectControl.loadProject(fileUrl)
                    fileDialogLoadProject.close()
                    if (Specific.Variables.projectControl.validCif) {
                        Generic.Constants.proxy.initialize()
//                        if (Generic.Constants.proxy.validPojectZip) {
//                            saveStateButton.enabled = true
//                        } else {
//                            saveStateButton.enabled = false
//                        }
                        Specific.Variables.projectOpened = true
                        Generic.Variables.projectPageFinished = true
                        Generic.Variables.dataPageFinished = true
                        Generic.Variables.samplePageFinished = true
                        Generic.Variables.analysisPageFinished = true
                        Generic.Variables.summaryPageFinished = Generic.Variables.isDebug ? true : false
                        saveButton.enabled = true
                    }
                    else {
                        failOpenDialog.visible = true
                        Specific.Variables.projectOpened = false
                        Generic.Variables.projectPageFinished = Generic.Variables.isDebug ? true : false
                        Generic.Variables.dataPageFinished = Generic.Variables.isDebug ? true : false
                        Generic.Variables.samplePageFinished = Generic.Variables.isDebug ? true : false
                        Generic.Variables.analysisPageFinished = Generic.Variables.isDebug ? true : false
                        Generic.Variables.summaryPageFinished = Generic.Variables.isDebug ? true : false
                    }
                }
            }

            // Save project dialog
            Dialogs1.FileDialog{
                id: fileDialogSaveProject
                visible: Generic.Variables.showSaveDialog
                selectExisting: false
                nameFilters: ["Project files (*.zip)"]
                folder: settings.value("lastOpenedProjectFolder", examplesDir) //QtLabsPlatform.StandardPaths.writableLocation(QtLabsPlatform.StandardPaths.HomeLocation)
                onAccepted: {
                    Generic.Constants.proxy.saveProjectAs(fileUrl)
                    Generic.Variables.showSaveDialog = 0
                    if (Specific.Variables.projectControl.savedProject === false) {
                        failSaveDialog.visible = true
                    }
                    if (Generic.Variables.closeAppAfterSaving == 1) {
                        Qt.quit()
                    }
                }
            }

            // Create project dialog
            Dialogs1.FileDialog{
                id: fileDialogCreateProject
                selectExisting: false
                nameFilters: ["Project files (*.zip)"]
                folder: settings.value("lastOpenedProjectFolder", examplesDir) //QtLabsPlatform.StandardPaths.writableLocation(QtLabsPlatform.StandardPaths.HomeLocation)
                onAccepted: {
                    fileDialogCreateProject.close()
                    Generic.Constants.proxy.createProject(fileUrl)
                    titleInput.text = Specific.Variables.projectControl.projectFileNameWithoutExt() + '\n'
                    projectInfoDialog.visible = true
                    Generic.Variables.projectPageFinished = true
                    Generic.Variables.dataPageFinished = Generic.Variables.isDebug ? true : false
                    Generic.Variables.samplePageFinished = Generic.Variables.isDebug ? true : false
                    Generic.Variables.analysisPageFinished = Generic.Variables.isDebug ? true : false
                    Generic.Variables.summaryPageFinished = Generic.Variables.isDebug ? true : false
                }
            }

            // Fail open dialog
            GenericControls.Dialog {
                id: failOpenDialog
                title: "Warning"
                Column {
                    padding: 20
                    spacing: 15
                    Text {
                        text: "File was not a valid main 'cif' file."
                    }
                }
            }

            // Fail save dialog
            GenericControls.Dialog {
                id: failSaveDialog
                title: "Error"
                Column {
                    padding: 20
                    spacing: 15
                    Text {
                        text: "The project file was not saved."
                    }
                }
            }

            // Project description dialog
            GenericControls.Dialog {
                id: projectInfoDialog
                title: "Project Description"

                Column {
                    id: projectInfoDialogContent
                    padding: 20
                    spacing: 30

                    Grid {
                        columns: 2
                        rowSpacing: 10
                        columnSpacing: 15

                        Text {
                            text: "Project Title:"
                        }
                        TextInput {
                            id: titleInput
                            focus: true
                            cursorVisible: true
                            selectByMouse: true
                            color: Generic.Style.buttonBkgHighlightedColor
                            selectedTextColor: "white"
                            selectionColor: Generic.Style.tableHighlightRowColor
                        }
                        Text {
                            text: "Keywords:"
                        }
                        TextInput {
                            id: keywordsInput
                            selectByMouse: true
                            color: Generic.Style.buttonBkgHighlightedColor
                            selectedTextColor: "white"
                            selectionColor: Generic.Style.tableHighlightRowColor
                            text: "neutron powder diffraction, 1d"
                        }
                    }

                    GenericAppDialog.Button {
                        anchors.horizontalCenter: projectInfoDialogContent.horizontalCenter
                        text: "OK"
                        onClicked: {
                            Specific.Variables.projectControl.writeMain(titleInput.text, keywordsInput.text)
                            Generic.Constants.proxy.initialize()
                            Generic.Constants.proxy.createProjectZip()
                            Specific.Variables.projectOpened = true
                            projectInfoDialog.close()
                        }
                    }

                }
            }
        }
    }

    // Groupbox

    GenericAppElements.GroupBox {
        title: "Recent Projects"
        //enabled: false
        content: GenericAppElements.ColumnLayout {
            spacing: 0

            GenericAppElements.ParametersTable {
                Layout.fillWidth: true
                model: ListModel {
                    ListElement { number:"1"; name:"Fe3O4";           path:"~/Exp/LLB/2019-03/";  cdate:"11.03.2019" }
                    ListElement { number:"2"; name:"PbSO4";           path:"~/Exp/ILL/2010-02/";  cdate:"02.02.2010" }
                    ListElement { number:"3"; name:"Fitting_test";    path:"~/Exp/ESS/2020-11/";  cdate:"15.11.2020" }
                    ListElement { number:"4"; name:"SiO_test";        path:"~/Exp/MLZ/2018-07/";  cdate:"23.07.2018" }
                }
                Controls1.TableViewColumn { title:"No.";            role:"number";  resizable: false }
                Controls1.TableViewColumn { title:"Name";           role:"name" }
                Controls1.TableViewColumn { title:"Path";           role:"path" }
                Controls1.TableViewColumn { title:"Creation date";  role:"cdate";   resizable: false }
                Controls1.TableViewColumn { role:"remove";          title:"Remove"; resizable: false }
                GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
            }
        }

        GenericAppElements.GuideWindow {
            message: "The sidebar groups can be folded and unfolded.\n\nClick on the group name to unfold the group."
            position: "left"
            guideCurrentIndex: 3
            toolbarCurrentIndex: Generic.Variables.ProjectIndex
            guidesCount: Generic.Variables.ProjectGuidesCount
        }
    }


    // Groupbox

    GenericAppElements.GroupBox {
        title: "Examples"
        //enabled: false
        content: GenericAppElements.ColumnLayout {
            spacing: 0

            GenericAppElements.ParametersTable {
                Layout.fillWidth: true
                model: ListModel {
                    ListElement { number:"1"; name:"Fe3O4";    keywords:"polarised neutron powder diffraction, 1d, LLB" }
                    ListElement { number:"2"; name:"PbSO4";    keywords:"unpolarised neutron powder diffraction, 1d, ILL" }
                }
                Controls1.TableViewColumn { title:"No.";                role:"number";  resizable: false }
                Controls1.TableViewColumn { title:"Name";               role:"name" }
                Controls1.TableViewColumn { title:"Keywords";           role:"keywords" }
                GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet }
            }
        }
    }


    // Groupbox

    /*
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
            guideCurrentIndex: 3
            toolbarCurrentIndex: Generic.Variables.ProjectIndex
            guidesCount: Generic.Variables.ProjectGuidesCount
        }
    }
    */

    // Spacer

    Item { Layout.fillHeight: true }

    // Groupbox

    GenericAppElements.FlowButtons {
        documentationUrl: "https://easydiffraction.org/umanual_use.html#3.2.2.-project"
        goNextButton: GenericAppContentAreaButtons.GoNext {
            text: "Sample"
            enabled: Specific.Variables.projectOpened
            ToolTip.text: qsTr("Go to the next step: Sample")
            onClicked: {
                Generic.Variables.toolbarCurrentIndex = Generic.Variables.SampleIndex
            }
            GenericAppElements.GuideWindow {
                message: "Click here to go to the next page: Sample."
                position: "top"
                guideCurrentIndex: 4
                toolbarCurrentIndex: Generic.Variables.ProjectIndex
                guidesCount: Generic.Variables.ProjectGuidesCount
            }
        }
    }

}

