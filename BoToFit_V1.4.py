'''
Install with:
* Windows - pyinstaller --onefile -i"C:\icon.ico" --add-data C:\icon.ico;images C:\BoToFit_V1.4.py

Package requirements:
* PyQt<=5.12.2
'''

from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
import os, psutil, shutil, time, math, threading, subprocess, pkgutil
import pyqtgraph as pg
import numpy as np
import pandas as pd
from scipy.interpolate import InterpolatedUnivariateSpline

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Ui_MainWindow(QtGui.QMainWindow):

    def __create_element(self, object, geometry, objectName, text=None, font=None, placeholder=None, visible=None, stylesheet=None, checked=None, checkable=None, title=None, combo=None, enabled=None):

        object.setObjectName(objectName)

        if not geometry == [999, 999, 999, 999]: object.setGeometry(QtCore.QRect(geometry[0], geometry[1], geometry[2], geometry[3]))

        if not text == None: object.setText(text)
        if not title == None: object.setTitle(title)
        if not font == None: object.setFont(font)
        if not placeholder == None: object.setPlaceholderText(placeholder)
        if not visible == None: object.setVisible(visible)
        if not checked == None: object.setChecked(checked)
        if not checkable == None: object.setCheckable(checked)
        if not enabled == None: object.setEnabled(enabled)

        if not stylesheet == None: object.setStyleSheet(stylesheet)

        if not combo == None:
            for i in combo: object.addItem(str(i))

    ## define user interface elements
    def setupUi(self, MainWindow):

        # Background and foreground for graphs
        pg.setConfigOption('background', (255, 255, 255))
        pg.setConfigOption('foreground', 'k')

        # Fonts
        font_headline = QtGui.QFont()
        font_headline.setPointSize(8)
        font_headline.setBold(True)

        font_graphs = QtGui.QFont()
        font_graphs.setPixelSize(10)
        font_graphs.setBold(False)

        font_ee = QtGui.QFont()
        font_ee.setPointSize(8)
        font_ee.setBold(False)

        # Main Window
        MainWindow_size = [1090, 752]
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(MainWindow_size[0], MainWindow_size[1])
        MainWindow.setMinimumSize(QtCore.QSize(MainWindow_size[0], MainWindow_size[1]))
        MainWindow.setMaximumSize(QtCore.QSize(MainWindow_size[0], MainWindow_size[1]))
        MainWindow.setFont(font_ee)
        MainWindow.setWindowTitle("BoToFit")

        # when we create .exe with pyinstaller, we need to store icon inside it. Then we find it inside unpacked temp directory.
        for i in pkgutil.iter_importers():
            path = str(i).split("'")[1].replace("\\\\", "\\") if str(i).find('FileFinder')>=0 else None
            if not path == None: self.iconpath = path + "\\images\\icon.ico"
        MainWindow.setWindowIcon(QtGui.QIcon(self.iconpath))
        MainWindow.setIconSize(QtCore.QSize(30, 30))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Block: Data file and structure
        self.label_DataFile = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_DataFile, [20, 0, 191, 16], "label_DataFile", text="Data file(s) and structure:", font=font_headline, stylesheet="QLabel { color : blue; }")

        self.groupBox_DataFile = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_DataFile, [10, 1, 661, 49], "groupBox_DataFile", font=font_ee)
        self.lineEdit_DataFile = QtWidgets.QLineEdit(self.groupBox_DataFile)
        self.__create_element(self.lineEdit_DataFile, [5, 23, 370, 21], "lineEdit_DataFile", font=font_ee)
        self.toolButton_DataFile = QtWidgets.QToolButton(self.groupBox_DataFile)
        self.__create_element(self.toolButton_DataFile, [378, 23, 26, 21], "toolButton_DataFile", text="...", font=font_ee)
        self.comboBox_DataFile_Column1 = QtWidgets.QComboBox(self.groupBox_DataFile)
        self.__create_element(self.comboBox_DataFile_Column1, [435, 23, 71, 21], "comboBox_DataFile_Column1", font=font_ee)
        self.comboBox_DataFile_Column2 = QtWidgets.QComboBox(self.groupBox_DataFile)
        self.__create_element(self.comboBox_DataFile_Column2, [510, 23, 71, 21], "comboBox_DataFile_Column2", font=font_ee)
        self.comboBox_DataFile_Column3 = QtWidgets.QComboBox(self.groupBox_DataFile)
        self.__create_element(self.comboBox_DataFile_Column3, [585, 23, 71, 21], "comboBox_DataFile_Column3", font=font_ee)
        values = ["ang(Qz)", "I", "dI", "ang(rad)"]
        for comboBox in [self.comboBox_DataFile_Column1, self.comboBox_DataFile_Column2, self.comboBox_DataFile_Column3]:
            for i in range(0, 4):
                comboBox.addItem("")
                comboBox.setItemText(i, values[i])
        self.comboBox_DataFile_Column1.setCurrentIndex(0)
        self.comboBox_DataFile_Column2.setCurrentIndex(1)
        self.comboBox_DataFile_Column3.setCurrentIndex(2)

        self.checkBox_DataFile_Preformatted = QtWidgets.QCheckBox(self.centralwidget)
        self.__create_element(self.checkBox_DataFile_Preformatted, [480, 0, 192, 18], "checkBox_DataFile_Preformatted", text="Data files are already preformatted", font=font_ee)

        # Block: Start fit with
        self.label_StartFitWith = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_StartFitWith, [20, 50, 141, 16], "label_StartFitWith", text="Start fit with:", font=font_headline, stylesheet="QLabel { color : blue; }")
        self.tabWidget_StartFitWith = QtWidgets.QTabWidget(self.centralwidget)
        self.__create_element(self.tabWidget_StartFitWith, [10, 68, 661, 271], "tabWidget_StartFitWith", font=font_ee)

        # - tab "Film description" / "Fraction 1
        self.tab_FilmDescription = QtWidgets.QWidget()
        self.tab_FilmDescription.setObjectName("tab_FilmDescription")
        self.tabWidget_StartFitWith.addTab(self.tab_FilmDescription, "")
        self.tabWidget_StartFitWith.setTabText(self.tabWidget_StartFitWith.indexOf(self.tab_FilmDescription), "Film description")
        self.tableWidget_FilmDescription = QtWidgets.QTableWidget(self.tab_FilmDescription)
        self.__create_element(self.tableWidget_FilmDescription, [-2, -1, 660, 222], "tableWidget_FilmDescription", font=font_ee)
        self.tableWidget_FilmDescription.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableWidget_FilmDescription.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_FilmDescription.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_FilmDescription.setColumnCount(13)
        self.tableWidget_FilmDescription.setRowCount(1)
        # reform the table if Pol/NoPol mode is chosen
        self.tableWidget_FilmDescription.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem())
        columnNames = ["layer", "thickness", "", "SLD", "", "iSLD", "", "mSLD", "", "cos(d-gamma)", "", "roughness", ""]
        
        for i in range(0, 13):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget_FilmDescription.setHorizontalHeaderItem(i, item)
            self.tableWidget_FilmDescription.horizontalHeaderItem(i).setText(columnNames[i])

        self.tableWidget_FilmDescription.verticalHeaderItem(0).setText("Back")
        self.tableWidget_FilmDescription.horizontalHeaderItem(4).setFont(font_headline)

        columnNames = ["Substrate", "inf", "", "2.07", "", "0", "", "", "", "", "", "10", ""]
        for i in range(0, 13):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            if i in (0, 1, 2): item.setFlags(QtCore.Qt.NoItemFlags)
            elif i in (4, 6, 8, 10, 12):
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                if i == 8: item.setCheckState(QtCore.Qt.Unchecked)
                else: item.setCheckState(QtCore.Qt.Checked)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget_FilmDescription.setItem(0, i, item)
            self.tableWidget_FilmDescription.item(0, i).setText(columnNames[i])

        self.tableWidget_FilmDescription.setRowHeight(0, 21)
        self.tableWidget_FilmDescription.horizontalHeader().setDefaultSectionSize(23)
        self.tableWidget_FilmDescription.verticalHeader().setVisible(False)

        self.pushButton_FilmDescription_LoadEntry = QtWidgets.QPushButton(self.tab_FilmDescription)
        self.__create_element(self.pushButton_FilmDescription_LoadEntry, [1, 223, 111, 19], "pushButton_FilmDescription_LoadEntry", text="Load entry file", font=font_ee)
        self.pushButton_FilmDescription_LoadFitbag = QtWidgets.QPushButton(self.tab_FilmDescription)
        self.__create_element(self.pushButton_FilmDescription_LoadFitbag, [120, 223, 111, 19], "pushButton_FilmDescription_LoadFitbag", text="Load FitBag", font=font_ee)
        self.pushButton_FilmDescription_AddLayer = QtWidgets.QPushButton(self.tab_FilmDescription)
        self.__create_element(self.pushButton_FilmDescription_AddLayer, [491, 223, 80, 19], "pushButton_FilmDescription_AddLayer", text="Add layer", font=font_ee)
        self.pushButton_FilmDescription_RemoveLayer = QtWidgets.QPushButton(self.tab_FilmDescription)
        self.__create_element(self.pushButton_FilmDescription_RemoveLayer, [575, 223, 80, 19], "pushButton_FilmDescription_RemoveLayer", text="Remove layer", font=font_ee)

        # - tab "Film description"(2) / "Fraction 2
        self.tab_FilmDescription_2 = QtWidgets.QWidget()
        self.tab_FilmDescription_2.setObjectName("tab_FilmDescription_2")
        self.tabWidget_StartFitWith.addTab(self.tab_FilmDescription_2, "")
        self.tabWidget_StartFitWith.setTabText(self.tabWidget_StartFitWith.indexOf(self.tab_FilmDescription_2), "Fraction 2")
        self.tableWidget_FilmDescription_2 = QtWidgets.QTableWidget(self.tab_FilmDescription_2)
        self.__create_element(self.tableWidget_FilmDescription_2, [-2, -1, 660, 247], "tableWidget_FilmDescription_2", font=font_ee)
        self.tableWidget_FilmDescription_2.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableWidget_FilmDescription_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_FilmDescription_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_FilmDescription_2.setColumnCount(13)
        self.tableWidget_FilmDescription_2.setRowCount(1)
        # reform the table if Pol/NoPol mode is chosen
        self.tableWidget_FilmDescription_2.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem())
        columnNames = ["layer", "thickness", "", "SLD", "", "iSLD", "", "mSLD", "", "cos(d-gamma)", "", "roughness", ""]

        for i in range(0, 13):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget_FilmDescription_2.setHorizontalHeaderItem(i, item)
            self.tableWidget_FilmDescription_2.horizontalHeaderItem(i).setText(columnNames[i])

        self.tableWidget_FilmDescription_2.verticalHeaderItem(0).setText("Back")
        self.tableWidget_FilmDescription_2.horizontalHeaderItem(4).setFont(font_headline)

        columnNames = ["Substrate", "inf", "", "2.07", "", "0", "", "", "", "", "", "10", ""]
        for i in range(0, 13):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            if i in (0, 1, 2): item.setFlags(QtCore.Qt.NoItemFlags)
            elif i in (4, 6, 8, 10, 12):
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                if i == 8: item.setCheckState(QtCore.Qt.Unchecked)
                else: item.setCheckState(QtCore.Qt.Checked)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget_FilmDescription_2.setItem(0, i, item)
            self.tableWidget_FilmDescription_2.item(0, i).setText(columnNames[i])

        self.tableWidget_FilmDescription_2.setRowHeight(0, 21)
        self.tableWidget_FilmDescription_2.horizontalHeader().setDefaultSectionSize(23)
        self.tableWidget_FilmDescription_2.verticalHeader().setVisible(False)

        # - tab "Scan parameters"
        self.tab_ScanParameters = QtWidgets.QWidget()
        self.tab_ScanParameters.setObjectName("tab_ScanParameters")
        self.tabWidget_StartFitWith.addTab(self.tab_ScanParameters, "")
        self.tabWidget_StartFitWith.setTabText(self.tabWidget_StartFitWith.indexOf(self.tab_ScanParameters), "Scan parameters")
        self.label_ScanParameters_NumberOfPtsForResolutionFunction = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_NumberOfPtsForResolutionFunction, [8, 9, 311, 17], "label_ScanParameters_NumberOfPtsForResolutionFunction", text="Number of points for resolution function", font=font_ee)
        self.lineEdit_ScanParameters_NumberOfPtsForResolutionFunction = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_NumberOfPtsForResolutionFunction, [223, 9, 60, 17], "lineEdit_ScanParameters_NumberOfPtsForResolutionFunction", font=font_ee)
        self.label_ScanParameters_StepForResolutionFunction = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_StepForResolutionFunction, [8, 27, 291, 17], "label_ScanParameters_StepForResolutionFunction", text="Step for resolution function (mrad)", font=font_ee)
        self.lineEdit_ScanParameters_StepForResolutionFunction = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_StepForResolutionFunction, [223, 27, 60, 17], "lineEdit_ScanParameters_StepForResolutionFunction", font=font_ee)
        self.label_ScanParameters_Sigma = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_Sigma, [8, 45, 291, 17], "label_ScanParameters_Sigma", text="\"Sigma\" of resolution function (mrad)", font=font_ee)
        self.lineEdit_ScanParameters_Sigma = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_Sigma, [223, 45, 60, 17], "lineEdit_ScanParameters_Sigma", font=font_ee)
        self.label_ScanParameters_ZeroCorrection = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_ZeroCorrection, [8, 63, 281, 17], "label_ScanParameters_ZeroCorrection", text="Correction of the detector \"zero\"", font=font_ee)
        self.lineEdit_ScanParameters_ZeroCorrection = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_ZeroCorrection, [223, 63, 60, 17], "lineEdit_ScanParameters_ZeroCorrection", font=font_ee)

        self.label_ScanParameters_Wavelength = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_Wavelength, [350, 9, 131, 17], "label_ScanParameters_Wavelength", text="Wavelength (A)", font=font_ee)
        self.lineEdit_ScanParameters_Wavelength = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_Wavelength, [560, 9, 60, 17], "lineEdit_ScanParameters_Wavelength", font=font_ee)
        self.label_ScanParameters_ScalingFactor = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_ScalingFactor, [350, 27, 101, 17], "label_ScanParameters_ScalingFactor", text="Scaling factor", font=font_ee)
        self.lineEdit_ScanParameters_ScalingFactor = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_ScalingFactor, [560, 27, 60, 17], "lineEdit_ScanParameters_ScalingFactor", placeholder="", font=font_ee)
        self.checkBox_ScanParameters_ScalingFactor = QtWidgets.QCheckBox(self.tab_ScanParameters)
        self.__create_element(self.checkBox_ScanParameters_ScalingFactor, [623, 27, 20, 18], "checkBox_ScanParameters_ScalingFactor")
        self.label_ScanParameters_Background = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_Background, [350, 45, 91, 17], "label_ScanParameters_Background", text="Background", font=font_ee)
        self.lineEdit_ScanParameters_Background = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_Background, [560, 45, 60, 17], "lineEdit_ScanParameters_Background", font=font_ee)
        self.checkBox_ScanParameters_Background = QtWidgets.QCheckBox(self.tab_ScanParameters)
        self.__create_element(self.checkBox_ScanParameters_Background, [623, 45, 21, 18], "checkBox_ScanParameters_Background")
        self.label_ScanParameters_CrossoverOverillumination = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_CrossoverOverillumination, [350, 63, 311, 17], "label_ScanParameters_CrossoverOverillumination", text="Crossover angle overillumination (mrad)", font=font_ee)
        self.lineEdit_ScanParameters_CrossoverOverillumination = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_CrossoverOverillumination, [560, 63, 60, 17], "lineEdit_ScanParameters_CrossoverOverillumination", font=font_ee)
        self.checkBox_ScanParameters_CrossoverOverillumination = QtWidgets.QCheckBox(self.tab_ScanParameters)
        self.__create_element(self.checkBox_ScanParameters_CrossoverOverillumination, [623, 63, 21, 18], "checkBox_ScanParameters_CrossoverOverillumination")

        self.label_ScanParameters_PointsToExclude_first = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_PointsToExclude_first, [350, 93, 191, 16], "label_ScanParameters_PointsToExclude_first", text="Number of first points to exclude")
        self.lineEdit_ScanParameters_PointsToExclude_first = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_PointsToExclude_first, [560, 93, 60, 17], "lineEdit_ScanParameters_PointsToExclude_first", text="5")
        self.label_ScanParameters_PointsToExclude_last = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_PointsToExclude_last, [350, 111, 191, 17], "label_ScanParameters_PointsToExclude_last", text="Number of last points to exclude")
        self.lineEdit_ScanParameters_PointsToExclude_last = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_PointsToExclude_last, [560, 111, 60, 17], "lineEdit_ScanParameters_PointsToExclude_last", text="0")

        self.pushButton_ResolutionFunction_Show = QtWidgets.QPushButton(self.tab_ScanParameters)
        self.__create_element(self.pushButton_ResolutionFunction_Show, [8, 93, 180, 32], "pushButton_ResolutionFunction_Show", text="Show resolution function view", font=font_headline)

        self.graphicsView_ResolutionFunction = pg.PlotWidget(self.tab_ScanParameters, viewBox=pg.ViewBox())
        self.__create_element(self.graphicsView_ResolutionFunction, [0, 0, 0, 0], "graphicsView_ResolutionFunction")
        self.graphicsView_ResolutionFunction.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_ResolutionFunction.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_ResolutionFunction.getAxis("left").tickFont = font_graphs
        self.graphicsView_ResolutionFunction.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_ResolutionFunction.showAxis("top")
        self.graphicsView_ResolutionFunction.getAxis("top").setTicks([])
        self.graphicsView_ResolutionFunction.showAxis("right")
        self.graphicsView_ResolutionFunction.getAxis("right").setTicks([])

        self.label_ScanParameters_Piy = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_Piy, [8, 144, 291, 17], "label_ScanParameters_Piy", text="Pi(y): incident polarization (polariser)", font=font_ee)
        self.lineEdit_ScanParameters_Piy = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_Piy, [269, 144, 60, 17], "lineEdit_ScanParameters_Piy", font=font_ee)
        self.checkBox_ScanParameters_Piy = QtWidgets.QCheckBox(self.tab_ScanParameters)
        self.__create_element(self.checkBox_ScanParameters_Piy, [332, 144, 21, 18], "checkBox_ScanParameters_Piy")
        self.label_ScanParameters_Pfy = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_Pfy, [8, 162, 251, 17], "label_ScanParameters_Pfy", text="Pf(y): outgoing polarization (analyser)", font=font_ee)
        self.lineEdit_ScanParameters_Pfy = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_Pfy, [269, 162, 60, 17], "lineEdit_ScanParameters_Pfy", font=font_ee)
        self.checkBox_ScanParameters_Pfy = QtWidgets.QCheckBox(self.tab_ScanParameters)
        self.__create_element(self.checkBox_ScanParameters_Pfy, [332, 162, 21, 18], "checkBox_ScanParameters_Pfy")
        self.label_ScanParameters_Cg = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_Cg, [8, 180, 291, 17], "label_ScanParameters_Cg", text="cg: mean value <cos(gamma)> of big domains", font=font_ee)
        self.lineEdit_ScanParameters_Cg = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_Cg, [269, 180, 60, 17], "lineEdit_ScanParameters_Cg", font=font_ee)
        self.checkBox_ScanParameters_Cg = QtWidgets.QCheckBox(self.tab_ScanParameters)
        self.__create_element(self.checkBox_ScanParameters_Cg, [332, 180, 21, 18], "checkBox_ScanParameters_Cg")
        self.label_ScanParameters_Cg_2 = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_Cg_2, [362, 180, 291, 17], "label_ScanParameters_Cg_2", text="cg (fraction 2)", font=font_ee)
        self.lineEdit_ScanParameters_Cg_2 = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_Cg_2, [450, 180, 60, 17], "lineEdit_ScanParameters_Cg_2", font=font_ee)
        self.checkBox_ScanParameters_Cg_2 = QtWidgets.QCheckBox(self.tab_ScanParameters)
        self.__create_element(self.checkBox_ScanParameters_Cg_2, [513, 180, 21, 18], "checkBox_ScanParameters_Cg_2")
        self.label_ScanParameters_Sg = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_Sg, [8, 198, 291, 17], "label_ScanParameters_Sg", text="sg: mean value <sin(gamma)> of big domains", font=font_ee)
        self.lineEdit_ScanParameters_Sg = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_Sg, [269, 198, 60, 17], "lineEdit_ScanParameters_Sg", font=font_ee)
        self.checkBox_ScanParameters_Sg = QtWidgets.QCheckBox(self.tab_ScanParameters)
        self.__create_element(self.checkBox_ScanParameters_Sg, [332, 198, 21, 18], "checkBox_ScanParameters_Sg")
        self.label_ScanParameters_Sg_2 = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_Sg_2, [362, 198, 291, 17], "label_ScanParameters_Sg_2", text="sg (fraction 2)", font=font_ee)
        self.lineEdit_ScanParameters_Sg_2 = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_Sg_2, [450, 198, 60, 17], "lineEdit_ScanParameters_Sg_2", font=font_ee)
        self.checkBox_ScanParameters_Sg_2 = QtWidgets.QCheckBox(self.tab_ScanParameters)
        self.__create_element(self.checkBox_ScanParameters_Sg_2, [513, 198, 21, 18], "checkBox_ScanParameters_Sg_2")
        self.label_ScanParameters_Sg2 = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_Sg2, [8, 216, 291, 17], "label_ScanParameters_Sg2", text="sg2: mean value <sin^2(gamma)> of big domains", font=font_ee)
        self.lineEdit_ScanParameters_Sg2 = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_Sg2, [269, 216, 60, 17], "lineEdit_ScanParameters_Sg2", font=font_ee)
        self.checkBox_ScanParameters_Sg2 = QtWidgets.QCheckBox(self.tab_ScanParameters)
        self.__create_element(self.checkBox_ScanParameters_Sg2, [332, 216, 21, 18], "checkBox_ScanParameters_Sg2")
        self.label_ScanParameters_Sg2_2 = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_Sg2_2, [362, 216, 291, 17], "label_ScanParameters_Sg2_2", text="sg2 (fraction 2)", font=font_ee)
        self.lineEdit_ScanParameters_Sg2_2 = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_Sg2_2, [450, 216, 60, 17], "lineEdit_ScanParameters_Sg2_2", font=font_ee)
        self.checkBox_ScanParameters_Sg2_2 = QtWidgets.QCheckBox(self.tab_ScanParameters)
        self.__create_element(self.checkBox_ScanParameters_Sg2_2, [513, 216, 21, 18], "checkBox_ScanParameters_Sg2_2")

        self.label_ScanParameters_FractionAmount = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_FractionAmount, [362, 144, 291, 17], "label_ScanParameters_FractionAmount",
                              text="Fraction amount (0 < \"fraction 1\" < 1)", font=font_ee)
        self.lineEdit_ScanParameters_FractionAmount = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_FractionAmount, [560, 144, 60, 17], "lineEdit_ScanParameters_FractionAmount", font=font_ee)
        self.checkBox_ScanParameters_FractionAmount = QtWidgets.QCheckBox(self.tab_ScanParameters)
        self.__create_element(self.checkBox_ScanParameters_FractionAmount, [623, 144, 21, 18], "checkBox_ScanParameters_FractionAmount")

        self.label_ScanParameters_GradientPeriod = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_GradientPeriod, [362, 144, 291, 17], "label_ScanParameters_GradientPeriod", text="Gradient (-1 < \"grad\"< 1):   Period", font=font_ee)
        self.lineEdit_ScanParameters_GradientPeriod = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_GradientPeriod, [560, 144, 60, 17], "lineEdit_ScanParameters_GradientPeriod", font=font_ee)
        self.checkBox_ScanParameters_GradientPeriod = QtWidgets.QCheckBox(self.tab_ScanParameters)
        self.__create_element(self.checkBox_ScanParameters_GradientPeriod, [623, 144, 21, 18], "checkBox_ScanParameters_GradientPeriod")
        self.label_ScanParameters_GradientRoughness = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_GradientRoughness, [498, 162, 251, 17], "label_ScanParameters_GradientRoughness", text="Roughness", font=font_ee)
        self.lineEdit_ScanParameters_GradientRoughness = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_GradientRoughness, [560, 162, 60, 17], "lineEdit_ScanParameters_GradientRoughness", font=font_ee)
        self.checkBox_ScanParameters_GradientRoughness = QtWidgets.QCheckBox(self.tab_ScanParameters)
        self.__create_element(self.checkBox_ScanParameters_GradientRoughness, [623, 162, 21, 18], "checkBox_ScanParameters_GradientRoughness")
        self.label_ScanParameters_GradientSld = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_GradientSld, [498, 180, 291, 17], "label_ScanParameters_GradientSld", text="SLD", font=font_ee)
        self.lineEdit_ScanParameters_GradientSld = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_GradientSld, [560, 180, 60, 17], "lineEdit_ScanParameters_GradientSld", font=font_ee)
        self.checkBox_ScanParameters_GradientSld = QtWidgets.QCheckBox(self.tab_ScanParameters)
        self.__create_element(self.checkBox_ScanParameters_GradientSld, [623, 180, 21, 18], "checkBox_ScanParameters_GradientSld")
        self.label_ScanParameters_GradientMsld = QtWidgets.QLabel(self.tab_ScanParameters)
        self.__create_element(self.label_ScanParameters_GradientMsld, [498, 198, 291, 17], "label_ScanParameters_GradientMsld", text="mSLD", font=font_ee)
        self.lineEdit_ScanParameters_GradientMsld = QtWidgets.QLineEdit(self.tab_ScanParameters)
        self.__create_element(self.lineEdit_ScanParameters_GradientMsld, [560, 198, 60, 17], "lineEdit_ScanParameters_GradientMsld", font=font_ee)
        self.checkBox_ScanParameters_GradientMsld = QtWidgets.QCheckBox(self.tab_ScanParameters)
        self.__create_element(self.checkBox_ScanParameters_GradientMsld, [623, 198, 21, 18], "checkBox_ScanParameters_GradientMsld")

        self.tabWidget_StartFitWith.setCurrentIndex(0)

        # Block: Save results at
        self.label_SaveAt = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_SaveAt, [20, 340, 151, 16], "label_SaveAt", text="Save fit results at:", font=font_headline, stylesheet="QLabel { color : blue; }")
        self.groupBox_SaveAt = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_SaveAt, [10, 341, 531, 49], "groupBox_SaveAt", font=font_ee)
        self.lineEdit_SaveAt_Dir_1 = QtWidgets.QLineEdit(self.groupBox_SaveAt)
        self.__create_element(self.lineEdit_SaveAt_Dir_1, [5, 23, 281, 21], "lineEdit_SaveAt_Dir_1", font=font_ee)
        self.toolButton_SaveAt_Dir_1 = QtWidgets.QToolButton(self.groupBox_SaveAt)
        self.__create_element(self.toolButton_SaveAt_Dir_1, [290, 23, 26, 21], "toolButton_SaveAt_Dir_1", text="...", font=font_ee)
        self.lineEdit_SaveAt_Dir_2 = QtWidgets.QLineEdit(self.groupBox_SaveAt)
        self.__create_element(self.lineEdit_SaveAt_Dir_2, [325, 23, 200, 21], "lineEdit_SaveAt_Dir_2", font=font_ee, placeholder="Sub directory [first data file name]")

        # Button: Start fitting
        self.pushButton_StartFitting = QtWidgets.QPushButton(self.centralwidget)
        self.__create_element(self.pushButton_StartFitting, [550, 358, 121, 32], "pushButton_StartFitting", text="Start Fitting", font=font_headline)

        # Block: Fit results
        self.label_FitResults = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_FitResults, [690, 0, 101, 16], "label_FitResults", text="Fit results:", font=font_headline, stylesheet="QLabel { color : blue; }")
        self.label_FitResults.setFont(font_headline)
        self.label_FitResults.setGeometry(QtCore.QRect(690, 0, 101, 16))
        self.label_FitResults.setObjectName("label_FitResults")
        self.label_FitResults.setText("Fit results:")
        self.groupBox_FitResults = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_FitResults, [680, 1, 401, 389], "groupBox_FitResults", font=font_headline)
        self.tableWidget_FitResults = QtWidgets.QTableWidget(self.groupBox_FitResults)
        self.__create_element(self.tableWidget_FitResults, [1, 48, 400, 317], "tableWidget_FitResults", font=font_ee)
        self.tableWidget_FitResults.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_FitResults.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.tableWidget_FitResults.setPalette(palette)
        self.tableWidget_FitResults.setColumnCount(6)
        self.tableWidget_FitResults.setRowCount(0)

        columnNames = ["No", "Parameter", "Value", "Error", "Factor"]
        column_widths = [33, 38, 116, 70, 70, 70]
        for i in range(0, 6):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_FitResults.setHorizontalHeaderItem(i, item)
            self.tableWidget_FitResults.setColumnWidth(i, column_widths[i])
            if i == 0: continue
            self.tableWidget_FitResults.horizontalHeaderItem(i).setText(columnNames[i-1])

        self.tableWidget_FitResults.horizontalHeaderItem(0).setFont(font_headline)
        self.tableWidget_FitResults.verticalHeader().setVisible(False)
        self.checkBox_FitResults_SelectAll = QtWidgets.QCheckBox(self.tableWidget_FitResults.horizontalHeader())
        self.__create_element(self.checkBox_FitResults_SelectAll, [self.tableWidget_FitResults.columnWidth(0) / 9, 1, 14, 14], "checkBox_FitResults_SelectAll")
        self.label_FitResults_NumberOfIterations = QtWidgets.QLabel(self.groupBox_FitResults)
        self.__create_element(self.label_FitResults_NumberOfIterations, [10, 18, 161, 31], "label_FitResults_NumberOfIterations", text="No. iterations:", font=font_ee)
        self.lineEdit_FitResults_NumberOfIterations = QtWidgets.QLineEdit(self.groupBox_FitResults)
        self.__create_element(self.lineEdit_FitResults_NumberOfIterations, [82, 23, 40, 21], "lineEdit_FitResults_NumberOfIterations", font=font_ee)
        self.lineEdit_FitResults_NumberOfIterations.setReadOnly(True)
        self.label_FitResults_ChiSquare_Previous = QtWidgets.QLabel(self.groupBox_FitResults)
        self.__create_element(self.label_FitResults_ChiSquare_Previous, [135, 18, 151, 31], "label_FitResults_ChiSquare_Previous", text="Chi_sq.norm: previous", font=font_ee)
        self.lineEdit_FitResults_ChiSquare_Previous = QtWidgets.QLineEdit(self.groupBox_FitResults)
        self.__create_element(self.lineEdit_FitResults_ChiSquare_Previous, [250, 23, 50, 21], "lineEdit_FitResults_ChiSquare_Previous", font=font_ee)
        self.lineEdit_FitResults_ChiSquare_Previous.setReadOnly(True)
        self.label_FitResults_ChiSquare_Actual = QtWidgets.QLabel(self.groupBox_FitResults)
        self.__create_element(self.label_FitResults_ChiSquare_Actual, [312, 18, 151, 31], "label_FitResults_ChiSquare_Actual", text="actual", font=font_ee)
        self.lineEdit_FitResults_ChiSquare_Actual = QtWidgets.QLineEdit(self.groupBox_FitResults)
        self.__create_element(self.lineEdit_FitResults_ChiSquare_Actual, [346, 23, 50, 21], "lineEdit_FitResults_ChiSquare_Actual", font=font_ee)
        self.lineEdit_FitResults_ChiSquare_Actual.setReadOnly(True)

        self.pushButton_FitResults_CopyToStartFitWith = QtWidgets.QPushButton(self.groupBox_FitResults)
        self.__create_element(self.pushButton_FitResults_CopyToStartFitWith, [5, 367, 392, 19], "pushButton_FitResults_CopyToStartFitWith", text="Use selected (#) values as 'Start fit with' parameters", font=font_ee)

        self.checkBox_ShowFixed = QtWidgets.QCheckBox(self.centralwidget)
        self.__create_element(self.checkBox_ShowFixed, [945, 0, 192, 18], "checkBox_ShowFixed", text="Show fixed parameters", font=font_ee)

        # Block: Reflectivity profile and Difference
        self.label_ReflectivityProfileAndDiff = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_ReflectivityProfileAndDiff, [20, 393, 541, 16], "label_ReflectivityProfileAndDiff", text="Reflectivity profile (I[               ] vs. Qz[Å**-1]) and Difference (Exper/Fit):", font=font_headline, stylesheet="QLabel { color : blue; }")
        self.groupBox_ReflectivityProfile = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_ReflectivityProfile, [10, 394, 660, 315], "groupBox_ReflectivityProfile")
        self.graphicsView_Diff = pg.PlotWidget(self.groupBox_ReflectivityProfile, viewBox=pg.ViewBox())
        self.__create_element(self.graphicsView_Diff, [2, 223, 657, 91], "graphicsView_Diff")
        self.graphicsView_Diff.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_Diff.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_Diff.getAxis("left").tickFont = font_graphs
        self.graphicsView_Diff.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_Diff.showAxis("top")
        self.graphicsView_Diff.getAxis("top").setTicks([])
        self.graphicsView_Diff.showAxis("right")
        self.graphicsView_Diff.getAxis("right").setTicks([])
        self.graphicsView_ReflectivityProfile = pg.PlotWidget(self.groupBox_ReflectivityProfile, viewBox=pg.ViewBox())
        self.__create_element(self.graphicsView_ReflectivityProfile, [2, 19, 657, 205], "graphicsView_ReflectivityProfile")
        self.graphicsView_ReflectivityProfile.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_ReflectivityProfile.getAxis("bottom").setStyle(showValues=False)
        self.graphicsView_ReflectivityProfile.getAxis("left").tickFont = font_graphs
        self.graphicsView_ReflectivityProfile.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_ReflectivityProfile.showAxis("top")
        self.graphicsView_ReflectivityProfile.getAxis("top").setTicks([])
        self.graphicsView_ReflectivityProfile.showAxis("right")
        self.graphicsView_ReflectivityProfile.getAxis("right").setTicks([])
        self.graphicsView_Diff.getViewBox().setXLink(self.graphicsView_ReflectivityProfile)
        self.comboBox_ReflectivityProfile_Scale = QtWidgets.QComboBox(self.centralwidget)
        self.__create_element(self.comboBox_ReflectivityProfile_Scale, [143, 392, 41, 18], "comboBox_ReflectivityProfile_Scale", font=font_ee)
        for i, value in enumerate(["log", "lin"]):
            self.comboBox_ReflectivityProfile_Scale.addItem("")
            self.comboBox_ReflectivityProfile_Scale.setItemText(i, value)

        # Block: SLD profile
        self.label_SldProfile = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_SldProfile, [690, 393, 481, 16], "label_SldProfile", text="SLD profile (SLD [in Å**-2, *10e6] vs. Distance from interface [Å]:", font=font_headline, stylesheet="QLabel { color : blue; }")
        self.groupBox_SldProfile = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_SldProfile, [680, 394, 401, 315], "groupBox_SldProfile")
        MainWindow.setCentralWidget(self.centralwidget)
        self.graphicsView_SldProfile = pg.PlotWidget(self.groupBox_SldProfile)
        self.__create_element(self.graphicsView_SldProfile, [2, 19, 398, 295], "graphicsView_SldProfile")
        self.graphicsView_SldProfile.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_SldProfile.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_SldProfile.getAxis("left").tickFont = font_graphs
        self.graphicsView_SldProfile.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_SldProfile.showAxis("top")
        self.graphicsView_SldProfile.getAxis("top").setTicks([])
        self.graphicsView_SldProfile.showAxis("right")
        self.graphicsView_SldProfile.getAxis("right").setTicks([])

        # Menu
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.__create_element(self.menubar, [0, 0, 1229, 29], "menubar")
        MainWindow.setMenuBar(self.menubar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.__create_element(self.menuBar, [0, 0, 1229, 26], "menuBar")
        self.menu_MenuBar = QtWidgets.QMenu(self.menuBar)

        self.__create_element(self.menu_MenuBar, [999, 999, 999, 999], "menu_MenuBar", title="Mode")
        self.menuBar.addAction(self.menu_MenuBar.menuAction())
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.__create_element(self.menuHelp, [999, 999, 999, 999], "menuHelp", title="Help")
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.actionVersion = QtWidgets.QAction(MainWindow)
        self.__create_element(self.actionVersion, [999, 999, 999, 999], "actionVersion", text="V1.4")
        self.menuHelp.addAction(self.actionVersion)
        MainWindow.setMenuBar(self.menuBar)
        self.menu_Mono = QtWidgets.QMenu(self.menu_MenuBar)
        self.__create_element(self.menu_Mono, [999, 999, 999, 999], "menu_Mono", title="Mono")
        self.menu_MenuBar.addAction(self.menu_Mono.menuAction())

        self.menu_Mono_NoPolarisation = QtWidgets.QMenu(self.menu_Mono)
        self.__create_element(self.menu_Mono_NoPolarisation, [999, 999, 999, 999], "menu_Mono_NoPolarisation", title="No polarisation")
        self.menu_Mono.addAction(self.menu_Mono_NoPolarisation.menuAction())
        self.action_Mono_NoPolarisation = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_NoPolarisation, [999, 999, 999, 999], "action_Mono_NoPolarisation", checked=True, checkable=True, text="Default")  # m_0
        self.menu_Mono_NoPolarisation.addAction(self.action_Mono_NoPolarisation)
        self.action_Mono_NoPolarisation_Multi = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_NoPolarisation_Multi, [999, 999, 999, 999], "action_Mono_NoPolarisation_Multi", checked=True, checkable=True, text="Periodical multilayers")  # m_0_m
        self.menu_Mono_NoPolarisation.addAction(self.action_Mono_NoPolarisation_Multi)
        self.action_Mono_NoPolarisation_SL = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_NoPolarisation_SL, [999, 999, 999, 999], "action_Mono_NoPolarisation_SL", checked=True, checkable=True, text="Solid-Liquid")  # m_0_sl
        self.menu_Mono_NoPolarisation.addAction(self.action_Mono_NoPolarisation_SL)
        self.action_Mono_NoPolarisation_Frac = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_NoPolarisation_Frac, [999, 999, 999, 999], "action_Mono_NoPolarisation_Frac", checked=True, checkable=True, text="Fraction")  # m_0_f
        self.menu_Mono_NoPolarisation.addAction(self.action_Mono_NoPolarisation_Frac)
        self.menu_Mono_2Polarisations = QtWidgets.QMenu(self.menu_Mono)
        self.__create_element(self.menu_Mono_2Polarisations, [999, 999, 999, 999], "menu_Mono_2Polarisations", title="2 polarisations")
        self.menu_Mono.addAction(self.menu_Mono_2Polarisations.menuAction())
        self.action_Mono_2Polarisations = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_2Polarisations, [999, 999, 999, 999], "action_Mono_2Polarisations", checked=True, checkable=True, text="Default")  # m_2
        self.menu_Mono_2Polarisations.addAction(self.action_Mono_2Polarisations)
        self.action_Mono_2Polarisations_Multi = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_2Polarisations_Multi, [999, 999, 999, 999], "action_Mono_2Polarisations_Multi", checked=True, checkable=True, text="Periodical multilayers")  # m_2_m
        self.menu_Mono_2Polarisations.addAction(self.action_Mono_2Polarisations_Multi)
        self.action_Mono_2Polarisations_Frac = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_2Polarisations_Frac, [999, 999, 999, 999], "action_Mono_2Polarisations_Frac", checked=True, checkable=True, text="Fraction")  # m_2_f
        self.menu_Mono_2Polarisations.addAction(self.action_Mono_2Polarisations_Frac)
        self.menu_Mono_4Polarisations = QtWidgets.QMenu(self.menu_Mono)
        self.__create_element(self.menu_Mono_4Polarisations, [999, 999, 999, 999], "menu_Mono_4Polarisations", title="4 polarisations")
        self.menu_Mono.addAction(self.menu_Mono_4Polarisations.menuAction())
        self.action_Mono_4Polarisations = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_4Polarisations, [999, 999, 999, 999], "action_Mono_4Polarisations", checked=True, checkable=True, text="Default")  # m_4
        self.menu_Mono_4Polarisations.addAction(self.action_Mono_4Polarisations)
        self.action_Mono_4Polarisations_Multi = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_4Polarisations_Multi, [999, 999, 999, 999], "action_Mono_4Polarisations_Multi", checked=True, checkable=True, text="Periodical multilayers")  # m_4_m
        self.menu_Mono_4Polarisations.addAction(self.action_Mono_4Polarisations_Multi)
        self.action_Mono_4Polarisations_Frac = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_4Polarisations_Frac, [999, 999, 999, 999], "action_Mono_4Polarisations_Frac", checked=True, checkable=True, text="Fraction")  # m_4_f
        self.menu_Mono_4Polarisations.addAction(self.action_Mono_4Polarisations_Frac)

        self.menu_Tof = QtWidgets.QMenu(self.menu_MenuBar)
        self.__create_element(self.menu_Tof, [999, 999, 999, 999], "menu_Tof", title="TOF")
        self.menu_MenuBar.addAction(self.menu_Tof.menuAction())
        self.menu_Tof_NoPolarisation = QtWidgets.QMenu(self.menu_Mono)
        self.__create_element(self.menu_Tof_NoPolarisation, [999, 999, 999, 999], "menu_Tof_NoPolarisation", title="No polarisation")
        self.menu_Tof.addAction(self.menu_Tof_NoPolarisation.menuAction())
        self.action_Tof_NoPolarisation = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Tof_NoPolarisation, [999, 999, 999, 999], "action_Tof_NoPolarisation", checked=True, checkable=True, text="Default") # t_0
        self.menu_Tof_NoPolarisation.addAction(self.action_Tof_NoPolarisation)
        self.action_Tof_NoPolarisation_SL = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Tof_NoPolarisation_SL, [999, 999, 999, 999], "action_Tof_NoPolarisation_SL", checked=True, checkable=True, text="Solid-Liquid")  # t_0_sl
        self.menu_Tof_NoPolarisation.addAction(self.action_Tof_NoPolarisation_SL)
        self.action_Tof_2Polarisations = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Tof_2Polarisations, [999, 999, 999, 999], "action_Tof_2Polarisations", checked=True, checkable=True, text="2 polarisations") # t_2
        self.menu_Tof.addAction(self.action_Tof_2Polarisations)
        self.action_Tof_4Polarisations = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Tof_4Polarisations, [999, 999, 999, 999], "action_Tof_4Polarisations", checked=True, checkable=True, text="4 polarisations") # t_4
        self.menu_Tof.addAction(self.action_Tof_4Polarisations)

        # Statusbar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

