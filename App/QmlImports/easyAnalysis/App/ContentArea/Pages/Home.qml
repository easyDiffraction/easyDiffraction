import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea.MainArea 1.0 as GenericMainArea
import easyAnalysis.App.ContentArea.MainArea.Pages.Home 1.0 as GenericMainAreaSampleModel
import easyAnalysis.App.ContentArea.Sidebar.Pages.Home 1.0 as GenericSidebarSampleModel

GenericAppElements.ContentAreaStack {

    mainAreaContent: StackLayout {
        GenericMainAreaSampleModel.Project { }
    }

    sideBarContent: StackLayout {
        GenericSidebarSampleModel.Project { }
    }

}
