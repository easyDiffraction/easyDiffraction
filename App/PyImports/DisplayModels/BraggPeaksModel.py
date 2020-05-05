from easyInterface import logger

from PySide2.QtCore import Qt, QPointF, Slot
from PySide2.QtCharts import QtCharts

from PyImports.DisplayModels.BaseModel import BaseModel


class BraggPeaksModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._seriesRef = None
        self._log = self._log = logger.getLogger(self.__class__.__module__)

    def _setModelsFromProjectDict(self):
        """
        Create the model needed for GUI measured data table and chart.
        """
        self._log.info("Starting to set Model from Project Dict")

        for calc_dict in self._project_dict['calculations'].values():
            for phase_id in self._project_dict['phases'].keys():
                column_count = len(calc_dict['bragg_peaks'][phase_id].items()) - 1  # Because of name
                row_count = len(list(calc_dict['bragg_peaks'][phase_id].items())[1][1])  # We know name should be at [0]

                self._model.blockSignals(True)

                self._model.clear()
                self._model.setColumnCount(column_count)
                self._model.setRowCount(row_count)

                # Add all the columns from calc_dict['bragg_peaks'][phase_id] to self._model
                column_index = 0
                for data_id, data_list in calc_dict['bragg_peaks'][phase_id].items():
                    if data_id == 'name':
                        continue
                    for row_index, value in enumerate(data_list):
                        index = self._model.index(row_index, column_index)
                        self._model.setData(index, value, Qt.DisplayRole)
                    column_index += 1
                self._model.blockSignals(False)
                self._headers_model.blockSignals(False)

                # Emit signal which is caught by the QStandardItemModel-based
                # QML GUI elements in order to update their views
                self._model.layoutChanged.emit()

                # Update chart series here, as this method is significantly
                # faster, compared to the updating at the QML GUI side via the
                # QStandardItemModel
                self._updateQmlChartViewSeries()

        self._log.info("Finished setting Model from Project Dict")

    def _updateQmlChartViewSeries(self):
        """
        Updates QML LineSeries of ChartView.
        """
        self._log.info("Starting to update ChartView")

        experiment_id = self._calculator_interface.experimentsIds()[0]
        ttheta_offset = self._project_dict['experiments'][experiment_id]['offset'].value

        series = []
        for calc_dict in self._project_dict['calculations'].values():
            for phase_id in self._project_dict['phases'].keys():
                x_list = calc_dict['bragg_peaks'][phase_id]['ttheta']
                for x in x_list:
                    series.append(QPointF(x - ttheta_offset, 0))

        # Replace series
        if self._seriesRef is not None:
            self._seriesRef.replace(series)

        self._log.info("Finished updating ChartView")

    @Slot(QtCharts.QXYSeries)
    def setSeries(self, series):
        """
        Sets series to be a reference to the QML LineSeries of ChartView.
        """
        self._seriesRef = series
