import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Layouts 1.12
import QtCharts 2.3
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyDiffraction 1.0 as Specific

Rectangle {
    id: wrapper

    // Create report onRefinementDone
    Timer {
        interval: 1000
        running: Specific.Variables.refinementDone
        repeat: false
        onTriggered: {
            const html = writeHTML()
            textArea.text = html
            Generic.Constants.proxy.store_report(html)
        }
    }

    // TextArea
    Flickable {
        anchors.fill: parent
        flickableDirection: Flickable.VerticalFlick
        boundsBehavior: Flickable.StopAtBounds
        clip: true

        ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded; minimumSize: 0.1 }

        TextArea.flickable: TextArea {
            id: textArea
            anchors.fill: parent
            padding: 10
            readOnly: true
            antialiasing: true
            smooth: true
            textFormat: Text.RichText
            font.family: Generic.Style.fontFamily
            font.pixelSize: Generic.Style.fontPixelSize
            onVisibleChanged: if (visible) update()
        }
    }

    /////////////
    // Write HTML
    /////////////

    function writeHtmlHead() {
        let s = ''
        s += '<head>'
        s += '<style>'
        s += 'table {'
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
        s += `a:link { color: ${Generic.Style.blueColor}; }`
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
        for (let row_index = 0; row_index < Specific.Variables.fitables.rowCount(); row_index++) {
            const index = Specific.Variables.fitables.index(row_index, 0)
            const label = Specific.Variables.fitables.data(index, Qt.UserRole + 2)
            const refine = Specific.Variables.fitables.data(index, Qt.UserRole + 7)
            const value = refine ? Specific.Variables.fitables.data(index, Qt.UserRole + 3).toFixed(5) + ' ' + Specific.Variables.fitables.data(index, Qt.UserRole + 8): ''
            const error = refine ? Specific.Variables.fitables.data(index, Qt.UserRole + 4).toFixed(5) + ' ' + Specific.Variables.fitables.data(index, Qt.UserRole + 8): ''
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
        s += `<h1>${Specific.Variables.projectName}</h1>`
        s += '<p>'
        s += `<b>Software:</b> <a href="${Specific.Variables.projectDict.app.url}">${Specific.Variables.projectDict.app.name} v${Specific.Variables.projectDict.app.version}</a><br>`
        s += `<b>Calculator:</b> <a href="${Specific.Variables.projectDict.calculator.url}">${Specific.Variables.projectDict.calculator.name} v${Specific.Variables.projectDict.calculator.version}</a><br>`
        s += `<b>Keywords:</b> ${Specific.Variables.projectKeywords}<br>`
        s += `<b>Phase labels:</b> ${Specific.Variables.phaseIds().join(', ')}<br>`
        s += `<b>Experiment labels:</b> ${Specific.Variables.experimentIds().join(', ')}<br>`
        //s += `<b>Instrument:</b> Unknown<br>`
        s += `<b>Modified:</b> ${Specific.Variables.projectModifiedDate}<br>`
        s += `<b>Goodness-of-fit (chi2):</b> ${Generic.Variables.chiSquared} <br>`
        s += '</p>'
        s += '<h2>Parameters</h2>'
        s += '<p>'
        s += writeHtmlTable()
        s += '<br></p>'
        s += '<h2>Fitting</h2>'
        s += '<p>'
        s += `<img src="${Qt.resolvedUrl(Specific.Variables.projectControl.fullFilePath("refinement.png"))}">`
        s += '</p>'
        s += '<h2>Structure</h2>'
        s += '<p>'
        s += `<img src="${Qt.resolvedUrl(Specific.Variables.projectControl.fullFilePath("structure.png"))}">`
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
        return s
    }

    GenericAppElements.GuideWindow {
        message: "A report here includes brief project details,\nlist of fitable parameters, fitting plot and\nstructure view."
        position: "right"
        guideCurrentIndex: 0
        toolbarCurrentIndex: Generic.Variables.SummaryIndex
        guidesCount: Generic.Variables.SummaryGuidesCount
    }
}
