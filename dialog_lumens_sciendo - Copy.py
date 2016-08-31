#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime, glob, tempfile, csv
from qgis.core import *
from processing.tools import *
from PyQt4 import QtCore, QtGui

from utils import QPlainTextEditLogger
from dialog_lumens_base import DialogLumensBase
from dialog_lumens_viewer import DialogLumensViewer
import resource


class DialogLumensSCIENDO(QtGui.QDialog, DialogLumensBase):
    """LUMENS "SCIENDO" module dialog class.
    """
    
    def loadTemplateFiles(self):
        """Method for loading the list of module template files inside the project folder.
        
        This method is also called to load the module template files in the main window dashboard tab.
        """
        templateFiles = [os.path.basename(name) for name in glob.glob(os.path.join(self.settingsPath, '*.ini')) if os.path.isfile(os.path.join(self.settingsPath, name))]
        
        if templateFiles:
            self.comboBoxLowEmissionDevelopmentAnalysisTemplate.clear()
            self.comboBoxLowEmissionDevelopmentAnalysisTemplate.addItems(sorted(templateFiles))
            self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
            self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
            
            self.comboBoxLandUseChangeModelingTemplate.clear()
            self.comboBoxLandUseChangeModelingTemplate.addItems(sorted(templateFiles))
            self.comboBoxLandUseChangeModelingTemplate.setEnabled(True)
            self.buttonLoadLandUseChangeModelingTemplate.setEnabled(True)
            
            # MainWindow SCIENDO dashboard templates
            self.main.comboBoxLowEmissionDevelopmentAnalysisTemplate.clear()
            self.main.comboBoxLowEmissionDevelopmentAnalysisTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
            self.main.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
            
            self.main.comboBoxLandUseChangeModelingTemplate.clear()
            self.main.comboBoxLandUseChangeModelingTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxLandUseChangeModelingTemplate.setEnabled(True)
            self.main.buttonProcessSCIENDOLandUseChangeModelingTemplate.setEnabled(True)
        else:
            self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
            self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
            
            self.comboBoxLandUseChangeModelingTemplate.setDisabled(True)
            self.buttonLoadLandUseChangeModelingTemplate.setDisabled(True)
            
            # MainWindow SCIENDO dashboard templates
            self.main.comboBoxLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
            self.main.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
            
            self.main.comboBoxLandUseChangeModelingTemplate.setDisabled(True)
            self.main.buttonProcessSCIENDOLandUseChangeModelingTemplate.setDisabled(True)
    
    
    def loadTemplate(self, tabName, fileName, returnTemplateSettings=False):
        """Method for loading the values saved in the module template file to the form widgets.
        
        Args:
            tabName (str): the tab where the form widget values will be populated.
            templateFile (str): a file path to the template file that will be loaded.
            returnTemplateSettings (bool): if true return a dict of the settings in the template file.
        """
        templateFilePath = os.path.join(self.settingsPath, fileName)
        settings = QtCore.QSettings(templateFilePath, QtCore.QSettings.IniFormat)
        settings.setFallbacksEnabled(True) # only use ini files
        
        templateSettings = {}
        dialogsToLoad = None
        
        td = datetime.date.today()
        
        if tabName == 'Low Emission Development Analysis':
            dialogsToLoad = (
                'DialogLumensSCIENDOHistoricalBaselineProjection',
                'DialogLumensSCIENDOHistoricalBaselineAnnualProjection',
                'DialogLumensSCIENDODriversAnalysis',
                'DialogLumensSCIENDOBuildScenario',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Historical baseline projection' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDOHistoricalBaselineProjection')
            
            templateSettings['DialogLumensSCIENDOHistoricalBaselineProjection'] = {}
            templateSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['QUESCDatabase'] = QUESCDatabase = settings.value('QUESCDatabase')
            templateSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['iteration'] = iteration = settings.value('iteration')
            
            if not returnTemplateSettings:
                if QUESCDatabase:
                    indexQUESCDatabase = self.comboBoxHistoricalBaselineProjectionQUESCDatabase.findText(QUESCDatabase)
                    if indexQUESCDatabase != -1:
                        self.comboBoxHistoricalBaselineProjectionQUESCDatabase.setCurrentIndex(indexQUESCDatabase)
                        
                if iteration:
                    self.spinBoxHistoricalBaselineProjectionIteration.setValue(int(iteration))
                else:
                    self.spinBoxHistoricalBaselineProjectionIteration.setValue(5)
            
            settings.endGroup()
            # /dialog
            
            # 'Historical baseline annual projection' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDOHistoricalBaselineAnnualProjection')
            
            templateSettings['DialogLumensSCIENDOHistoricalBaselineAnnualProjection'] = {}
            templateSettings['DialogLumensSCIENDOHistoricalBaselineAnnualProjection']['iteration'] = iteration = settings.value('iteration')
            
            if not returnTemplateSettings:
                if iteration:
                    self.spinBoxHistoricalBaselineAnnualProjectionIteration.setValue(int(iteration))
                else:
                    self.spinBoxHistoricalBaselineAnnualProjectionIteration.setValue(5)
            
            settings.endGroup()
            # /dialog
            
            # 'Drivers analysis' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDODriversAnalysis')
            
            templateSettings['DialogLumensSCIENDODriversAnalysis'] = {}
            templateSettings['DialogLumensSCIENDODriversAnalysis']['landUseCoverChangeDrivers'] = landUseCoverChangeDrivers = settings.value('landUseCoverChangeDrivers')
            templateSettings['DialogLumensSCIENDODriversAnalysis']['landUseCoverChangeType'] = landUseCoverChangeType = settings.value('landUseCoverChangeType')
            
            if not returnTemplateSettings:
                if landUseCoverChangeDrivers and os.path.exists(landUseCoverChangeDrivers):
                    self.lineEditDriversAnalysisLandUseCoverChangeDrivers.setText(landUseCoverChangeDrivers)
                else:
                    self.lineEditDriversAnalysisLandUseCoverChangeDrivers.setText('')
                if landUseCoverChangeType:
                    self.lineEditDriversAnalysisLandUseCoverChangeType.setText(landUseCoverChangeType)
                else:
                    self.lineEditDriversAnalysisLandUseCoverChangeType.setText('Land use change')
            
            settings.endGroup()
            # /dialog
            
            # 'Build scenario' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDOBuildScenario')
            
            templateSettings['DialogLumensSCIENDOBuildScenario'] = {}
            templateSettings['DialogLumensSCIENDOBuildScenario']['historicalBaselineCar'] = historicalBaselineCar = settings.value('historicalBaselineCar')
            
            if not returnTemplateSettings:
                if historicalBaselineCar and os.path.exists(historicalBaselineCar):
                    self.lineEditBuildScenarioHistoricalBaselineCar.setText(historicalBaselineCar)
                else:
                    self.lineEditBuildScenarioHistoricalBaselineCar.setText('')
            
            if not returnTemplateSettings:
                self.currentLowEmissionDevelopmentAnalysisTemplate = templateFile
                self.loadedLowEmissionDevelopmentAnalysisTemplate.setText(templateFile)
                self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setCurrentIndex(self.comboBoxLowEmissionDevelopmentAnalysisTemplate.findText(templateFile))
                self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        elif tabName == 'Land Use Change Modeling':
            dialogsToLoad = (
                'DialogLumensSCIENDOCalculateTransitionMatrix',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Land Use Change Modeling' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDOCalculateTransitionMatrix')
            
            templateSettings['DialogLumensSCIENDOCalculateTransitionMatrix'] = {}
            templateSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['factorsDir'] = factorsDir = settings.value('factorsDir')
            templateSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['landUseLookup'] = landUseLookup = settings.value('landUseLookup')
            templateSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['baseYear'] = baseYear = settings.value('baseYear')
            templateSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['location'] = location = settings.value('location')
            
            if not returnTemplateSettings:
                if factorsDir and os.path.isdir(factorsDir):
                    self.lineEditLandUseChangeModelingFactorsDir.setText(factorsDir)
                else:
                    self.lineEditLandUseChangeModelingFactorsDir.setText('')
                if landUseLookup and os.path.exists(landUseLookup):
                    self.lineEditLandUseChangeModelingLandUseLookup.setText(landUseLookup)
                else:
                    self.lineEditLandUseChangeModelingLandUseLookup.setText('')
                if baseYear:
                    self.spinBoxLandUseChangeModelingBaseYear.setValue(int(baseYear))
                else:
                    self.spinBoxLandUseChangeModelingBaseYear.setValue(td.year)
                if location:
                    self.lineEditLandUseChangeModelingLocation.setText(location)
                else:
                    self.lineEditLandUseChangeModelingLocation.setText('location')
                
                self.currentLandUseChangeModelingTemplate = templateFile
                self.loadedLandUseChangeModelingTemplate.setText(templateFile)
                self.comboBoxLandUseChangeModelingTemplate.setCurrentIndex(self.comboBoxLandUseChangeModelingTemplate.findText(templateFile))
                self.buttonSaveLandUseChangeModelingTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        
        if returnTemplateSettings:
            return templateSettings
        else:
            # Log to history log
            logging.getLogger(self.historyLog).info('Loaded template: %s', templateFile)
    
    
    def checkForDuplicateTemplates(self, tabName, templateToSkip):
        """Method for checking whether the new template values to be saved already exists in a saved template file.
        
        Args:
            tabName (str): the tab to be checked.
            templateToSkip (str): the template file to skip (when saving an existing template file).
        """
        duplicateTemplate = None
        templateFiles = [os.path.basename(name) for name in glob.glob(os.path.join(self.settingsPath, '*.ini')) if os.path.isfile(os.path.join(self.settingsPath, name))]
        dialogsToLoad = None
        
        if tabName == 'Low Emission Development Analysis':
            dialogsToLoad = (
                'DialogLumensSCIENDOHistoricalBaselineProjection',
                'DialogLumensSCIENDOHistoricalBaselineAnnualProjection',
                'DialogLumensSCIENDODriversAnalysis',
                'DialogLumensSCIENDOBuildScenario',
            )
        elif tabName == 'Land Use Change Modeling':
            dialogsToLoad = (
                'DialogLumensSCIENDOCalculateTransitionMatrix',
            )
        
        for templateFile in templateFiles:
            if templateFile == templateToSkip:
                continue
            
            duplicateTemplate = templateFile
            templateSettings = self.loadTemplate(tabName, templateFile, True)
            
            print 'DEBUG'
            print templateFile, templateSettings
            
            # Loop thru all dialogs in a tab
            for dialog in dialogsToLoad:
                # Loop thru all settings in a dialog
                for key, val in self.main.appSettings[dialog].iteritems():
                    if templateSettings[dialog][key] != val:
                        # A setting doesn't match! This is not a matching template file, move along
                        duplicateTemplate = None
                    else:
                        print 'DEBUG equal settings'
                        print templateSettings[dialog][key], val
        
        # Found a duplicate template, offer to load it?
        if duplicateTemplate:
            reply = QtGui.QMessageBox.question(
                self,
                'Load Existing Template',
                'The template you are about to save matches an existing template.\nDo you want to load \'{0}\' instead?'.format(duplicateTemplate),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
            if reply == QtGui.QMessageBox.Yes:
                if tabName == 'Low Emission Development Analysis':
                    self.handlerLoadLowEmissionDevelopmentAnalysisTemplate(duplicateTemplate)
                elif tabName == 'Land Use Change Modeling':
                    self.handlerLoadLandUseChangeModelingTemplate(duplicateTemplate)
                
                return True
        
        return False
    
    
    def saveTemplate(self, tabName, fileName):
        """Method for saving the form values based on the associated tab and dialog to a template file.
        
        Args:
            tabName (str): the tab with the form values to save.
            fileName (str): the target template file name to create.
        """
        self.setAppSettings()
        
        # Check if current form values duplicate an existing template
        if not self.checkForDuplicateTemplates(tabName, fileName):
            templateFilePath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderSCIENDO'], fileName)
            settings = QtCore.QSettings(templateFilePath, QtCore.QSettings.IniFormat)
            settings.setFallbacksEnabled(True) # only use ini files
            
            dialogsToSave = None
            
            if tabName == 'Low Emission Development Analysis':
                dialogsToSave = (
                    'DialogLumensSCIENDOHistoricalBaselineProjection',
                    'DialogLumensSCIENDOHistoricalBaselineAnnualProjection',
                    'DialogLumensSCIENDODriversAnalysis',
                    'DialogLumensSCIENDOBuildScenario',
                )
            elif tabName == 'Land Use Change Modeling':
                dialogsToSave = (
                    'DialogLumensSCIENDOCalculateTransitionMatrix',
                )
            
            settings.beginGroup(tabName)
            for dialog in dialogsToSave:
                settings.beginGroup(dialog)
                for key, val in self.main.appSettings[dialog].iteritems():
                    settings.setValue(key, val)
                settings.endGroup()
            settings.endGroup()
            
            # Log to history log
            logging.getLogger(self.historyLog).info('Saved template: %s', fileName)
    
    
    def __init__(self, parent):
        super(DialogLumensSCIENDO, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = 'LUMENS SCIENDO'
        self.checkBoxQUESCDatabaseCount = 0
        self.listOfQUESCDatabase = []
        self.settingsPath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderSCIENDO'])
        self.currentLowEmissionDevelopmentAnalysisTemplate = None
        self.currentLandUseChangeModelingTemplate = None
        
        # Init logging
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLumensSCIENDO init'
            self.logger = logging.getLogger(type(self).__name__)
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            fh = logging.FileHandler(os.path.join(self.main.appSettings['appDir'], 'logs', type(self).__name__ + '.log'))
            fh.setFormatter(formatter)
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)
            self.logger.setLevel(logging.DEBUG)
        
        self.setupUi(self)
        
        # History log
        self.historyLog = '{0}{1}'.format('history', type(self).__name__)
        self.historyLogPath = os.path.join(self.settingsPath, self.historyLog + '.log')
        self.historyLogger = logging.getLogger(self.historyLog)
        fh = logging.FileHandler(self.historyLogPath)
        fh.setFormatter(formatter)
        self.log_box.setFormatter(formatter)
        self.historyLogger.addHandler(fh)
        self.historyLogger.addHandler(self.log_box)
        self.historyLogger.setLevel(logging.INFO)
        
        self.loadHistoryLog()
        
        self.loadTemplateFiles()
        
        self.tabWidget.currentChanged.connect(self.handlerTabWidgetChanged)
        
        # 'Low Emission Development Analysis' tab checkboxes
        self.checkBoxHistoricalBaselineProjection.toggled.connect(self.toggleHistoricalBaselineProjection)
        self.checkBoxHistoricalBaselineAnnualProjection.toggled.connect(self.toggleHistoricalBaselineAnnualProjection)
        self.checkBoxDriversAnalysis.toggled.connect(self.toggleDriversAnalysis)
        self.checkBoxBuildScenario.toggled.connect(self.toggleBuildScenario)
        
        # 'Low Emission Development Analysis' tab buttons
        self.buttonSelectDriversAnalysisLandUseCoverChangeDrivers.clicked.connect(self.handlerSelectDriversAnalysisLandUseCoverChangeDrivers)
        self.buttonSelectBuildScenarioHistoricalBaselineCar.clicked.connect(self.handlerSelectBuildScenarioHistoricalBaselineCar)
        self.buttonProcessLowEmissionDevelopmentAnalysis.clicked.connect(self.handlerProcessLowEmissionDevelopmentAnalysis)
        self.buttonHelpSCIENDOLowEmissionDevelopmentAnalysis.clicked.connect(lambda:self.handlerDialogHelp('SCIENDO'))
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.clicked.connect(self.handlerLoadLowEmissionDevelopmentAnalysisTemplate)
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.clicked.connect(self.handlerSaveLowEmissionDevelopmentAnalysisTemplate)
        self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate.clicked.connect(self.handlerSaveAsLowEmissionDevelopmentAnalysisTemplate)
        
        # 'Land Use Change Modeling' tab buttons
        self.buttonSelectLandUseChangeModelingFactorsDir.clicked.connect(self.handlerSelectLandUseChangeModelingFactorsDir)
        self.buttonSelectLandUseChangeModelingLandUseLookup.clicked.connect(self.handlerSelectLandUseChangeModelingLandUseLookup)
        self.buttonProcessLandUseChangeModeling.clicked.connect(self.handlerProcessLandUseChangeModeling)
        self.buttonHelpSCIENDOLandUseChangeModeling.clicked.connect(lambda:self.handlerDialogHelp('SCIENDO'))
        self.buttonLoadLandUseChangeModelingTemplate.clicked.connect(self.handlerLoadLandUseChangeModelingTemplate)
        self.buttonSaveLandUseChangeModelingTemplate.clicked.connect(self.handlerSaveLandUseChangeModelingTemplate)
        self.buttonSaveAsLandUseChangeModelingTemplate.clicked.connect(self.handlerSaveAsLandUseChangeModelingTemplate)
    
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.setStyleSheet('QDialog { background-color: #222; } QMessageBox QLabel{ color: #fff; }')
        self.dialogLayout = QtGui.QVBoxLayout()
        self.tabWidget = QtGui.QTabWidget()
        tabWidgetStylesheet = """
        QTabWidget::pane {
            border: none;
            background-color: #fff;
        }
        QTabBar::tab {
            background-color: #222;
            color: #fff;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: #fff;
            color: #000;
        }
        """
        self.tabWidget.setStyleSheet(tabWidgetStylesheet)
        
        self.tabLowEmissionDevelopmentAnalysis = QtGui.QWidget()
        self.tabLandUseChangeModeling = QtGui.QWidget()
        self.tabCropSimulation = QtGui.QWidget()
        self.tabLog = QtGui.QWidget()
        
        self.tabWidget.addTab(self.tabLowEmissionDevelopmentAnalysis, 'Low Emission Development Analysis')
        self.tabWidget.addTab(self.tabLandUseChangeModeling, 'Land Use Change Modeling')
        self.tabWidget.addTab(self.tabCropSimulation, 'Crop Simulation')
        self.tabWidget.addTab(self.tabLog, 'Log')
        
        ###self.layoutTabLowEmissionDevelopmentAnalysis = QtGui.QVBoxLayout()
        self.layoutTabLowEmissionDevelopmentAnalysis = QtGui.QGridLayout()
        ##self.layoutTabLandUseChangeModeling = QtGui.QVBoxLayout()
        self.layoutTabLandUseChangeModeling = QtGui.QGridLayout()
        self.layoutTabLog = QtGui.QVBoxLayout()
        
        self.tabLowEmissionDevelopmentAnalysis.setLayout(self.layoutTabLowEmissionDevelopmentAnalysis)
        self.tabLandUseChangeModeling.setLayout(self.layoutTabLandUseChangeModeling)
        self.tabLog.setLayout(self.layoutTabLog)
        
        self.dialogLayout.addWidget(self.tabWidget)
        
        #***********************************************************
        # Setup 'Low Emission Development Analysis' tab
        #***********************************************************
        # 'Historical baseline projection' GroupBox
        self.groupBoxHistoricalBaselineProjection = QtGui.QGroupBox('Historical baseline projection')
        self.layoutGroupBoxHistoricalBaselineProjection = QtGui.QHBoxLayout()
        self.groupBoxHistoricalBaselineProjection.setLayout(self.layoutGroupBoxHistoricalBaselineProjection)
        self.layoutOptionsHistoricalBaselineProjection = QtGui.QVBoxLayout()
        self.layoutOptionsHistoricalBaselineProjection.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsHistoricalBaselineProjection = QtGui.QWidget()
        self.contentOptionsHistoricalBaselineProjection.setLayout(self.layoutOptionsHistoricalBaselineProjection)
        self.layoutOptionsHistoricalBaselineProjection.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxHistoricalBaselineProjection = QtGui.QCheckBox()
        self.checkBoxHistoricalBaselineProjection.setChecked(False)
        self.contentOptionsHistoricalBaselineProjection.setDisabled(True)
        self.layoutGroupBoxHistoricalBaselineProjection.addWidget(self.checkBoxHistoricalBaselineProjection)
        self.layoutGroupBoxHistoricalBaselineProjection.addWidget(self.contentOptionsHistoricalBaselineProjection)
        self.layoutGroupBoxHistoricalBaselineProjection.insertStretch(2, 1)
        self.layoutGroupBoxHistoricalBaselineProjection.setAlignment(self.checkBoxHistoricalBaselineProjection, QtCore.Qt.AlignTop)
        self.layoutHistoricalBaselineProjectionInfo = QtGui.QVBoxLayout()
        self.layoutHistoricalBaselineProjection = QtGui.QGridLayout()
        self.layoutOptionsHistoricalBaselineProjection.addLayout(self.layoutHistoricalBaselineProjectionInfo)
        self.layoutOptionsHistoricalBaselineProjection.addLayout(self.layoutHistoricalBaselineProjection)
        
        self.labelHistoricalBaselineProjectionInfo = QtGui.QLabel()
        self.labelHistoricalBaselineProjectionInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutHistoricalBaselineProjectionInfo.addWidget(self.labelHistoricalBaselineProjectionInfo)
        
        self.labelHistoricalBaselineProjectionQUESCDatabase = QtGui.QLabel()
        self.labelHistoricalBaselineProjectionQUESCDatabase.setText('QUES-C Database:')
        self.layoutHistoricalBaselineProjection.addWidget(self.labelHistoricalBaselineProjectionQUESCDatabase, 0, 0)
        
        self.comboBoxHistoricalBaselineProjectionQUESCDatabase = QtGui.QComboBox()
        self.comboBoxHistoricalBaselineProjectionQUESCDatabase.setDisabled(True)
        self.layoutHistoricalBaselineProjection.addWidget(self.comboBoxHistoricalBaselineProjectionQUESCDatabase, 0, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxHistoricalBaselineProjectionQUESCDatabase)
        
        self.labelHistoricalBaselineProjectionIteration = QtGui.QLabel()
        self.labelHistoricalBaselineProjectionIteration.setText('&Iteration:')
        self.layoutHistoricalBaselineProjection.addWidget(self.labelHistoricalBaselineProjectionIteration, 1, 0)
        
        self.spinBoxHistoricalBaselineProjectionIteration = QtGui.QSpinBox()
        self.spinBoxHistoricalBaselineProjectionIteration.setRange(1, 99)
        self.spinBoxHistoricalBaselineProjectionIteration.setValue(3)
        self.layoutHistoricalBaselineProjection.addWidget(self.spinBoxHistoricalBaselineProjectionIteration, 1, 1)
        self.labelHistoricalBaselineProjectionIteration.setBuddy(self.spinBoxHistoricalBaselineProjectionIteration) 
        
        # 'Historical baseline annual projection' GroupBox
        self.groupBoxHistoricalBaselineAnnualProjection = QtGui.QGroupBox('Historical baseline annual projection')
        self.layoutGroupBoxHistoricalBaselineAnnualProjection = QtGui.QHBoxLayout()
        self.groupBoxHistoricalBaselineAnnualProjection.setLayout(self.layoutGroupBoxHistoricalBaselineAnnualProjection)
        self.layoutOptionsHistoricalBaselineAnnualProjection = QtGui.QVBoxLayout()
        self.layoutOptionsHistoricalBaselineAnnualProjection.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsHistoricalBaselineAnnualProjection = QtGui.QWidget()
        self.contentOptionsHistoricalBaselineAnnualProjection.setLayout(self.layoutOptionsHistoricalBaselineAnnualProjection)
        self.layoutOptionsHistoricalBaselineAnnualProjection.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxHistoricalBaselineAnnualProjection = QtGui.QCheckBox()
        self.checkBoxHistoricalBaselineAnnualProjection.setChecked(False)
        self.contentOptionsHistoricalBaselineAnnualProjection.setDisabled(True)
        self.layoutGroupBoxHistoricalBaselineAnnualProjection.addWidget(self.checkBoxHistoricalBaselineAnnualProjection)
        self.layoutGroupBoxHistoricalBaselineAnnualProjection.addWidget(self.contentOptionsHistoricalBaselineAnnualProjection)
        self.layoutGroupBoxHistoricalBaselineAnnualProjection.insertStretch(2, 1)
        self.layoutGroupBoxHistoricalBaselineAnnualProjection.setAlignment(self.checkBoxHistoricalBaselineAnnualProjection, QtCore.Qt.AlignTop)
        self.layoutHistoricalBaselineAnnualProjectionInfo = QtGui.QVBoxLayout()
        self.layoutHistoricalBaselineAnnualProjection = QtGui.QGridLayout()
        self.layoutOptionsHistoricalBaselineAnnualProjection.addLayout(self.layoutHistoricalBaselineAnnualProjectionInfo)
        self.layoutOptionsHistoricalBaselineAnnualProjection.addLayout(self.layoutHistoricalBaselineAnnualProjection)
        
        self.labelHistoricalBaselineAnnualProjectionInfo = QtGui.QLabel()
        self.labelHistoricalBaselineAnnualProjectionInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutHistoricalBaselineAnnualProjectionInfo.addWidget(self.labelHistoricalBaselineAnnualProjectionInfo)
        
        self.labelHistoricalBaselineAnnualProjectionIteration = QtGui.QLabel()
        self.labelHistoricalBaselineAnnualProjectionIteration.setText('&Iteration:')
        self.layoutHistoricalBaselineAnnualProjection.addWidget(self.labelHistoricalBaselineAnnualProjectionIteration, 0, 0)
        
        self.spinBoxHistoricalBaselineAnnualProjectionIteration = QtGui.QSpinBox()
        self.spinBoxHistoricalBaselineAnnualProjectionIteration.setRange(1, 9999)
        self.spinBoxHistoricalBaselineAnnualProjectionIteration.setValue(5)
        self.layoutHistoricalBaselineAnnualProjection.addWidget(self.spinBoxHistoricalBaselineAnnualProjectionIteration, 0, 1)
        self.labelHistoricalBaselineAnnualProjectionIteration.setBuddy(self.spinBoxHistoricalBaselineAnnualProjectionIteration)
        
        self.populateQUESCDatabase()

        # 'Drivers analysis' GroupBox
        self.groupBoxDriversAnalysis = QtGui.QGroupBox('Drivers analysis')
        self.layoutGroupBoxDriversAnalysis = QtGui.QHBoxLayout()
        self.groupBoxDriversAnalysis.setLayout(self.layoutGroupBoxDriversAnalysis)
        self.layoutOptionsDriversAnalysis = QtGui.QVBoxLayout()
        self.layoutOptionsDriversAnalysis.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsDriversAnalysis = QtGui.QWidget()
        self.contentOptionsDriversAnalysis.setLayout(self.layoutOptionsDriversAnalysis)
        self.layoutOptionsDriversAnalysis.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxDriversAnalysis = QtGui.QCheckBox()
        self.checkBoxDriversAnalysis.setChecked(False)
        self.contentOptionsDriversAnalysis.setDisabled(True)
        self.layoutGroupBoxDriversAnalysis.addWidget(self.checkBoxDriversAnalysis)
        self.layoutGroupBoxDriversAnalysis.addWidget(self.contentOptionsDriversAnalysis)
        self.layoutGroupBoxDriversAnalysis.setAlignment(self.checkBoxDriversAnalysis, QtCore.Qt.AlignTop)
        self.layoutDriversAnalysisInfo = QtGui.QVBoxLayout()
        self.layoutDriversAnalysis = QtGui.QGridLayout()
        self.layoutOptionsDriversAnalysis.addLayout(self.layoutDriversAnalysisInfo)
        self.layoutOptionsDriversAnalysis.addLayout(self.layoutDriversAnalysis)
        
        self.labelDriversAnalysisInfo = QtGui.QLabel()
        self.labelDriversAnalysisInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutDriversAnalysisInfo.addWidget(self.labelDriversAnalysisInfo)
        
        self.labelDriversAnalysisLandUseCoverChangeDrivers = QtGui.QLabel()
        self.labelDriversAnalysisLandUseCoverChangeDrivers.setText('Drivers of land use/cover change:')
        self.layoutDriversAnalysis.addWidget(self.labelDriversAnalysisLandUseCoverChangeDrivers, 0, 0)
        
        self.lineEditDriversAnalysisLandUseCoverChangeDrivers = QtGui.QLineEdit()
        self.lineEditDriversAnalysisLandUseCoverChangeDrivers.setReadOnly(True)
        self.layoutDriversAnalysis.addWidget(self.lineEditDriversAnalysisLandUseCoverChangeDrivers, 0, 1)
        
        self.buttonSelectDriversAnalysisLandUseCoverChangeDrivers = QtGui.QPushButton()
        self.buttonSelectDriversAnalysisLandUseCoverChangeDrivers.setText('&Browse')
        self.layoutDriversAnalysis.addWidget(self.buttonSelectDriversAnalysisLandUseCoverChangeDrivers, 0, 2)
        
        self.labelDriversAnalysislandUseCoverChangeType = QtGui.QLabel()
        self.labelDriversAnalysislandUseCoverChangeType.setText('Land use/cover change type:')
        self.layoutDriversAnalysis.addWidget(self.labelDriversAnalysislandUseCoverChangeType, 1, 0)
        
        self.lineEditDriversAnalysisLandUseCoverChangeType = QtGui.QLineEdit()
        self.lineEditDriversAnalysisLandUseCoverChangeType.setText('Land use change')
        self.layoutDriversAnalysis.addWidget(self.lineEditDriversAnalysisLandUseCoverChangeType, 1, 1)
        self.labelDriversAnalysislandUseCoverChangeType.setBuddy(self.lineEditDriversAnalysisLandUseCoverChangeType)
        
        # 'Build scenario' GroupBox
        self.groupBoxBuildScenario = QtGui.QGroupBox('Build scenario')
        self.layoutGroupBoxBuildScenario = QtGui.QHBoxLayout()
        self.groupBoxBuildScenario.setLayout(self.layoutGroupBoxBuildScenario)
        self.layoutOptionsBuildScenario = QtGui.QVBoxLayout()
        self.layoutOptionsBuildScenario.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsBuildScenario = QtGui.QWidget()
        self.contentOptionsBuildScenario.setLayout(self.layoutOptionsBuildScenario)
        self.layoutOptionsBuildScenario.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxBuildScenario = QtGui.QCheckBox()
        self.checkBoxBuildScenario.setChecked(False)
        self.contentOptionsBuildScenario.setDisabled(True)
        self.layoutGroupBoxBuildScenario.addWidget(self.checkBoxBuildScenario)
        self.layoutGroupBoxBuildScenario.addWidget(self.contentOptionsBuildScenario)
        self.layoutGroupBoxBuildScenario.setAlignment(self.checkBoxBuildScenario, QtCore.Qt.AlignTop)
        self.layoutBuildScenarioInfo = QtGui.QVBoxLayout()
        self.layoutBuildScenario = QtGui.QGridLayout()
        self.layoutOptionsBuildScenario.addLayout(self.layoutBuildScenarioInfo)
        self.layoutOptionsBuildScenario.addLayout(self.layoutBuildScenario)
        
        self.labelBuildScenarioInfo = QtGui.QLabel()
        self.labelBuildScenarioInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutBuildScenarioInfo.addWidget(self.labelBuildScenarioInfo)
        
        self.labelBuildScenarioHistoricalBaselineCar = QtGui.QLabel()
        self.labelBuildScenarioHistoricalBaselineCar.setText('Historical baseline car:')
        self.layoutBuildScenario.addWidget(self.labelBuildScenarioHistoricalBaselineCar, 0, 0)
        
        self.lineEditBuildScenarioHistoricalBaselineCar = QtGui.QLineEdit()
        self.lineEditBuildScenarioHistoricalBaselineCar.setReadOnly(True)
        self.layoutBuildScenario.addWidget(self.lineEditBuildScenarioHistoricalBaselineCar, 0, 1)
        
        self.buttonSelectBuildScenarioHistoricalBaselineCar = QtGui.QPushButton()
        self.buttonSelectBuildScenarioHistoricalBaselineCar.setText('&Browse')
        self.layoutBuildScenario.addWidget(self.buttonSelectBuildScenarioHistoricalBaselineCar, 0, 2)
        
        # Process tab button
        self.layoutButtonLowEmissionDevelopmentAnalysis = QtGui.QHBoxLayout()
        self.buttonProcessLowEmissionDevelopmentAnalysis = QtGui.QPushButton()
        self.buttonProcessLowEmissionDevelopmentAnalysis.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonProcessLowEmissionDevelopmentAnalysis.setText('&Process')
        icon = QtGui.QIcon(':/ui/icons/iconActionHelp.png')
        self.buttonHelpSCIENDOLowEmissionDevelopmentAnalysis = QtGui.QPushButton()
        self.buttonHelpSCIENDOLowEmissionDevelopmentAnalysis.setIcon(icon)
        self.layoutButtonLowEmissionDevelopmentAnalysis.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonLowEmissionDevelopmentAnalysis.addWidget(self.buttonProcessLowEmissionDevelopmentAnalysis)
        self.layoutButtonLowEmissionDevelopmentAnalysis.addWidget(self.buttonHelpSCIENDOLowEmissionDevelopmentAnalysis)
        
        # Template GroupBox
        self.groupBoxLowEmissionDevelopmentAnalysisTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLowEmissionDevelopmentAnalysisTemplate.setLayout(self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate)
        self.layoutLowEmissionDevelopmentAnalysisTemplateInfo = QtGui.QVBoxLayout()
        self.layoutLowEmissionDevelopmentAnalysisTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate.addLayout(self.layoutLowEmissionDevelopmentAnalysisTemplateInfo)
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate.addLayout(self.layoutLowEmissionDevelopmentAnalysisTemplate)
        
        self.labelLoadedLowEmissionDevelopmentAnalysisTemplate = QtGui.QLabel()
        self.labelLoadedLowEmissionDevelopmentAnalysisTemplate.setText('Loaded template:')
        self.layoutLowEmissionDevelopmentAnalysisTemplate.addWidget(self.labelLoadedLowEmissionDevelopmentAnalysisTemplate, 0, 0)
        
        self.loadedLowEmissionDevelopmentAnalysisTemplate = QtGui.QLabel()
        self.loadedLowEmissionDevelopmentAnalysisTemplate.setText('<None>')
        self.layoutLowEmissionDevelopmentAnalysisTemplate.addWidget(self.loadedLowEmissionDevelopmentAnalysisTemplate, 0, 1)
        
        self.labelLowEmissionDevelopmentAnalysisTemplate = QtGui.QLabel()
        self.labelLowEmissionDevelopmentAnalysisTemplate.setText('Template name:')
        self.layoutLowEmissionDevelopmentAnalysisTemplate.addWidget(self.labelLowEmissionDevelopmentAnalysisTemplate, 1, 0)
        
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate = QtGui.QComboBox()
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.addItem('No template found')
        self.layoutLowEmissionDevelopmentAnalysisTemplate.addWidget(self.comboBoxLowEmissionDevelopmentAnalysisTemplate, 1, 1)
        
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate = QtGui.QHBoxLayout()
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate = QtGui.QPushButton()
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setText('Load')
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate = QtGui.QPushButton()
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.setText('Save')
        self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate = QtGui.QPushButton()
        self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate.setText('Save As')
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate.addWidget(self.buttonLoadLowEmissionDevelopmentAnalysisTemplate)
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate.addWidget(self.buttonSaveLowEmissionDevelopmentAnalysisTemplate)
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate.addWidget(self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate)
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate.addLayout(self.layoutButtonLowEmissionDevelopmentAnalysisTemplate)
        
        # Place the GroupBoxes
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxHistoricalBaselineProjection, 0, 0)
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxHistoricalBaselineAnnualProjection, 1, 0)
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxDriversAnalysis, 2, 0)
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxBuildScenario, 3, 0)
        self.layoutTabLowEmissionDevelopmentAnalysis.addLayout(self.layoutButtonLowEmissionDevelopmentAnalysis, 4, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxLowEmissionDevelopmentAnalysisTemplate, 0, 1, 4, 1)
        self.layoutTabLowEmissionDevelopmentAnalysis.setColumnStretch(0, 3)
        self.layoutTabLowEmissionDevelopmentAnalysis.setColumnStretch(1, 1) # Smaller template column
        
        #***********************************************************
        # Setup 'Land Use Change Modeling' tab
        #***********************************************************
        # 'Raster Cube' GroupBox
        self.groupBoxCreateRasterCubeOfFactors = QtGui.QGroupBox('Create raster cube of factors')
        self.layoutGroupBoxCreateRasterCubeOfFactors = QtGui.QVBoxLayout()
        self.layoutGroupBoxCreateRasterCubeOfFactors.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxCreateRasterCubeOfFactors.setLayout(self.layoutGroupBoxCreateRasterCubeOfFactors)
        self.layoutCreateRasterCubeOfFactorsInfo = QtGui.QVBoxLayout()
        self.layoutCreateRasterCubeOfFactors = QtGui.QVBoxLayout()
        self.layoutGroupBoxCreateRasterCubeOfFactors.addLayout(self.layoutCreateRasterCubeOfFactorsInfo)
        self.layoutGroupBoxCreateRasterCubeOfFactors.addLayout(self.layoutCreateRasterCubeOfFactors)
        
        self.labelCreateRasterCubeOfFactorsInfo = QtGui.QLabel()
        self.labelCreateRasterCubeOfFactorsInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutCreateRasterCubeOfFactorsInfo.addWidget(self.labelCreateRasterCubeOfFactorsInfo)
        
        self.layoutButtonAddFactor = QtGui.QHBoxLayout()
        self.layoutButtonAddFactor.setContentsMargins(0, 0, 0, 0)
        self.layoutButtonAddFactor.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.buttonAddFactorRow = QtGui.QPushButton()
        self.buttonAddFactorRow.setText('Add Factor')
        self.buttonAddFactorRow.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.layoutButtonAddFactor.addWidget(self.buttonAddFactorRow)
        
        self.layoutContentAddFactor = QtGui.QVBoxLayout()
        self.layoutContentAddFactor.setContentsMargins(5, 5, 5, 5)
        self.contentAddFactor = QtGui.QWidget()
        self.contentAddFactor.setLayout(self.layoutContentAddFactor)
        self.scrollAddFactor = QtGui.QScrollArea()
        self.scrollAddFactor.setWidgetResizable(True)
        self.scrollAddFactor.setWidget(self.contentAddFactor)
        self.layoutTableAddFactor = QtGui.QVBoxLayout()
        self.layoutTableAddFactor.setAlignment(QtCore.Qt.AlignTop)
        self.layoutContentAddFactor.addLayout(self.layoutTableAddFactor)
        
        self.layoutCreateRasterCubeOfFactors.addLayout(self.layoutButtonAddFactor)
        self.layoutCreateRasterCubeOfFactors.addWidget(self.scrollAddFactor)
        
        # 'Functions' GroupBox
        self.groupBoxLandUseChangeModelingFunctions = QtGui.QGroupBox('Functions')
        self.layoutGroupBoxLandUseChangeModelingFunctions = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeModelingFunctions.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeModelingFunctions.setLayout(self.layoutGroupBoxLandUseChangeModelingFunctions)
        self.layoutLandUseChangeModelingFunctionsInfo = QtGui.QVBoxLayout()
        self.layoutLandUseChangeModelingFunctions = QtGui.QGridLayout()
        self.layoutGroupBoxLandUseChangeModelingFunctions.addLayout(self.layoutLandUseChangeModelingFunctionsInfo)
        self.layoutGroupBoxLandUseChangeModelingFunctions.addLayout(self.layoutLandUseChangeModelingFunctions)
        
        self.labelLandUseChangeModelingFunctionsInfo = QtGui.QLabel()
        self.labelLandUseChangeModelingFunctionsInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutLandUseChangeModelingFunctionsInfo.addWidget(self.labelLandUseChangeModelingFunctionsInfo)
        
        self.checkBoxCalculateTransitionMatrix = QtGui.QCheckBox('Calculate transition matrix')
        self.checkBoxCreateRasterCubeOfFactors = QtGui.QCheckBox('Create raster cube of factors')
        self.checkBoxCalculateWeightOfEvidence = QtGui.QCheckBox('Calculate weight of evidence')
        self.checkBoxSimulateLandUseChange = QtGui.QCheckBox('Simulate land use change')
        self.checkBoxSimulateWithScenario = QtGui.QCheckBox('Simulate with scenario')
        
        self.layoutLandUseChangeModelingFunctions.addWidget(self.checkBoxCalculateTransitionMatrix)
        self.layoutLandUseChangeModelingFunctions.addWidget(self.checkBoxCreateRasterCubeOfFactors)
        self.layoutLandUseChangeModelingFunctions.addWidget(self.checkBoxCalculateWeightOfEvidence)
        self.layoutLandUseChangeModelingFunctions.addWidget(self.checkBoxSimulateLandUseChange)
        self.layoutLandUseChangeModelingFunctions.addWidget(self.checkBoxSimulateWithScenario)
        
        # 'Parameters' GroupBox
        self.groupBoxLandUseChangeModelingParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxLandUseChangeModelingParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeModelingParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeModelingParameters.setLayout(self.layoutGroupBoxLandUseChangeModelingParameters)
        self.layoutLandUseChangeModelingParametersInfo = QtGui.QVBoxLayout()
        self.layoutLandUseChangeModelingParameters = QtGui.QGridLayout()
        self.layoutGroupBoxLandUseChangeModelingParameters.addLayout(self.layoutLandUseChangeModelingParametersInfo)
        self.layoutGroupBoxLandUseChangeModelingParameters.addLayout(self.layoutLandUseChangeModelingParameters)
        
        self.labelLandUseChangeModelingParametersInfo = QtGui.QLabel()
        self.labelLandUseChangeModelingParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutLandUseChangeModelingParametersInfo.addWidget(self.labelLandUseChangeModelingParametersInfo)
        
        self.labelLandUseChangeModelingFactorsDir = QtGui.QLabel()
        self.labelLandUseChangeModelingFactorsDir.setText('Factors directory:')
        self.layoutLandUseChangeModelingParameters.addWidget(self.labelLandUseChangeModelingFactorsDir, 0, 0)
        
        self.lineEditLandUseChangeModelingFactorsDir = QtGui.QLineEdit()
        self.lineEditLandUseChangeModelingFactorsDir.setReadOnly(True)
        self.layoutLandUseChangeModelingParameters.addWidget(self.lineEditLandUseChangeModelingFactorsDir, 0, 1)
        
        self.buttonSelectLandUseChangeModelingFactorsDir = QtGui.QPushButton()
        self.buttonSelectLandUseChangeModelingFactorsDir.setText('&Browse')
        self.layoutLandUseChangeModelingParameters.addWidget(self.buttonSelectLandUseChangeModelingFactorsDir, 0, 2)
        
        self.labelLandUseChangeModelingLandUseLookup = QtGui.QLabel()
        self.labelLandUseChangeModelingLandUseLookup.setText('Land use lookup table:')
        self.layoutLandUseChangeModelingParameters.addWidget(self.labelLandUseChangeModelingLandUseLookup, 1, 0)
        
        self.lineEditLandUseChangeModelingLandUseLookup = QtGui.QLineEdit()
        self.lineEditLandUseChangeModelingLandUseLookup.setReadOnly(True)
        self.layoutLandUseChangeModelingParameters.addWidget(self.lineEditLandUseChangeModelingLandUseLookup, 1, 1)
        
        self.buttonSelectLandUseChangeModelingLandUseLookup = QtGui.QPushButton()
        self.buttonSelectLandUseChangeModelingLandUseLookup.setText('&Browse')
        self.layoutLandUseChangeModelingParameters.addWidget(self.buttonSelectLandUseChangeModelingLandUseLookup, 1, 2)
        
        self.labelLandUseChangeModelingBaseYear = QtGui.QLabel()
        self.labelLandUseChangeModelingBaseYear.setText('Base &year:')
        self.layoutLandUseChangeModelingParameters.addWidget(self.labelLandUseChangeModelingBaseYear, 2, 0)
        
        self.spinBoxLandUseChangeModelingBaseYear = QtGui.QSpinBox()
        self.spinBoxLandUseChangeModelingBaseYear.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxLandUseChangeModelingBaseYear.setValue(td.year)
        self.layoutLandUseChangeModelingParameters.addWidget(self.spinBoxLandUseChangeModelingBaseYear, 2, 1)
        self.labelLandUseChangeModelingBaseYear.setBuddy(self.spinBoxLandUseChangeModelingBaseYear)
        
        self.labelLandUseChangeModelingLocation = QtGui.QLabel()
        self.labelLandUseChangeModelingLocation.setText('Location:')
        self.layoutLandUseChangeModelingParameters.addWidget(self.labelLandUseChangeModelingLocation, 3, 0)
        
        self.lineEditLandUseChangeModelingLocation = QtGui.QLineEdit()
        self.lineEditLandUseChangeModelingLocation.setText('location')
        self.layoutLandUseChangeModelingParameters.addWidget(self.lineEditLandUseChangeModelingLocation, 3, 1)
        self.labelLandUseChangeModelingLocation.setBuddy(self.lineEditLandUseChangeModelingLocation)
        
        # Process tab button
        self.layoutButtonLandUseChangeModeling = QtGui.QHBoxLayout()
        self.buttonProcessLandUseChangeModeling = QtGui.QPushButton()
        self.buttonProcessLandUseChangeModeling.setText('&Process')
        self.buttonHelpSCIENDOLandUseChangeModeling = QtGui.QPushButton()
        self.buttonHelpSCIENDOLandUseChangeModeling.setIcon(icon)
        self.layoutButtonLandUseChangeModeling.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonLandUseChangeModeling.addWidget(self.buttonProcessLandUseChangeModeling)
        self.layoutButtonLandUseChangeModeling.addWidget(self.buttonHelpSCIENDOLandUseChangeModeling)
        
        # Template GroupBox
        self.groupBoxLandUseChangeModelingTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxLandUseChangeModelingTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeModelingTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeModelingTemplate.setLayout(self.layoutGroupBoxLandUseChangeModelingTemplate)
        self.layoutLandUseChangeModelingTemplateInfo = QtGui.QVBoxLayout()
        self.layoutLandUseChangeModelingTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxLandUseChangeModelingTemplate.addLayout(self.layoutLandUseChangeModelingTemplateInfo)
        self.layoutGroupBoxLandUseChangeModelingTemplate.addLayout(self.layoutLandUseChangeModelingTemplate)
        
        self.labelLoadedLandUseChangeModelingTemplate = QtGui.QLabel()
        self.labelLoadedLandUseChangeModelingTemplate.setText('Loaded template:')
        self.layoutLandUseChangeModelingTemplate.addWidget(self.labelLoadedLandUseChangeModelingTemplate, 0, 0)
        
        self.loadedLandUseChangeModelingTemplate = QtGui.QLabel()
        self.loadedLandUseChangeModelingTemplate.setText('<None>')
        self.layoutLandUseChangeModelingTemplate.addWidget(self.loadedLandUseChangeModelingTemplate, 0, 1)
        
        self.labelLandUseChangeModelingTemplate = QtGui.QLabel()
        self.labelLandUseChangeModelingTemplate.setText('Template name:')
        self.layoutLandUseChangeModelingTemplate.addWidget(self.labelLandUseChangeModelingTemplate, 1, 0)
        
        self.comboBoxLandUseChangeModelingTemplate = QtGui.QComboBox()
        self.comboBoxLandUseChangeModelingTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLandUseChangeModelingTemplate.setDisabled(True)
        self.comboBoxLandUseChangeModelingTemplate.addItem('No template found')
        self.layoutLandUseChangeModelingTemplate.addWidget(self.comboBoxLandUseChangeModelingTemplate, 1, 1)
        
        self.layoutButtonLandUseChangeModelingTemplate = QtGui.QHBoxLayout()
        self.layoutButtonLandUseChangeModelingTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadLandUseChangeModelingTemplate = QtGui.QPushButton()
        self.buttonLoadLandUseChangeModelingTemplate.setDisabled(True)
        self.buttonLoadLandUseChangeModelingTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadLandUseChangeModelingTemplate.setText('Load')
        self.buttonSaveLandUseChangeModelingTemplate = QtGui.QPushButton()
        self.buttonSaveLandUseChangeModelingTemplate.setDisabled(True)
        self.buttonSaveLandUseChangeModelingTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveLandUseChangeModelingTemplate.setText('Save')
        self.buttonSaveAsLandUseChangeModelingTemplate = QtGui.QPushButton()
        self.buttonSaveAsLandUseChangeModelingTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsLandUseChangeModelingTemplate.setText('Save As')
        self.layoutButtonLandUseChangeModelingTemplate.addWidget(self.buttonLoadLandUseChangeModelingTemplate)
        self.layoutButtonLandUseChangeModelingTemplate.addWidget(self.buttonSaveLandUseChangeModelingTemplate)
        self.layoutButtonLandUseChangeModelingTemplate.addWidget(self.buttonSaveAsLandUseChangeModelingTemplate)
        self.layoutGroupBoxLandUseChangeModelingTemplate.addLayout(self.layoutButtonLandUseChangeModelingTemplate)
        
        # Place the GroupBoxes
        self.layoutTabLandUseChangeModeling.addWidget(self.groupBoxCreateRasterCubeOfFactors, 0, 0)
        self.layoutTabLandUseChangeModeling.addWidget(self.groupBoxLandUseChangeModelingFunctions, 1, 0)
        self.layoutTabLandUseChangeModeling.addWidget(self.groupBoxLandUseChangeModelingParameters, 2, 0)
        self.layoutTabLandUseChangeModeling.addLayout(self.layoutButtonLandUseChangeModeling, 3, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabLandUseChangeModeling.addWidget(self.groupBoxLandUseChangeModelingTemplate, 0, 1, 3, 1)
        self.layoutTabLandUseChangeModeling.setColumnStretch(0, 3)
        self.layoutTabLandUseChangeModeling.setColumnStretch(1, 1) # Smaller template column
        
        #***********************************************************
        # Setup 'Log' tab
        #***********************************************************
        # 'History Log' GroupBox
        self.groupBoxHistoryLog = QtGui.QGroupBox('{0} {1}'.format(self.dialogTitle, 'history log'))
        self.layoutGroupBoxHistoryLog = QtGui.QVBoxLayout()
        self.layoutGroupBoxHistoryLog.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxHistoryLog.setLayout(self.layoutGroupBoxHistoryLog)
        self.layoutHistoryLogInfo = QtGui.QVBoxLayout()
        self.layoutHistoryLog = QtGui.QVBoxLayout()
        self.layoutGroupBoxHistoryLog.addLayout(self.layoutHistoryLogInfo)
        self.layoutGroupBoxHistoryLog.addLayout(self.layoutHistoryLog)
        
        self.labelHistoryLogInfo = QtGui.QLabel()
        self.labelHistoryLogInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutHistoryLogInfo.addWidget(self.labelHistoryLogInfo)
        
        self.log_box = QPlainTextEditLogger(self)
        self.layoutHistoryLog.addWidget(self.log_box.widget)
        
        self.layoutTabLog.addWidget(self.groupBoxHistoryLog)
        
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(700, 600)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Overload method that is called when the dialog widget is shown.
        
        Args:
            event (QShowEvent): the show widget event.
        """
        super(DialogLumensSCIENDO, self).showEvent(event)
    
    
    def closeEvent(self, event):
        """Overload method that is called when the dialog widget is closed.
        
        Args:
            event (QCloseEvent): the close widget event.
        """
        super(DialogLumensSCIENDO, self).closeEvent(event)
    
    
    def loadHistoryLog(self):
        """Method for loading the module history log file.
        """
        if os.path.exists(self.historyLogPath):
            logText = open(self.historyLogPath).read()
            self.log_box.widget.setPlainText(logText)
    
    
    def handlerTabWidgetChanged(self, index):
        """Slot method for scrolling the log to the latest output.
        
        Args:
            index (int): the current tab index.
        """
        if self.tabWidget.widget(index) == self.tabLog:
            self.log_box.widget.verticalScrollBar().triggerAction(QtGui.QAbstractSlider.SliderToMaximum)


    def populateQUESCDatabase(self):
        layoutCheckBoxQUESCDatabase = QtGui.QVBoxLayout()
        self.checkBoxQUESCDatabaseCount = 0
        if len(self.main.dataTable):
            dataTable = self.main.dataTable
            dataQUESCDatabase = []
            for value in dataTable.values():
                dataTableName = value[list(value)[0]]
                if 'QUESC_database_' in dataTableName:
                    dataQUESCDatabase.append(dataTableName)
            for name in dataQUESCDatabase:
                self.checkBoxQUESCDatabaseCount = self.checkBoxQUESCDatabaseCount + 1
                checkBoxHistoricalBaselineAnnualProjectionQUESCDatabase = QtGui.QCheckBox()
                checkBoxHistoricalBaselineAnnualProjectionQUESCDatabase.setObjectName('checkBoxHistoricalBaselineAnnualProjectionQUESCDatabase_{0}'.format(str(self.checkBoxQUESCDatabaseCount)))
                checkBoxHistoricalBaselineAnnualProjectionQUESCDatabase.setText(name)
                layoutCheckBoxQUESCDatabase.addWidget(checkBoxHistoricalBaselineAnnualProjectionQUESCDatabase)
                checkBoxHistoricalBaselineAnnualProjectionQUESCDatabase.toggled.connect(self.toggleHistoricalBaselineAnnualProjectionQUESCDatabase)
        else:
            labelQUESCDatabaseHistoricalBaselineAnnualProjection = QtGui.QLabel()
            labelQUESCDatabaseHistoricalBaselineAnnualProjection.setText('\nNo QUES-C Database found!\n')
            layoutCheckBoxQUESCDatabase.addWidget(labelQUESCDatabaseHistoricalBaselineAnnualProjection)
            
        self.layoutOptionsHistoricalBaselineAnnualProjection.addLayout(layoutCheckBoxQUESCDatabase)
                        
    
    #***********************************************************
    # 'Low Emission Development Analysis' tab QGroupBox toggle handlers
    #***********************************************************
    def toggleHistoricalBaselineProjection(self, checked):
        """Slot method for handling checkbox toggling.
        
        Args:
            checked (bool): the checkbox status.
        """
        if checked:
            self.contentOptionsHistoricalBaselineProjection.setEnabled(True)
        else:
            self.contentOptionsHistoricalBaselineProjection.setDisabled(True)
    
    
    def toggleHistoricalBaselineAnnualProjection(self, checked):
        """Slot method for handling checkbox toggling.
        
        Args:
            checked (bool): the checkbox status.
        """
        if checked:
            self.contentOptionsHistoricalBaselineAnnualProjection.setEnabled(True)
        else:
            self.contentOptionsHistoricalBaselineAnnualProjection.setDisabled(True)


    def toggleHistoricalBaselineAnnualProjectionQUESCDatabase(self, checked):
        """Slot method for handling checkbox toggling.
        
        Args:
            checked (bool): the checkbox status.
        """
        checkBoxSender = self.sender()
        objectName = checkBoxSender.objectName()
        checkBoxIndex = objectName.split('_')[1]
        
        checkBoxQUESCDatabase = self.contentOptionsHistoricalBaselineAnnualProjection.findChild(QtGui.QCheckBox, 'checkBoxHistoricalBaselineAnnualProjectionQUESCDatabase_' + checkBoxIndex)
        checkBoxName = checkBoxQUESCDatabase.text()
        
        if checked:
            self.listOfQUESCDatabase.append(checkBoxName)
        else:
            self.listOfQUESCDatabase.remove(checkBoxName)
    
    
    def toggleDriversAnalysis(self, checked):
        """Slot method for handling checkbox toggling.
        
        Args:
            checked (bool): the checkbox status.
        """
        if checked:
            self.contentOptionsDriversAnalysis.setEnabled(True)
        else:
            self.contentOptionsDriversAnalysis.setDisabled(True)
    
    
    def toggleBuildScenario(self, checked):
        """Slot method for handling checkbox toggling.
        
        Args:
            checked (bool): the checkbox status.
        """
        if checked:
            self.contentOptionsBuildScenario.setEnabled(True)
        else:
            self.contentOptionsBuildScenario.setDisabled(True)
    
    
    #***********************************************************
    # 'Low Emission Development Analysis' tab QPushButton handlers
    #***********************************************************
    def handlerLoadLowEmissionDevelopmentAnalysisTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxLowEmissionDevelopmentAnalysisTemplate.currentText()
        reply = None
        
        if fileName:
            templateFile = fileName
        else:
            reply = QtGui.QMessageBox.question(
                self,
                'Load Template',
                'Do you want to load \'{0}\'?'.format(templateFile),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
        if reply == QtGui.QMessageBox.Yes or fileName:
            self.loadTemplate('Low Emission Development Analysis', templateFile)
    
    
    def handlerSaveLowEmissionDevelopmentAnalysisTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentLowEmissionDevelopmentAnalysisTemplate
        
        if fileName:
            templateFile = fileName
        
        reply = QtGui.QMessageBox.question(
            self,
            'Save Template',
            'Do you want save \'{0}\'?\nThis action will overwrite the template file.'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
            
        if reply == QtGui.QMessageBox.Yes:
            self.saveTemplate('Low Emission Development Analysis', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsLowEmissionDevelopmentAnalysisTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveLowEmissionDevelopmentAnalysisTemplate(fileName)
            else:
                self.saveTemplate('Low Emission Development Analysis', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadLowEmissionDevelopmentAnalysisTemplate(fileName)
          
    
    def handlerSelectDriversAnalysisLandUseCoverChangeDrivers(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use/Cover Change Drivers', QtCore.QDir.homePath(), 'Land Use/Cover Change Drivers (*{0})'.format(self.main.appSettings['selectTextfileExt'])))
        
        if file:
            self.lineEditDriversAnalysisLandUseCoverChangeDrivers.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectBuildScenarioHistoricalBaselineCar(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Historical Baseline Car', QtCore.QDir.homePath(), 'Historical Baseline Car (*{0})'.format(self.main.appSettings['selectCarfileExt'])))
        
        if file:
            self.lineEditBuildScenarioHistoricalBaselineCar.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # 'Land Use Change Modeling' tab QPushButton handlers
    #***********************************************************
    def handlerLoadLandUseChangeModelingTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxLandUseChangeModelingTemplate.currentText()
        reply = None
        
        if fileName:
            templateFile = fileName
        else:
            reply = QtGui.QMessageBox.question(
                self,
                'Load Template',
                'Do you want to load \'{0}\'?'.format(templateFile),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
        if reply == QtGui.QMessageBox.Yes or fileName:
            self.loadTemplate('Land Use Change Modeling', templateFile)
    
    
    def handlerSaveLandUseChangeModelingTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentLandUseChangeModelingTemplate
        
        if fileName:
            templateFile = fileName
        
        reply = QtGui.QMessageBox.question(
            self,
            'Save Template',
            'Do you want save \'{0}\'?\nThis action will overwrite the template file.'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
            
        if reply == QtGui.QMessageBox.Yes:
            self.saveTemplate('Land Use Change Modeling', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsLandUseChangeModelingTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveLandUseChangeModelingTemplate(fileName)
            else:
                self.saveTemplate('Land Use Change Modeling', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadLandUseChangeModelingTemplate(fileName)
    
    
    def handlerSelectLandUseChangeModelingFactorsDir(self):
        """Slot method for a directory select dialog.
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Factors Directory'))
        
        if dir:
            self.lineEditLandUseChangeModelingFactorsDir.setText(dir)
            logging.getLogger(type(self).__name__).info('select directory: %s', dir)
    
    
    def handlerSelectLandUseChangeModelingLandUseLookup(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Lookup Table', QtCore.QDir.homePath(), 'Land Use Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandUseChangeModelingLandUseLookup.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # Process tabs
    #***********************************************************
    def setAppSettings(self):
        """Set the required values from the form widgets.
        """
        # 'Historical baseline projection' groupbox fields
        self.main.appSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['QUESCDatabase'] \
            = unicode(self.comboBoxHistoricalBaselineProjectionQUESCDatabase.currentText())
        self.main.appSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['iteration'] \
            = self.spinBoxHistoricalBaselineProjectionIteration.value()
        
        # 'Historical baseline annual projection' groupbox fields
        self.main.appSettings['DialogLumensSCIENDOHistoricalBaselineAnnualProjection']['iteration'] \
            = self.spinBoxHistoricalBaselineAnnualProjectionIteration.value()
        
        # 'Drivers analysis' groupbox fields
        self.main.appSettings['DialogLumensSCIENDODriversAnalysis']['landUseCoverChangeDrivers'] \
            = unicode(self.lineEditDriversAnalysisLandUseCoverChangeDrivers.text())
        self.main.appSettings['DialogLumensSCIENDODriversAnalysis']['landUseCoverChangeType'] \
            = unicode(self.lineEditDriversAnalysisLandUseCoverChangeType.text())
        
        # 'Build scenario' groupbox fields
        self.main.appSettings['DialogLumensSCIENDOBuildScenario']['historicalBaselineCar'] \
            = unicode(self.lineEditBuildScenarioHistoricalBaselineCar.text())
        
        # 'Land Use Change Modeling' tab fields
        self.main.appSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['factorsDir'] \
            = self.main.appSettings['DialogLumensSCIENDOCreateRasterCube']['factorsDir'] \
            = self.main.appSettings['DialogLumensSCIENDOCalculateWeightofEvidence']['factorsDir'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateLandUseChange']['factorsDir'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateWithScenario']['factorsDir'] \
            = unicode(self.lineEditLandUseChangeModelingFactorsDir.text()).replace(os.path.sep, '/')
        self.main.appSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['landUseLookup'] \
            = self.main.appSettings['DialogLumensSCIENDOCreateRasterCube']['landUseLookup'] \
            = self.main.appSettings['DialogLumensSCIENDOCalculateWeightofEvidence']['landUseLookup'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateLandUseChange']['landUseLookup'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateWithScenario']['landUseLookup'] \
            = unicode(self.lineEditLandUseChangeModelingLandUseLookup.text())
        self.main.appSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['baseYear'] \
            = self.main.appSettings['DialogLumensSCIENDOCreateRasterCube']['baseYear'] \
            = self.main.appSettings['DialogLumensSCIENDOCalculateWeightofEvidence']['baseYear'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateLandUseChange']['baseYear'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateWithScenario']['baseYear'] \
            = self.spinBoxLandUseChangeModelingBaseYear.value()
        self.main.appSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['location'] \
            = self.main.appSettings['DialogLumensSCIENDOCreateRasterCube']['location'] \
            = self.main.appSettings['DialogLumensSCIENDOCalculateWeightofEvidence']['location'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateLandUseChange']['location'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateWithScenario']['location'] \
            = unicode(self.lineEditLandUseChangeModelingLocation.text())

    
    def writeListCsv(self, listOfData, forwardDirSeparator=False):
        """Method for writing the dissolved table to a temp csv file. Inspired from DialogLumensViewer.
        
        Args:
            listOfData (list): a list which is contained the list of checked QUES-C database 
            forwardDirSeparator (bool): return the temp csv file path with forward slash dir separator.
        """        
        handle, csvFilePath = tempfile.mkstemp(suffix='.csv')
        
        with os.fdopen(handle, 'w') as f:
            writer = csv.writer(f)
            
            for tableRow in listOfData:
                writer.writerow([tableRow])
            
        if forwardDirSeparator:
            return csvFilePath.replace(os.path.sep, '/')
            
        return csvFilePath
    
    
    def handlerProcessLowEmissionDevelopmentAnalysis(self):
        """Slot method to pass the form values and execute the "SCIENDO Low Emission Development Analysis" R algorithms.
        
        Depending on the checked groupbox, the "SCIENDO Low Emission Development Analysis" process calls the following algorithms:
        1. r:projectionhistoricalbaseline
        2. r:historicalbaselineannualprojection
        3. modeler:drivers_analysis
        4. r:abacususingabsolutearea
        """
        self.setAppSettings()
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        
        if self.checkBoxHistoricalBaselineProjection.isChecked():
            formName = 'DialogLumensSCIENDOHistoricalBaselineProjection'
            algName = 'r:projectionhistoricalbaseline'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessLowEmissionDevelopmentAnalysis.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    activeProject,
                    self.main.appSettings[formName]['QUESCDatabase'],
                    self.main.appSettings[formName]['iteration'],
                    None,
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessLowEmissionDevelopmentAnalysis.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        
        if self.checkBoxHistoricalBaselineAnnualProjection.isChecked():
            if len(self.listOfQUESCDatabase) > 1:
                formName = 'DialogLumensSCIENDOHistoricalBaselineAnnualProjection'
                algName = 'r:historicalbaselineannualprojection'
                
                self.listOfQUESCDatabase.sort()
                QUESCDatabaseCsv = self.writeListCsv(self.listOfQUESCDatabase, True)
                
                if self.validForm(formName):
                    logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                    logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                    self.buttonProcessLowEmissionDevelopmentAnalysis.setDisabled(True)
                    
                    # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                    self.main.setWindowState(QtCore.Qt.WindowMinimized)
                    
                    outputs = general.runalg(
                        algName,
                        activeProject,
                        self.main.appSettings[formName]['iteration'],
                        QUESCDatabaseCsv,
                        None,
                    )
                    
                    # Display ROut file in debug mode
                    if self.main.appSettings['debug']:
                        dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                        dialog.exec_()
                    
                    ##print outputs
                    
                    # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                    self.main.setWindowState(QtCore.Qt.WindowActive)
                    
                    self.outputsMessageBox(algName, outputs, '', '')
                    
                    self.buttonProcessLowEmissionDevelopmentAnalysis.setEnabled(True)
                    logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                    logging.getLogger(self.historyLog).info('alg end: %s' % formName)
            else: 
                QtGui.QMessageBox.information(self, 'Historical Baseline Annual Projection', 'Choose at least two QUES-C database.')
                return 
        
        
        if self.checkBoxDriversAnalysis.isChecked():
            formName = 'DialogLumensSCIENDODriversAnalysis'
            algName = 'modeler:drivers_analysis'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessLowEmissionDevelopmentAnalysis.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['landUseCoverChangeDrivers'],
                    self.main.appSettings[formName]['landUseCoverChangeType'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessLowEmissionDevelopmentAnalysis.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        
        
        if self.checkBoxBuildScenario.isChecked():
            formName = 'DialogLumensSCIENDOBuildScenario'
            algName = 'r:abacususingabsolutearea'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessLowEmissionDevelopmentAnalysis.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['historicalBaselineCar'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessLowEmissionDevelopmentAnalysis.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
    
    
    def handlerProcessLandUseChangeModeling(self):
        """Slot method to pass the form values and execute the "SCIENDO Land Use Change Modeling" R algorithms.
        
        Depending on the checked groupbox, the "SCIENDO Land Use Change Modeling" process calls the following algorithms:
        1. modeler:sciendo1_calculate_transition_matrix
        2. modeler:sciendo1_create_raster_cube
        3. modeler:sciendo3_calculate_weight_of_evidence
        4. modeler:sciendo4_simulate_land_use_change
        5. modeler:sciendo5_simulate_with_scenario
        """
        if self.checkBoxCalculateTransitionMatrix.isChecked():
            formName = 'DialogLumensSCIENDOCalculateTransitionMatrix'
            algName = 'modeler:sciendo1_calculate_transition_matrix'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessLandUseChangeModeling.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['factorsDir'],
                    self.main.appSettings[formName]['landUseLookup'],
                    self.main.appSettings[formName]['baseYear'],
                    self.main.appSettings[formName]['location'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessLandUseChangeModeling.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        
        if self.checkBoxCreateRasterCubeOfFactors.isChecked():
            formName = 'DialogLumensSCIENDOCreateRasterCube'
            algName = 'modeler:sciendo1_create_raster_cube'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessLandUseChangeModeling.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['factorsDir'],
                    self.main.appSettings[formName]['landUseLookup'],
                    self.main.appSettings[formName]['baseYear'],
                    self.main.appSettings[formName]['location'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessLandUseChangeModeling.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        
        if self.checkBoxCalculateWeightOfEvidence.isChecked():
            formName = 'DialogLumensSCIENDOCalculateWeightofEvidence'
            algName = 'modeler:sciendo3_calculate_weight_of_evidence'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessLandUseChangeModeling.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['factorsDir'],
                    self.main.appSettings[formName]['landUseLookup'],
                    self.main.appSettings[formName]['baseYear'],
                    self.main.appSettings[formName]['location'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessLandUseChangeModeling.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        
        if self.checkBoxSimulateLandUseChange.isChecked():
            formName = 'DialogLumensSCIENDOSimulateLandUseChange'
            algName = 'modeler:sciendo4_simulate_land_use_change'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessLandUseChangeModeling.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['factorsDir'],
                    self.main.appSettings[formName]['landUseLookup'],
                    self.main.appSettings[formName]['baseYear'],
                    self.main.appSettings[formName]['location'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessLandUseChangeModeling.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        
        if self.checkBoxSimulateWithScenario.isChecked():
            formName = 'DialogLumensSCIENDOSimulateWithScenario'
            algName = 'modeler:sciendo5_simulate_with_scenario'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessLandUseChangeModeling.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['factorsDir'],
                    self.main.appSettings[formName]['landUseLookup'],
                    self.main.appSettings[formName]['baseYear'],
                    self.main.appSettings[formName]['location'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessLandUseChangeModeling.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
    
