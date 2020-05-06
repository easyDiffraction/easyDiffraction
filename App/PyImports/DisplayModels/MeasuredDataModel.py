from PySide2.QtCore import Qt, QPointF, Slot, Signal, Property
from PySide2.QtCharts import QtCharts

from easyInterface import logger
from PyImports.DisplayModels.BaseModel import BaseModel


class MeasuredDataModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._y_obs_column = 1
        self._sy_obs_column = 2
        self._y_max = 1
        self._y_min = 0
        self._upperSeriesRefs = []  # list of references to QML LineSeries (for 2 charts)
        self._lowerSeriesRefs = []  # list of references to QML LineSeries (for 2 charts)
        self._log = logger.getLogger(self.__class__.__module__)

    def _setModelsFromProjectDict(self):
        """
        Create the model needed for GUI measured data table and chart.
        """
        self._log.info("Starting to set Model from Project Dict")

        for experiment_id, experiment_dict in self._project_dict['experiments'].items():

            reduced_experiment_dict = {}
            for key, value in experiment_dict['measured_pattern'].items():
                if value is not None:
                    reduced_experiment_dict[key] = value

            column_count = len(reduced_experiment_dict)
            row_count = len(list(reduced_experiment_dict.values())[0])

            self._model.blockSignals(True)
            self._headers_model.blockSignals(True)

            self._model.clear()
            self._model.setColumnCount(column_count)
            self._model.setRowCount(row_count)

            self._headers_model.clear()
            self._headers_model.setColumnCount(column_count)
            self._headers_model.setRowCount(1)

            # Add all the columns from experiment_dict['measured_pattern'] to self._model
            for colum_index, (data_id, data_list) in enumerate(reduced_experiment_dict.items()):
                index = self._headers_model.index(0, colum_index)
                self._headers_model.setData(index, data_id, Qt.DisplayRole)

                for row_index, value in enumerate(data_list):
                    index = self._model.index(row_index, colum_index)
                    self._model.setData(index, value, Qt.DisplayRole)

            self._model.blockSignals(False)
            self._headers_model.blockSignals(False)

            # Emit signal which is caught by the QStandardItemModel-based
            # QML GUI elements in order to update their views
            self._model.layoutChanged.emit()
            self._headers_model.layoutChanged.emit()

            # Update chart series here, as this method is significantly
            # faster, compared to the updating at the QML GUI side via the
            # QStandardItemModel
            self._updateQmlChartViewSeries()

        self._log.info("Finished setting Model from Project Dict")

    def _updateQmlChartViewSeries(self):
        """
        Updates QML LineSeries of ChartView.
        """
        self._log.info("Starting update of ChartView")

        # Indices of the self._model columns to be plotted on chart
        x_column = 0

        # Get values from model
        x_list = []
        y_obs_lower_list = []
        y_obs_upper_list = []
        for row_index in range(self._model.rowCount()):
            x = self._model.data(self._model.index(row_index, x_column))
            y_obs = self._model.data(self._model.index(row_index, self._y_obs_column))
            sy_obs = self._model.data(self._model.index(row_index, self._sy_obs_column))
            x_list.append(x)
            y_obs_lower_list.append(y_obs - sy_obs)
            y_obs_upper_list.append(y_obs + sy_obs)

        # Update Min and Max
        self._setYMax(max(y_obs_upper_list))
        self._setYMin(min(y_obs_lower_list))

        # Clear series
        upper_series = []
        lower_series = []

        # Insert data into the Series format with QPointF's
        for x, y_obs_lower, y_obs_upper in zip(x_list, y_obs_lower_list, y_obs_upper_list):
            upper_series.append(QPointF(x, y_obs_upper))
            lower_series.append(QPointF(x, y_obs_lower))

        # Replace series
        for s in self._upperSeriesRefs:
            s.replace(upper_series)
        for s in self._lowerSeriesRefs:
            s.replace(lower_series)

        self._log.info("Finished update of ChartView")

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

    @Slot(str)
    def setDataType(self, type):
        """
        Sets data type to be displayed on QML ChartView.
        """
        self._log.debug(type)
        if (type == "Sum"):
            self._y_obs_column = 1
            self._sy_obs_column = 2
        elif (type == "Difference"):
            self._y_obs_column = 3
            self._sy_obs_column = 4
        elif (type == "Up"):
            self._y_obs_column = 5
            self._sy_obs_column = 6
        elif (type == "Down"):
            self._y_obs_column = 7
            self._sy_obs_column = 8
        self._updateQmlChartViewSeries()

    def _yMax(self):
        """
        Returns max value for Y-axis.
        """
        return self._y_max

    def _yMin(self):
        """
        Returns min value for Y-axis.
        """
        return self._y_min

    def _setYMax(self, value):
        """
        Sets max value for Y-axis.
        """
        self._y_max = value
        self._yMaxChanged.emit()

    def _setYMin(self, value):
        """
        Sets min value for Y-axis.
        """
        self._y_min = value
        self._yMinChanged.emit()

    _yMaxChanged = Signal()
    _yMinChanged = Signal()

    yMax = Property(float, _yMax, notify=_yMaxChanged)
    yMin = Property(float, _yMin, notify=_yMinChanged)
