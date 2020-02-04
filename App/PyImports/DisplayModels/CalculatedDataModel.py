import logging

from PySide2.QtCore import Qt, QPointF, Slot
from PySide2.QtCharts import QtCharts

from PyImports.DisplayModels.BaseModel import BaseModel


class CalculatedDataModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._calcSeriesRef = None
        self._lowerDiffSeriesRef = None
        self._upperDiffSeriesRef = None

    def _setModelsFromProjectDict(self):
        """
        Create the model needed for GUI measured data table and chart.
        """
        logging.info("-> start")

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

        calcSeries = []
        lowerDiffSeries = []
        upperDiffSeries = []

        for calc_dict, experiment_dict in zip(self._project_dict['calculations'].values(), self._project_dict['experiments'].values()):
            x_list = calc_dict['calculated_pattern']['x']
            y_calc_list = calc_dict['calculated_pattern']['y_calc']
            y_obs_list = experiment_dict['measured_pattern']['y_obs']
            sy_obs_list = experiment_dict['measured_pattern']['sy_obs']

            for x, y_calc, y_obs, sy_obs in zip(x_list, y_calc_list, y_obs_list, sy_obs_list):
                calcSeries.append(QPointF(x, y_calc))
                lowerDiffSeries.append(QPointF(x, y_obs + sy_obs - y_calc))
                upperDiffSeries.append(QPointF(x, y_obs - sy_obs - y_calc))

        # Replace series
        self._calcSeriesRef.replace(calcSeries)
        self._lowerDiffSeriesRef.replace(lowerDiffSeries)
        self._upperDiffSeriesRef.replace(upperDiffSeries)

        logging.info("<===== end")

    @Slot(QtCharts.QXYSeries)
    def setCalcSeries(self, series):
        """
        Sets calculated series to be a reference to the QML LineSeries of ChartView.
        """
        self._calcSeriesRef = series

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
