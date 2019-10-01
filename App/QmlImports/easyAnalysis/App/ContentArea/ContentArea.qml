import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.ContentArea 1.0 as GenericAppContentArea
import easyAnalysis.App.ContentArea.Pages 1.0 as GenericAppContentAreaPages

StackLayout {
    //width: parent.width
    //Layout.fillWidth: true
    //Layout.fillHeight: true

    currentIndex: Generic.Variables.toolbarCurrentIndex

    GenericAppContentAreaPages.Home {}

    // -------
    //GenericAppContentArea.Spacer {}
    // -------

    GenericAppContentAreaPages.ExperimentalData {}
    //GenericAppContentAreaPages.InstrumentModel {}
    GenericAppContentAreaPages.SampleModel {}

    // -------
    //GenericAppContentArea.Spacer {}
    // -------

    //GenericAppContentAreaPages.Linking {}

    // -------
    //GenericAppContentArea.Spacer {}
    // -------

    GenericAppContentAreaPages.Analysis {}

    // -------
    //GenericAppContentArea.Spacer {}
    // -------

    GenericAppContentAreaPages.Summary {}
}
