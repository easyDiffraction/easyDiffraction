import os
from copy import deepcopy

from PySide2.QtCore import QObject, Signal, Slot, Property
from PySide2.QtGui import QPdfWriter, QTextDocument

from PyImports.DisplayModels import *
from PyImports.ProjectSentinel import ProjectControl, writeProject, writeEmptyProject
from PyImports.QtInterface import QtCalculatorInterface
from PyImports.Refinement import Refiner
from PyImports.ReleaseReader import Config

from easyInterface import logger
from easyInterface.Utils.Helpers import open_url
from easyInterface.Diffraction.Calculators.CryspyCalculator import CryspyCalculator


class ProxyPyQml(QObject):

    def __init__(self, release_config_file_path, parent=None):
        self.__log = logger.getLogger(__name__)
        self.__log.info("")
        super().__init__(parent)

        self.info = Config(release_config_file_path)['release']

        self.projectChanged.connect(self.onProjectChanged)

        self._project_rcif_path = None
        self._samples_rcif_path = None
        self._experiment_rcif_path = None
        self._calculator_interface = QtCalculatorInterface(CryspyCalculator())
        self._project_dict_copy = {}

        self._project_control = ProjectControl()
        self._measured_data_model = MeasuredDataModel()
        self._calculated_data_model = CalculatedDataModel()
        self._bragg_peaks_model = BraggPeaksModel()
        self._cell_parameters_model = CellParametersModel()
        self._cell_box_model = CellBoxModel()
        self._atom_sites_model = AtomSitesModel()
        self._atom_adps_model = AtomAdpsModel()
        self._atom_msps_model = AtomMspsModel()
        self._fitables_model = FitablesModel()
        self._status_model = StatusModel()

        self._refine_thread = None
        self._refinement_running = False
        self._refinement_done = False
        self._refinement_result = {}

        self._calculator_interface.clearUndoStack()
        self._need_to_save = False

    @Slot()
    def loadPhasesFromFile(self):
        """
        Replace internal structure models based on requested content from CIF
        """
        self._samples_rcif_path = self._project_control.phases_rcif_path
        self._calculator_interface.addPhaseDefinition(self._samples_rcif_path)
        # explicit emit required for the view to reload the model content
        self._calculator_interface.clearUndoStack()
        self.projectChanged.emit()
        self._need_to_save = False
        self.projectSaveStateChanged.emit()
        #self.onProjectUnsaved()
    
    @Slot()
    def loadExperiment(self):
        """
        Selects the appropriate loading algorithm
        """
    
        if self._project_control.experiment_file_format == "cif":
            self.loadExperimentFromCif()
        elif self._project_control.experiment_file_format == "xye":
            self.loadExperimentFromXye()
        else:
            raise IOError("Unexpected experiment_file_format in ProjectControl.")

    def loadExperimentFromXye(self):
        """
        Loads non cif data files, adds fake cif information, and loads
        """

        cif_string = self._project_control._cif_string
        cif_string = cif_string.replace("PHASE_NAME", self._calculator_interface.phasesIds()[0])
        
        self._calculator_interface.addExperimentDefinitionFromString(cif_string)
        self._measured_data_model.setCalculatorInterface(self._calculator_interface)
        # explicit emit required for the view to reload the model content
        self._calculator_interface.clearUndoStack()
        self.projectChanged.emit()
        self._need_to_save = False
        self.projectSaveStateChanged.emit()
        #self.onProjectUnsaved()

    def loadExperimentFromCif(self):
        """
        Replace internal experiment models based on requested content from CIF
        """
        self._experiment_rcif_path = self._project_control.experiment_rcif_path
        self._calculator_interface.addExperimentDefinition(self._experiment_rcif_path)
        self._measured_data_model.setCalculatorInterface(self._calculator_interface)
        # explicit emit required for the view to reload the model content
        self._calculator_interface.updateCalculations()
        self._calculator_interface.clearUndoStack()
        self.projectChanged.emit()
        self._need_to_save = False
        self.projectSaveStateChanged.emit()
        #self.onProjectUnsaved()

    @Slot(str)
    def updateMainCifFromGui(self, cif_string):
        name_list = [str_line for str_line in cif_string.split('\n') if str_line.startswith('_name ')]
        if len(name_list) != 1:
            self.__log.warning('Project name can not be set. Returning previous value')
            return
        name = name_list[0].split('_name ')[1]
        if name[-1] == ' ':
            name = name[:-1]
        keywords_list = [str_line for str_line in cif_string.split('\n') if str_line.startswith('_keywords ')]
        if len(keywords_list) != 1:
            self.__log.warning('Project keywords can not be set. Returning previous values')
            return
        keywords = keywords_list[0].split('_keywords ')[1]
        if keywords[-1] == ' ':
            keywords = keywords[:-1]
        keywords = keywords.strip('\'')
        keywords = keywords.split(',')
        keywords = [keyword[1:] if keyword[0] == ' ' else keyword for keyword in keywords]
        keywords = [keyword[:-1] if keyword[-1] == ' ' else keyword for keyword in keywords]
        self._project_control.manager.projectName = name
        self._calculator_interface.setProjectName(name)
        self._project_control.manager.projectKeywords = keywords
        self._calculator_interface.setProjectKeywords(keywords)
        self._need_to_save = True
        self.projectSaveStateChanged.emit()

    @Slot(str)
    def updatePhaseFromGui(self, cif_string):
        phase_name = self._calculator_interface.phasesIds()[0]
        cif_string = cif_string[cif_string.find('data_'):]
        new_phase = self._calculator_interface.getPhaseFromCif(cif_string)
        old_phase = self._calculator_interface.getPhase(phase_name)
        keys, values, modifier = old_phase.dictComparison(new_phase)
        modded_keys = [['phases', phase_name, *key] for key, value in zip(keys, values) if key[-1] != 'mapping' and key[-1] != 'hide']
        modded_values = [value for key, value in zip(keys, values) if key[-1] != 'mapping' and key[-1] != 'hide']

        self._calculator_interface.project_dict.startBulkUpdate('Manual update of samples.cif')
        self._calculator_interface.project_dict.bulkUpdate(modded_keys, modded_values)
        self._calculator_interface.setCalculatorFromProject()
        self._calculator_interface.updateCalculations()
        self._calculator_interface.project_dict.endBulkUpdate()

        #self.projectChanged.emit()
        self._calculator_interface.projectDictChanged.emit()
        self._need_to_save = True
        self.projectSaveStateChanged.emit()

    @Slot(str)
    def updateExperimentFromGui(self, cif_string):
        exp_name = self._calculator_interface.experimentsIds()[0]
        cif_string = cif_string[cif_string.find('data_'):]
        new_experiment = self._calculator_interface.getExperimentFromCif(cif_string)
        old_exp = self._calculator_interface.getExperiment(exp_name)
        keys, values, modifier = old_exp.dictComparison(new_experiment)
        modded_keys = [['experiments', exp_name, *key] for key in keys if key[-1] != 'mapping' and key[-1] != 'hide']
        modded_values = [value for key, value in zip(keys, values) if key[-1] != 'mapping' and key[-1] != 'hide']

        self._calculator_interface.project_dict.startBulkUpdate('Manual update of experiments.cif')
        self._calculator_interface.project_dict.bulkUpdate(modded_keys, modded_values)
        self._calculator_interface.setCalculatorFromProject()
        self._calculator_interface.updateCalculations()
        self._calculator_interface.project_dict.endBulkUpdate()

        #self.projectChanged.emit()
        self._calculator_interface.projectDictChanged.emit()
        self._need_to_save = True
        self.projectSaveStateChanged.emit()

    # Load CIF method, accessible from QML
    @Slot()
    def initialize(self):
        self.__log.info("")
        self._project_rcif_path = self._project_control.project_rcif_path
        #logging.info(self._calculator.asCifDict())
        # TODO This is where you would choose the calculator and import the module
        self._calculator_interface = QtCalculatorInterface(
            CryspyCalculator(self._project_rcif_path)
        )
        self._calculator_interface.project_dict['app']['name'] = self.info['name']
        self._calculator_interface.project_dict['app']['version'] = self.info['version']
        self._calculator_interface.project_dict['app']['url'] = self.info['url']
        self._calculator_interface.projectDictChanged.connect(self.projectChanged)
        self._calculator_interface.canUndoOrRedoChanged.connect(self.canUndoOrRedoChanged)
        self._calculator_interface.clearUndoStack()
        # TODO generates dictdiffer
        #  `ValueError: The truth value of an array with more than one element is ambiguous`
        #  Temp fix - Andrew
        self.onProjectSaved()

        models = [self._measured_data_model,
                  self._calculated_data_model,
                  self._bragg_peaks_model,
                  self._cell_parameters_model,
                  self._cell_box_model,
                  self._atom_sites_model,
                  self._atom_adps_model,
                  self._atom_msps_model,
                  self._fitables_model,
                  self._status_model
                  ]
        for model in models:
            model.setCalculatorInterface(self._calculator_interface)

        self._refine_thread = Refiner(self._calculator_interface, 'refine')
        self._refine_thread.failed.connect(self._thread_failed)
        self._refine_thread.finished.connect(self._thread_finished)
        self._refine_thread.finished.connect(self._status_model.onRefinementDone)

        # We can't link signals as the manager signals emitted before the dict is updated :-(
        self.projectChanged.emit()


    @Slot()
    def createProjectZip(self):
        self.__log.debug("")
        self._calculator_interface.writeMainCif(self._project_control.tempDir.name)
        writeEmptyProject(self._project_control, self._project_control.project_file)
        self.onProjectSaved()

    @Slot(str)
    def createProject(self, file_path):
        self.__log.debug("")
        self._project_control.createProject(file_path)
        # Note that the main rcif of self._project_control.project_rcif_path has not ben cleared
        self._project_control.project_rcif_path = ''
        self.onProjectSaved()
        self.initialize()
        self.projectChanged.emit()

    @Slot(str)
    def saveProjectAs(self, file_path):
        self.__log.debug("")
        self._project_control.project_file = file_path
        self.saveProject()

    @Slot()
    def saveProject(self):
        self.__log.debug("")
        self._calculator_interface.saveCifs(self._project_control.tempDir.name)
        writeProject(self._project_control, self._project_control.project_file)
        self.onProjectSaved()

    def onProjectSaved(self):
        self.__log.debug("")
        self._project_dict_copy = deepcopy(self._calculator_interface.project_dict)
        self._need_to_save = False
        self.projectSaveStateChanged.emit()
        self.projectChanged.emit() # update project.cif in gui (when filenames changed)

    def onProjectUnsaved(self):
        self.__log.debug("")
        self._need_to_save = True
        self.projectSaveStateChanged.emit()

    def onProjectChanged(self):
        keys, _, _ = self._calculator_interface.project_dict.dictComparison(self._project_dict_copy)
        self.__log.debug(f"keys: {keys}")
        self._need_to_save = True
        if not keys:
            self._need_to_save = False
        self.__log.debug(f"needToSave: {self._need_to_save}")
        self.projectSaveStateChanged.emit()

    def calculatorInterface(self):
        self.__log.debug("---")
        return self._calculator_interface

    def needToSave(self):
        self.__log.debug("+++")
        return self._need_to_save

    def projectFilePathSelected(self):
        self.__log.debug("***")
        return bool(self._project_control.project_file)

    # ##############
    # QML Properties
    # ##############

    # Notifications of changes for QML GUI about projectDictChanged,
    # which calls another signal projectChanged

    projectChanged = Signal()
    projectSaveStateChanged = Signal()
    canUndoOrRedoChanged = Signal()

    _calculatorInterface = Property('QVariant', calculatorInterface, notify=projectChanged)
    _needToSave = Property(bool, needToSave, notify=projectSaveStateChanged)
    _projectFilePathSelected = Property(bool, projectFilePathSelected, notify=projectSaveStateChanged)

    _undoText = Property('QVariant', lambda self: self._calculator_interface.undoText(), notify=canUndoOrRedoChanged)
    _redoText = Property('QVariant', lambda self: self._calculator_interface.redoText(), notify=canUndoOrRedoChanged)
    _canUndo = Property('QVariant', lambda self: self._calculator_interface.canUndo(), notify=canUndoOrRedoChanged)
    _canRedo = Property('QVariant', lambda self: self._calculator_interface.canRedo(), notify=canUndoOrRedoChanged)

    # Notifications of changes for QML GUI are done, when needed, in the
    # respective classes via dataChanged.emit() or layotChanged.emit() signals

    _proxy = Property('QVariant', lambda self: self, constant=True)
    _releaseInfo = Property('QVariant', lambda self: self.releaseInfo, constant=True)

    _projectControl = Property('QVariant', lambda self: self._project_control, constant=True)
    _projectManager = Property('QVariant', lambda self: self._project_control.manager, constant=True)

    _measuredData = Property('QVariant', lambda self: self._measured_data_model, constant=True)
    _calculatedData = Property('QVariant', lambda self: self._calculated_data_model, constant=True)
    _braggPeaks = Property('QVariant', lambda self: self._bragg_peaks_model, constant=True)
    _cellParameters = Property('QVariant', lambda self: self._cell_parameters_model.asModel(), constant=True)
    _cellBox = Property('QVariant', lambda self: self._cell_box_model.asModel(), constant=True)
    _atomSites = Property('QVariant', lambda self: self._atom_sites_model.asModel(), constant=True)
    _atomAdps = Property('QVariant', lambda self: self._atom_adps_model.asModel(), constant=True)
    _atomMsps = Property('QVariant', lambda self: self._atom_msps_model.asModel(), constant=True)
    _fitables = Property('QVariant', lambda self: self._fitables_model.asModel(), constant=True)

    _statusInfo = Property('QVariant', lambda self: self._status_model.returnStatusBarModel(), constant=True)
    _chartInfo = Property('QVariant', lambda self: self._status_model.returnChartModel(), constant=True)

    _releaseInfo = Property('QVariant', lambda self: self.info, constant=True)

    # ###############
    # REFINEMENT TYPE
    # ###############

    def refineSum(self):
        if not self._calculator_interface.experimentsIds():
            return False
        experiment_name = self._calculator_interface.experimentsIds()[0]
        return self._calculator_interface.project_dict['experiments'][experiment_name]['refinement_type'].sum

    def refineDiff(self):
        if not self._calculator_interface.experimentsIds():
            return False
        experiment_name = self._calculator_interface.experimentsIds()[0]
        return self._calculator_interface.project_dict['experiments'][experiment_name]['refinement_type'].diff

    def setRefineSum(self, state):
        experiment_name = self._calculator_interface.experimentsIds()[0]
        if self._calculator_interface.project_dict['experiments'][experiment_name]['refinement_type'].sum == state:
            return
        self._calculator_interface.project_dict['experiments'][experiment_name]['refinement_type'].sum = state

    def setRefineDiff(self, state):
        experiment_name = self._calculator_interface.experimentsIds()[0]
        if self._calculator_interface.project_dict['experiments'][experiment_name]['refinement_type'].diff == state:
            return
        self._calculator_interface.project_dict['experiments'][experiment_name]['refinement_type'].diff = state

    _refineSum = Property(bool, refineSum, setRefineSum, notify=projectChanged)
    _refineDiff = Property(bool, refineDiff, setRefineDiff, notify=projectChanged)

    # ##########
    # REFINEMENT
    # ##########

    def _thread_finished(self, res):
        """
        Notfy the listeners about refinement results
        """
        self._refinement_running = False
        self._refinement_done = True
        self._refinement_result = deepcopy(res)
        self.refinementStatusChanged.emit()

    def _thread_failed(self, reason):
        """
        Notify the GUI about failure so a message can be shown
        """
        self.__log.info("Refinement failed: " + str(reason))
        self._refinement_running = False
        self._refinement_done = False
        self.refinementStatusChanged.emit()

    @Slot()
    def refine(self):
        """
        Start refinement as a separate thread
        """
        self._calculator_interface.setCalculatorFromProject()
        self.__log.info("")
        if self._refinement_running:
            self.__log.info("Fitting stopped")
            # This lacks actual stopping functionality, needs to be added
            self._refinement_running = False
            self._refinement_done = True
            self.refinementStatusChanged.emit()
            return
        self._refinement_running = True
        self._refinement_done = False
        self.refinementStatusChanged.emit()
        self._refine_thread.start()

    refinementStatusChanged = Signal()
    _refinementStatus = Property('QVariant', lambda self: [self._refinement_running, self._refinement_done, self._refinement_result], notify=refinementStatusChanged)

    # ######
    # REPORT
    # ######

    @Slot(str)
    def store_report(self, report=""):
        """
        Keep the QML generated HTML report for saving
        """
        self.report_html = report

    @Slot(str, str)
    def save_report(self, filename="", extension=".HTML"):
        """
        Save the generated report to the specified file
        Currently only html
        """
        full_filename = filename + extension.lower()
        full_filename = os.path.join(self._project_control.get_project_dir_absolute_path(), full_filename)

        if not self.report_html:
            self.__log.info("No report to save")
            return

        if extension == '.HTML':
            # HTML can contain non-ascii, so need to open with right encoding
            with open(full_filename, 'w', encoding='utf-8') as report_file:
                report_file.write(self.report_html)
                self.__log.info("Report written")
        elif extension == '.PDF':
            document = QTextDocument(parent=None)
            document.setHtml(self.report_html)
            printer = QPdfWriter(full_filename)
            printer.setPageSize(printer.A3) # A3 to fit A4 page
            document.print_(printer)
        else:
            raise NotImplementedError

        # Show the generated report in the default browser
        url = os.path.realpath(full_filename)
        open_url(url=url)