class GUI(Ui_MainWindow):

    dir_current = os.getcwd().replace("\\", "/")
    def __init__(self):

        super(GUI, self).__init__()
        self.setupUi(self)

        self.inputStructure = [] # structure of the data file
        self.f_programMode() # No polarisation by default
        self.importing = False # Needs for table synchronisation in FRAC modes
        self.df_FITBAG = "" # stores fitbag as pandas dataframe
        self.Data_DataFiles = [] # scan points

        # Actions for buttons
        self.toolButton_DataFile.clicked.connect(self.f_button_dataFile)
        self.toolButton_SaveAt_Dir_1.clicked.connect(self.f_button_saveAt)
        self.pushButton_FilmDescription_AddLayer.clicked.connect(self.f_buttons_addRemoveLayer)
        self.pushButton_FilmDescription_RemoveLayer.clicked.connect(self.f_buttons_addRemoveLayer)
        self.pushButton_StartFitting.clicked.connect(self.f_button_startFitting)
        self.pushButton_FitResults_CopyToStartFitWith.clicked.connect(self.f_button_copyToStartWith)
        self.pushButton_FilmDescription_LoadEntry.clicked.connect(self.f_entryFile_load)
        self.pushButton_FilmDescription_LoadFitbag.clicked.connect(self.f_button_loadFitbagFile)
        self.pushButton_ResolutionFunction_Show.clicked.connect(self.f_resolutionFunction_draw)
        self.action_Mono_NoPolarisation.triggered.connect(self.f_programMode)
        self.action_Mono_2Polarisations.triggered.connect(self.f_programMode)
        self.action_Mono_4Polarisations.triggered.connect(self.f_programMode)
        self.action_Tof_NoPolarisation.triggered.connect(self.f_programMode)
        self.action_Tof_2Polarisations.triggered.connect(self.f_programMode)
        self.action_Tof_4Polarisations.triggered.connect(self.f_programMode)
        self.action_Mono_NoPolarisation_Multi.triggered.connect(self.f_programMode)
        self.action_Mono_2Polarisations_Multi.triggered.connect(self.f_programMode)
        self.action_Mono_4Polarisations_Multi.triggered.connect(self.f_programMode)
        self.action_Mono_NoPolarisation_Frac.triggered.connect(self.f_programMode)
        self.action_Mono_2Polarisations_Frac.triggered.connect(self.f_programMode)
        self.action_Mono_4Polarisations_Frac.triggered.connect(self.f_programMode)
        self.action_Mono_NoPolarisation_SL.triggered.connect(self.f_programMode)
        self.action_Tof_NoPolarisation_SL.triggered.connect(self.f_programMode)
        self.actionVersion.triggered.connect(self.f_menuInfo)
        self.checkBox_FitResults_SelectAll.clicked.connect(self.f_fitResults_selectAll)
        self.checkBox_DataFile_Preformatted.clicked.connect(self.f_dataFiles_parse)
        self.checkBox_ShowFixed.clicked.connect(self.f_fitResultsTable_fill)
        self.comboBox_DataFile_Column1.currentIndexChanged.connect(self.f_dataFiles_parse)
        self.comboBox_DataFile_Column2.currentIndexChanged.connect(self.f_dataFiles_parse)
        self.comboBox_DataFile_Column3.currentIndexChanged.connect(self.f_dataFiles_parse)
        self.comboBox_ReflectivityProfile_Scale.currentIndexChanged.connect(self.f_reflectivity_draw)
        self.comboBox_ReflectivityProfile_Scale.currentIndexChanged.connect(self.f_reformFitFunct_drawAndExport)
        self.tableWidget_FilmDescription.cellChanged.connect(self.f_fracThickness_synchronize)
        self.lineEdit_ScanParameters_PointsToExclude_first.editingFinished.connect(self.f_reflectivity_draw)
        self.lineEdit_ScanParameters_PointsToExclude_last.editingFinished.connect(self.f_reflectivity_draw)
        self.lineEdit_ScanParameters_StepForResolutionFunction.editingFinished.connect(self.f_resolutionFunction_draw)
        self.lineEdit_ScanParameters_NumberOfPtsForResolutionFunction.editingFinished.connect(self.f_resolutionFunction_draw)
        self.lineEdit_ScanParameters_Sigma.editingFinished.connect(self.f_resolutionFunction_draw)

        self.lineEdit_SaveAt_Dir_1.setPlaceholderText("Main dirictory [" + str(self.dir_current) + "/]")

    ##--> redefine user interface elements in differend modes
    
    def f_programMode(self):
        '''
        Different modes should have a bit different parameters available, so a bit different interfaces.
        '''

        # program name, file to wait, default entry
        self.MODE_SPECS = {"m_0": ("Film500x0.exe", "FitFunct.dat", "UserDefaults_nopol.ent"),
                            "m_2": ("Film500x2.exe", "Fit2DFunctDD.dat", "UserDefaults_2pol.ent"),
                            "m_4": ("Film500x4.exe", "Fit2DFunctDD.dat", "UserDefaults_4pol.ent"),
                            "t_0": ("FilmTOF500QX0.exe", "FitFunct.dat", "UserDefaults_TOF_nopol.ent"),
                            "t_2": ("FilmTOF500QX2.exe", "Fit2DFunctDD.dat", "UserDefaults_TOF_2pol.ent"),
                            "t_4": ("FilmTOF500QX4.exe", "Fit2DFunctDD.dat", "UserDefaults_TOF_4pol.ent"),
                            "m_0_m": ("Mult500x0d3Gr.exe", "FitFunct.dat", "UserDefaults_nopol_multi.ent"),
                            "m_2_m": ("Mult500x2d4Gr.exe", "Fit2DFunctDD.dat", "UserDefaults_2pol_multi.ent"),
                            "m_4_m": ("Mult500x4d4Gr.exe", "Fit2DFunctDD.dat", "UserDefaults_4pol_multi.ent"),
                            "m_0_f": ("Film500x0Nfrac.exe", "FitFunct.dat", "UserDefaults_nopol_frac.ent"),
                            "m_2_f": ("Film500x2Nfrac.exe", "Fit2DFunctDD.dat", "UserDefaults_2pol_frac.ent"),
                            "m_4_f": ("Film500x4Nfrac.exe", "Fit2DFunctDD.dat", "UserDefaults_4pol_frac.ent"),
                            "m_0_sl": ("Film500x0.exe", "FitFunct.dat", "UserDefaults_nopol_sl.ent"),
                            "t_0_sl": ("FilmTOF500QX0.exe", "FitFunct.dat", "UserDefaults_TOF_nopol_sl.ent")}

        DICT_MODES = {"action_Mono_NoPolarisation": "m_0", "action_Mono_2Polarisations": "m_2", "action_Mono_4Polarisations": "m_4",
                      "action_Tof_NoPolarisation": "t_0", "action_Tof_2Polarisations": "t_2", "action_Tof_4Polarisations": "t_4",
                      "action_Mono_NoPolarisation_Frac": "m_0_f", "action_Mono_2Polarisations_Frac": "m_2_f", "action_Mono_4Polarisations_Frac": "m_4_f",
                      "action_Mono_NoPolarisation_Multi": "m_0_m", "action_Mono_2Polarisations_Multi": "m_2_m", "action_Mono_4Polarisations_Multi": "m_4_m",
                      "action_Mono_NoPolarisation_SL": "m_0_sl", "action_Tof_NoPolarisation_SL": "t_0_sl", }

        # Step 1: define desired mode
        try: # check where we came from and change the interface accordingly
            self.BoToFit_mode = DICT_MODES[self.sender().objectName()]
            # Step 2: make sure that only one mode is checked in the mode menu
            for mode in [self.action_Mono_NoPolarisation, self.action_Mono_2Polarisations, self.action_Mono_4Polarisations, self.action_Tof_NoPolarisation, self.action_Tof_2Polarisations, self.action_Tof_4Polarisations, self.action_Mono_NoPolarisation_Multi, self.action_Mono_2Polarisations_Multi, self.action_Mono_4Polarisations_Multi, self.action_Mono_NoPolarisation_SL, self.action_Tof_NoPolarisation_SL, self.action_Mono_NoPolarisation_Frac, self.action_Mono_2Polarisations_Frac, self.action_Mono_4Polarisations_Frac]: mode.setChecked(True if mode.objectName() == self.sender().objectName() else False)
        except AttributeError: # first run of the program will have no "self.sender()"
            self.BoToFit_mode = DICT_MODES["action_Mono_NoPolarisation"]
            self.action_Mono_NoPolarisation.setChecked(True)

        # Step 3: reformat table(s) and show/hide available parameters for specific modes
        # show/hide tabs in the tabWidget
        TABS_AND_NAMES = [[self.tab_FilmDescription, ("Fraction 1" if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"] else "Film description")], [self.tab_FilmDescription_2, "Fraction 2"], [self.tab_ScanParameters, "Scan parameters"]]
        for i in reversed(range(0, self.tabWidget_StartFitWith.count())): self.tabWidget_StartFitWith.removeTab(i)
        for index, tab in enumerate(TABS_AND_NAMES):
            if index == 1 and self.BoToFit_mode not in ["m_0_f", "m_2_f", "m_4_f"]: continue
            self.tabWidget_StartFitWith.addTab(tab[0], tab[1])

        # show/hide frac parameters
        PARAMS_FRAC = [self.label_ScanParameters_FractionAmount, self.lineEdit_ScanParameters_FractionAmount, self.checkBox_ScanParameters_FractionAmount, self.label_ScanParameters_Cg_2, self.lineEdit_ScanParameters_Cg_2, self.checkBox_ScanParameters_Cg_2, self.label_ScanParameters_Sg_2, self.lineEdit_ScanParameters_Sg_2, self.checkBox_ScanParameters_Sg_2, self.label_ScanParameters_Sg2_2, self.lineEdit_ScanParameters_Sg2_2, self.checkBox_ScanParameters_Sg2_2]
        for param in PARAMS_FRAC[0:3]: param.setVisible(True if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"] else False)
        for param in PARAMS_FRAC[3:]: param.setVisible(True if self.BoToFit_mode in ["m_2_f", "m_4_f"] else False)

        # show/hide polarisation parameters
        PARAMS_POL = [self.label_ScanParameters_Piy, self.lineEdit_ScanParameters_Piy, self.checkBox_ScanParameters_Piy, self.label_ScanParameters_Pfy, self.lineEdit_ScanParameters_Pfy, self.checkBox_ScanParameters_Pfy, self.label_ScanParameters_Pfy, self.lineEdit_ScanParameters_Pfy, self.checkBox_ScanParameters_Pfy, self.label_ScanParameters_Cg, self.lineEdit_ScanParameters_Cg, self.checkBox_ScanParameters_Cg, self.label_ScanParameters_Sg, self.lineEdit_ScanParameters_Sg, self.checkBox_ScanParameters_Sg, self.label_ScanParameters_Sg2, self.lineEdit_ScanParameters_Sg2, self.checkBox_ScanParameters_Sg2]

        if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl"]: enable, col_width = False, [102, 107, 32, 107, 32, 107, 32, 0, 0, 0, 0, 107, 32]
        elif self.BoToFit_mode in ["m_2", "m_4", "t_2", "t_4", "m_2_m", "m_4_m", "m_0_f", "m_2_f", "m_4_f"]:
            col_width =  [57, 66, 32, 65, 32, 65, 32, 65, 32, 76, 32, 72, 32]
            enable = False if self.BoToFit_mode == "m_0_f" else True
        for param in PARAMS_POL: param.setVisible(enable)
        for i in range(0, 13):
            self.tableWidget_FilmDescription.setColumnWidth(i, col_width[i])
            self.tableWidget_FilmDescription_2.setColumnWidth(i, col_width[i])

        # show/hide multi parameters
        PARAM_MULTI = [self.label_ScanParameters_GradientPeriod, self.lineEdit_ScanParameters_GradientPeriod, self.checkBox_ScanParameters_GradientPeriod, self.label_ScanParameters_GradientRoughness, self.lineEdit_ScanParameters_GradientRoughness, self.checkBox_ScanParameters_GradientRoughness, self.label_ScanParameters_GradientSld, self.lineEdit_ScanParameters_GradientSld, self.checkBox_ScanParameters_GradientSld, self.label_ScanParameters_GradientMsld, self.lineEdit_ScanParameters_GradientMsld, self.checkBox_ScanParameters_GradientMsld]

        enable = [True if self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"] else False][0]
        for param in PARAM_MULTI: param.setVisible(enable)
        if self.BoToFit_mode == "m_0_m": # no mSLD gradient for NoPol_Multi
            for param in PARAM_MULTI[9:13]: param.setVisible(False)

        # reformat checkboxes (I, dI, Qz, rad) and Wavelength/Inc.angle field
        CHECKBOXES = [self.comboBox_DataFile_Column1, self.comboBox_DataFile_Column2, self.comboBox_DataFile_Column3]

        if self.BoToFit_mode in ["m_0", "m_2", "m_4", "m_0_m", "m_2_m", "m_4_m", "m_0_sl", "m_0_f", "m_2_f", "m_4_f"]:
            if self.comboBox_DataFile_Column1.count() < 4:
                for checkbox in CHECKBOXES:
                    checkbox.addItem("")
                    checkbox.setItemText(3, "ang(rad)")
            self.label_ScanParameters_Wavelength.setText("Wavelength (A)")

        elif self.BoToFit_mode in ["t_0", "t_2", "t_4", "t_0_sl"]:
            for checkbox in CHECKBOXES: checkbox.removeItem(3)
            self.label_ScanParameters_Wavelength.setText("Inc. ang. (mrad)")

        if self.checkBox_DataFile_Preformatted.isChecked(): self.comboBox_DataFile_Column3.setCurrentIndex(0 if self.BoToFit_mode in ["t_0", "t_2", "t_4", "t_0_sl"] else 3)

        # clean up lineEdits and checkboxes when we switch to the mode with less parameters
        for i in ([1, 2], [4, 5], [7, 8], [10, 11], [13, 14], [16, 17]): # PARAMS_POL
            PARAMS_POL[i[0]].setText("")
            PARAMS_POL[i[1]].setChecked(False)
        for i in ([1, 2], [4, 5], [7, 8], [10, 11]): # PARAM_MULTI
            PARAM_MULTI[i[0]].setText("")
            PARAM_MULTI[i[1]].setChecked(False)

        # Step 4: reformat table if SL mode is needed
        self.f_slLayer_add()

        # Step 5: load UserDefaults if such are presented
        try:
            if self.MODE_SPECS[self.BoToFit_mode][2] in os.listdir(self.dir_current + "/User_Defaults"):
                self.lineEdit_ScanParameters_Wavelength.setText("")
                self.f_entryFile_load(param_entryFunc=self.dir_current + "/User_Defaults/" + self.MODE_SPECS[self.BoToFit_mode][2])
        except: True

        # clear stuff, just in case
        self.f_clearStuff()
        self.lineEdit_DataFile.clear()
        self.FOLDER_DATA = ""
    ##<--

    ##--> buttons and triggers
    def f_button_dataFile(self):
        ''' if {NoPolarisation} and {toolButton_DataFile} is pressed: [user can choose only one file]
        elif {toolButton_DataFile} is pressed: [user can choose several file] '''

        self.inputStructure = [self.comboBox_DataFile_Column1.currentText(), self.comboBox_DataFile_Column2.currentText(), self.comboBox_DataFile_Column3.currentText()]

        if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]: dataFiles = QtWidgets.QFileDialog().getOpenFileName(None, "Data file", self.dir_current if len(self.lineEdit_SaveAt_Dir_1.text()) < 1 else self.lineEdit_SaveAt_Dir_1.text())[0]
        else: dataFiles = QtWidgets.QFileDialog().getOpenFileNames(None, "Data files", self.dir_current if len(self.lineEdit_SaveAt_Dir_1.text()) < 1 else self.lineEdit_SaveAt_Dir_1.text())[0]

        if dataFiles in ["", []]: return

        self.lineEdit_DataFile.setText(str(dataFiles))

        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]: dataFiles = dataFiles[0]

        dataFile_inputName = dataFiles[dataFiles.rfind("/") + 1: dataFiles.rfind(".")].replace(" ", "_")
        self.lineEdit_SaveAt_Dir_2.setText(dataFile_inputName + "/")

        # clear stuff after last run
        self.f_clearStuff()

        if self.BoToFit_mode in ["m_0", "m_2", "m_4", "m_0_m", "m_2_m", "m_4_m", "m_0_sl", "m_0_f", "m_2_f", "m_4_f"] and self.lineEdit_ScanParameters_Wavelength.text() == "": self.statusbar.showMessage("Input wavelength and reimport the file")
        else: self.f_dataFiles_parse()

    def f_buttons_addRemoveLayer(self):
        ''' We work with "Film description" table here'''

        # Step 1: check where we came here from (other function of button)
        try:
            sender_name = self.sender().objectName()
        except AttributeError: sender_name = "None" # if we come here from another function, we have no "self.sender()"

        # Step 2: Remove rows if user asked, otherwice - add
        if sender_name == "pushButton_FilmDescription_RemoveLayer": # remove lines from {tableWidget_FilmDescription}
            if not self.tableWidget_FilmDescription.rowCount() == self.tableWidget_FilmDescription.currentRow() + 1:
                self.tableWidget_FilmDescription.removeRow(self.tableWidget_FilmDescription.currentRow())
                self.tableWidget_FilmDescription_2.removeRow(self.tableWidget_FilmDescription_2.currentRow())
        else: # add lines into {tableWidget_FilmDescription}
            i = self.tableWidget_FilmDescription.currentRow() if self.tableWidget_FilmDescription.currentRow() >= 0 else 0

            for index, tableWidget in enumerate([self.tableWidget_FilmDescription, self.tableWidget_FilmDescription_2]):
                tableWidget.insertRow(i)
                tableWidget.setRowHeight(i, 21)
                for j in range(0, 13):
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    if j in (2, 4, 6, 8, 10, 12):
                        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        item.setCheckState(QtCore.Qt.Checked if j == 6 else QtCore.Qt.Unchecked)
                    if j in (1, 2) and index == 1: item.setFlags(QtCore.Qt.NoItemFlags)  # leave "thickness" only in the first table

                    tableWidget.setItem(i, j, item)

        # Step 3 (optional for FRAC): synchronize thicknesses
        self.f_fracThickness_synchronize()

    def f_button_saveAt(self):
        ''' default {save_at_dit} folder is the one where "BoToFit.exe" is located
        otherwice: defined by user '''

        dir = QtWidgets.QFileDialog().getExistingDirectory(None, "FileNames", self.dir_current)
        if dir: self.lineEdit_SaveAt_Dir_1.setText(str(dir) + "/")

    def f_button_copyToStartWith(self):
        COLUMNS = {"Thickness" : 1, "SLD" : 3, "iSLD" : 5, "mSLD" : 7, "Cos(d-gamma)" : 9, "Roughness" : 11}
        PARAMETERS = {'Scaling_factor': self.lineEdit_ScanParameters_ScalingFactor, 'Overillumination': self.lineEdit_ScanParameters_CrossoverOverillumination, 'Background': self.lineEdit_ScanParameters_Background, 'Pi(y)': self.lineEdit_ScanParameters_Piy, 'Pf(y)': self.lineEdit_ScanParameters_Pfy, 'grad.Period': self.lineEdit_ScanParameters_GradientPeriod, 'grad.Roughness': self.lineEdit_ScanParameters_GradientRoughness, 'grad.SLD': self.lineEdit_ScanParameters_GradientSld, 'grad.mSLD': self.lineEdit_ScanParameters_GradientMsld, "[F1]_amount" : self.lineEdit_ScanParameters_FractionAmount, '<cos(gamma)>':self.lineEdit_ScanParameters_Cg, '<sin(gamma)>': self.lineEdit_ScanParameters_Sg, '<sin2(gamma)>': self.lineEdit_ScanParameters_Sg2, '<cos(gamma)>_F2':self.lineEdit_ScanParameters_Cg_2, '<sin(gamma)>_F2': self.lineEdit_ScanParameters_Sg_2, '<sin2(gamma)>_F2': self.lineEdit_ScanParameters_Sg2_2}

        for i in range(0, self.tableWidget_FitResults.rowCount()):
            if not self.tableWidget_FitResults.item(i,0).checkState() == 2: continue

            parameter = self.tableWidget_FitResults.item(i, 2).text().split()

            if not len(parameter) == 1: # table
                if "(La" in parameter[0]: row = int(parameter[0][3 : parameter[0].find(")")]) - (0 if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] else 1)
                elif "(Su)" in parameter[0]: row = self.tableWidget_FilmDescription.rowCount() - 1
                # in FRAC modes we have one more parameter [Fr1]/[Fr2]
                table = self.tableWidget_FilmDescription_2 if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"] and "[F2]" in parameter[0] else self.tableWidget_FilmDescription
                table.item(row, COLUMNS[parameter[1]]).setText(str(float(self.tableWidget_FitResults.item(i, 3).text())))
            else: # other parameters
                PARAMETERS[parameter[0]].setText(str(float(self.tableWidget_FitResults.item(i, 3).text())))

    def f_button_loadFitbagFile(self):
        ''' if user decided to terminate fitting routine, uncompleted FitBag file will still be recorded in SaveAt directory. Lets allow user to load last iteration from that FitBag file. '''

        if self.pushButton_StartFitting.text() == "Stop fitting": # this means we came here while user wanted to stop BoToFit manually
            fitbag_file = self.FOLDER_DATA + ("Fit2DBag.dat" if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"] else "FitBag.dat")
        elif not self.FOLDER_DATA == "":   # otherwice user wants to open FitBag file manually (case 1)
            dir = self.FOLDER_DATA
            fitbag_file = QtWidgets.QFileDialog().getOpenFileName(None, "FitBag file", dir)[0]
        else: # (case 2)
            if not self.lineEdit_SaveAt_Dir_1.text() == "": dir = self.lineEdit_SaveAt_Dir_1.text()
            elif not self.lineEdit_DataFile.text() in ["", "[]"]:
                data_file = [file for file in self.lineEdit_DataFile.text().split("'") if len(file) > 2][0]
                dir = data_file[:data_file.rfind("/") + 1]
            else: dir = self.dir_current if len(self.lineEdit_SaveAt_Dir_1.text()) < 1 else self.lineEdit_SaveAt_Dir_1.text()
            fitbag_file = QtWidgets.QFileDialog().getOpenFileName(None, "FitBag file", dir)[0]
            self.FOLDER_DATA = fitbag_file[:fitbag_file.rfind("/")+1]

        if not fitbag_file: return

        self.f_entryForMultiGrPr_create(fitbag_file) # read FitBag file
        self.f_multyGrPr_run()

        # run multiGrPr and wait until it finished to work
        while "SLD_profile.dat" not in os.listdir(self.FOLDER_DATA): QtTest.QTest.qWait(1000)
        while os.path.getsize(self.FOLDER_DATA + 'SLD_profile.dat') < 1: QtTest.QTest.qWait(1000)

        self.f_sld_draw() # draw SLD

    def f_button_startFitting(self):
        ''' When user press "Start fitting" I start 2 threads: "BoToFit" and "Killer".
        If user press "Stop fitting" - I kill "BoToFit" process prematurely and try "start fitting" again with all parameters fixed, so I can get fitfunct file '''

        if self.lineEdit_DataFile.text() == "": return

        # CHECKUP - for "Stop fitting"
        try:
            if self.sender().text() == "Stop fitting":
                for proc in psutil.process_iter():
                    if proc.name() == self.MODE_SPECS[self.BoToFit_mode][0]: proc.kill()
                return
        except:
            True

        # CHECKUP - for Polarisation - check if User selected to fit both mSLD and cos(d-gamma) for the same layer
        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl"]:
            for tabWidget in (
                    [self.tableWidget_FilmDescription, self.tableWidget_FilmDescription_2] if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"] else [
                        self.tableWidget_FilmDescription]):
                for i in range(0, tabWidget.rowCount()):
                    if self.tableWidget_FilmDescription.item(i, 8).checkState() == 0 and self.tableWidget_FilmDescription.item(i, 10).checkState() == 0:
                        self.statusbar.showMessage("mSLD and cos(d-gamma) can not be fitted together for the same layer")
                        return

        time_start = time.time()

        # CLEANUP - delete some files and clear graphs before start
        self.df_FITBAG = ""
        self.lineEdit_FitResults_ChiSquare_Previous.setText(self.lineEdit_FitResults_ChiSquare_Actual.text())
        self.checkBox_FitResults_SelectAll.setChecked(False)
        self.f_clearStuff(chi_prev=False)
        self.f_reflectivity_draw()
        self.statusbar.clearMessage()

        # RUN - step 1 - create new directory or rewrite files if they already exists
        if not self.lineEdit_SaveAt_Dir_1.text(): self.lineEdit_SaveAt_Dir_1.setText(self.dir_current + "/")
        self.FOLDER_DATA = self.lineEdit_SaveAt_Dir_1.text() + self.lineEdit_SaveAt_Dir_2.text() + (
            "/" if not self.lineEdit_SaveAt_Dir_2.text()[-1] == "/" else "")
        if not os.path.exists(self.FOLDER_DATA): os.makedirs(self.FOLDER_DATA)

        # delete files from previous run
        for SLD_MultiGrPr_file in [self.MODE_SPECS[self.BoToFit_mode][1], 'SLD_profile.dat', 'SLD_profile_F1.dat', 'SLD_profile_F2.dat', 'multiGrPr.ent',
                                   'multiGrPr_2.ent', 'multiGrPr_F1.ent', 'multiGrPr_F2.ent']:
            try:
                os.remove(self.FOLDER_DATA + SLD_MultiGrPr_file)
            except:
                True

        # RUN - step 2 - get ready to start BoToFit
        self.f_inputDataFile_create()
        self.f_entryForBoToFit_create()

        # CHECKUP - dont run if Error in Statusbar
        if self.statusbar.currentMessage().find("Error") == 0: return

        # RUN - step 3 - Start BoToFit with its "killer" in 2 threads
        module = '"' + self.dir_current + '/BoToFit_Modules/' + self.MODE_SPECS[self.BoToFit_mode][0] + '"'
        entry = '"' + self.FOLDER_DATA + "boto.ent" + '"'
        data = '"' + self.FOLDER_DATA + "data_file_reformatted.dat" + '"'

        self.pushButton_StartFitting.setText("Stop fitting")
        self.statusbar.showMessage("Running...")

        # start BoToFit module with Threading
        for i in range(2):
            t = threading.Thread(target=self.f_BoToFit_run, args=(
            self.FOLDER_DATA, i, module, entry, data, self.lineEdit_ScanParameters_PointsToExclude_first.text(),
            self.lineEdit_ScanParameters_PointsToExclude_last.text()))
            t.start()

        # wait until "killer" is done or BoToFit has crashed
        BoToFit_threadIsDone = 0
        while BoToFit_threadIsDone == 0:
            QtTest.QTest.qWait(1000)
            list_proc = [proc.name() for proc in psutil.process_iter() if proc.name() == self.MODE_SPECS[self.BoToFit_mode][0]]
            ''' Button "Stop fitting" will kill "BoToFit" process, so we can move on '''
            if len(list_proc) == 0: BoToFit_threadIsDone = 1

        # RUN - step 4 - analize the results depending on "how BoToFit was stopped"
        if self.MODE_SPECS[self.BoToFit_mode][1] not in os.listdir(self.FOLDER_DATA):
            ''' If BoToFit stops prematurely '''
            # self.f_clearStuff(chi_prev=False)
            self.f_reflectivity_draw()
            self.statusbar.showMessage("BoToFit crashed or has been stopped by user. Anyway, consider using more reasonable 'Start fit' values.")
            self.f_button_loadFitbagFile()

            ''' Threading - Complimentary BoToFit - all params fixed (needed to get fitfunct) '''
            for i in range(2):
                t = threading.Thread(target=self.f_BoToFit_run,
                                     args=(self.FOLDER_DATA + "temp/", i, module, '"' + self.FOLDER_DATA + "temp/boto.ent" + '"', data,
                                           self.lineEdit_ScanParameters_PointsToExclude_first.text(),
                                           self.lineEdit_ScanParameters_PointsToExclude_last.text()))
                t.start()

            # wait until "killer" is done or "BoToFit" has crashed
            BoToFit_threadIsDone = 0
            while BoToFit_threadIsDone == 0:
                QtTest.QTest.qWait(1000)
                list_proc = []
                for proc in psutil.process_iter(): list_proc.append(proc.name())
                if self.MODE_SPECS[self.BoToFit_mode][0] not in list_proc: BoToFit_threadIsDone = 1

            if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]: files_fitFunc = ["FitFunct.dat"]
            elif self.BoToFit_mode in ["m_2", "t_2", "m_2_m", "m_2_f"]: files_fitFunc = ["Fit2DFunctUU.dat", "Fit2DFunctDD.dat"]
            elif self.BoToFit_mode in ["m_4", "t_4", "m_4_m", "m_4_f"]: files_fitFunc = ["Fit2DFunctUU.dat", "Fit2DFunctDD.dat", "Fit2DFunctUD.dat", "Fit2DFunctDU.dat"]

            # Mono_0_multy mode takes time to write a lot of points, so wait
            if self.BoToFit_mode == "m_0_m": QtTest.QTest.qWait(2000)

            for file in files_fitFunc:
                os.replace(self.FOLDER_DATA + "temp/" + file, self.FOLDER_DATA + file)
            shutil.rmtree(self.FOLDER_DATA + "temp", ignore_errors=True)

            self.f_reformFitFunct_drawAndExport()
            self.f_diff_draw()
            self.pushButton_StartFitting.setText("Start fitting")
            return

        else:
            ''' If BoToFit stops as it should '''
            self.pushButton_StartFitting.setText("Start fitting")

            # wait until fitting is done -> fill the table, draw graphs and create multiGrPr.ent using FitBag.dat file
            self.graphicsView_ReflectivityProfile.getPlotItem().clear()
            self.f_reflectivity_draw()
            self.f_reformFitFunct_drawAndExport()
            self.f_diff_draw()

            self.f_entryForMultiGrPr_create(
                self.FOLDER_DATA + ["Fit2DBag.dat" if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"] else "FitBag.dat"][0])

            self.f_multyGrPr_run()
            self.f_sld_draw()  # draw SLD

            self.statusbar.showMessage("Finished in " + str(round(float(time.time() - time_start), 1)) + " seconds")
    ##<--

    ##--> menu options
    def f_menuInfo(self):

        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(self.iconpath))
        msgBox.setText( "BoToFit " + self.actionVersion.text() + "\n\n"
                        "Algorithm: Boris.Toperverg@ruhr-uni-bochum.de\n"
                        "GUI: Alexey.Klechikov@gmail.com\n\n"
                        "Check for newer version at https://github.com/Alexey-Klechikov/BoToFit/releases")
        msgBox.exec_()
    ##<--

    ##--> "input file"
    def f_dataFiles_parse(self):
        ''' I write data points into self.Data_DataFiles variable in [*angle, *I, *dI] format to avoid multiple parsings of the same file
            inside the self.Data_DataFiles, the data are ordered as self.Data_DataFiles[File, polarization][Parameter][Point number]
            polarisation order in self.Data_DataFiles = [UU, (DD), (UD), DU]
        '''
        # change comboboxes if required
        if self.checkBox_DataFile_Preformatted.isChecked():
            comboboxes = [self.comboBox_DataFile_Column1, self.comboBox_DataFile_Column2, self.comboBox_DataFile_Column3]
            for i, combobox in enumerate(comboboxes): combobox.setCurrentIndex([1, 2, 0 if self.BoToFit_mode in ["t_0", "t_2", "t_4", "t_0_sl"] else 3][i])

        self.Data_DataFiles = []
        self.f_clearStuff(fitRes=False)

        # parse data files if none of comboboxes are the same
        self.inputStructure = [self.comboBox_DataFile_Column1.currentText(), self.comboBox_DataFile_Column2.currentText(), self.comboBox_DataFile_Column3.currentText()]
        if not ([x for n, x in enumerate(self.inputStructure) if x in self.inputStructure[:n]] == [] and not self.lineEdit_DataFile.text() in ["", "[]"] and "I" in self.inputStructure and "dI" in self.inputStructure):
            self.statusbar.showMessage("Error: recheck 'Data file structure' comboboxes.")
            return

        # preformatted BoToFit data file should contain all polarisations in the format "I dI (ang(Qz) if TOF else ang(rad))"
        if self.checkBox_DataFile_Preformatted.isChecked():
            with open([self.lineEdit_DataFile.text() if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"] else self.lineEdit_DataFile.text().split("'")[1]][0], "r") as dataFile_preformatted:

                lines = [line for line in dataFile_preformatted.readlines() if line.strip()]
                self.lineEdit_NumberOfPoints = len(lines) if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"] else [len(lines)/2 if self.BoToFit_mode in ["m_2", "t_2", "m_2_m", "m_2_f"] else len(lines)/4][0]

                data_angle, data_I, data_dI = [], [], []
                for i, line in enumerate(lines):
                    for ind, dat in enumerate((data_I, data_dI, data_angle)): dat.append(float(line.split()[ind]))
                    if (i + 1) % self.lineEdit_NumberOfPoints == 0:
                        self.Data_DataFiles.append((data_angle, data_I, data_dI))
                        data_angle, data_I, data_dI = [], [], []

        # otherwice we analize several files with chosen structure
        else:
            files = [""] if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_m", "m_0_f"] else ["", "", "", ""]

            # reformat data to *I *dI *angle(rad) in Mono mode
            if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]:
                files[0] = self.lineEdit_DataFile.text()
            else:
                for i in self.lineEdit_DataFile.text().split("'"):
                    if i.rfind("_uu") > 0 or i.rfind("_UU") > 0 or i.rfind("_u_") > 0 or i.rfind("_U_") > 0: files[0] = i
                    elif i.rfind("_dd") > 0 or i.rfind("_DD") > 0: files[1] = i
                    elif i.rfind("_ud") > 0 or i.rfind("_UD") > 0: files[2] = i
                    elif i.rfind("_du") > 0 or i.rfind("_DU") > 0 or i.rfind("_d_") > 0 or i.rfind("_D_") > 0: files[-1] = i

            for file in [i for i in files if len(i) > 0]:
                self.lineEdit_NumberOfPoints, data_angle, data_I, data_dI = 0, [], [], []

                with open(file, 'r') as dataFile_input:
                    for i, line in enumerate([line for line in dataFile_input.readlines() if line.strip()]):
                        if file[-4:] == '.mft' and i < 23: continue # for Figaro

                        data_angle.append(float(line.split()[self.inputStructure.index("ang(Qz)" if "ang(Qz)" in self.inputStructure else "ang(rad)")]))
                        data_I.append(float(line.split()[self.inputStructure.index("I")]))
                        data_dI.append(float(line.split()[self.inputStructure.index("dI")]))
                        self.lineEdit_NumberOfPoints += 1

                self.Data_DataFiles.append((data_angle, data_I, data_dI))

        # perform checkups of the data files
        self.statusbar.clearMessage()
        # 1 - missing files
        if (self.BoToFit_mode in ["m_2", "t_2", "m_2_m", "m_2_f"] and not len(self.Data_DataFiles) == 2) or (self.BoToFit_mode in ["m_4", "t_4", "m_4_m", "m_4_f"] and not len(self.Data_DataFiles) == 4):
            self.statusbar.showMessage("Error: Not enough Data files or missing points in the preformatted file.")
        # 2 - missing points
        elif (len(self.Data_DataFiles) == 2 and not len(self.Data_DataFiles[0]) == len(self.Data_DataFiles[1])) or (len(self.Data_DataFiles) == 4 and not len(self.Data_DataFiles[0]) == len(self.Data_DataFiles[1]) == len(self.Data_DataFiles[2]) == len(self.Data_DataFiles[3])):
            self.statusbar.showMessage("Error: Your input data files have different numbers of points.")
        # 3 - points aren't consistent
        else:
            for pol in self.Data_DataFiles:
                for i in range(1, len(pol[0])):
                    if pol[0][i] < pol[0][i-1]: self.statusbar.showMessage("Warning: Your point order is not consistent. Recheck the point at the angle " + str(pol[0][i-1]))

        if self.statusbar.currentMessage().find("Error") == 0: return

        self.f_reflectivity_draw()

    def f_inputDataFile_create(self):
        ''' input data files for BoToFit should have [*I *dI *angle(rad)] format in Mono mode and [*I *dI *Qz] in TOF mode '''

        with open(self.FOLDER_DATA + "data_file_reformatted.dat", 'w') as data_file_output:
            # check hidden table with experimental points already reformatted in Q I dI format
            for i in range(0, len(self.Data_DataFiles)):
                data_angle, data_I, data_dI = self.Data_DataFiles[i]

                for j in range(0, len(data_angle)):
                    if self.BoToFit_mode in ["t_0", "t_2", "t_4", "t_0_sl"]: data_file_output.write(str(data_I[j]) + "  " + str(data_dI[j]) + "    " + str(data_angle[j]) + "\n")
                    else: data_file_output.write(str(data_I[j]) + "  " + str(data_dI[j]) + "    " + str(data_angle[j] if not "ang(Qz)" in self.inputStructure else self.f_angleConvert("Qz", "rad", float(data_angle[j]))) + "\n")
    ##<--

    ##--> "BoToFit entry"
    def f_entryFile_load(self, param_entryFunc=""):
        ''' I use this function both at first run of the program to load "default" values and to import user's entry file '''
        if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: self.importing = True
        # remove cursor from the table for import
        self.tableWidget_FilmDescription.setCurrentCell(-1, -1)

        # Step 1: either we use entry sent as the parameter, or we allow user to open one manually
        file_entry = QtWidgets.QFileDialog().getOpenFileName(None, "Entry file", self.dir_current if len(self.lineEdit_SaveAt_Dir_1.text()) < 1 else self.lineEdit_SaveAt_Dir_1.text())[0] if not param_entryFunc else param_entryFunc
        if file_entry == "": return

        ENTRY = pd.read_csv(file_entry, header=None, squeeze=True)

        # Step 2: fill the form with parameters from the entry
        reference_index = 0
        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]:
            self.lineEdit_ScanParameters_Piy.setText(ENTRY[2].split()[0]) # Piy incident polarization (polariser)
            self.f_setChecked(self.checkBox_ScanParameters_Piy, ENTRY[3].split()[0])
            self.lineEdit_ScanParameters_Pfy.setText(ENTRY[8].split()[0]) # Pfy outgoing polarization (analyser)
            self.f_setChecked(self.checkBox_ScanParameters_Pfy, ENTRY[9].split()[0])
            reference_index = 12

        self.lineEdit_ScanParameters_Wavelength.setText(ENTRY[reference_index].split()[0]) # wavelength or incident angle
        self.lineEdit_ScanParameters_NumberOfPtsForResolutionFunction.setText(ENTRY[reference_index+2].split()[0]) # number of experimental points in alpha
        self.lineEdit_ScanParameters_StepForResolutionFunction.setText(ENTRY[reference_index+3].split()[0]) # step for resolution function (in mrad)
        self.lineEdit_ScanParameters_Sigma.setText(ENTRY[reference_index+4].split()[0]) # "sigma" of resolution function (in mrad)

        # Check if we input proper Entry file by checkup for number of layers (should be int, not float)
        try:
            self.statusbar.clearMessage()
            _ = int(ENTRY[reference_index + 5].split()[0])
            if self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"]: _, _, _ = int(ENTRY[reference_index + 6].split()[0]), int(ENTRY[reference_index + 7].split()[0]), int(ENTRY[reference_index + 8].split()[0])
        except:
            self.statusbar.showMessage("Error: Incompatible entry format.")
            return

        if self.BoToFit_mode in ["m_0", "m_2", "m_4", "t_0", "t_2", "t_4", "m_0_sl", "t_0_sl", "m_0_f", "m_2_f", "m_4_f"]: numberOfLayers, reference_index = int(ENTRY[reference_index+5].split()[0]), reference_index + 6   # no multi modules
        elif self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"]: # multi modules
            numberOfLayers_cap = int(ENTRY[reference_index + 5].split()[0]) # "ncap" number of cap layers
            numberOfLayers_sub = int(ENTRY[reference_index + 6].split()[0]) # "nsub" number of sub-ayers in a superstructure
            numberOfLayers_repetitions = int(ENTRY[reference_index + 7].split()[0]) # "nrep" number of repetitions
            numberOfLayers_buffer = int(ENTRY[reference_index + 8].split()[0]) # "nbuf" number of buffer layers
            numberOfLayers, reference_index = numberOfLayers_cap + numberOfLayers_sub + numberOfLayers_buffer, reference_index + 9

        # delete all layers except substrate from the table
        while not self.tableWidget_FilmDescription.rowCount() == 1: self.tableWidget_FilmDescription.removeRow(0)
        while not self.tableWidget_FilmDescription_2.rowCount() == 1:self.tableWidget_FilmDescription_2.removeRow(0)
        # add layers to the table
        for i in range(0, numberOfLayers):
            self.f_buttons_addRemoveLayer()
            self.tableWidget_FilmDescription.item(0, 0).setText(str(numberOfLayers - i))
            self.tableWidget_FilmDescription_2.item(0, 0).setText(str(numberOfLayers - i))

        # reformat the table in multi modes
        if self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"]:
            self.tableWidget_FilmDescription.setSpan(numberOfLayers_cap, 0, numberOfLayers_sub, 1)

            for row in range(0, numberOfLayers):
                if row < numberOfLayers_cap: self.tableWidget_FilmDescription.item(row, 0).setText(str(row+1))
                elif row < numberOfLayers_cap + numberOfLayers_sub: self.tableWidget_FilmDescription.item(row, 0).setText(str(row+1) + " x " + str(numberOfLayers_repetitions))
                else: self.tableWidget_FilmDescription.item(row, 0).setText(str(row+2-numberOfLayers_sub))

        # check if user wants to import SL entry, while SL checkbox isnt True
        if ENTRY[reference_index + 2].split()[1] == "+" and self.BoToFit_mode not in ["m_0_sl", "t_0_sl"]: self.statusbar.showMessage("Use 'Solid-Liquid' mode with this entry.")

        row, col, SL_sld_offset = 0, 1, ""
        for row in range(0, numberOfLayers+1):
            if not row == numberOfLayers:
                self.tableWidget_FilmDescription.item(row, col).setText(ENTRY[reference_index].split()[0].replace("d", "e")) # Thickness
                self.f_setChecked(self.tableWidget_FilmDescription.item(row, col + 1), ENTRY[reference_index+1].split()[0])
                self.tableWidget_FilmDescription_2.item(row, col).setText(ENTRY[reference_index].split()[0].replace("d", "e"))  # Thickness
                self.f_setChecked(self.tableWidget_FilmDescription_2.item(row, col + 1), ENTRY[reference_index + 1].split()[0])
            else: reference_index -= 2
            if self.BoToFit_mode not in ["m_0_f", "m_2_f", "m_4_f"]: # fill the table (not a FRAC mode)
                if SL_sld_offset == "": SL_sld_offset = float(ENTRY[reference_index + 2].split()[2]) if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] else 0
                self.tableWidget_FilmDescription.item(row, col + 2).setText(str(round(float(ENTRY[reference_index + 2].split()[0].replace("d", "e")) + SL_sld_offset, 5)))  # SLD
                self.f_setChecked(self.tableWidget_FilmDescription.item(row, col + 3), ENTRY[reference_index+3].split()[0])
                self.tableWidget_FilmDescription.item(row, col + 4).setText(ENTRY[reference_index + 4].split()[0].replace("d", "e"))  # iSLD
                self.f_setChecked(self.tableWidget_FilmDescription.item(row, col + 5), ENTRY[reference_index+5].split()[0])
                if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl"]:
                    self.tableWidget_FilmDescription.item(row, col + 10).setText(ENTRY[reference_index + 6].split()[0].replace("d", "e"))  # roughness
                    self.f_setChecked(self.tableWidget_FilmDescription.item(row, col + 11), ENTRY[reference_index + 7].split()[0])
                    reference_index += 8
                else:
                    self.tableWidget_FilmDescription.item(row, col + 6).setText(ENTRY[reference_index + 6].split()[0].replace("d", "e"))  # mSLD
                    self.f_setChecked(self.tableWidget_FilmDescription.item(row, col + 7), ENTRY[reference_index+7].split()[0])
                    self.tableWidget_FilmDescription.item(row, col + 8).setText(ENTRY[reference_index + 8].split()[0].replace("d", "e"))  # cos(d-gamma)
                    self.f_setChecked(self.tableWidget_FilmDescription.item(row, col + 9), ENTRY[reference_index+9].split()[0])
                    self.tableWidget_FilmDescription.item(row, col + 10).setText(ENTRY[reference_index + 10].split()[0].replace("d", "e"))  # roughness
                    self.f_setChecked(self.tableWidget_FilmDescription.item(row, col + 11), ENTRY[reference_index+11].split()[0])
                    reference_index += 12
            else:
                self.tableWidget_FilmDescription.item(row, col + 2).setText(str(round(float(ENTRY[reference_index + 2].split()[0].replace("d", "e")), 5)))  # SLD
                self.f_setChecked(self.tableWidget_FilmDescription.item(row, col + 3), ENTRY[reference_index + 3].split()[0])
                self.tableWidget_FilmDescription_2.item(row, col + 2).setText(str(round(float(ENTRY[reference_index + 4].split()[0].replace("d", "e")), 5)))  # SLD 1
                self.f_setChecked(self.tableWidget_FilmDescription_2.item(row, col + 3), ENTRY[reference_index + 5].split()[0])
                self.tableWidget_FilmDescription.item(row, col + 4).setText(ENTRY[reference_index + 6].split()[0].replace("d", "e"))  # iSLD
                self.f_setChecked(self.tableWidget_FilmDescription.item(row, col + 5), ENTRY[reference_index + 7].split()[0])
                self.tableWidget_FilmDescription_2.item(row, col + 4).setText(ENTRY[reference_index + 8].split()[0].replace("d", "e"))  # iSLD 2
                self.f_setChecked(self.tableWidget_FilmDescription_2.item(row, col + 5), ENTRY[reference_index + 9].split()[0])
                self.tableWidget_FilmDescription.item(row, col + 6).setText(ENTRY[reference_index + 10].split()[0].replace("d", "e"))  # mSLD
                self.f_setChecked(self.tableWidget_FilmDescription.item(row, col + 7), ENTRY[reference_index + 11].split()[0])
                self.tableWidget_FilmDescription_2.item(row, col + 6).setText(ENTRY[reference_index + 12].split()[0].replace("d", "e"))  # mSLD 2
                self.f_setChecked(self.tableWidget_FilmDescription_2.item(row, col + 7), ENTRY[reference_index + 13].split()[0])
                self.tableWidget_FilmDescription.item(row, col + 8).setText(ENTRY[reference_index + 14].split()[0].replace("d", "e"))  # cos(d-gamma)
                self.f_setChecked(self.tableWidget_FilmDescription.item(row, col + 9), ENTRY[reference_index + 15].split()[0])
                self.tableWidget_FilmDescription_2.item(row, col + 8).setText(ENTRY[reference_index + 16].split()[0].replace("d", "e"))  # cos(d-gamma) 2
                self.f_setChecked(self.tableWidget_FilmDescription_2.item(row, col + 9), ENTRY[reference_index + 17].split()[0])
                self.tableWidget_FilmDescription.item(row, col + 10).setText(ENTRY[reference_index + 18].split()[0].replace("d", "e"))  # roughness
                self.f_setChecked(self.tableWidget_FilmDescription.item(row, col + 11), ENTRY[reference_index + 19].split()[0])
                self.tableWidget_FilmDescription_2.item(row, col + 10).setText(ENTRY[reference_index + 20].split()[0].replace("d", "e"))  # roughness 2
                self.f_setChecked(self.tableWidget_FilmDescription_2.item(row, col + 11), ENTRY[reference_index + 21].split()[0])
                reference_index += 22

        if self.BoToFit_mode in ["m_0_sl", "t_0_sl"]: # Solid-Liquid
            self.f_slLayer_add()
            self.tableWidget_FilmDescription.item(0, 3).setText(str(float(SL_sld_offset)))

        if self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"]: # periodical multilayers
            self.lineEdit_ScanParameters_GradientPeriod.setText(ENTRY[reference_index].split()[0])    # Gradient Period (-1 < "grad"< 1)
            self.f_setChecked(self.checkBox_ScanParameters_GradientPeriod, ENTRY[reference_index + 1].split()[0])
            self.lineEdit_ScanParameters_GradientRoughness.setText(ENTRY[reference_index + 2].split()[0])     # Gradient Roughness (DW)  (-1 < "grad"< 1)
            self.f_setChecked(self.checkBox_ScanParameters_GradientRoughness, ENTRY[reference_index + 3].split()[0])
            self.lineEdit_ScanParameters_GradientSld.setText(ENTRY[reference_index + 4].split()[0])       # Gradient SLD (Nb) (-1 < "grad"< 1)
            self.f_setChecked(self.checkBox_ScanParameters_GradientSld, ENTRY[reference_index + 5].split()[0])
            if not self.BoToFit_mode == "m_0_m":
                self.lineEdit_ScanParameters_GradientMsld.setText(ENTRY[reference_index + 6].split()[0])      # Gradient mSLD (Np) (-1 < "grad"< 1)
                self.f_setChecked(self.checkBox_ScanParameters_GradientMsld, ENTRY[reference_index + 7].split()[0])
                reference_index += 8
            else: reference_index += 6

        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]:
            self.lineEdit_ScanParameters_Cg.setText(ENTRY[reference_index].split()[0])     # cg: mean value <cos(gamma)> over big domains
            self.f_setChecked(self.checkBox_ScanParameters_Cg, ENTRY[reference_index + 1].split()[0])
            if self.BoToFit_mode not in ["m_2_f", "m_4_f"]:
                self.lineEdit_ScanParameters_Sg.setText(ENTRY[reference_index + 2].split()[0])     # sg: mean value <sin(gamma)> over big domains
                self.f_setChecked(self.checkBox_ScanParameters_Sg, ENTRY[reference_index + 3].split()[0])
                self.lineEdit_ScanParameters_Sg2.setText(ENTRY[reference_index + 4].split()[0])    # sg2: mean value <sin^2(gamma)> over big domains
                self.f_setChecked(self.checkBox_ScanParameters_Sg2, ENTRY[reference_index + 5].split()[0])
                reference_index += 6
            else:
                self.lineEdit_ScanParameters_Sg.setText(ENTRY[reference_index + 2].split()[0])  # sg: mean value <sin(gamma)> over big domains
                self.f_setChecked(self.checkBox_ScanParameters_Sg, ENTRY[reference_index + 3].split()[0])
                self.lineEdit_ScanParameters_Sg2.setText(ENTRY[reference_index + 4].split()[0])  # sg2: mean value <sin^2(gamma)> over big domains
                self.f_setChecked(self.checkBox_ScanParameters_Sg2, ENTRY[reference_index + 5].split()[0])
                self.lineEdit_ScanParameters_Cg_2.setText(ENTRY[reference_index + 6].split()[0])  # cg 2
                self.f_setChecked(self.checkBox_ScanParameters_Cg_2, ENTRY[reference_index + 7].split()[0])
                self.lineEdit_ScanParameters_Sg_2.setText(ENTRY[reference_index + 8].split()[0])  # sg 2
                self.f_setChecked(self.checkBox_ScanParameters_Sg_2, ENTRY[reference_index + 9].split()[0])
                self.lineEdit_ScanParameters_Sg2_2.setText(ENTRY[reference_index + 10].split()[0])    # sg2 2
                self.f_setChecked(self.checkBox_ScanParameters_Sg2_2, ENTRY[reference_index + 11].split()[0])
                reference_index += 12

        if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]:
            self.lineEdit_ScanParameters_FractionAmount.setText(ENTRY[reference_index].split()[0]) # fraction amount
            self.f_setChecked(self.checkBox_ScanParameters_FractionAmount, ENTRY[reference_index + 1].split()[0])
            reference_index += 2

        self.lineEdit_ScanParameters_ScalingFactor.setText(ENTRY[reference_index].split()[0])     # ct  total scaling factor
        self.f_setChecked(self.checkBox_ScanParameters_ScalingFactor, ENTRY[reference_index + 1].split()[0])
        self.lineEdit_ScanParameters_CrossoverOverillumination.setText(ENTRY[reference_index + 2].split()[0])     # alpha_0 crossover angle overillumination (in mrad)
        self.f_setChecked(self.checkBox_ScanParameters_CrossoverOverillumination, ENTRY[reference_index + 3].split()[0])
        self.lineEdit_ScanParameters_Background.setText(ENTRY[reference_index + 4].split()[0])    # bgr 'background'
        self.f_setChecked(self.checkBox_ScanParameters_Background, ENTRY[reference_index + 5].split()[0])
        self.lineEdit_ScanParameters_ZeroCorrection.setText(ENTRY[reference_index + 6].split()[0])   # correction of the detector 'zero' (in mrad)

        if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: self.importing = False

        self.f_resolutionFunction_draw()

    def f_entryForBoToFit_create(self):
        ''' BoToFit needs its own entry file, so we make one using data from the table '''
        ENTRY, self.ncap, self.nsub, self.nrep, self.nbuf = [], 0, 0, 0, 0

        # polarisation
        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]:
            ENTRY.append("0     Pix incident polarization (polariser)\nf\n" + self.lineEdit_ScanParameters_Piy.text() + '    Piy\n' + self.f_checkChecked(self.checkBox_ScanParameters_Piy) + "\n" + "0     Piz\nf\n\n")
            ENTRY.append("0     Pfx outgoing polarization (analyser)\nf\n" + self.lineEdit_ScanParameters_Pfy.text() + '    Pfy\n' + self.f_checkChecked(self.checkBox_ScanParameters_Pfy) + "\n" + "0     Pfz\nf\n\n")
        # wavelength / inc.angle
        if self.BoToFit_mode not in ["t_0", "t_2", "t_4", "t_0_sl"]: ENTRY.append(self.lineEdit_ScanParameters_Wavelength.text() + '        wavelength (in Angstrem)\n')
        else: ENTRY.append(self.lineEdit_ScanParameters_Wavelength.text() + '        incident angle (in mrad)\n')
        # other parameters (header)
        ENTRY.append(str(self.lineEdit_NumberOfPoints) + "        *nn number of experimental points in alpha (<1001)\n")
        ENTRY.append(self.lineEdit_ScanParameters_NumberOfPtsForResolutionFunction.text() + "        *j0 number of points for resolution function (odd) (<102)\n")
        ENTRY.append(self.lineEdit_ScanParameters_StepForResolutionFunction.text() + "        step for resolution function (in mrad)\n")
        ENTRY.append(self.lineEdit_ScanParameters_Sigma.text() + "        *sigma of resolution function (in mrad)\n\n")
        # number of layers
        if self.BoToFit_mode in ["m_0", "m_2", "m_4", "t_0", "t_2", "t_4", "m_0_f", "m_2_f", "m_4_f"]: ENTRY.append(str(self.tableWidget_FilmDescription.rowCount() - 1) + "        number of layers (excluding substrate) (<21)\n\n")
        elif self.BoToFit_mode in ["m_0_sl", "t_0_sl"]: ENTRY.append(str(self.tableWidget_FilmDescription.rowCount() - 2) + "        number of layers (excluding substrate_sl) (<21)\n\n")
        else:
            for row, span in enumerate([self.tableWidget_FilmDescription.rowSpan(row, 0) for row in range(0, self.tableWidget_FilmDescription.rowCount() - 1)]):
                if self.nsub == 0 and self.nrep == 0 and span == 1 and not "x" in self.tableWidget_FilmDescription.item(row, 0).text(): self.ncap += 1
                elif self.nsub == 0 and (span > 1 or "x" in self.tableWidget_FilmDescription.item(row, 0).text()):
                    self.nsub, self.nrep = span, int(self.tableWidget_FilmDescription.item(row, 0).text()[self.tableWidget_FilmDescription.item(row, 0).text().find("x") + 1:])
                elif self.nrep > 0 and span == 1: self.nbuf += 1
            ENTRY.append(str(self.ncap) + "        \"ncap\" number of cap layers\n")
            ENTRY.append(str(self.nsub) + "        \"nsub\" number of sub-layers in a superstructure\n")
            ENTRY.append(str(self.nrep) + "        \"nrep\" number of repetitions\n")
            ENTRY.append(str(self.nbuf) + "        \"nbuf\" number of buffer layers\n\n")
        # read the table
        for i in range(1 if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] else 0, self.tableWidget_FilmDescription.rowCount()):
            comment = ""
            # Thickness
            if not self.tableWidget_FilmDescription.item(i, 0).text() in ["Substrate", "Liquid"]:
                if self.BoToFit_mode in ["m_0", "m_2", "m_4", "t_0", "t_2", "t_4", "m_0_f", "m_2_f", "m_4_f"]: layer = str(i+1)
                elif self.BoToFit_mode in ["m_0_sl", "t_0_sl"]: layer = str(i)
                elif self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"]:
                    if i < self.ncap: layer = "Cap " + str(i+1)
                    elif i < self.ncap + self.nsub: layer = "Sub " + str(i+1-self.ncap)
                    elif i < self.ncap + self.nsub + self.nbuf: layer = "Buffer " + str(i+1-self.ncap-self.nsub)

                ENTRY.append(self.tableWidget_FilmDescription.item(i, 1).text() + "        layer " + layer + " - thickness (in A)\n" + self.f_checkChecked(self.tableWidget_FilmDescription.item(i, 2)) + "\n")
            else: comment = "substrate's"
            # SLD: In Solid-Liquid mode we subtract buffer SLD from all other SLD's.
            sld = self.tableWidget_FilmDescription.item(i, 3).text() if self.BoToFit_mode not in ["m_0_sl", "t_0_sl"] else str(str(float(self.tableWidget_FilmDescription.item(i, 3).text()) - float(self.tableWidget_FilmDescription.item(0, 3).text())) + " + " + self.tableWidget_FilmDescription.item(0, 3).text())
            ENTRY.append(sld + "        "+ comment + " nbr nuclear SLD Nb'  (in A**-2) *1e-6\n" + self.f_checkChecked(self.tableWidget_FilmDescription.item(i, 4)) + "\n")
            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]:
                ENTRY.append(self.tableWidget_FilmDescription_2.item(i, 3).text() + "        "+ comment + "    nbr2 nuclear SLD Nb'  (in A**-2) *1e-6\n" + self.f_checkChecked(self.tableWidget_FilmDescription_2.item(i, 4)) + "\n")
            # iSLD
            ENTRY.append(self.tableWidget_FilmDescription.item(i, 5).text() + "        " + comment + "    nbi nuclear SLD Nb'' (in A**-2) *1e-6\n" + self.f_checkChecked(self.tableWidget_FilmDescription.item(i, 6)) + "\n")
            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]:
                ENTRY.append(self.tableWidget_FilmDescription_2.item(i, 5).text() + "        "+ comment + "    nbi2 nuclear SLD Nb'' (in A**-2) *1e-6\n" + self.f_checkChecked(self.tableWidget_FilmDescription_2.item(i, 6)) + "\n")
            # mSLD, <cos(delta_gamma)>
            if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl"]:
                # mSLD
                ENTRY.append(self.tableWidget_FilmDescription.item(i, 7).text() + "        " + comment + "   Np magnetic SLD (in A**-2)*1e-6\n" + self.f_checkChecked(self.tableWidget_FilmDescription.item(i, 8)) + "\n")
                if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]:
                    ENTRY.append(self.tableWidget_FilmDescription_2.item(i, 7).text() + "        " + comment + "   Np2 magnetic SLD (in A**-2)*1e-6\n" + self.f_checkChecked(self.tableWidget_FilmDescription_2.item(i, 8)) + "\n")
                # <cos(delta_gamma)>
                ENTRY.append(self.tableWidget_FilmDescription.item(i, 9).text() + "        " + comment + "   c=<cos(delta_gamma)>\n" + self.f_checkChecked(self.tableWidget_FilmDescription.item(i, 10)) + "\n")
                if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]:
                    ENTRY.append(self.tableWidget_FilmDescription_2.item(i, 9).text() + "        " + comment + "   c2=<cos(delta_gamma)>\n" + self.f_checkChecked(self.tableWidget_FilmDescription_2.item(i, 10)) + "\n")
            # roughness
            ENTRY.append(self.tableWidget_FilmDescription.item(i, 11).text() + "        " + comment + "  dw Debye-Waller in [AA]\n" + self.f_checkChecked(self.tableWidget_FilmDescription.item(i, 12)) + "\n")
            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]:
                ENTRY.append(self.tableWidget_FilmDescription_2.item(i, 11).text() + "        " + comment + "  dw2 Debye-Waller in [AA]\n" + self.f_checkChecked(self.tableWidget_FilmDescription_2.item(i, 12)) + "\n\n")
            else: ENTRY.append("\n")
        # gradients
        if self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"]:
            ENTRY.append(self.lineEdit_ScanParameters_GradientPeriod.text() + '        Period gradient (-1 < "grad"< 1)\n' + self.f_checkChecked(self.checkBox_ScanParameters_GradientPeriod) + "\n")
            ENTRY.append(self.lineEdit_ScanParameters_GradientRoughness.text() + '        DW gradient (-1 < "grad"< 1)\n' + self.f_checkChecked(self.checkBox_ScanParameters_GradientRoughness) + "\n")
            ENTRY.append(self.lineEdit_ScanParameters_GradientSld.text() + '        Nb gradient (-1 < "grad"< 1)\n' + self.f_checkChecked(self.checkBox_ScanParameters_GradientSld) + "\n")
            ENTRY.append(self.lineEdit_ScanParameters_GradientMsld.text() + '        Np gradient (-1 < "grad"< 1)\n' + self.f_checkChecked(self.checkBox_ScanParameters_GradientMsld) + "\n\n" if not self.BoToFit_mode == "m_0_m" else "\n")
        # <cos(gamma)>, <sin(gamma)>, <sin^2(gamma)>
        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]:
            ENTRY.append(self.lineEdit_ScanParameters_Cg.text() + '        cg: mean value <cos(gamma)> over big domains\n' + self.f_checkChecked(self.checkBox_ScanParameters_Cg) + "\n")
            ENTRY.append(self.lineEdit_ScanParameters_Sg.text() + '        sg: mean value <sin(gamma)> over big domains\n' + self.f_checkChecked(self.checkBox_ScanParameters_Sg) + "\n")
            ENTRY.append(self.lineEdit_ScanParameters_Sg2.text() + '        sg2: mean value <sin^2(gamma)> over big domains\n' + self.f_checkChecked(self.checkBox_ScanParameters_Sg2) + "\n")
            if self.BoToFit_mode in ["m_2_f", "m_4_f"]:
                ENTRY.append(self.lineEdit_ScanParameters_Cg_2.text() + '        cg_2: mean value <cos(gamma)> over big domains\n' + self.f_checkChecked(self.checkBox_ScanParameters_Cg_2) + "\n")
                ENTRY.append(self.lineEdit_ScanParameters_Sg_2.text() + '        sg_2: mean value <sin(gamma)> over big domains\n' + self.f_checkChecked(self.checkBox_ScanParameters_Sg_2) + "\n")
                ENTRY.append(self.lineEdit_ScanParameters_Sg2_2.text() + '        sg2_2: mean value <sin^2(gamma)> over big domains\n' + self.f_checkChecked(self.checkBox_ScanParameters_Sg2_2) + "\n")
        # fraction amount
        if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]:
            ENTRY.append(self.lineEdit_ScanParameters_FractionAmount.text() + '        fraction of 1-st type of domains\n' + self.f_checkChecked(self.checkBox_ScanParameters_FractionAmount) + "\n\n")
        elif self.BoToFit_mode not in ["m_0_f", "m_0", "t_0"]: ENTRY.append("\n")
        # other parameters (footer)
        ENTRY.append(self.lineEdit_ScanParameters_ScalingFactor.text() + "        *ct  total scaling factor\n" + self.f_checkChecked(self.checkBox_ScanParameters_ScalingFactor) + "\n")
        ENTRY.append(self.lineEdit_ScanParameters_CrossoverOverillumination.text() + "        *alpha_0 crossover angle overillumination (in mrad)\n" + self.f_checkChecked(self.checkBox_ScanParameters_CrossoverOverillumination) + "\n")
        ENTRY.append(self.lineEdit_ScanParameters_Background.text() + "        *bgr background\n" + self.f_checkChecked(self.checkBox_ScanParameters_Background) + "\n")
        ENTRY.append("\n" + self.lineEdit_ScanParameters_ZeroCorrection.text() + "        correction of the detector 'zero' (in mrad)")

        with open(self.FOLDER_DATA + 'boto.ent', 'w') as file_entry:
            for i in ENTRY:
                try:
                    _ = float(i.split()[0])
                except:
                    if not i in [" ", "\n"]: self.statusbar.showMessage("Error: recheck the field <" + i + "> for the proper input.")
                file_entry.write(i)

    def f_entryForBoToFit_create_fromFitbag(self, FITBAG):
        ''' You come here from "create_entry_for_MultiGrPr" function. This is needed to create simulated reflectivity curve even when BoToFit crashed or has been stopped '''
        ENTRY_TEMP, self.ncap, self.nsub, self.nrep, self.nbuf = [], 0, 0, 0, 0

        # polarisation
        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]:
            ENTRY_TEMP.append("0     Pix incident polarization (polariser)\nf\n" + str(float(FITBAG[FITBAG["Name"] == "Pi(y)"]['Value'])) + "    Piy\nf\n" + "0     Piz\nf\n\n")
            ENTRY_TEMP.append("0     Pfx outgoing polarization (analyser)\nf\n" + str(float(FITBAG[FITBAG["Name"] == "Pf(y)"]['Value'])) + "    Pfy\nf\n" + "0     Pfz\nf\n\n")

        # wavelength / inc.angle
        if self.BoToFit_mode not in ["t_0", "t_2", "t_4", "t_0_sl"]: ENTRY_TEMP.append(self.lineEdit_ScanParameters_Wavelength.text() + '    wavelength (in Angstrem)\n')
        else: ENTRY_TEMP.append(self.lineEdit_ScanParameters_Wavelength.text() + '    incident angle (in mrad)\n')

        # other parameters (header)
        ENTRY_TEMP.append(str(self.lineEdit_NumberOfPoints) + "        *nn number of experimental points in alpha (<1001)\n")
        ENTRY_TEMP.append(self.lineEdit_ScanParameters_NumberOfPtsForResolutionFunction.text() + "        *j0 number of points for resolution function (odd) (<102)\n")
        ENTRY_TEMP.append(self.lineEdit_ScanParameters_StepForResolutionFunction.text() + "        step for resolution function (in mrad)\n")
        ENTRY_TEMP.append(self.lineEdit_ScanParameters_Sigma.text() + "        *sigma of resolution function (in mrad)\n\n")

        # number of layers
        if self.BoToFit_mode in ["m_0", "m_2", "m_4", "t_0", "t_2", "t_4", "m_0_f", "m_2_f", "m_4_f"]:
            ENTRY_TEMP.append(str(self.tableWidget_FilmDescription.rowCount() - 1) + "        number of layers (excluding substrate) (<21)\n\n")
        elif self.BoToFit_mode in ["m_0_sl", "t_0_sl"]:
            ENTRY_TEMP.append(str(self.tableWidget_FilmDescription.rowCount() - 2) + "        number of layers (excluding substrate_sl) (<21)\n\n")
        else:
            for row, span in enumerate([self.tableWidget_FilmDescription.rowSpan(row, 0) for row in range(0, self.tableWidget_FilmDescription.rowCount() - 1)]):
                if self.nsub == 0 and self.nrep == 0 and span == 1 and not "x" in self.tableWidget_FilmDescription.item(row, 0).text(): self.ncap += 1
                elif self.nsub == 0 and (span > 1 or "x" in self.tableWidget_FilmDescription.item(row, 0).text()):
                    self.nsub, self.nrep = span, int(self.tableWidget_FilmDescription.item(row, 0).text()[self.tableWidget_FilmDescription.item(row, 0).text().find("x") + 1:])
                elif self.nrep > 0 and span == 1: self.nbuf += 1
            ENTRY_TEMP.append(str(self.ncap) + "        \"ncap\" number of cap layers\n")
            ENTRY_TEMP.append(str(self.nsub) + "        \"nsub\" number of sub-layers in a superstructure\n")
            ENTRY_TEMP.append(str(self.nrep) + "        \"nrep\" number of repetitions\n")
            ENTRY_TEMP.append(str(self.nbuf) + "        \"nbuf\" number of buffer layers\n\n")

        # table
        for layer_number in range(0, self.tableWidget_FilmDescription.rowCount() - (1 if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] else 0)):
            comment = ""

            # Thickness
            if not layer_number == self.tableWidget_FilmDescription.rowCount() - (1 if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] else 0) - 1:
                if self.BoToFit_mode not in ["m_0_m", "m_2_m", "m_4_m"]: layer = str(layer_number + 1)
                else:
                    if layer_number < self.ncap: layer = "Cap " + str(layer_number + 1)
                    elif layer_number < self.ncap + self.nsub: layer = "Sub " + str(layer_number + 1 - self.ncap)
                    elif layer_number < self.ncap + self.nsub + self.nbuf: layer = "Buffer " + str(layer_number + 1 - self.ncap - self.nsub)

                ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "Thickness"].iloc[layer_number]['Value'])) + "        layer " + layer + " - thickness (in A)\nf\n")

            else: comment = "substrate's"

            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: iloc_index = layer_number * 2
            else: iloc_index = layer_number
            # SLD: In Solid-Liquid mode we subtract buffer SLD from all other SLD's.
            ENTRY_TEMP.append(str((float(FITBAG[FITBAG["Name"] == "SLD"].iloc[iloc_index]['Value']) * 1e6)) + (" + " + self.tableWidget_FilmDescription.item(0, 3).text() if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] else "") + "        " + comment + " nbr nuclear SLD Nb'  (in A**-2) *1e-6\nf\n")
            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "SLD"].iloc[iloc_index + 1]['Value']) * 1e6) + "        " + comment + "    nbr2 nuclear SLD Nb'  (in A**-2) *1e-6\nf\n")
            # iSLD
            ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "iSLD"].iloc[iloc_index]['Value']) * 1e6) + "        " + comment + "    nbi nuclear SLD Nb'' (in A**-2) *1e-6\nf\n")
            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "iSLD"].iloc[iloc_index + 1]['Value']) * 1e6) + "        " + comment + "    nbi2 nuclear SLD Nb'' (in A**-2) *1e-6\nf\n")
            # mSLD, <cos(delta_gamma)>
            if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl"]:
                # mSLD
                ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "mSLD"].iloc[iloc_index]['Value']) * 1e6) + "        " + comment + "   Np magnetic SLD (in A**-2)*1e-6\nf\n")
                if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "mSLD"].iloc[iloc_index + 1]['Value'])  * 1e6) + "        " + comment + "   Np2 magnetic SLD (in A**-2)*1e-6\nf\n")
                # <cos(delta_gamma)>
                ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "Cos(d-gamma)"].iloc[iloc_index]['Value'])) + "        " + comment + "   c=<cos(delta_gamma)>\nf\n")
                if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "Cos(d-gamma)"].iloc[iloc_index + 1]['Value'])) + "        " + comment + "   c2=<cos(delta_gamma)>\nf\n")
            # roughness
            ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "Roughness"].iloc[iloc_index]['Value'])) + "        " + comment + "  dw Debye-Waller in [AA]\nf\n")
            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "Roughness"].iloc[iloc_index + 1]['Value'])) + "        " + comment + "  dw2 Debye-Waller in [AA]\nf\n\n")
            else: ENTRY_TEMP.append("\n")

        # gradients
        if self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"]:
            ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "grad.Period"]['Value'])) + "        Period gradient (-1 < 'grad'< 1)\nf\n")
            ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "grad.Roughness"]['Value'])) + "        DW gradient (-1 < 'grad'< 1)\nf\n")
            ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "grad.SLD"]['Value'])) + "        Nb gradient (-1 < 'grad'< 1)\nf\n")
            ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "grad.mSLD"]['Value'])) + "        Np gradient (-1 < 'grad'< 1)\nf\n\n" if not self.BoToFit_mode == "m_0_m" else "\n")
        # <cos(gamma)>, <sin(gamma)>, <sin^2(gamma)>
        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]:
            ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "<cos(gamma)>"]['Value'])) + "        cg: mean value <cos(gamma)> over big domains\nf\n")
            ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "<sin(gamma)>"]['Value'])) + "        sg: mean value <sin(gamma)> over big domains\nf\n")
            ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "<sin2(gamma)>"]['Value'])) + "        sg2: mean value <sin^2(gamma)> over big domains\nf\n")
            if self.BoToFit_mode in ["m_2_f", "m_4_f"]:
                ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "<cos(gamma)>_F2"]['Value'])) + "        cg_2: mean value <cos(gamma)> over big domains\nf\n")
                ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "<sin(gamma)>_F2"]['Value'])) + "        sg_2: mean value <sin(gamma)> over big domains\nf\n")
                ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "<sin2(gamma)>_F2"]['Value'])) + "        sg2_2: mean value <sin^2(gamma)> over big domains\nf\n")
        # fraction amount
        if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: ENTRY_TEMP.append(self.lineEdit_ScanParameters_FractionAmount.text() + "        fraction of 1-st type of domains\nf\n\n")
        elif self.BoToFit_mode not in ["m_0_f", "m_0", "t_0"]: ENTRY_TEMP.append("\n")
        # other parameters (footer)
        ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "Scaling_factor"]['Value'])) + "        *ct  total scaling factor\nf\n")
        ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "Overillumination"]['Value'])) + "        *alpha_0 crossover angle overillumination (in mrad)\nf\n")
        ENTRY_TEMP.append(str(float(FITBAG[FITBAG["Name"] == "Background"]['Value'])) + "        *bgr background\nf\n")
        ENTRY_TEMP.append("\n" + self.lineEdit_ScanParameters_ZeroCorrection.text() + "        correction of the detector 'zero' (in mrad)")

        if not os.path.exists(self.FOLDER_DATA + "temp/"): os.makedirs(self.FOLDER_DATA + "temp/")

        with open(self.FOLDER_DATA + 'temp/boto.ent', 'w') as file_entry:
            for i in ENTRY_TEMP: file_entry.write(i)
    ##<--

    ##--> "Results table" and "multiGrPr entry"
    def f_entryForMultiGrPr_create(self, FITBAG_FILE, frac=False):
        # multiGrPr template
        multiGrPr_data = [[0, 0.977836, 0],
                          [0, 0.985158, 0],
                          [0, 0, 30, 0, 30, -200, 1000, 1999, 0.36, 3],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [1, 0, 0],
                          [1, 0, 0]]

        multiGrPr_info = [["Pix incident polarization (polariser)", "Piy", "Piz"],
                          ["Pfx outgoing polarization (analyser)", "Pfy", "Pfz"],
                          ["Wavelength lambda (in A)", "Min. angle of incidence alphai  (in mrad)", "Max. angle of incidence alhamax (in mrad)", "Min. angle of exit  (in mrad)", "Max. angle of exit  (in mrad)", "Min. z  (in Angstrom)", "Max. z  (in Angstrom)", "'nn' number of points in alphai (alphaf)", "'delta' width of Gaussian in (mrad)", "'nn0' number of withs averaged"],
                          ["Number of cap layers", "Number of sub-layers", "Number of repetitions", "Number of buffer layers"],
                          ["Layer 1  thickness in (A)", "Real part of nuclear SLD Nb'  (in A**-2) *1e-6", "Imaginary part of nuclear SLD Nb'' (in A**-2) *1e-6", "Magn. scatt. length density (SLD) Np (in A**-2) *1e-6", "c=<cos(delta_gamma)>_{over small domains}", "dw Debye-Waller in [AA]"],
                          ["Gradient Period", "Gradient SLD", "Gradient mSLD", "Gradient Roughness"],
                          ["Substrate Real part of nuclear SLD Nb' (in A**-2) *1e-6", "Imaginary part of nuclear SLD Nb'' (in A**-2) *1e-6", "Magnetic scattering length density Np (in A**-2) *1e-6", "c=<cos(delta_phi)>_{over small domains}", "dw Debye-Waller in [AA]"],
                          ["cg: mean value <cos(gamma)>  of 'big domains'' ! cg^2<1-sg2", "sg: mean <sin(gamma)>", "sg2: mean value <sin^2(gamma)> of 'big domains'"],
                          ["ct  total scaling factor", "alpha_0 [mrad] crossover illumination angle", "bgr"]]

        # Step 1: add some layers into the template
        nonInfLayers_index = [1 if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] else 0, self.tableWidget_FilmDescription.rowCount() - 1]

        for i in range(nonInfLayers_index[0] + 1, nonInfLayers_index[1]):
            multiGrPr_data.insert(5, [0, 0, 0, 0, 0, 0])
            multiGrPr_info.insert(5, ["Layer " + str(self.tableWidget_FilmDescription.rowCount() - i) + " thickness in (A)", "real part of nuclear SLD Nb'  (in A**-2) *1e-6",
                                      "imaginary part of nuclear SLD Nb'' (in A**-2) *1e-6", "magn. scatt. length density (SLD) Np (in A**-2) *1e-6", "c=<cos(delta_gamma)>_{over small domains}", "dw Debye-Waller in [AA]", "Gradient Period", "Gradient SLD", "Gradient mSLD", "Gradient Roughness"])

        # Step 2: reformat FitBag file and create Pandas dataframe "self.df_FITBAG"
        dict_replace = {"total scaling": "Scaling_factor", "alpha_0": "Overillumination", "Re{Nb1}": "SLD", "Re{Nb2}": "SLD", "Re{Nb}": "SLD", "Im{Nb1}": "iSLD", "Im{Nb2}": "iSLD", "Im{Nb}": "iSLD", "N_p1": "mSLD", "N_p2": "mSLD", "N_p": "mSLD",  "Debye-Waller1": "Roughness", "Debye-Waller2": "Roughness", "Debye-Waller": "Roughness", "background": "Background", "<Cos(delta_gamma": "Cos(d-gamma)", "<Cos(d_gamma)>":"Cos(d-gamma)", "<Cos(gamma)>":"<cos(gamma)>", "<Cos(gamma1)>":"<cos(gamma)>", "<Cos(gamma2)>":"<cos(gamma)>_F2", "<Sin(gamma)>":"<sin(gamma)>", "<Sin(gamma1)>":"<sin(gamma)>", "<Sin(gamma2)>":"<sin(gamma)>_F2", "<Sin^2(gamma)>":"<sin2(gamma)>", "<Sin^2(gamma1)>":"<sin2(gamma)>", "<Sin^2(gamma2)>":"<sin2(gamma)>_F2", "+/-": "", "on bound": "", "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%": "skip", "<grad>":"grad.Period", "<gradDw>":"grad.Roughness", "<gradDW>":"grad.Roughness", "<gradNb>":"grad.SLD", "<gradNp>":"grad.mSLD", "thickness":"Thickness", "<frac>":"[F1]_amount"}
        fitbag_data = []
        with open(FITBAG_FILE, "r") as fit_file:
            for line_number, line in reversed(list(enumerate(fit_file.readlines()))):
                for i in dict_replace.keys(): line = line.replace(i, dict_replace[i])

                line_arr = line.split()
                if len(line_arr) == 0 or line_arr[0] in ['skip', "sqrt(D):", "D=<Cos(gam)^2>-<Cos(gam)>^2:"]: continue

                fitbag_data.append(line_arr)
                if line.find(" iterate ") > 0: break

        self.df_FITBAG = pd.DataFrame(fitbag_data[::-1], columns=["Number", "Name", "Value", "Error", "Factor"]).fillna("None")
        
        # Step 3: fill multiGrPr_data
        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]:
            multiGrPr_data[0][1] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "Pi(y)"]['Value'])
            multiGrPr_data[1][1] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "Pf(y)"]['Value'])
        multiGrPr_data[2][0] = self.lineEdit_ScanParameters_Wavelength.text()

        if self.BoToFit_mode not in ["m_0_m", "m_2_m", "m_4_m"]: multiGrPr_data[3][3] = nonInfLayers_index[1] - nonInfLayers_index[0]
        else: multiGrPr_data[3] = self.ncap, self.nsub, self.nrep, self.nbuf
        # layers
        for layer_number in range(0, nonInfLayers_index[1] - nonInfLayers_index[0]):
            multiGrPr_data[4 + layer_number][0] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "Thickness"].iloc[layer_number]['Value'])
            
            # by changing iloc_index we will create 2 different multiGrPr.ent for 2 FRACs
            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: iloc_index = layer_number*2 + (1 if frac else 0)
            else: iloc_index = layer_number
            
            multiGrPr_data[4 + layer_number][1] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "SLD"].iloc[iloc_index]['Value']) * 1e+6
            multiGrPr_data[4 + layer_number][2] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "iSLD"].iloc[iloc_index]['Value']) * 1e+6
            if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl"]:
                multiGrPr_data[4 + layer_number][3] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "mSLD"].iloc[iloc_index]['Value']) * 1e+6
                multiGrPr_data[4 + layer_number][4] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "Cos(d-gamma)"].iloc[iloc_index]['Value'])
            multiGrPr_data[4 + layer_number][5] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "Roughness"].iloc[iloc_index]['Value'])
        # gradients
        if self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"]:
            multiGrPr_data[-4][0] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "grad.Period"]['Value'])
            multiGrPr_data[-4][1] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "grad.SLD"]['Value'])
            if not self.BoToFit_mode == "m_0_m": multiGrPr_data[-3][2] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "grad.mSLD"]['Value'])
            multiGrPr_data[-4][3] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "grad.Roughness"]['Value'])
        # substrate
        iloc_index_substrate = (nonInfLayers_index[1] - nonInfLayers_index[0]) * (2 if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"] else 1)  + (1 if frac else 0)
        multiGrPr_data[-3][0] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "SLD"].iloc[iloc_index_substrate]['Value']) * 1e+6
        multiGrPr_data[-3][1] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "iSLD"].iloc[iloc_index_substrate]['Value']) * 1e+6
        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl"]:
            multiGrPr_data[-3][2] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "mSLD"].iloc[iloc_index_substrate]['Value']) * 1e+6
            multiGrPr_data[-3][3] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "Cos(d-gamma)"].iloc[iloc_index_substrate]['Value'])
        multiGrPr_data[-3][4] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "Roughness"].iloc[iloc_index_substrate]['Value'])
        # estimate total thickness
        if self.BoToFit_mode not in ["m_0_m", "m_2_m", "m_4_m"]:
            for layer_number in range(0, nonInfLayers_index[1] - nonInfLayers_index[0]): multiGrPr_data[2][6] += float(self.df_FITBAG[self.df_FITBAG["Name"] == "Thickness"].iloc[layer_number]['Value'])
        else:
            for layer_number in range(0, nonInfLayers_index[1] - nonInfLayers_index[0]):
                multiGrPr_data[2][6] += float(self.df_FITBAG[self.df_FITBAG["Name"] == "Thickness"].iloc[layer_number]['Value'])
                if layer_number + 1 > self.ncap and layer_number < self.ncap + self.nsub:
                    multiGrPr_data[2][6] += float(self.df_FITBAG[self.df_FITBAG["Name"] == "Thickness"].iloc[layer_number]['Value']) * self.nrep

        if self.BoToFit_mode in ["m_2", "m_4", "t_2", "t_4", "m_2_m", "m_4_m", "m_2_f", "m_4_f"]:
            multiGrPr_data[-2][0] = float(self.df_FITBAG[self.df_FITBAG["Name"] == ("<cos(gamma)>_F2" if frac else "<cos(gamma)>")]['Value'])
            multiGrPr_data[-2][1] = float(self.df_FITBAG[self.df_FITBAG["Name"] == ("<sin(gamma)>_F2" if frac else "<sin(gamma)>")]['Value'])
            multiGrPr_data[-2][2] = float(self.df_FITBAG[self.df_FITBAG["Name"] == ("<sin2(gamma)>_F2" if frac else "<sin2(gamma)>")]['Value'])
        multiGrPr_data[-1][0] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "Scaling_factor"]['Value'])
        multiGrPr_data[-1][1] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "Overillumination"]['Value'])
        multiGrPr_data[-1][2] = float(self.df_FITBAG[self.df_FITBAG["Name"] == "Background"]['Value'])

        # Write file
        with open(self.FOLDER_DATA + ('multiGrPr.ent' if not frac else 'multiGrPr_2.ent'), 'w') as multiGrPr:
            for i in range(0, len(multiGrPr_data)):
                for j in range(0, len(multiGrPr_data[i])):
                    multiGrPr.write(str(round(float(multiGrPr_data[i][j]), 6)) + "     " + str(multiGrPr_info[i][j]) + "\n")
                multiGrPr.write("\n")

        if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"] and frac == False:
            self.f_entryForMultiGrPr_create(FITBAG_FILE, frac=True)
        else:
            self.f_fitResultsTable_fill()

            if self.statusbar.currentMessage() == "BoToFit crashed or has been stopped by user. Anyway, consider using more reasonable 'Start fit' values.": self.f_entryForBoToFit_create_fromFitbag(self.df_FITBAG)

    def f_fitResultsTable_fill(self):
        if not self.df_FITBAG.__class__ == pd.core.frame.DataFrame: return
        # clear results_table before another fit
        for i in range(0, self.tableWidget_FitResults.rowCount()): self.tableWidget_FitResults.removeRow(0)

        self.lineEdit_FitResults_ChiSquare_Actual.setText(str(float(self.df_FITBAG[self.df_FITBAG["Number"] == "hi_sq.norm:"]["Name"])))
        self.lineEdit_FitResults_NumberOfIterations.setText(str(int(self.df_FITBAG[self.df_FITBAG["Name"] == "iterate"]['Number'])))

        layer_name, counter_i, prefix_Frac = "", 0, " "

        for row_df in self.df_FITBAG.iterrows():
            # define prefix & layer name for parameters
            if row_df[1]["Number"] in ["Layer", "Substrate", "hi_sq.norm:"] or row_df[1]["Name"] == "iterate":
                layer_name = ("(La" if row_df[1]["Number"] == "Layer" else "(Su") + (row_df[1]["Name"] if row_df[1]["Number"] == "Layer" else "") + ")"
                continue

            if not row_df[1]["Name"] in ['Thickness', 'SLD', 'iSLD', 'mSLD', 'Cos(d-gamma)', 'Roughness']: layer_name = ""

            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]:
                if row_df[1]["Name"] in ['SLD', 'iSLD', 'mSLD', 'Cos(d-gamma)', 'Roughness']: prefix_Frac = "[F1] " if not prefix_Frac == "[F1] " else "[F2] "
                else: prefix_Frac = "    "

            # show fixed values
            if row_df[1]["Error"] == "fixed" and not self.checkBox_ShowFixed.isChecked(): continue

            # create table rows and set their properties
            self.tableWidget_FitResults.insertRow(self.tableWidget_FitResults.rowCount())
            self.tableWidget_FitResults.setRowHeight(counter_i, 22)
            for j in range(0, 6):
                item = QtWidgets.QTableWidgetItem()
                if not j == 2: item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
                if j == 0:
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    item.setCheckState(QtCore.Qt.Unchecked)
                self.tableWidget_FitResults.setItem(counter_i, j, item)

            # fill the row
            self.tableWidget_FitResults.item(counter_i, 1).setText(str(counter_i + 1))
            self.tableWidget_FitResults.item(counter_i, 2).setText(layer_name + (prefix_Frac if row_df[1]["Name"] in ['SLD', 'iSLD', 'mSLD', 'Cos(d-gamma)', 'Roughness'] else " ") + str(row_df[1]["Name"]))
            self.tableWidget_FitResults.item(counter_i, 3).setText(str(round(float(row_df[1]["Value"]) * (1e6 if row_df[1]["Name"] in ['SLD', 'iSLD', 'mSLD'] else 1) + (float(self.tableWidget_FilmDescription.item(0,3).text()) if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] and row_df[1]["Name"] == 'SLD' else 0), 8)))
            if row_df[1]["Error"] == "fixed": self.tableWidget_FitResults.item(counter_i, 4).setText("fixed")
            elif not "infinite" in [row_df[1]["Value"], row_df[1]["Error"], row_df[1]["Factor"]]:
                self.tableWidget_FitResults.item(counter_i, 4).setText(str(round(float(row_df[1]["Error"]) * (1e6 if row_df[1]["Name"] in ['SLD', 'iSLD', 'mSLD'] else 1), 8)))
                self.tableWidget_FitResults.item(counter_i, 5).setText(str(round(float(row_df[1]["Factor"]), 8)))
            else: self.tableWidget_FitResults.item(counter_i, 4).setText(str(row_df[1]["Error"]))

            counter_i += 1
    ##<--

    ##--> draw graphs
    def f_reflectivity_draw(self):
        ''' draw reflectivity in Angle vs. lg(I) scale using data from hidden table '''
        color = [0, 0, 0]

        if "ang(Qz)" in self.inputStructure: self.label_ReflectivityProfileAndDiff.setText("Reflectivity profile (I[              ] vs. Qz[Å**-1]) and Difference (Exper/Fit):")
        elif "ang(rad)" in self.inputStructure: self.label_ReflectivityProfileAndDiff.setText("Reflectivity profile (I[              ] vs. Angle[mrad]) and Difference (Exper/Fit):")

        self.graphicsView_ReflectivityProfile.getPlotItem().clear()

        for i in range(0, len(self.Data_DataFiles)):
            data_angle, data_I, data_dI = self.Data_DataFiles[i]

            # change color from black when 2 or 4 polarisations
            if self.BoToFit_mode in ["m_2", "t_2", "m_2_m", "m_2_f"] and i == 1: color = [255, 0, 0]
            elif self.BoToFit_mode in ["m_4", "t_4", "m_4_m", "m_4_f"]: color = [255, 0, 0] if i == 1 else ([0, 255, 0] if i == 2 else ([0, 0, 255] if i == 3 else [0, 0, 0]))

            # pyqtgraph can not rescale data in log scale, so we do it manually if needed
            plot_I, plot_angle, plot_dI_errBottom, plot_dI_errTop = [], [], [], []

            for j in range(0, len(data_angle)):
                if float(data_I[j]) > 0:
                    plot_angle.append(float(data_angle[j]))
                    if self.comboBox_ReflectivityProfile_Scale.currentText() == "log":
                        plot_I.append(math.log10(float(data_I[j])))
                        plot_dI_errTop.append(abs(math.log10(float(data_I[j]) + float(data_dI[j])) - math.log10(float(data_I[j]))))

                        if float(data_I[j]) > float(data_dI[j]): plot_dI_errBottom.append(math.log10(float(data_I[j])) - math.log10(float(data_I[j]) - float(data_dI[j])))
                        else: plot_dI_errBottom.append(0)
                    else:
                        plot_I.append(float(data_I[j]))
                        plot_dI_errTop.append(float(data_dI[j]))
                        plot_dI_errBottom.append(float(data_dI[j]))

            s1 = pg.ErrorBarItem(x=np.array(plot_angle[int(self.lineEdit_ScanParameters_PointsToExclude_first.text()): -int(self.lineEdit_ScanParameters_PointsToExclude_last.text()) - 1]), y=np.array(plot_I[int(self.lineEdit_ScanParameters_PointsToExclude_first.text()): -int(self.lineEdit_ScanParameters_PointsToExclude_last.text()) - 1]), top=np.array(plot_dI_errTop[int(self.lineEdit_ScanParameters_PointsToExclude_first.text()): -int(self.lineEdit_ScanParameters_PointsToExclude_last.text()) - 1]), bottom=np.array(plot_dI_errBottom[int(self.lineEdit_ScanParameters_PointsToExclude_first.text()): -int(self.lineEdit_ScanParameters_PointsToExclude_last.text()) - 1]), pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
            self.graphicsView_ReflectivityProfile.addItem(s1)

            s2 = pg.ScatterPlotItem(x=plot_angle[int(self.lineEdit_ScanParameters_PointsToExclude_first.text()): -int(self.lineEdit_ScanParameters_PointsToExclude_last.text()) - 1], y=plot_I[int(self.lineEdit_ScanParameters_PointsToExclude_first.text()): -int(self.lineEdit_ScanParameters_PointsToExclude_last.text()) - 1], symbol="o", size=2, pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
            self.graphicsView_ReflectivityProfile.addItem(s2)

    def f_reformFitFunct_drawAndExport(self):
        ''' draw BoToFit final fit function on top of the graph with experimental points '''

        if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]: files_fitFunc = [["FitFunct.dat", [0, 0, 0]], []]
        elif self.BoToFit_mode in ["m_2", "t_2", "m_2_m", "m_2_f"]: files_fitFunc = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]]]
        elif self.BoToFit_mode in ["m_4", "t_4", "m_4_m", "m_4_f"]: files_fitFunc = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]], ["Fit2DFunctUD.dat", [0, 255, 0]], ["Fit2DFunctDU.dat", [0, 0, 255]]]

        for file in files_fitFunc:
            plot_I, plot_angle = [], []

            # check if we have file to work with
            try:
                if files_fitFunc[0][0] not in os.listdir(self.FOLDER_DATA) or file == []: return
            except FileNotFoundError: return

            with open(self.FOLDER_DATA + file[0], 'r') as file_fitFunct:
                for line in file_fitFunct.readlines():
                    try:
                        if str(line.split()[1]) == "-Infinity": continue

                        if self.comboBox_ReflectivityProfile_Scale.currentText() == "log": plot_I.append(math.log10(float(line.split()[1])))
                        else: plot_I.append(float(line.split()[1]))

                        if self.BoToFit_mode in ["t_0", "t_2", "t_4", "t_0_sl"]: plot_angle.append(float(line.split()[0]))
                        else: plot_angle.append(self.f_angleConvert("rad", "Qz", float(line.split()[0])) if "ang(Qz)" in self.inputStructure else float(line.split()[0]))
                    except: True

                s3 = pg.PlotDataItem(plot_angle, plot_I, pen = pg.mkPen(color=(file[1][0], file[1][1], file[1][2]), width=2))
                self.graphicsView_ReflectivityProfile.addItem(s3)

    def f_sld_draw(self):
        ''' draw SLD profiles, calculated in multiGrPr.exe '''

        self.graphicsView_SldProfile.getPlotItem().clear()

        for index, SLD_profile in enumerate(['SLD_profile.dat', 'SLD_profile_F2.dat'] if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"] else ['SLD_profile.dat']):
            dist, sld_1, sld_2 = [], [], []
            points, cut_1_l, cut_2_l, cut_1_r, cut_2_r = -1, [-1, -1], [-1, -1], [-1, -1], [-1, -1]

            with open(self.FOLDER_DATA + SLD_profile, 'r') as sld_file:
                for line_number, line in enumerate(sld_file.readlines()):
                    try:
                        sld_1.append((float(line.split()[1].replace("D", "E"))))
                        sld_2.append((float(line.split()[2].replace("D", "E"))))
                        dist.append(float(line.split()[0].replace("D", "E")))
                    except: True
                    points = len(dist)

                # find parts of SLD profile to trim
                # -- left
                try:
                    for i in range(0, points):
                        cut_1_l[index] = i if not round(sld_1[i], 3) == round(sld_1[0], 3) else -1
                        if cut_1_l[index] > -1: break
                    for i in range(0, points):
                        cut_2_l[index] = i if not round(sld_2[i], 3) == round(sld_2[0], 3) else -1
                        if cut_2_l[index] > -1: break
                except: cut_1_l[index] = cut_2_l[index] = 0

                # -- right
                try:
                    for i in range(points-100, 0, -1):
                        cut_1_r[index] = i if not round(sld_1[i], 3) == round(sld_1[points - 100], 3) else -1
                        if cut_1_r[index] > -1: break
                    for i in range(points-100, 0, -1):
                        cut_2_r[index] = i if not round(sld_2[i], 3) == round(sld_2[points - 100], 3) else -1
                        if cut_2_r[index] > -1: break
                except: cut_1_r[index] = cut_2_r[index] = points

                # -- limits
                if index == 0: left_lim, right_lim = min(cut_1_l[0], cut_2_l[0]), max(cut_1_r[0], cut_2_r[0]) + 50
                elif index == 1: left_lim, right_lim = min(cut_1_l[1], cut_2_l[1], left_lim), max(cut_1_r[1] + 50, cut_2_r[1] + 50, right_lim)

                s4 = pg.PlotDataItem(dist[left_lim:right_lim], sld_1[left_lim:right_lim], pen=pg.mkPen(color=(255,0,0), width=2, style=(QtCore.Qt.SolidLine if SLD_profile == 'SLD_profile.dat' else QtCore.Qt.DashLine)))
                self.graphicsView_SldProfile.addItem(s4)

                s5 = pg.PlotDataItem(dist[left_lim:right_lim], sld_2[left_lim:right_lim], pen=pg.mkPen(color=(0,0,0), width=2, style=(QtCore.Qt.SolidLine if SLD_profile == 'SLD_profile.dat' else QtCore.Qt.DashLine)))
                self.graphicsView_SldProfile.addItem(s5)

    def f_diff_draw(self):
        '''
        Here I compare experimental points with fitting curves
        polarisation order in self.Data_DataFiles = [UU, (DD), (UD), DU]
        '''

        self.graphicsView_Diff.getPlotItem().clear()

        if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]: files_fitFunc = [["FitFunct.dat", [0, 0, 0]], []]
        elif self.BoToFit_mode in ["m_2", "t_2", "m_2_m", "m_2_f"]: files_fitFunc = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]]]
        elif self.BoToFit_mode in ["m_4", "t_4", "m_4_m", "m_4_f"]: files_fitFunc = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]], ["Fit2DFunctUD.dat", [0, 255, 0]], ["Fit2DFunctDU.dat", [0, 0, 255]]]

        for i, file in enumerate(files_fitFunc):
            fitFunct_I, fitFunct_angle, diff_I, scale_angle, zero_I = [], [], [], [], []

            if file == []: return

            with open(self.FOLDER_DATA + file[0], 'r') as file_fitFunct:
                for line in file_fitFunct.readlines():
                    if line.split()[1] == "-Infinity": continue

                    try:
                        if self.BoToFit_mode in ["t_0", "t_2", "t_4", "t_0_sl"]: fitFunct_angle.append((float(line.split()[0])))
                        else:
                            if "ang(rad)" in self.inputStructure:
                                fitFunct_angle.append((float(line.split()[0])))
                            else: fitFunct_angle.append((4 * math.pi / float(self.lineEdit_ScanParameters_Wavelength.text())) * math.sin(float(line.split()[0])))
                        fitFunct_I.append(float(line.split()[1]))
                    except: True

                s = InterpolatedUnivariateSpline(np.array(fitFunct_angle), np.array(fitFunct_I), k=1)

            scale_angle = self.Data_DataFiles[i][0][int(self.lineEdit_ScanParameters_PointsToExclude_first.text()) : -int(self.lineEdit_ScanParameters_PointsToExclude_last.text())-1]
            data_I = self.Data_DataFiles[i][1][int(self.lineEdit_ScanParameters_PointsToExclude_first.text()) : -int(self.lineEdit_ScanParameters_PointsToExclude_last.text())-1]

            for i in range(0, len(scale_angle)):
                if data_I[i] != 0: diff_I.append(data_I[i] / s(scale_angle[i]))
                else: zero_I.append(i)

            s6 = pg.PlotDataItem(np.delete(scale_angle, zero_I), diff_I, pen = pg.mkPen(color=(file[1][0], file[1][1], file[1][2]), width=2))
            self.graphicsView_Diff.addItem(s6)

    def f_resolutionFunction_draw(self):
        if self.sender().text() == "Show resolution function view":
            self.graphicsView_ResolutionFunction.setGeometry(QtCore.QRect(300, -10, 380, 150))
            self.pushButton_ResolutionFunction_Show.setText("Hide resolution function view")
        elif self.sender().text() == "Hide resolution function view":
            self.graphicsView_ResolutionFunction.setGeometry(QtCore.QRect(0, 0, 0, 0))
            self.pushButton_ResolutionFunction_Show.setText("Show resolution function view")

        scaler, collX, collY = 0, [], []
        self.graphicsView_ResolutionFunction.getPlotItem().clear()

        # Credits for resolution function calculation: Anton Devishvili
        for i in range(0, int(self.lineEdit_ScanParameters_NumberOfPtsForResolutionFunction.text()) + 2):
            x = float(self.lineEdit_ScanParameters_StepForResolutionFunction.text()) * (i - (float(self.lineEdit_ScanParameters_NumberOfPtsForResolutionFunction.text()) + 1) / 2)
            y = np.exp(-((x / float(self.lineEdit_ScanParameters_Sigma.text()))**2) / 2)
            if i in [0, int(self.lineEdit_ScanParameters_NumberOfPtsForResolutionFunction.text()) + 1]: y = 0
            scaler += y

            collX.append(x)
            collY.append(y)

        collY = collY / scaler

        srf = pg.PlotDataItem(collX, collY, pen=pg.mkPen(color=(255, 0, 0), width=2))
        self.graphicsView_ResolutionFunction.addItem(srf)
    ##<--

    ##--> extra functions to shorten the code
    def f_clearStuff(self, graphs=True, fitRes=True, chi_prev=True):
        if graphs:
            for item in (self.graphicsView_ReflectivityProfile.getPlotItem(), self.graphicsView_SldProfile.getPlotItem(), self.graphicsView_Diff.getPlotItem()): item.clear()

        if fitRes:
            for item in (self.lineEdit_FitResults_NumberOfIterations, self.lineEdit_FitResults_ChiSquare_Actual): item.clear()
            for i in range(0, self.tableWidget_FitResults.rowCount()): self.tableWidget_FitResults.removeRow(0)

        if chi_prev: self.lineEdit_FitResults_ChiSquare_Previous.clear()

    def f_angleConvert(self, input_unit, output_unit, input_value):
        if output_unit == "Qz": output_value = float(input_value) if input_unit == "Qz" else (4 * math.pi / float(self.lineEdit_ScanParameters_Wavelength.text())) * math.sin(float(input_value))
        elif output_unit == "rad": output_value = float(input_value) if input_unit == "rad" else math.asin(float(input_value) * float(self.lineEdit_ScanParameters_Wavelength.text()) / (4 * math.pi))

        return output_value

    def f_fitResults_selectAll(self):
        for i in range(0, self.tableWidget_FitResults.rowCount()):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Checked if self.checkBox_FitResults_SelectAll.isChecked() else QtCore.Qt.Unchecked)
            self.tableWidget_FitResults.setItem(i, 0, item)

    def f_BoToFit_run(self, data_folder, thread, module, entry, data, ptsToSkip_left, ptsToSkip_right):
        if thread == 0:
            '''
            define that BoToFit is done by checking the folder for "self.MODE_SPECS[self.BoToFit_mode][1]"
            '''

            # check every second if BoToFit is done
            while self.MODE_SPECS[self.BoToFit_mode][1] not in os.listdir(data_folder):
                QtTest.QTest.qWait(1000)

                # check if BoToFit crashed
                list_proc = []
                for proc in psutil.process_iter(): list_proc.append(proc.name())
                if self.MODE_SPECS[self.BoToFit_mode][0] not in list_proc: return

            # wait 5 sec more to make sure that FitFunct file is ready
            QtTest.QTest.qWait(5000)

            # when its done, kill BoToFit process
            for proc in psutil.process_iter():
                if proc.name() == self.MODE_SPECS[self.BoToFit_mode][0]:
                    proc.kill()
        else:
            communicate_string = str(entry) + '\r\n' + str(data) + '\r\n' + str(ptsToSkip_left) + '\r\n' + str(ptsToSkip_right) + '\r\n'
            file = subprocess.Popen(str(module), stdin=subprocess.PIPE, cwd=data_folder)
            file.communicate(input=bytes(communicate_string, 'utf-8'))

    def f_multyGrPr_run(self):
        # run multiGrPr.exe (twice for FRAC modules)
        # multiGrPr.exe can process only the 'multiGrPr.ent' file. So when we have 2 FRACtions, we do some renaiming
        for index in range(2 if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"] else 1):
            if index == 1:
                for i, f in zip(['SLD_profile.dat', 'multiGrPr.ent', 'multiGrPr_2.ent'], ['SLD_profile_F1.dat', 'multiGrPr_F1.ent', 'multiGrPr.ent']):
                    try:
                        os.rename(self.FOLDER_DATA + i, self.FOLDER_DATA + f)
                    except: True

            subprocess.Popen(str(self.dir_current + '/BoToFit_Modules/multiGrPr.exe'), cwd=str(self.FOLDER_DATA))

            # run multiGrPr and wait until it finished to work
            while "SLD_profile.dat" not in os.listdir(self.FOLDER_DATA): QtTest.QTest.qWait(1000)
            while os.path.getsize(self.FOLDER_DATA + 'SLD_profile.dat') < 1: QtTest.QTest.qWait(1000)

            # SLD needs correction for Solid-Liquid mode
            if self.BoToFit_mode in ["m_0_sl", "t_0_sl"]:
                with open(self.FOLDER_DATA + "SLD_profile.dat", "r") as SLD_file_original: SLD = SLD_file_original.readlines()
                with open(self.FOLDER_DATA + "SLD_profile.dat", "w") as SLD_file_new:
                    for i in SLD:
                        dist, sld1, sld2 = i.replace("-", "D-").replace("D", "E").replace("EE", "E").replace(" E", " ").split()
                        SLD_file_new.write(dist + " " + str(float(sld1) + float(self.tableWidget_FilmDescription.item(0, 3).text())) + " " + str(float(sld2) + float(self.tableWidget_FilmDescription.item(0, 3).text())) + "\n")

            if index == 1:
                for i, f in zip(['SLD_profile.dat', 'multiGrPr.ent', 'SLD_profile_F1.dat', 'multiGrPr_F1.ent'],
                                ['SLD_profile_F2.dat', 'multiGrPr_F2.ent', 'SLD_profile.dat', 'multiGrPr.ent']):
                    try:
                        os.rename(self.FOLDER_DATA + i, self.FOLDER_DATA + f)
                    except: True

                for SLD_MultiGrPr_file in ['SLD_profile_F1.dat', 'SLD_profile_F1.dat', 'multiGrPr_2.ent', 'multiGrPr_F1.ent']:
                    try:
                        os.remove(self.FOLDER_DATA + SLD_MultiGrPr_file)
                    except: True
    
    def f_slLayer_add(self):
        if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] and not self.tableWidget_FilmDescription.item(0, 0).text() == "Substrate (Solid)":
            self.f_buttons_addRemoveLayer()

            columnNames = ["Substrate (Solid)", "inf", "", "0", "", "-", "", "", "", "", "", "-", ""]
            for i in range(0, 13):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                if not i == 3: item.setFlags(QtCore.Qt.NoItemFlags)
                self.tableWidget_FilmDescription.setItem(0, i, item)
                self.tableWidget_FilmDescription.item(0, i).setText(columnNames[i])

            self.tableWidget_FilmDescription.item(self.tableWidget_FilmDescription.rowCount() - 1, 0).setText("Liquid")

        elif self.BoToFit_mode not in ["m_0_sl", "t_0_sl"] and self.tableWidget_FilmDescription.item(self.tableWidget_FilmDescription.rowCount() - 1, 0).text() == "Liquid":
            self.tableWidget_FilmDescription.item(self.tableWidget_FilmDescription.rowCount() - 1, 0).setText("Substrate")
            if self.tableWidget_FilmDescription.item(0, 0).text() == "Substrate (Solid)" and self.tableWidget_FilmDescription.item(0, 1).text() == "inf":
                self.tableWidget_FilmDescription.removeRow(0)

    def f_fracThickness_synchronize(self):
        # this function is used only for FRAC
        if self.BoToFit_mode not in ["m_0_f", "m_2_f", "m_4_f"] or self.importing: return

        try:
            for index in range(self.tableWidget_FilmDescription.rowCount()):
                self.tableWidget_FilmDescription_2.item(index, 1).setText(self.tableWidget_FilmDescription.item(index, 1).text())
                self.tableWidget_FilmDescription_2.item(index, 2).setCheckState(0 if self.tableWidget_FilmDescription.item(index, 2).checkState() == 0 else 2)
        except: True

    def f_setChecked(self, parameter, checked):
        parameter.setCheckState(0 if checked == "n" else 2)

    def f_checkChecked(self, parameter):
        checked = "n" if parameter.checkState() == 0 else "f"
        return checked

if __name__ == "__main__":
    import sys
    QtWidgets.QApplication.setStyle("Fusion")
    app = QtWidgets.QApplication(sys.argv)
    prog = GUI()
    prog.show()
    sys.exit(app.exec_())

