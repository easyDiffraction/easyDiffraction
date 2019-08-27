import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyAnalysis.App.ContentArea.Buttons 1.0 as GenericAppContentAreaButtons
import easyAnalysis.Logic 1.0 as GenericLogic

ColumnLayout {
    spacing: 0

    ////////////////////////
    // Check if data changed
    ////////////////////////

    Text {
        id: dataChanged
        visible: false
        text: proxy.time_stamp
        onTextChanged: {
            print("Time stamp: ", proxy.time_stamp)

            // Create dictionary b_scattering:color
            const bscatList = Array.from(new Set(proxy.atom_site_bscat_list()))
            let bscatColorDict = {}
            for (let i = 0; i < bscatList.length; i++ ) {
                bscatColorDict[bscatList[i]] = Generic.Style.atomColorList[i]
            }

            // Update Parameters

            // singony, spaceGroup, setting
            singonyComboBox.model = [proxy.tmp_singony()]
            spaceGroupComboBox.model = [proxy.tmp_spgr_number() + ".  " + proxy.tmp_spgr_name()]
            settingComboBox.model = [proxy.tmp_spgr_choice()]

            // structuralPhasesModel
            structuralPhasesModel.clear()
            structuralPhasesModel.append({
                'num':1,
                'name':proxy.tmp_phase_name(),
                'note':proxy.tmp_phase_comment()
            })

            // latticeParametersModel
            latticeParametersModel.clear()
            latticeParametersModel.append({
                'a':proxy.cell_length_a(),
                'b':proxy.cell_length_b(),
                'c':proxy.cell_length_c(),
                'alpha':proxy.cell_angle_alpha(),
                'beta':proxy.cell_angle_beta(),
                'gamma':proxy.cell_angle_gamma()
            })

            // atomsModel
            atomsModel.clear()
            for (let i = 0; i < proxy.atom_site_label_list().length; i++ ) {
                atomsModel.append({
                    'num':i+1,
                    'label':proxy.atom_site_label_list()[i],
                    'atom':proxy.atom_site_type_symbol_list()[i],
                    'color':bscatColorDict[proxy.atom_site_bscat_list()[i]],
                    'x':proxy.atom_site_fract_x_list()[i],
                    'y':proxy.atom_site_fract_y_list()[i],
                    'z':proxy.atom_site_fract_z_list()[i],
                    'occ':proxy.atom_site_occupancy_list()[i]
                })
            }

            // adpModel
            adpModel.clear()
            for (let i = 0; i < proxy.atom_site_label_list().length; i++ ) {
                const type = proxy.atom_site_adp_type_list()[i]
                adpModel.append({
                    'num':i+1,
                    'label':proxy.atom_site_label_list()[i],
                    'type':type,
                    'uiso':proxy.atom_site_b_iso_or_equiv_list()[i],
                    'u11':type === "uani" ? proxy.atom_site_aniso_U_11_list()[i] : "",
                    'u22':type === "uani" ? proxy.atom_site_aniso_U_22_list()[i] : "",
                    'u33':type === "uani" ? proxy.atom_site_aniso_U_33_list()[i] : "",
                    'u12':type === "uani" ? proxy.atom_site_aniso_U_12_list()[i] : "",
                    'u13':type === "uani" ? proxy.atom_site_aniso_U_13_list()[i] : "",
                    'u23':type === "uani" ? proxy.atom_site_aniso_U_23_list()[i] : "",
                })
            }

            // chiModel
            chiModel.clear()
            for (let i = 0; i < proxy.atom_site_label_list().length; i++ ) {
                const chi_type = proxy.atom_site_flag_m_list()[i] ? proxy.atom_site_chi_type_list()[i] : "none"
                chiModel.append({
                    'num':i+1,
                    'label':proxy.atom_site_label_list()[i],
                    'type':chi_type,
                    'chiiso':"",
                    'chi11':chi_type === "cani" ? proxy.atom_site_cani_chi_11_list()[i] : "",
                    'chi22':chi_type === "cani" ? proxy.atom_site_cani_chi_22_list()[i] : "",
                    'chi33':chi_type === "cani" ? proxy.atom_site_cani_chi_33_list()[i] : "",
                    'chi12':chi_type === "cani" ? proxy.atom_site_cani_chi_12_list()[i] : "",
                    'chi13':chi_type === "cani" ? proxy.atom_site_cani_chi_13_list()[i] : "",
                    'chi23':chi_type === "cani" ? proxy.atom_site_cani_chi_23_list()[i] : "",
                })
            }
        }
    }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Structural phases"
        collapsible: false
        content: GenericAppElements.ColumnLayout {
            // Table
            GenericAppElements.ParametersTable {
                selectable: false
                enabled: false

                model: ListModel {
                    id: structuralPhasesModel
                    ListElement { num:0; name:""; note:"" }
                }

                Controls1.TableViewColumn { role:"num";     title:"No.";    resizable: false }
                Controls1.TableViewColumn { role:"name";    title:"Name ";   resizable: false }
                Controls1.TableViewColumn { role:"note";    title:"Note" }
                Controls1.TableViewColumn { role:"remove";  title:"Remove"; resizable: false }
            }

            // Buttons
            GenericAppElements.GridLayout {
                columns: 2

                GenericAppContentAreaButtons.Add { id: addButton; enabled: false; text: "Add new phase manually"; }
                GenericAppContentAreaButtons.RemoveAll { enabled: false; text: "Remove all phases" }
                GenericAppContentAreaButtons.Import { id: importButton; enabled: false; text: "Import new phase from CIF" }
                GenericAppContentAreaButtons.Export { enabled: false; text: "Export selected phase to CIF" }

                GenericAppElements.GuideWindow {
                    id: guidWindow
                    message: "Click here to add or import a new proxy."
                    toY: (addButton.y + addButton.height + importButton.y) / 2

                    visible: Generic.Variables.showGuide && Generic.Variables.toolbarCurrentIndex === Generic.Variables.SampleModelIndex ? true : false

                    GenericAppContentAreaButtons.Add { id: addButtonClone }
                    GenericAppContentAreaButtons.Import { id: importButtonClone }
                    Component.onCompleted: {
                        GenericLogic.Copy.copyButton(addButton, addButtonClone)
                        GenericLogic.Copy.copyButton(importButton, importButtonClone)
                    }
                }
            }
        }
    }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        id: group1
        title: "Symmetry and cell parameters"
        collapsed: true
        content: GenericAppElements.ColumnLayout {
            GenericAppElements.GridLayout {
                columns: 3
                rowSpacing: 2
                enabled: false

                Text { text: "Crystal system"; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }
                Text { text: "Space Group    "; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }
                Text { text: "Setting             "; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }

                GenericAppElements.ComboBox { id: singonyComboBox }
                GenericAppElements.ComboBox { id: spaceGroupComboBox }
                GenericAppElements.ComboBox { id: settingComboBox }
            }

            GenericAppElements.GridLayout {
                columns: 1
                rowSpacing: 2
                Text { text: "Cell parameters"; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }

                GenericAppElements.ParametersTable {
                    enabled: false

                    model: ListModel {
                        id: latticeParametersModel
                        ListElement { a:""; b:""; c:""; alpha:""; beta:""; gamma:"" }
                    }

                    Controls1.TableViewColumn { role:"a";       title:"a (\u212B)" }
                    Controls1.TableViewColumn { role:"b";       title:"b (\u212B)" }
                    Controls1.TableViewColumn { role:"c";       title:"c (\u212B)" }
                    Controls1.TableViewColumn { role:"alpha";   title:"alpha (°)" }
                    Controls1.TableViewColumn { role:"beta";    title:"beta (°)" }
                    Controls1.TableViewColumn { role:"gamma";   title:"gamma (°)" }
                }
            }
        }
    }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Atoms, atomic coordinates and occupations"
        collapsed: false
        content: GenericAppElements.ColumnLayout {
            GenericAppElements.ParametersTable {
                enabled: false

                model: ListModel {
                    id: atomsModel
                    ListElement { num:0; label:""; atom:""; color:""; x:""; y:""; z:""; occ:"" }
                }

                Controls1.TableViewColumn { role:"num";     title:"No.";    resizable: false }
                Controls1.TableViewColumn { role:"label";   title:"Label";  resizable: false }
                Controls1.TableViewColumn { role:"atom";    title:"Atom";   resizable: false }
                Controls1.TableViewColumn { role:"color";   title:"Color";  resizable: false }
                Controls1.TableViewColumn { role:"x";       title:"x" }
                Controls1.TableViewColumn { role:"y";       title:"y" }
                Controls1.TableViewColumn { role:"z";       title:"z" }
                Controls1.TableViewColumn { role:"occ";     title:"Occ" }
                Controls1.TableViewColumn { role:"remove";  title:"Remove"; resizable: false }
            }

            // Buttons
            GenericAppElements.GridLayout {
                columns: 2
                GenericAppContentAreaButtons.Add { enabled: false; text: "Add new atom"; }
                GenericAppContentAreaButtons.RemoveAll { enabled: false; text: "Remove all atoms" }
            }
        }
    }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Atomic displacement parameters (\u200A\u00D7\u200A10\u2075\u200A)"
        collapsed: true
        content: GenericAppElements.ColumnLayout {
            GenericAppElements.ParametersTable {
                enabled: false

                model: ListModel {
                    id: adpModel
                    ListElement { num:0; label:""; type:""; uiso:""; u11:""; u22:""; u33:""; u12:""; u13:""; u23:"" }
                }

                Controls1.TableViewColumn { role:"num";     title:"No.";    resizable: false }
                Controls1.TableViewColumn { role:"label";   title:"Label";  resizable: false }
                Controls1.TableViewColumn { role:"type";    title:"Type";   resizable: false }
                Controls1.TableViewColumn { role:"uiso";    title:"Uiso" }
                Controls1.TableViewColumn { role:"u11";     title:"U11" }
                Controls1.TableViewColumn { role:"u22";     title:"U22" }
                Controls1.TableViewColumn { role:"u33";     title:"U33" }
                Controls1.TableViewColumn { role:"u12";     title:"U12" }
                Controls1.TableViewColumn { role:"u13";     title:"U13" }
                Controls1.TableViewColumn { role:"u23";     title:"U23" }
            }
        }
    }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Magnetic susceptibility parameters"
        collapsed: true
        content: GenericAppElements.ColumnLayout {
            GenericAppElements.ParametersTable {
                enabled: false

                model: ListModel {
                    id: chiModel
                    ListElement { num:0; label:""; type:""; chiiso:""; chi11:""; chi22:""; chi33:""; chi12:""; chi13:""; chi23:"" }
                }

                Controls1.TableViewColumn { role:"num";     title:"No.";    resizable: false }
                Controls1.TableViewColumn { role:"label";   title:"Label";  resizable: false }
                Controls1.TableViewColumn { role:"type";    title:"Type";   resizable: false }
                Controls1.TableViewColumn { role:"chiiso";  title:"\u03C7iso" }
                Controls1.TableViewColumn { role:"chi11";   title:"\u03C711" }
                Controls1.TableViewColumn { role:"chi22";   title:"\u03C722" }
                Controls1.TableViewColumn { role:"chi33";   title:"\u03C733" }
                Controls1.TableViewColumn { role:"chi12";   title:"\u03C712" }
                Controls1.TableViewColumn { role:"chi13";   title:"\u03C713" }
                Controls1.TableViewColumn { role:"chi23";   title:"\u03C723" }
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
            GenericAppContentAreaButtons.GoPrevious {
                text: "Experimental Data"
                ToolTip.text: qsTr("Go to the previous step: Experimental data")
                onClicked: {
                    Generic.Variables.toolbarCurrentIndex = Generic.Variables.ExperimentalDataIndex
                }
            }
            GenericAppContentAreaButtons.GoNext {
                text: "Analysis"
                ToolTip.text: qsTr("Go to the next step: Analysis")
                onClicked: {
                    Generic.Variables.samplePageFinished = true
                    Generic.Variables.toolbarCurrentIndex = Generic.Variables.AnalysisIndex
                }
            }

            GenericAppContentAreaButtons.SaveState {
            }
            GenericAppContentAreaButtons.Help {
                onClicked: Qt.openUrlExternally("https://easydiffraction.github.io/documentation_use.html#3.2.3.-sample-model")
            }
            GenericAppContentAreaButtons.Bug {
                onClicked: Qt.openUrlExternally("https://easydiffraction.github.io/contact.html")
            }
        }
    }

}

