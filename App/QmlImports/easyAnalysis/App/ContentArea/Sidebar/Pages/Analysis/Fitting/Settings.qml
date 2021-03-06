import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import easyAnalysis 1.0 as Generic
import easyAnalysis.Controls 1.0 as GenericControls

import easyAnalysis.App.Elements 1.0 as GenericAppElements

ColumnLayout {
    spacing: 0

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "View settings"
        //enabled: false
        //collapsed: false
        content: GenericAppElements.GridLayout {
            columns: 2

            GenericAppElements.CheckBox {
                checked: Generic.Variables.showLegend
                text: qsTr("Show legend")
                onToggled: {
                    if (Generic.Variables.showLegend !== checked) {
                        Generic.Variables.showLegend = checked
                    }
                }
            }
            GenericAppElements.CheckBox {
                checked: Generic.Variables.showRefinemetResults
                text:qsTr("Show refinement results")
                onToggled: {
                    if (Generic.Variables.showRefinemetResults !== checked) {
                        Generic.Variables.showRefinemetResults = checked
                    }
                }
            }

            GenericAppElements.CheckBox { checked:true;  text:qsTr("Show experimental data"); GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet } }
            GenericAppElements.CheckBox { checked:true;  text:qsTr("Show difference plot"); GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet } }
            GenericAppElements.CheckBox { checked:true;  text:qsTr("Show background plot"); GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet } }
            GenericAppElements.CheckBox { checked:true;  text:qsTr("Show Bragg positions"); GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NotYet } }

            //GenericAppElements.CheckBox { Layout.fillWidth:true; checked:true;  text:qsTr("Display coordinate system") }
        }
    }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Calculator"
        //enabled: false
        content: GenericAppElements.GridLayout {
            columns: 2
            columnSpacing: 20
            // Row
            Text {
                font.pixelSize: Generic.Style.fontPixelSize
                font.family: Generic.Style.fontFamily
                text: qsTr("Library")
            }
            GenericAppElements.ComboBox {
                model: ["Cryspy"]
                Layout.fillWidth: true
                GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NoEditingYet }
            }
        }
    }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Minimizer"
        //enabled: false
        content: GenericAppElements.GridLayout {
            columns: 2
            columnSpacing: 20
            // Row
            Text {
                font.pixelSize: Generic.Style.fontPixelSize
                font.family: Generic.Style.fontFamily
                text: qsTr("Library")
            }
            GenericAppElements.ComboBox {
                model: ["Scipy"]
                Layout.fillWidth: true
                GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NoEditingYet }
            }
            // Row
            Text {
                font.pixelSize: Generic.Style.fontPixelSize
                font.family: Generic.Style.fontFamily
                text: qsTr("Type")
            }
            GenericAppElements.ComboBox {
                model: ["Local optimization"]
                Layout.fillWidth: true
                GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NoEditingYet }
            }
            // Row
            Text {
                font.pixelSize: Generic.Style.fontPixelSize
                font.family: Generic.Style.fontFamily
                text: qsTr("Method")
            }
            GenericAppElements.ComboBox {
                model: ["Broyden–Fletcher–Goldfarb–Shanno (BFGS)"]
                Layout.fillWidth: true
                GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NoEditingYet }
            }
            // Row
            Text {
                font.pixelSize: Generic.Style.fontPixelSize
                font.family: Generic.Style.fontFamily
                text: qsTr("Max. iterations")
            }
            TextField { Layout.fillWidth: true; implicitHeight: 32; text: "100"; GenericControls.EditingToolTip { type: GenericControls.EditingToolTip.NoEditingYet }}
        }
    }



    /////////
    // Spacer
    /////////
    Item { Layout.fillHeight: true }

}
