import logging

from PySide2.QtCore import Qt, QPointF, Slot
from PySide2.QtCharts import QtCharts

from PyImports.Models.BaseModel import BaseModel


class MeasuredDataModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._upperSeries = []  # list of references to QML LineSeries (for 2 charts)
        self._lowerSeries = []  # list of references to QML LineSeries (for 2 charts)

    def _setModelsFromProjectDict(self):
        """
        Create the model needed for GUI measured data table and chart.
        """
        logging.info("-> start")

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

            for colum_index, (data_id, data_list) in enumerate(experiment_dict['measured_pattern'].items()):
                index = self._headers_model.index(0, colum_index)
                self._headers_model.setData(index, data_id, Qt.DisplayRole)
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

        logging.info("<- end")

    def _updateQmlChartViewSeries(self):
        """
        Updates QML LineSeries of ChartView.
        """
        logging.info("=====> start")

        # Indices of the self._model columns to be plotted on chart
        x_column = 0        # first column in experiment_dict['measured_pattern']
        y_obs_column = 1    # second column in experiment_dict['measured_pattern']
        sy_obs_column = 2   # third column in experiment_dict['measured_pattern']

        # Get values from model
        x_list = []
        y_obs_lower_list = []
        y_obs_upper_list = []
        for row_index in range(self._model.rowCount()):
            index = self._model.index(row_index, x_column)
            x_list.append(self._model.data(index))

            index = self._model.index(row_index, y_obs_column)
            y_obs = self._model.data(index)

            index = self._model.index(row_index, sy_obs_column)
            sy_obs = self._model.data(index)

            y_obs_lower_list.append(y_obs - sy_obs)
            y_obs_upper_list.append(y_obs + sy_obs)

        # Clear series
        for s in self._upperSeries:
            s.clear()
        for s in self._lowerSeries:
            s.clear()

        # Insert data into the Series format with QPointF's
        for x, y_obs_lower, y_obs_upper in zip(x_list, y_obs_lower_list, y_obs_upper_list):
            for s in self._upperSeries:
                s.append(QPointF(x, y_obs_upper))
            for s in self._lowerSeries:
                s.append(QPointF(x, y_obs_lower))

        logging.info("<===== end")

    @Slot(QtCharts.QXYSeries)
    def setLowerSeries(self, series):
        """
        Sets lower series to be a reference to the QML LineSeries of ChartView.
        """
        self._lowerSeries.append(series)

    @Slot(QtCharts.QXYSeries)
    def setUpperSeries(self, series):
        """
        Sets upper series to be a reference to the QML LineSeries of ChartView.
        """
        self._upperSeries.append(series)
