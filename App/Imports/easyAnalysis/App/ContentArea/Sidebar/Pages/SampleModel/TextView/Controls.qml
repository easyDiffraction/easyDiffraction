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

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Structural phases"
        collapsible: false
        content: GenericAppElements.ColumnLayout {
            // Table
            GenericAppElements.ParametersTable {
                id: textview
                selectable: true
                model: ListModel {
                    ListElement { num:"1"; name:"CeCuAl3"; note:"RT #13744 ThCr2Si2 type" }
                    ListElement { num:"2"; name:"Al";      note:"Impurity" }
                }
                Controls1.TableViewColumn { role:"num";     title:"No.";    resizable: false }
                Controls1.TableViewColumn { role:"name";    title:"Name";   resizable: false }
                Controls1.TableViewColumn { role:"note";    title:"Note" }
                Controls1.TableViewColumn { title:"Remove"; resizable: false; delegate: GenericAppContentAreaButtons.Remove {} }
            }

            // Buttons
            GenericAppElements.GridLayout {
                columns: 2

                GenericAppContentAreaButtons.Add { id: addButton; text: "Add new phase manually"; }
                GenericAppContentAreaButtons.RemoveAll { text: "Remove all phases" }
                GenericAppContentAreaButtons.Import { id: importButton; text: "Import new phase from CIF" }
                GenericAppContentAreaButtons.Export { text: "Export selected phase to CIF" }
            }
        }
    }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Symmetry and unit cell parameters"
        collapsed: true
        content: GenericAppElements.ColumnLayout {
            GenericAppElements.GridLayout {
                columns: 3
                rowSpacing: 2
                Text { text: "System"; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }
                Text { text: "Space Group"; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }
                Text { text: "Setting"; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }
                GenericAppElements.ComboBox { currentIndex: 3; model: ["Triclinic", "Monoclinic", "Orthorhombic", "Tetragonal", "Trigonal", "Hexagonal", "Cubic"] }
                GenericAppElements.ComboBox { currentIndex: 3; model: ["104.   P 4 n c", "105.   P 42 m c", "106.   P 42 b c", "107.   I 4 m m", "108.   I 4 c m", "109.   I 41 m d", "110.   I 41 c d"] }
                GenericAppElements.ComboBox { currentIndex: 0; model: ["1.   I 4 m m"] }
            }
            GenericAppElements.GridLayout {
                columns: 1
                rowSpacing: 2
                Text { text: "Lattice parameters"; color: Generic.Style.sidebarLabelColor; font.pointSize: Generic.Style.fontPointSize - 1 }
                GenericAppElements.ParametersTable {
                    model: ListModel {
                        ListElement { a:"4.256782"; b:"4.256782"; c:"10.633879"; alpha:"90.0"; beta:"90.0"; gamma:"90.0" }
                    }
                    Controls1.TableViewColumn { role:"a";       title:"a (\u212B)" }
                    Controls1.TableViewColumn { role:"b";       title:"b (\u212B)" }
                    Controls1.TableViewColumn { role:"c";       title:"c (\u212B)"  }
                    Controls1.TableViewColumn { role:"alpha";   title:"alpha (°)"  }
                    Controls1.TableViewColumn { role:"beta";    title:"beta (°)"  }
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
        collapsed: true
        content: GenericAppElements.ColumnLayout {
            GenericAppElements.ParametersTable {
                model: ListModel {
                    ListElement { num:"1"; label:"Ce1"; atom:"Ce"; color:"#408002"; x:"0.00000"; y:"0.00000"; z:"0.00000"; occ:"1.00000" }
                    ListElement { num:"2"; label:"Cu1"; atom:"Cu"; color:"#0F80FF"; x:"0.00000"; y:"0.00000"; z:"0.63224"; occ:"0.92491" }
                    ListElement { num:"3"; label:"Al1"; atom:"Al"; color:"#FC6666"; x:"0.00000"; y:"0.00000"; z:"0.63224"; occ:"0.07509" }
                    ListElement { num:"4"; label:"Cu2"; atom:"Cu"; color:"#0F80FF"; x:"0.00000"; y:"0.00000"; z:"0.40437"; occ:"0.04446" }
                    ListElement { num:"5"; label:"Al2"; atom:"Al"; color:"#FC6666"; x:"0.00000"; y:"0.00000"; z:"0.40437"; occ:"0.95553" }
                    ListElement { num:"6"; label:"Al3"; atom:"Al"; color:"#FC6666"; x:"0.00000"; y:"0.50000"; z:"0.24981"; occ:"1.00000" }
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
                model: ListModel {
                    ListElement { num:"1"; label:"Ce1"; type:1; uiso:"";    u11:"570"; u22:"570"; u33:"620"; u12:"-10"; u13:"20";  u23:"130" }
                    ListElement { num:"2"; label:"Cu1"; type:0; uiso:"830"; u11:"";    u22:"";    u33:"";    u12:"";    u13:"";    u23:""    }
                    ListElement { num:"3"; label:"Al1"; type:0; uiso:"830"; u11:"";    u22:"";    u33:"";    u12:"";    u13:"";    u23:""    }
                    ListElement { num:"4"; label:"Cu2"; type:1; uiso:"";    u11:"570"; u22:"570"; u33:"620"; u12:"-10"; u13:"20";  u23:"130" }
                    ListElement { num:"5"; label:"Al2"; type:1; uiso:"";    u11:"570"; u22:"570"; u33:"620"; u12:"-10"; u13:"20";  u23:"130" }
                    ListElement { num:"6"; label:"Al3"; type:1; uiso:"";    u11:"570"; u22:"570"; u33:"620"; u12:"-10"; u13:"20";  u23:"130" }
                }
                Controls1.TableViewColumn { role:"num";     title:"No.";    resizable: false }
                Controls1.TableViewColumn { role:"label";   title:"Label";  resizable: false }
                Controls1.TableViewColumn { role:"type";    title:"Type";   resizable: false; delegate: GenericAppElements.CellComboBox { currentIndex: styleData.value; model: ["iso", "aniso"] } }
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
        title: "Magnetic structure"
        collapsed: true
        content: GenericAppElements.ColumnLayout {
            Text { text: "To be added" }
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
                text: "Next step: Linking table"
                ToolTip.text: qsTr("Go to the next step: Linking table")
                onClicked: {
                    Generic.Variables.samplePageFinished = true
                    Generic.Variables.toolbarCurrentIndex = Generic.Variables.LinkingIndex
                }
            }
            GenericAppContentAreaButtons.SaveState {}
            GenericAppContentAreaButtons.Help {}
            GenericAppContentAreaButtons.Bug {}
        }
    }

}

