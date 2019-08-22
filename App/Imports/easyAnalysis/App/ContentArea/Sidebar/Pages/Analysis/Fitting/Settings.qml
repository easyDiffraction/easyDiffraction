import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis.App.Elements 1.0 as GenericAppElements

ColumnLayout {
    spacing: 0

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "View settings"
        content: GenericAppElements.GridLayout {
            columns: 2
            GenericAppElements.CheckBox { checked:true;  text:qsTr("Show experimental data") }
            GenericAppElements.CheckBox { checked:true;  text:qsTr("Show difference plot") }
            GenericAppElements.CheckBox { checked:false; text:qsTr("Show Bragg positions") }
            GenericAppElements.CheckBox { checked:false; text:qsTr("Show legend") }
            //GenericAppElements.CheckBox { Layout.fillWidth:true; checked:true;  text:qsTr("Display coordinate system") }
        }
    }

    ///////////
    // Groupbox
    ///////////
    GenericAppElements.GroupBox {
        title: "Minimizer"
        content: GenericAppElements.GridLayout {
            columns: 2
            columnSpacing: 20
            // Row
            Text { text: qsTr("Type") }
            GenericAppElements.ComboBox {
                model: ["Minuit2", "GSL Levenberg-Marquat", "TMVA Genetic"]
                Layout.fillWidth: true
            }
            // Row
            Text { text: qsTr("Algorithm") }
            GenericAppElements.ComboBox {
                model: ["Migrad", "Simplex", "Combined", "Scan"]
                Layout.fillWidth: true
            }
            // Row
            Text { text: qsTr("Tolerance") }
            TextField { Layout.fillWidth: true; implicitHeight: 32; text: "0.01"}
        }
    }



    /////////
    // Spacer
    /////////
    Item { Layout.fillHeight: true }

}
