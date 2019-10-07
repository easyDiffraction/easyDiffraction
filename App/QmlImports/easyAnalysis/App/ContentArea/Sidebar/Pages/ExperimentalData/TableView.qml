import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea.Sidebar.Pages.ExperimentalData.TableView 1.0 as GenericSidebarContent
import easyAnalysis.App.ContentArea.Sidebar.Pages.ExperimentalData.PlotView 1.0 as ConstrainedSidebarContent

GenericAppElements.SidebarStack {
    controlsContent: GenericSidebarContent.Controls { anchors.fill: parent }
    settingsContent: GenericSidebarContent.Settings { anchors.fill: parent }
}
