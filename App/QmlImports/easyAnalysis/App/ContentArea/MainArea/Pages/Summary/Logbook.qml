import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Layouts 1.12
import QtCharts 2.3
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyDiffraction 1.0 as Specific

Rectangle {
    property int commonMargin: 10

    id: wrapper

    //anchors.fill: parent
    Layout.fillWidth: true

    function writeHtmlHead() {
        let s = ''
        s += '<head>'
        s += '<style>'
        s += 'table {'
        s += 'font-family: arial, sans-serif;'
        s += 'border-collapse: collapse;'
        s += '}'
        s += 'td, th {'
        s += 'border: 1px solid #ddd;'
        s += 'padding: 2px;'
        s += 'padding-left: 12px;'
        s += 'padding-right: 12px;'
        s += '}'
        s += 'tr:nth-child(even) {'
        s += 'background-color: #eee;'
        s += '}'
        s += '</style>'
        s += '</head>'
        return s
    }

    function writeHtmlTable() {
        let s = ''
        s += '<table>'
        s += '<tr>'
        s += '<th align="right">No.</th>'
        s += '<th align="left">Parameter</th>'
        s += '<th align="right">Value</th>'
        s += '<th align="right">Error</th>'
        s += '<th align="right">Fit</th>'
        s += '</tr>'
        for (let row_index = 0; row_index < proxy.fitables.rowCount(); row_index++) {
            const index = proxy.fitables.index(row_index, 0)
            const label = proxy.fitables.data(index, Qt.UserRole + 2)
            const refine = proxy.fitables.data(index, Qt.UserRole + 7)
            const value = proxy.fitables.data(index, Qt.UserRole + 3).toFixed(5)
            const error = refine ? proxy.fitables.data(index, Qt.UserRole + 4).toFixed(5) : ''
            const fit = refine ? '+' : ''
            s += '<tr>'
            s += '<td align="right">' + (row_index + 1) + '</td>'
            s += '<td align="left">' + label + '</td>'
            s += '<td align="right">' + value + '</td>'
            s += '<td align="right">' + error + '</td>'
            s += '<td align="right">' + fit + '</td>'
            s += '</tr>'
        }
        s += '</table>'
        return s
    }

    function writeHtmlBody() {
        let s = ''
        s += '<body>'
        s += '<h1>' + proxy.project.info.name + '</h1>'
        s += '<p>'
        s += '<b>Creation date: </b>11.04.2019<br>'
        s += '<b>Keywords: </b>' + proxy.project.info.keywords.join(', ') + '<br>'
        s += '<b>Instrument: </b>6T2 at LLB<br>'
        s += '</p>'
        s += '<h2>Parameters</h2>'
        s += '<p>'
        s += writeHtmlTable()
        s += '</p>'
        s += '<p>'
        s += '<p></p>'
        s += '<b>Chi2: </b>' + Generic.Variables.chiSquared + '<br>'
        s += '</p>'
        //s += '<h2>&nbsp;</h2>'
        s += '<h2>Fitting</h2>'
        s += '<p>'
        s += '<img src="' + proxy.project_dir_absolute_path + '/saved_refinement.png" width="' + Math.round(wrapper.width * 0.8) + '" >'
        s += '</p>'
        //s += '<h2>&nbsp;</h2>'
        s += '<h2>Structure</h2>'
        s += '<p>'
        s += '<img src="' + proxy.project_dir_absolute_path + '/saved_structure.png" width="' + Math.round(wrapper.width * 0.8) + '" >'
        s += '</p>'
        s += '</body>'
        return s
    }

    function writeHTML() {
        let s = ''
        s += '<!DOCTYPE html>'
        s += '<html>'
        s += writeHtmlHead()
        s += writeHtmlBody()
        s += '</html>'
        proxy.store_report(s)
        return proxy.get_report_html()
    }

    Flickable {
        id: flickable
        anchors.fill: parent
        flickableDirection: Flickable.VerticalFlick
        boundsBehavior: Flickable.StopAtBounds

        ScrollBar.vertical: ScrollBar {}

        TextArea.flickable: TextArea {
            visible: true
            Layout.fillWidth: true
            padding: commonMargin
            topPadding: 3*commonMargin
            bottomPadding: 0
            readOnly: true
            antialiasing: true
            textFormat: Text.RichText
            text: Specific.Variables.projectOpened ? writeHTML() : ""
        }
    }
}
