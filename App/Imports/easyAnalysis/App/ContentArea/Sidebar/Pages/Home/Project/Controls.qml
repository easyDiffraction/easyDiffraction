import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3
import Qt.labs.settings 1.1
import Qt.labs.platform 1.1 as QtLabsPlatform
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons
import easyAnalysis.Logic 1.0 as GenericLogic

ColumnLayout {
    spacing: 0

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Get Started"
        collapsible: false
        content: GenericAppElements.GridLayout {
            columns: 2

            // Buttons
            GenericAppContentAreaButtons.Create { id: createButton; enabled: false; text: qsTr("Create a new project") }
            GenericAppContentAreaButtons.Open { text: qsTr("Open another project"); onClicked: fileDialog.open() }
            GenericAppContentAreaButtons.Clone { id: cloneButton; enabled: false; text: qsTr("Clone an existing project") }
            GenericAppContentAreaButtons.Save { enabled: false; text: qsTr("Save project as...") }

            // Persistent settings
            Settings { id: settings }
            //settings.setValue("appWindowWidth", window.width)

            // Open project dialog
            FileDialog{
                id: fileDialog
                nameFilters: [ "RhoChi files (*.rcif)" ]
                folder: settings.value("lastOpenedProjectFolder", QtLabsPlatform.StandardPaths.writableLocation(QtLabsPlatform.StandardPaths.HomeLocation))
                onAccepted: {
                    settings.setValue("lastOpenedProjectFolder", folder)
                    //print("-----------fileUrl------------", fileUrl.toString().replace("file://",""))
                    proxy.load_rhochi_model_and_update_proxy(fileUrl.toString().replace("file://",""))
                    Generic.Variables.modelLoaded = true
                    Generic.Variables.homePageFinished = false
                    Generic.Variables.dataPageFinished = false
                    Generic.Variables.samplePageFinished = false
                    Generic.Variables.analysisPageFinished = false
                    Generic.Variables.summaryPageFinished = false
                    fileDialog.close()
                }
            }

            // Guide window
            GenericAppElements.GuideWindow {
                id: guidWindow
                message: "Click here to create a new project or clone an existing one."
                toY: (createButton.y + createButton.height + cloneButton.y) / 2

                visible: Generic.Variables.showGuide && Generic.Variables.toolbarCurrentIndex === Generic.Variables.HomeIndex ? true : false

                GenericAppContentAreaButtons.Import { id: createButtonClone }
                GenericAppContentAreaButtons.Cloud { id: cloneButtonClone }
                Component.onCompleted: {
                    GenericLogic.Copy.copyButton(createButton, createButtonClone)
                    GenericLogic.Copy.copyButton(cloneButton, cloneButtonClone)
                }
            }
        }
    }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Recent Projects"
        collapsed: true
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
    }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Examples"
        collapsed: true
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

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Program Preferences"
        collapsed: false
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
    }

    /////////
    // Spacer
    /////////
    Item { Layout.fillHeight: true }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        collapsible: false
        showBorder: false
        content: GenericAppElements.RowLayout {
            GenericAppContentAreaButtons.GoNext {
                text: "Experimental Data"
                ToolTip.text: qsTr("Go to the next step: Experimental data")
                enabled: Generic.Variables.modelLoaded
                highlighted: Generic.Variables.modelLoaded

                onClicked: {
                    Generic.Variables.homePageFinished = true
                    Generic.Variables.toolbarCurrentIndex = Generic.Variables.ExperimentalDataIndex
                }
            }
            GenericAppContentAreaButtons.SaveState {}
            GenericAppContentAreaButtons.Help {}
            GenericAppContentAreaButtons.Bug {}
        }
    }

}

