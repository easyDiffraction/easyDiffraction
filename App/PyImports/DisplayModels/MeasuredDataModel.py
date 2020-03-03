import logging

from PySide2.QtCore import Qt, QPointF, Slot
from PySide2.QtCharts import QtCharts


from easyInterface import logger
from PyImports.DisplayModels.BaseModel import BaseModel


class MeasuredDataModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._upperSeriesRefs = []  # list of references to QML LineSeries (for 2 charts)
        self._lowerSeriesRefs = []  # list of references to QML LineSeries (for 2 charts)
        self._log = logger.getLogger(__class__.__module__)

    def _setModelsFromProjectDict(self):
        """
        Create the model needed for GUI measured data table and chart.
        """
        self._log.info("-> start")

        for experiment_id, experiment_dict in self._project_dict['experiments'].items():
            column_count = len(experiment_dict['measured_pattern'].items())
            row_count = len(list(experiment_dict['measured_pattern'].items())[0][1])

            self._model.blockSignals(True)
            self._headers_model.blockSignals(True)

            self._model.clear()
            self._model.setColumnCount(column_count)
            self._model.setRowCount(row_count)

            self._headers_model.clear()
            self._headers_model.setColumnCount(column_count)
            self._headers_model.setRowCount(1)

            # Add all the columns from experiment_dict['measured_pattern'] to self._model
            for colum_index, (data_id, data_list) in enumerate(experiment_dict['measured_pattern'].items()):
                index = self._headers_model.index(0, colum_index)
                self._headers_model.setData(index, data_id, Qt.DisplayRole)
                if data_list is None:
                    index = self._model.index(0, colum_index)
                    self._model.setData(index, None, Qt.DisplayRole)
                else:
                    for row_index, value in enumerate(data_list):
                        index = self._model.index(row_index, colum_index)
                        self._model.setData(index, value, Qt.DisplayRole)

            self._model.blockSignals(False)
            self._headers_model.blockSignals(False)

            # Emit signal which is catched by the QStandartItemModel-based
            # QML GUI elements in order to update their views
            self._model.layoutChanged.emit()
            self._headers_model.layoutChanged.emit()

            # Update chart series here, as this method is significantly
            # faster, compared to the updating at the QML GUI side via the
            # QStandartItemModel
            self._updateQmlChartViewSeries()

        self._log.info("<- end")

    def _updateQmlChartViewSeries(self):
        """
        Updates QML LineSeries of ChartView.
        """
        self._log.info("=====> start")

        # Indices of the self._model columns to be plotted on chart
        x_column = 0
        y_obs_column = 1
        sy_obs_column = 2

        # Get values from model
        x_list = []
        y_obs_lower_list = []
        y_obs_upper_list = []
        for row_index in range(self._model.rowCount()):
            x = self._model.data(self._model.index(row_index, x_column))
            y_obs = self._model.data(self._model.index(row_index, y_obs_column))
            sy_obs = self._model.data(self._model.index(row_index, sy_obs_column))
            x_list.append(x)
            y_obs_lower_list.append(y_obs - sy_obs)
            y_obs_upper_list.append(y_obs + sy_obs)

        # Clear series
        upperSeries = []
        lowerSeries = []

        # Insert data into the Series format with QPointF's
        for x, y_obs_lower, y_obs_upper in zip(x_list, y_obs_lower_list, y_obs_upper_list):
            upperSeries.append(QPointF(x, y_obs_upper))
            lowerSeries.append(QPointF(x, y_obs_lower))

        # Replace series
        for s in self._upperSeriesRefs:
            s.replace(upperSeries)
        for s in self._lowerSeriesRefs:
            s.replace(lowerSeries)

        self._log.info("<===== end")

    def onProjectChanged(self):
        """
        Reimplement BaseModel method, as we do not want to update measured data every time.
        """
        pass

    @Slot(QtCharts.QXYSeries)
    def setLowerSeries(self, series):
        """
        Sets lower series to be a reference to the QML LineSeries of ChartView.
        """
        self._lowerSeriesRefs.append(series)

    @Slot(QtCharts.QXYSeries)
    def setUpperSeries(self, series):
        """
        Sets upper series to be a reference to the QML LineSeries of ChartView.
        """
        self._upperSeriesRefs.append(series)
