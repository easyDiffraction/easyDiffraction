import numpy as np

from easyInterface import logger

from PySide2.QtCore import Qt, QPointF, Slot, Signal, Property
from PySide2.QtCharts import QtCharts

from PyImports.DisplayModels.BaseModel import BaseModel


class CalculatedDataModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._y_calc_name = "y_calc_sum"
        self._y_obs_name = "y_obs"
        self._sy_obs_name = "sy_obs"
        self._y_max = 1
        self._y_min = 0
        self._y_diff_max = 1
        self._y_diff_min = 0
        self._calcSeriesRef = None
        self._calcBkgSeriesRef = None
        self._lowerDiffSeriesRef = None
        self._upperDiffSeriesRef = None
        self._log = logger.getLogger(self.__class__.__module__)

    def _setModelsFromProjectDict(self):
        """
        Create the model needed for GUI measured data table and chart.
        """
        self._log.info("Starting to set Model from Project Dict")

        for calc_dict in self._project_dict['calculations'].values():
            column_count = len(calc_dict['calculated_pattern'].items())
            row_count = len(list(calc_dict['calculated_pattern'].items())[0][1])

            self._model.blockSignals(True)
            self._headers_model.blockSignals(True)

            self._model.clear()
            self._model.setColumnCount(column_count)
            self._model.setRowCount(row_count)

            self._headers_model.clear()
            self._headers_model.setColumnCount(column_count)
            self._headers_model.setRowCount(1)

            # Add all the columns from calc_dict['calculated_pattern'] to self._model
            for colum_index, (data_id, data_list) in enumerate(calc_dict['calculated_pattern'].items()):
                index = self._headers_model.index(0, colum_index)
                self._headers_model.setData(index, data_id, Qt.DisplayRole)
                for row_index, value in enumerate(data_list):
                    index = self._model.index(row_index, colum_index)
                    self._model.setData(index, value, Qt.DisplayRole)

            self._model.blockSignals(False)
            self._headers_model.blockSignals(False)

            # Emit signal which is catched by the QStandardItemModel-based
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

        if not self._project_dict:
            return

        calcSeries = []
        calcBkgSeries = []
        lowerDiffSeries = []
        upperDiffSeries = []

        for calc_dict, experiment_dict in zip(self._project_dict['calculations'].values(), self._project_dict['experiments'].values()):
            x_list = calc_dict['calculated_pattern']['x']
            y_calc_list = calc_dict['calculated_pattern'][self._y_calc_name]
            y_obs_list = experiment_dict['measured_pattern'][self._y_obs_name]
            sy_obs_list = experiment_dict['measured_pattern'][self._sy_obs_name]

            y_calc_bkg_list = []
            if self._y_calc_name == 'y_calc_sum':
                y_calc_bkg_list = calc_dict['calculated_pattern']['y_calc_bkg']
            elif self._y_calc_name == 'y_calc_up' or self._y_calc_name == 'y_calc_down':
                y_calc_bkg_list = np.divide(np.array(calc_dict['calculated_pattern']['y_calc_bkg']), 2).tolist()
            elif self._y_calc_name == 'y_calc_diff':
                y_calc_bkg_list = [0] * len(x_list)

            # Insert data into the Series format with QPointF's
            for x, y_calc, y_calc_bkg, y_obs, sy_obs in zip(x_list, y_calc_list, y_calc_bkg_list, y_obs_list, sy_obs_list):
                calcSeries.append(QPointF(x, y_calc))
                calcBkgSeries.append(QPointF(x, y_calc_bkg))
                upperDiffSeries.append(QPointF(x, y_obs + sy_obs - y_calc))
                lowerDiffSeries.append(QPointF(x, y_obs - sy_obs - y_calc))

            # Update Min and Max
            self._setYMax(max(y_calc_list))
            self._setYMin(min(y_calc_list))
            self._setYDiffMax(max([y_obs + sy_obs - y_calc for (y_obs, sy_obs, y_calc) in zip(y_obs_list, sy_obs_list, y_calc_list)]))
            self._setYDiffMin(min([y_obs - sy_obs - y_calc for (y_obs, sy_obs, y_calc) in zip(y_obs_list, sy_obs_list, y_calc_list)]))

        # Replace series
        if self._calcSeriesRef is not None:
            self._calcSeriesRef.replace(calcSeries)
            self._calcBkgSeriesRef.replace(calcBkgSeries)
            self._lowerDiffSeriesRef.replace(lowerDiffSeries)
            self._upperDiffSeriesRef.replace(upperDiffSeries)

        self._log.info("Finished update of ChartView")

    @Slot(QtCharts.QXYSeries)
    def setCalcSeries(self, series):
        """
        Sets calculated series to be a reference to the QML LineSeries of ChartView.
        """
        self._calcSeriesRef = series

    @Slot(QtCharts.QXYSeries)
    def setCalcBkgSeries(self, series):
        """
        Sets calculated background series to be a reference to the QML LineSeries of ChartView.
        """
        self._calcBkgSeriesRef = series

    @Slot(QtCharts.QXYSeries)
    def setLowerDiffSeries(self, series):
        """
        Sets lower difference series to be a reference to the QML LineSeries of ChartView.
        """
        self._lowerDiffSeriesRef = series

    @Slot(QtCharts.QXYSeries)
    def setUpperDiffSeries(self, series):
        """
        Sets upper difference series to be a reference to the QML LineSeries of ChartView.
        """
        self._upperDiffSeriesRef = series

    @Slot(str)
    def setDataType(self, type):
        """
        Sets data type to be displayed on QML ChartView.
        """
        self._log.debug(type)
        if (type == "Sum"):
            self._y_calc_name = "y_calc_sum"
            self._y_obs_name = "y_obs"
            self._sy_obs_name = "sy_obs"
        elif (type == "Difference"):
            self._y_calc_name = "y_calc_diff"
            self._y_obs_name = "y_obs_diff"
            self._sy_obs_name = "sy_obs_diff"
        elif (type == "Up"):
            self._y_calc_name = "y_calc_up"
            self._y_obs_name = "y_obs_up"
            self._sy_obs_name = "sy_obs_up"
        elif (type == "Down"):
            self._y_calc_name = "y_calc_down"
            self._y_obs_name = "y_obs_down"
            self._sy_obs_name = "sy_obs_down"
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

    def _yDiffMax(self):
        """
        Returns max value for difference Y-axis.
        """
        return self._y_diff_max

    def _yDiffMin(self):
        """
        Returns min value for difference Y-axis.
        """
        return self._y_diff_min

    def _setYDiffMax(self, value):
        """
        Sets max value for difference Y-axis.
        """
        self._y_diff_max = value
        self._yDiffMaxChanged.emit()

    def _setYDiffMin(self, value):
        """
        Sets min value for difference Y-axis.
        """
        self._y_diff_min = value
        self._yDiffMinChanged.emit()

    _yMaxChanged = Signal()
    _yMinChanged = Signal()
    _yDiffMaxChanged = Signal()
    _yDiffMinChanged = Signal()

    yMax = Property(float, _yMax, notify=_yMaxChanged)
    yMin = Property(float, _yMin, notify=_yMinChanged)
    yDiffMax = Property(float, _yDiffMax, notify=_yDiffMaxChanged)
    yDiffMin = Property(float, _yDiffMin, notify=_yDiffMinChanged)
