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

    def __create_element(self, object, geometry, object_name, text=None, font=None, placeholder=None, visible=None, stylesheet=None, checked=None, checkable=None, title=None, combo=None, enabled=None):

        object.setObjectName(object_name)

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
        self.label_Data_file = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Data_file, [20, 0, 191, 16], "label_Data_file", text="Data file(s) and structure:", font=font_headline, stylesheet="QLabel { color : blue; }")

        self.groupBox_Data_file = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_Data_file, [10, 1, 661, 49], "groupBox_Data_file", font=font_ee)
        self.lineEdit_Data_file = QtWidgets.QLineEdit(self.groupBox_Data_file)
        self.__create_element(self.lineEdit_Data_file, [5, 23, 370, 21], "lineEdit_Data_file", font=font_ee)
        self.toolButton_Data_file = QtWidgets.QToolButton(self.groupBox_Data_file)
        self.__create_element(self.toolButton_Data_file, [378, 23, 26, 21], "toolButton_Data_file", text="...", font=font_ee)
        self.comboBox_Data_file_Column_1 = QtWidgets.QComboBox(self.groupBox_Data_file)
        self.__create_element(self.comboBox_Data_file_Column_1, [435, 23, 71, 21], "comboBox_Data_file_Column_1", font=font_ee)
        self.comboBox_Data_file_Column_2 = QtWidgets.QComboBox(self.groupBox_Data_file)
        self.__create_element(self.comboBox_Data_file_Column_2, [510, 23, 71, 21], "comboBox_Data_file_Column_2", font=font_ee)
        self.comboBox_Data_file_Column_3 = QtWidgets.QComboBox(self.groupBox_Data_file)
        self.__create_element(self.comboBox_Data_file_Column_3, [585, 23, 71, 21], "comboBox_Data_file_Column_3", font=font_ee)
        values = ["ang(Qz)", "I", "dI", "ang(rad)"]
        for comboBox in [self.comboBox_Data_file_Column_1, self.comboBox_Data_file_Column_2, self.comboBox_Data_file_Column_3]:
            for i in range(0, 4):
                comboBox.addItem("")
                comboBox.setItemText(i, values[i])
        self.comboBox_Data_file_Column_1.setCurrentIndex(0)
        self.comboBox_Data_file_Column_2.setCurrentIndex(1)
        self.comboBox_Data_file_Column_3.setCurrentIndex(2)

        self.checkBox_Data_file_preformatted = QtWidgets.QCheckBox(self.centralwidget)
        self.__create_element(self.checkBox_Data_file_preformatted, [480, 0, 192, 18], "checkBox_Data_file_preformatted", text="Data files are already preformatted", font=font_ee)

        # Block: Start fit with
        self.label_Start_fit_with = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Start_fit_with, [20, 50, 141, 16], "label_Start_fit_with", text="Start fit with:", font=font_headline, stylesheet="QLabel { color : blue; }")
        self.tabWidget_Start_fit_with = QtWidgets.QTabWidget(self.centralwidget)
        self.__create_element(self.tabWidget_Start_fit_with, [10, 68, 661, 271], "tabWidget_Start_fit_with", font=font_ee)

        # - tab "Film description" / "Fraction 1
        self.tab_Film_description = QtWidgets.QWidget()
        self.tab_Film_description.setObjectName("tab_Film_description")
        self.tabWidget_Start_fit_with.addTab(self.tab_Film_description, "")
        self.tabWidget_Start_fit_with.setTabText(self.tabWidget_Start_fit_with.indexOf(self.tab_Film_description), "Film description")
        self.tableWidget_Film_description = QtWidgets.QTableWidget(self.tab_Film_description)
        self.__create_element(self.tableWidget_Film_description, [-2, -1, 660, 222], "tableWidget_Film_description", font=font_ee)
        self.tableWidget_Film_description.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableWidget_Film_description.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_Film_description.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_Film_description.setColumnCount(13)
        self.tableWidget_Film_description.setRowCount(1)
        # reform the table if Pol/NoPol mode is chosen
        self.tableWidget_Film_description.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem())
        column_names = ["layer", "thickness", "", "SLD", "", "iSLD", "", "mSLD", "", "cos(d-gamma)", "", "roughness", ""]
        
        for i in range(0, 13):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget_Film_description.setHorizontalHeaderItem(i, item)
            self.tableWidget_Film_description.horizontalHeaderItem(i).setText(column_names[i])

        self.tableWidget_Film_description.verticalHeaderItem(0).setText("Back")
        self.tableWidget_Film_description.horizontalHeaderItem(4).setFont(font_headline)

        column_names = ["Substrate", "inf", "", "2.07", "", "0", "", "", "", "", "", "10", ""]
        for i in range(0, 13):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            if i in (0, 1, 2): item.setFlags(QtCore.Qt.NoItemFlags)
            elif i in (4, 6, 8, 10, 12):
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                if i == 8: item.setCheckState(QtCore.Qt.Unchecked)
                else: item.setCheckState(QtCore.Qt.Checked)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget_Film_description.setItem(0, i, item)
            self.tableWidget_Film_description.item(0, i).setText(column_names[i])

        self.tableWidget_Film_description.setRowHeight(0, 21)
        self.tableWidget_Film_description.horizontalHeader().setDefaultSectionSize(23)
        self.tableWidget_Film_description.verticalHeader().setVisible(False)

        self.pushButton_Film_description_Load_entry = QtWidgets.QPushButton(self.tab_Film_description)
        self.__create_element(self.pushButton_Film_description_Load_entry, [1, 223, 111, 19], "pushButton_Film_description_Load_entry", text="Load entry file", font=font_ee)
        self.pushButton_Film_description_Load_fitbag = QtWidgets.QPushButton(self.tab_Film_description)
        self.__create_element(self.pushButton_Film_description_Load_fitbag, [120, 223, 111, 19], "pushButton_Film_description_Load_fitbag", text="Load FitBag", font=font_ee)
        self.pushButton_Film_description_Add_layer = QtWidgets.QPushButton(self.tab_Film_description)
        self.__create_element(self.pushButton_Film_description_Add_layer, [491, 223, 80, 19], "pushButton_Film_description_Add_layer", text="Add layer", font=font_ee)
        self.pushButton_Film_description_Remove_layer = QtWidgets.QPushButton(self.tab_Film_description)
        self.__create_element(self.pushButton_Film_description_Remove_layer, [575, 223, 80, 19], "pushButton_Film_description_Remove_layer", text="Remove layer", font=font_ee)

        # - tab "Film description"(2) / "Fraction 2
        self.tab_Film_description_2 = QtWidgets.QWidget()
        self.tab_Film_description_2.setObjectName("tab_Film_description_2")
        self.tabWidget_Start_fit_with.addTab(self.tab_Film_description_2, "")
        self.tabWidget_Start_fit_with.setTabText(self.tabWidget_Start_fit_with.indexOf(self.tab_Film_description_2), "Fraction 2")
        self.tableWidget_Film_description_2 = QtWidgets.QTableWidget(self.tab_Film_description_2)
        self.__create_element(self.tableWidget_Film_description_2, [-2, -1, 660, 247], "tableWidget_Film_description_2", font=font_ee)
        self.tableWidget_Film_description_2.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableWidget_Film_description_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_Film_description_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_Film_description_2.setColumnCount(13)
        self.tableWidget_Film_description_2.setRowCount(1)
        # reform the table if Pol/NoPol mode is chosen
        self.tableWidget_Film_description_2.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem())
        column_names = ["layer", "thickness", "", "SLD", "", "iSLD", "", "mSLD", "", "cos(d-gamma)", "", "roughness", ""]

        for i in range(0, 13):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget_Film_description_2.setHorizontalHeaderItem(i, item)
            self.tableWidget_Film_description_2.horizontalHeaderItem(i).setText(column_names[i])

        self.tableWidget_Film_description_2.verticalHeaderItem(0).setText("Back")
        self.tableWidget_Film_description_2.horizontalHeaderItem(4).setFont(font_headline)

        column_names = ["Substrate", "inf", "", "2.07", "", "0", "", "", "", "", "", "10", ""]
        for i in range(0, 13):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            if i in (0, 1, 2): item.setFlags(QtCore.Qt.NoItemFlags)
            elif i in (4, 6, 8, 10, 12):
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                if i == 8: item.setCheckState(QtCore.Qt.Unchecked)
                else: item.setCheckState(QtCore.Qt.Checked)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget_Film_description_2.setItem(0, i, item)
            self.tableWidget_Film_description_2.item(0, i).setText(column_names[i])

        self.tableWidget_Film_description_2.setRowHeight(0, 21)
        self.tableWidget_Film_description_2.horizontalHeader().setDefaultSectionSize(23)
        self.tableWidget_Film_description_2.verticalHeader().setVisible(False)

        # - tab "Scan parameters"
        self.tab_Scan_parameters = QtWidgets.QWidget()
        self.tab_Scan_parameters.setObjectName("tab_Scan_parameters")
        self.tabWidget_Start_fit_with.addTab(self.tab_Scan_parameters, "")
        self.tabWidget_Start_fit_with.setTabText(self.tabWidget_Start_fit_with.indexOf(self.tab_Scan_parameters), "Scan parameters")
        self.label_Scan_parameters_Number_of_pts_for_resolution_function = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Number_of_pts_for_resolution_function, [8, 9, 311, 17], "label_Scan_parameters_Number_of_pts_for_resolution_function", text="Number of points for resolution function", font=font_ee)
        self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function, [223, 9, 60, 17], "lineEdit_Scan_parameters_Number_of_pts_for_resolution_function", font=font_ee)
        self.label_Scan_parameters_Step_for_resolution_function = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Step_for_resolution_function, [8, 27, 291, 17], "label_Scan_parameters_Step_for_resolution_function", text="Step for resolution function (mrad)", font=font_ee)
        self.lineEdit_Scan_parameters_Step_for_resolution_function = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Step_for_resolution_function, [223, 27, 60, 17], "lineEdit_Scan_parameters_Step_for_resolution_function", font=font_ee)
        self.label_Scan_parameters_Sigma = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Sigma, [8, 45, 291, 17], "label_Scan_parameters_Sigma", text="\"Sigma\" of resolution function (mrad)", font=font_ee)
        self.lineEdit_Scan_parameters_Sigma = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Sigma, [223, 45, 60, 17], "lineEdit_Scan_parameters_Sigma", font=font_ee)
        self.label_Scan_parameters_Zero_correction = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Zero_correction, [8, 63, 281, 17], "label_Scan_parameters_Zero_correction", text="Correction of the detector \"zero\"", font=font_ee)
        self.lineEdit_Scan_parameters_Zero_correction = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Zero_correction, [223, 63, 60, 17], "lineEdit_Scan_parameters_Zero_correction", font=font_ee)

        self.label_Scan_parameters_Wavelength = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Wavelength, [350, 9, 131, 17], "label_Scan_parameters_Wavelength", text="Wavelength (A)", font=font_ee)
        self.lineEdit_Scan_parameters_Wavelength = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Wavelength, [560, 9, 60, 17], "lineEdit_Scan_parameters_Wavelength", font=font_ee)
        self.label_Scan_parameters_Scaling_factor = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Scaling_factor, [350, 27, 101, 17], "label_Scan_parameters_Scaling_factor", text="Scaling factor", font=font_ee)
        self.lineEdit_Scan_parameters_Scaling_factor = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Scaling_factor, [560, 27, 60, 17], "lineEdit_Scan_parameters_Scaling_factor", placeholder="", font=font_ee)
        self.checkBox_Scan_parameters_Scaling_factor = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Scaling_factor, [623, 27, 20, 18], "checkBox_Scan_parameters_Scaling_factor")
        self.label_Scan_parameters_Background = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Background, [350, 45, 91, 17], "label_Scan_parameters_Background", text="Background", font=font_ee)
        self.lineEdit_Scan_parameters_Background = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Background, [560, 45, 60, 17], "lineEdit_Scan_parameters_Background", font=font_ee)
        self.checkBox_Scan_parameters_Background = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Background, [623, 45, 21, 18], "checkBox_Scan_parameters_Background")
        self.label_Scan_parameters_Crossover_overillumination = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Crossover_overillumination, [350, 63, 311, 17], "label_Scan_parameters_Crossover_overillumination", text="Crossover angle overillumination (mrad)", font=font_ee)
        self.lineEdit_Scan_parameters_Crossover_overillumination = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Crossover_overillumination, [560, 63, 60, 17], "lineEdit_Scan_parameters_Crossover_overillumination", font=font_ee)
        self.checkBox_Scan_parameters_Crossover_overillumination = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Crossover_overillumination, [623, 63, 21, 18], "checkBox_Scan_parameters_Crossover_overillumination")

        self.label_Scan_parameters_Points_to_exclude_First = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Points_to_exclude_First, [350, 93, 191, 16], "label_Scan_parameters_Points_to_exclude_First", text="Number of first points to exclude")
        self.lineEdit_Scan_parameters_Points_to_exclude_First = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Points_to_exclude_First, [560, 93, 60, 17], "lineEdit_Scan_parameters_Points_to_exclude_First", text="5")
        self.label_Scan_parameters_Points_to_exclude_Last = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Points_to_exclude_Last, [350, 111, 191, 17], "label_Scan_parameters_Points_to_exclude_Last", text="Number of last points to exclude")
        self.lineEdit_Scan_parameters_Points_to_exclude_Last = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Points_to_exclude_Last, [560, 111, 60, 17], "lineEdit_Scan_parameters_Points_to_exclude_Last", text="0")

        self.pushButton_Resolution_function_Show = QtWidgets.QPushButton(self.tab_Scan_parameters)
        self.__create_element(self.pushButton_Resolution_function_Show, [8, 93, 180, 32], "pushButton_Resolution_function_Show", text="Show resolution function view", font=font_headline)

        self.graphicsView_Resolution_function = pg.PlotWidget(self.tab_Scan_parameters, viewBox=pg.ViewBox())
        self.__create_element(self.graphicsView_Resolution_function, [0, 0, 0, 0], "graphicsView_Resolution_function")
        self.graphicsView_Resolution_function.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_Resolution_function.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_Resolution_function.getAxis("left").tickFont = font_graphs
        self.graphicsView_Resolution_function.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_Resolution_function.showAxis("top")
        self.graphicsView_Resolution_function.getAxis("top").setTicks([])
        self.graphicsView_Resolution_function.showAxis("right")
        self.graphicsView_Resolution_function.getAxis("right").setTicks([])

        self.label_Scan_parameters_Piy = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Piy, [8, 144, 291, 17], "label_Scan_parameters_Piy", text="Pi(y): incident polarization (polariser)", font=font_ee)
        self.lineEdit_Scan_parameters_Piy = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Piy, [269, 144, 60, 17], "lineEdit_Scan_parameters_Piy", font=font_ee)
        self.checkBox_Scan_parameters_Piy = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Piy, [332, 144, 21, 18], "checkBox_Scan_parameters_Piy")
        self.label_Scan_parameters_Pfy = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Pfy, [8, 162, 251, 17], "label_Scan_parameters_Pfy", text="Pf(y): outgoing polarization (analyser)", font=font_ee)
        self.lineEdit_Scan_parameters_Pfy = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Pfy, [269, 162, 60, 17], "lineEdit_Scan_parameters_Pfy", font=font_ee)
        self.checkBox_Scan_parameters_Pfy = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Pfy, [332, 162, 21, 18], "checkBox_Scan_parameters_Pfy")
        self.label_Scan_parameters_Cg = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Cg, [8, 180, 291, 17], "label_Scan_parameters_Cg", text="cg: mean value <cos(gamma)> of big domains", font=font_ee)
        self.lineEdit_Scan_parameters_Cg = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Cg, [269, 180, 60, 17], "lineEdit_Scan_parameters_Cg", font=font_ee)
        self.checkBox_Scan_parameters_Cg = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Cg, [332, 180, 21, 18], "checkBox_Scan_parameters_Cg")
        self.label_Scan_parameters_Cg_2 = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Cg_2, [362, 180, 291, 17], "label_Scan_parameters_Cg_2", text="cg (fraction 2)", font=font_ee)
        self.lineEdit_Scan_parameters_Cg_2 = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Cg_2, [450, 180, 60, 17], "lineEdit_Scan_parameters_Cg_2", font=font_ee)
        self.checkBox_Scan_parameters_Cg_2 = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Cg_2, [513, 180, 21, 18], "checkBox_Scan_parameters_Cg_2")
        self.label_Scan_parameters_Sg = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Sg, [8, 198, 291, 17], "label_Scan_parameters_Sg", text="sg: mean value <sin(gamma)> of big domains", font=font_ee)
        self.lineEdit_Scan_parameters_Sg = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Sg, [269, 198, 60, 17], "lineEdit_Scan_parameters_Sg", font=font_ee)
        self.checkBox_Scan_parameters_Sg = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Sg, [332, 198, 21, 18], "checkBox_Scan_parameters_Sg")
        self.label_Scan_parameters_Sg_2 = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Sg_2, [362, 198, 291, 17], "label_Scan_parameters_Sg_2", text="sg (fraction 2)", font=font_ee)
        self.lineEdit_Scan_parameters_Sg_2 = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Sg_2, [450, 198, 60, 17], "lineEdit_Scan_parameters_Sg_2", font=font_ee)
        self.checkBox_Scan_parameters_Sg_2 = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Sg_2, [513, 198, 21, 18], "checkBox_Scan_parameters_Sg_2")
        self.label_Scan_parameters_Sg2 = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Sg2, [8, 216, 291, 17], "label_Scan_parameters_Sg2", text="sg2: mean value <sin^2(gamma)> of big domains", font=font_ee)
        self.lineEdit_Scan_parameters_Sg2 = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Sg2, [269, 216, 60, 17], "lineEdit_Scan_parameters_Sg2", font=font_ee)
        self.checkBox_Scan_parameters_Sg2 = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Sg2, [332, 216, 21, 18], "checkBox_Scan_parameters_Sg2")
        self.label_Scan_parameters_Sg2_2 = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Sg2_2, [362, 216, 291, 17], "label_Scan_parameters_Sg2_2", text="sg2 (fraction 2)", font=font_ee)
        self.lineEdit_Scan_parameters_Sg2_2 = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Sg2_2, [450, 216, 60, 17], "lineEdit_Scan_parameters_Sg2_2", font=font_ee)
        self.checkBox_Scan_parameters_Sg2_2 = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Sg2_2, [513, 216, 21, 18], "checkBox_Scan_parameters_Sg2_2")

        self.label_Scan_parameters_Fraction_amount = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Fraction_amount, [362, 144, 291, 17], "label_Scan_parameters_Fraction_amount",
                              text="Fraction amount (0 < \"fraction 1\" < 1)", font=font_ee)
        self.lineEdit_Scan_parameters_Fraction_amount = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Fraction_amount, [560, 144, 60, 17], "lineEdit_Scan_parameters_Fraction_amount", font=font_ee)
        self.checkBox_Scan_parameters_Fraction_amount = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Fraction_amount, [623, 144, 21, 18], "checkBox_Scan_parameters_Fraction_amount")

        self.label_Scan_parameters_Gradient_period = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Gradient_period, [362, 144, 291, 17], "label_Scan_parameters_Gradient_period", text="Gradient (-1 < \"grad\"< 1):   Period", font=font_ee)
        self.lineEdit_Scan_parameters_Gradient_period = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Gradient_period, [560, 144, 60, 17], "lineEdit_Scan_parameters_Gradient_period", font=font_ee)
        self.checkBox_Scan_parameters_Gradient_period = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Gradient_period, [623, 144, 21, 18], "checkBox_Scan_parameters_Gradient_period")
        self.label_Scan_parameters_Gradient_roughness = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Gradient_roughness, [498, 162, 251, 17], "label_Scan_parameters_Gradient_roughness", text="Roughness", font=font_ee)
        self.lineEdit_Scan_parameters_Gradient_roughness = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Gradient_roughness, [560, 162, 60, 17], "lineEdit_Scan_parameters_Gradient_roughness", font=font_ee)
        self.checkBox_Scan_parameters_Gradient_roughness = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Gradient_roughness, [623, 162, 21, 18], "checkBox_Scan_parameters_Gradient_roughness")
        self.label_Scan_parameters_Gradient_sld = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Gradient_sld, [498, 180, 291, 17], "label_Scan_parameters_Gradient_sld", text="SLD", font=font_ee)
        self.lineEdit_Scan_parameters_Gradient_sld = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Gradient_sld, [560, 180, 60, 17], "lineEdit_Scan_parameters_Gradient_sld", font=font_ee)
        self.checkBox_Scan_parameters_Gradient_sld = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Gradient_sld, [623, 180, 21, 18], "checkBox_Scan_parameters_Gradient_sld")
        self.label_Scan_parameters_Gradient_msld = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Gradient_msld, [498, 198, 291, 17], "label_Scan_parameters_Gradient_msld", text="mSLD", font=font_ee)
        self.lineEdit_Scan_parameters_Gradient_msld = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Gradient_msld, [560, 198, 60, 17], "lineEdit_Scan_parameters_Gradient_msld", font=font_ee)
        self.checkBox_Scan_parameters_Gradient_msld = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Gradient_msld, [623, 198, 21, 18], "checkBox_Scan_parameters_Gradient_msld")

        self.tabWidget_Start_fit_with.setCurrentIndex(0)

        # Block: Save results at
        self.label_Save_at = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Save_at, [20, 340, 151, 16], "label_Save_at", text="Save fit results at:", font=font_headline, stylesheet="QLabel { color : blue; }")
        self.groupBox_Save_at = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_Save_at, [10, 341, 531, 49], "groupBox_Save_at", font=font_ee)
        self.lineEdit_Save_at_Dir_1 = QtWidgets.QLineEdit(self.groupBox_Save_at)
        self.__create_element(self.lineEdit_Save_at_Dir_1, [5, 23, 281, 21], "lineEdit_Save_at_Dir_1", font=font_ee)
        self.toolButton_Save_at_Dir_1 = QtWidgets.QToolButton(self.groupBox_Save_at)
        self.__create_element(self.toolButton_Save_at_Dir_1, [290, 23, 26, 21], "toolButton_Save_at_Dir_1", text="...", font=font_ee)
        self.lineEdit_Save_at_Dir_2 = QtWidgets.QLineEdit(self.groupBox_Save_at)
        self.__create_element(self.lineEdit_Save_at_Dir_2, [325, 23, 200, 21], "lineEdit_Save_at_Dir_2", font=font_ee, placeholder="Sub directory [first data file name]")

        # Button: Start fitting
        self.pushButton_Start_fitting = QtWidgets.QPushButton(self.centralwidget)
        self.__create_element(self.pushButton_Start_fitting, [550, 358, 121, 32], "pushButton_Start_fitting", text="Start Fitting", font=font_headline)

        # Block: Fit results
        self.label_Fit_results = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Fit_results, [690, 0, 101, 16], "label_Fit_results", text="Fit results:", font=font_headline, stylesheet="QLabel { color : blue; }")
        self.label_Fit_results.setFont(font_headline)
        self.label_Fit_results.setGeometry(QtCore.QRect(690, 0, 101, 16))
        self.label_Fit_results.setObjectName("label_Fit_results")
        self.label_Fit_results.setText("Fit results:")
        self.groupBox_Fit_results = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_Fit_results, [680, 1, 401, 389], "groupBox_Fit_results", font=font_headline)
        self.tableWidget_Fit_results = QtWidgets.QTableWidget(self.groupBox_Fit_results)
        self.__create_element(self.tableWidget_Fit_results, [1, 48, 400, 317], "tableWidget_Fit_results", font=font_ee)
        self.tableWidget_Fit_results.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_Fit_results.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.tableWidget_Fit_results.setPalette(palette)
        self.tableWidget_Fit_results.setColumnCount(6)
        self.tableWidget_Fit_results.setRowCount(0)

        column_names = ["No", "Parameter", "Value", "Error", "Factor"]
        column_widths = [33, 38, 116, 70, 70, 70]
        for i in range(0, 6):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_Fit_results.setHorizontalHeaderItem(i, item)
            self.tableWidget_Fit_results.setColumnWidth(i, column_widths[i])
            if i == 0: continue
            self.tableWidget_Fit_results.horizontalHeaderItem(i).setText(column_names[i-1])

        self.tableWidget_Fit_results.horizontalHeaderItem(0).setFont(font_headline)
        self.tableWidget_Fit_results.verticalHeader().setVisible(False)
        self.checkBox_Fit_results_Select_all = QtWidgets.QCheckBox(self.tableWidget_Fit_results.horizontalHeader())
        self.__create_element(self.checkBox_Fit_results_Select_all, [self.tableWidget_Fit_results.columnWidth(0) / 9, 1, 14, 14], "checkBox_Fit_results_Select_all")
        self.label_Fit_results_Number_of_iterations = QtWidgets.QLabel(self.groupBox_Fit_results)
        self.__create_element(self.label_Fit_results_Number_of_iterations, [10, 18, 161, 31], "label_Fit_results_Number_of_iterations", text="No. iterations:", font=font_ee)
        self.lineEdit_Fit_results_Number_of_iterations = QtWidgets.QLineEdit(self.groupBox_Fit_results)
        self.__create_element(self.lineEdit_Fit_results_Number_of_iterations, [82, 23, 40, 21], "lineEdit_Fit_results_Number_of_iterations", font=font_ee)
        self.lineEdit_Fit_results_Number_of_iterations.setReadOnly(True)
        self.label_Fit_results_Chi_square_Previous = QtWidgets.QLabel(self.groupBox_Fit_results)
        self.__create_element(self.label_Fit_results_Chi_square_Previous, [135, 18, 151, 31], "label_Fit_results_Chi_square_Previous", text="Chi_sq.norm: previous", font=font_ee)
        self.lineEdit_Fit_results_Chi_square_Previous = QtWidgets.QLineEdit(self.groupBox_Fit_results)
        self.__create_element(self.lineEdit_Fit_results_Chi_square_Previous, [250, 23, 50, 21], "lineEdit_Fit_results_Chi_square_Previous", font=font_ee)
        self.lineEdit_Fit_results_Chi_square_Previous.setReadOnly(True)
        self.label_Fit_results_Chi_square_Actual = QtWidgets.QLabel(self.groupBox_Fit_results)
        self.__create_element(self.label_Fit_results_Chi_square_Actual, [312, 18, 151, 31], "label_Fit_results_Chi_square_Actual", text="actual", font=font_ee)
        self.lineEdit_Fit_results_Chi_square_Actual = QtWidgets.QLineEdit(self.groupBox_Fit_results)
        self.__create_element(self.lineEdit_Fit_results_Chi_square_Actual, [346, 23, 50, 21], "lineEdit_Fit_results_Chi_square_Actual", font=font_ee)
        self.lineEdit_Fit_results_Chi_square_Actual.setReadOnly(True)

        self.pushButton_Fit_results_Copy_to_Start_fit_with = QtWidgets.QPushButton(self.groupBox_Fit_results)
        self.__create_element(self.pushButton_Fit_results_Copy_to_Start_fit_with, [5, 367, 392, 19], "pushButton_Fit_results_Copy_to_Start_fit_with", text="Use selected (#) values as 'Start fit with' parameters", font=font_ee)

        self.checkBox_Show_fixed = QtWidgets.QCheckBox(self.centralwidget)
        self.__create_element(self.checkBox_Show_fixed, [945, 0, 192, 18], "checkBox_Show_fixed", text="Show fixed parameters", font=font_ee)

        # Block: Reflectivity profile and Difference
        self.label_Reflectivity_profile_and_Diff = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Reflectivity_profile_and_Diff, [20, 393, 541, 16], "label_Reflectivity_profile_and_Diff", text="Reflectivity profile (I[               ] vs. Qz[Å**-1]) and Difference (Exper/Fit):", font=font_headline, stylesheet="QLabel { color : blue; }")
        self.groupBox_Reflectivity_profile = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_Reflectivity_profile, [10, 394, 660, 315], "groupBox_Reflectivity_profile")
        self.graphicsView_Diff = pg.PlotWidget(self.groupBox_Reflectivity_profile, viewBox=pg.ViewBox())
        self.__create_element(self.graphicsView_Diff, [2, 223, 657, 91], "graphicsView_Diff")
        self.graphicsView_Diff.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_Diff.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_Diff.getAxis("left").tickFont = font_graphs
        self.graphicsView_Diff.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_Diff.showAxis("top")
        self.graphicsView_Diff.getAxis("top").setTicks([])
        self.graphicsView_Diff.showAxis("right")
        self.graphicsView_Diff.getAxis("right").setTicks([])
        self.graphicsView_Reflectivity_profile = pg.PlotWidget(self.groupBox_Reflectivity_profile, viewBox=pg.ViewBox())
        self.__create_element(self.graphicsView_Reflectivity_profile, [2, 19, 657, 205], "graphicsView_Reflectivity_profile")
        self.graphicsView_Reflectivity_profile.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_Reflectivity_profile.getAxis("bottom").setStyle(showValues=False)
        self.graphicsView_Reflectivity_profile.getAxis("left").tickFont = font_graphs
        self.graphicsView_Reflectivity_profile.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_Reflectivity_profile.showAxis("top")
        self.graphicsView_Reflectivity_profile.getAxis("top").setTicks([])
        self.graphicsView_Reflectivity_profile.showAxis("right")
        self.graphicsView_Reflectivity_profile.getAxis("right").setTicks([])
        self.graphicsView_Diff.getViewBox().setXLink(self.graphicsView_Reflectivity_profile)
        self.comboBox_Reflectivity_profile_Scale = QtWidgets.QComboBox(self.centralwidget)
        self.__create_element(self.comboBox_Reflectivity_profile_Scale, [143, 392, 41, 18], "comboBox_Reflectivity_profile_Scale", font=font_ee)
        for i, value in enumerate(["log", "lin"]):
            self.comboBox_Reflectivity_profile_Scale.addItem("")
            self.comboBox_Reflectivity_profile_Scale.setItemText(i, value)

        # Block: SLD profile
        self.label_Sld_profile = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Sld_profile, [690, 393, 481, 16], "label_Sld_profile", text="SLD profile (SLD [in Å**-2, *10e6] vs. Distance from interface [Å]:", font=font_headline, stylesheet="QLabel { color : blue; }")
        self.groupBox_Sld_profile = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_Sld_profile, [680, 394, 401, 315], "groupBox_Sld_profile")
        MainWindow.setCentralWidget(self.centralwidget)
        self.graphicsView_Sld_profile = pg.PlotWidget(self.groupBox_Sld_profile)
        self.__create_element(self.graphicsView_Sld_profile, [2, 19, 398, 295], "graphicsView_Sld_profile")
        self.graphicsView_Sld_profile.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_Sld_profile.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_Sld_profile.getAxis("left").tickFont = font_graphs
        self.graphicsView_Sld_profile.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_Sld_profile.showAxis("top")
        self.graphicsView_Sld_profile.getAxis("top").setTicks([])
        self.graphicsView_Sld_profile.showAxis("right")
        self.graphicsView_Sld_profile.getAxis("right").setTicks([])

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

        self.menu_Mono_No_polarisation = QtWidgets.QMenu(self.menu_Mono)
        self.__create_element(self.menu_Mono_No_polarisation, [999, 999, 999, 999], "menu_Mono_No_polarisation", title="No polarisation")
        self.menu_Mono.addAction(self.menu_Mono_No_polarisation.menuAction())
        self.action_Mono_No_polarisation = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_No_polarisation, [999, 999, 999, 999], "action_Mono_No_polarisation", checked=True, checkable=True, text="Default")  # m_0
        self.menu_Mono_No_polarisation.addAction(self.action_Mono_No_polarisation)
        self.action_Mono_No_polarisation_multi = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_No_polarisation_multi, [999, 999, 999, 999], "action_Mono_No_polarisation_multi", checked=True, checkable=True, text="Periodical multilayers")  # m_0_m
        self.menu_Mono_No_polarisation.addAction(self.action_Mono_No_polarisation_multi)
        self.action_Mono_No_polarisation_SL = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_No_polarisation_SL, [999, 999, 999, 999], "action_Mono_No_polarisation_SL", checked=True, checkable=True, text="Solid-Liquid")  # m_0_sl
        self.menu_Mono_No_polarisation.addAction(self.action_Mono_No_polarisation_SL)
        self.action_Mono_No_polarisation_frac = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_No_polarisation_frac, [999, 999, 999, 999], "action_Mono_No_polarisation_frac", checked=True, checkable=True, text="Fraction")  # m_0_f
        self.menu_Mono_No_polarisation.addAction(self.action_Mono_No_polarisation_frac)
        self.menu_Mono_2_polarisations = QtWidgets.QMenu(self.menu_Mono)
        self.__create_element(self.menu_Mono_2_polarisations, [999, 999, 999, 999], "menu_Mono_2_polarisations", title="2 polarisations")
        self.menu_Mono.addAction(self.menu_Mono_2_polarisations.menuAction())
        self.action_Mono_2_polarisations = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_2_polarisations, [999, 999, 999, 999], "action_Mono_2_polarisations", checked=True, checkable=True, text="Default")  # m_2
        self.menu_Mono_2_polarisations.addAction(self.action_Mono_2_polarisations)
        self.action_Mono_2_polarisations_multi = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_2_polarisations_multi, [999, 999, 999, 999], "action_Mono_2_polarisations_multi", checked=True, checkable=True, text="Periodical multilayers")  # m_2_m
        self.menu_Mono_2_polarisations.addAction(self.action_Mono_2_polarisations_multi)
        self.action_Mono_2_polarisations_frac = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_2_polarisations_frac, [999, 999, 999, 999], "action_Mono_2_polarisations_frac", checked=True, checkable=True, text="Fraction")  # m_2_f
        self.menu_Mono_2_polarisations.addAction(self.action_Mono_2_polarisations_frac)
        self.menu_Mono_4_polarisations = QtWidgets.QMenu(self.menu_Mono)
        self.__create_element(self.menu_Mono_4_polarisations, [999, 999, 999, 999], "menu_Mono_4_polarisations", title="4 polarisations")
        self.menu_Mono.addAction(self.menu_Mono_4_polarisations.menuAction())
        self.action_Mono_4_polarisations = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_4_polarisations, [999, 999, 999, 999], "action_Mono_4_polarisations", checked=True, checkable=True, text="Default")  # m_4
        self.menu_Mono_4_polarisations.addAction(self.action_Mono_4_polarisations)
        self.action_Mono_4_polarisations_multi = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_4_polarisations_multi, [999, 999, 999, 999], "action_Mono_4_polarisations_multi", checked=True, checkable=True, text="Periodical multilayers")  # m_4_m
        self.menu_Mono_4_polarisations.addAction(self.action_Mono_4_polarisations_multi)
        self.action_Mono_4_polarisations_frac = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_4_polarisations_frac, [999, 999, 999, 999], "action_Mono_4_polarisations_frac", checked=True, checkable=True, text="Fraction")  # m_4_f
        self.menu_Mono_4_polarisations.addAction(self.action_Mono_4_polarisations_frac)

        self.menu_Tof = QtWidgets.QMenu(self.menu_MenuBar)
        self.__create_element(self.menu_Tof, [999, 999, 999, 999], "menu_Tof", title="TOF")
        self.menu_MenuBar.addAction(self.menu_Tof.menuAction())
        self.menu_Tof_No_polarisation = QtWidgets.QMenu(self.menu_Mono)
        self.__create_element(self.menu_Tof_No_polarisation, [999, 999, 999, 999], "menu_Tof_No_polarisation", title="No polarisation")
        self.menu_Tof.addAction(self.menu_Tof_No_polarisation.menuAction())
        self.action_Tof_No_polarisation = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Tof_No_polarisation, [999, 999, 999, 999], "action_Tof_No_polarisation", checked=True, checkable=True, text="Default") # t_0
        self.menu_Tof_No_polarisation.addAction(self.action_Tof_No_polarisation)
        self.action_Tof_No_polarisation_SL = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Tof_No_polarisation_SL, [999, 999, 999, 999], "action_Tof_No_polarisation_SL", checked=True, checkable=True, text="Solid-Liquid")  # t_0_sl
        self.menu_Tof_No_polarisation.addAction(self.action_Tof_No_polarisation_SL)
        self.action_Tof_2_polarisations = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Tof_2_polarisations, [999, 999, 999, 999], "action_Tof_2_polarisations", checked=True, checkable=True, text="2 polarisations") # t_2
        self.menu_Tof.addAction(self.action_Tof_2_polarisations)
        self.action_Tof_4_polarisations = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Tof_4_polarisations, [999, 999, 999, 999], "action_Tof_4_polarisations", checked=True, checkable=True, text="4 polarisations") # t_4
        self.menu_Tof.addAction(self.action_Tof_4_polarisations)

        # Statusbar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

class GUI(Ui_MainWindow):

    current_dir = os.getcwd().replace("\\", "/")
    def __init__(self):

        super(GUI, self).__init__()
        self.setupUi(self)

        self.input_structure = [] # structure of the data file
        self.program_mode() # No polarisation by default
        self.importing = False # Needs for table synchronisation in FRAC modes
        self.FITBAG_df = "" # stores fitbag as pandas dataframe
        self.DATA_FILES_DATA = [] # scan points

        # Actions for buttons
        self.toolButton_Data_file.clicked.connect(self.button_data_file)
        self.toolButton_Save_at_Dir_1.clicked.connect(self.button_save_at)
        self.pushButton_Film_description_Add_layer.clicked.connect(self.buttons_add_remove_layer)
        self.pushButton_Film_description_Remove_layer.clicked.connect(self.buttons_add_remove_layer)
        self.pushButton_Start_fitting.clicked.connect(self.button_start_fitting)
        self.pushButton_Fit_results_Copy_to_Start_fit_with.clicked.connect(self.button_copy_to_start_with)
        self.pushButton_Film_description_Load_entry.clicked.connect(self.load_entry_file)
        self.pushButton_Film_description_Load_fitbag.clicked.connect(self.button_load_fitbag_file)
        self.pushButton_Resolution_function_Show.clicked.connect(self.draw_resolution_function)
        self.action_Mono_No_polarisation.triggered.connect(self.program_mode)
        self.action_Mono_2_polarisations.triggered.connect(self.program_mode)
        self.action_Mono_4_polarisations.triggered.connect(self.program_mode)
        self.action_Tof_No_polarisation.triggered.connect(self.program_mode)
        self.action_Tof_2_polarisations.triggered.connect(self.program_mode)
        self.action_Tof_4_polarisations.triggered.connect(self.program_mode)
        self.action_Mono_No_polarisation_multi.triggered.connect(self.program_mode)
        self.action_Mono_2_polarisations_multi.triggered.connect(self.program_mode)
        self.action_Mono_4_polarisations_multi.triggered.connect(self.program_mode)
        self.action_Mono_No_polarisation_frac.triggered.connect(self.program_mode)
        self.action_Mono_2_polarisations_frac.triggered.connect(self.program_mode)
        self.action_Mono_4_polarisations_frac.triggered.connect(self.program_mode)
        self.action_Mono_No_polarisation_SL.triggered.connect(self.program_mode)
        self.action_Tof_No_polarisation_SL.triggered.connect(self.program_mode)
        self.actionVersion.triggered.connect(self.menu_info)
        self.checkBox_Fit_results_Select_all.clicked.connect(self.fit_results_select_all)
        self.checkBox_Data_file_preformatted.clicked.connect(self.parse_data_files)
        self.checkBox_Show_fixed.clicked.connect(self.fill_Fit_results_table)
        self.comboBox_Data_file_Column_1.currentIndexChanged.connect(self.parse_data_files)
        self.comboBox_Data_file_Column_2.currentIndexChanged.connect(self.parse_data_files)
        self.comboBox_Data_file_Column_3.currentIndexChanged.connect(self.parse_data_files)
        self.comboBox_Reflectivity_profile_Scale.currentIndexChanged.connect(self.draw_reflectivity)
        self.comboBox_Reflectivity_profile_Scale.currentIndexChanged.connect(self.draw_and_export_reform_FitFunct)
        self.tableWidget_Film_description.cellChanged.connect(self.synchronize_frac_thickness)
        self.lineEdit_Scan_parameters_Points_to_exclude_First.editingFinished.connect(self.draw_reflectivity)
        self.lineEdit_Scan_parameters_Points_to_exclude_Last.editingFinished.connect(self.draw_reflectivity)
        self.lineEdit_Scan_parameters_Step_for_resolution_function.editingFinished.connect(self.draw_resolution_function)
        self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function.editingFinished.connect(self.draw_resolution_function)
        self.lineEdit_Scan_parameters_Sigma.editingFinished.connect(self.draw_resolution_function)

        self.lineEdit_Save_at_Dir_1.setPlaceholderText("Main dirictory [" + str(self.current_dir) + "/]")

    ##--> redefine user interface elements in differend modes
    def program_mode(self):
        '''
        Different modes should have a bit different parameters available, so a bit different interfaces.
        '''

        # program name, file to wait, default entry
        self.MODE_SPECS = {"m_0": ["Film500x0.exe", "FitFunct.dat", "UserDefaults_nopol.ent"],
                            "m_2": ["Film500x2.exe", "Fit2DFunctDD.dat", "UserDefaults_2pol.ent"],
                            "m_4": ["Film500x4.exe", "Fit2DFunctDD.dat", "UserDefaults_4pol.ent"],
                            "t_0": ["FilmTOF500QX0.exe", "FitFunct.dat", "UserDefaults_TOF_nopol.ent"],
                            "t_2": ["FilmTOF500QX2.exe", "Fit2DFunctDD.dat", "UserDefaults_TOF_2pol.ent"],
                            "t_4": ["FilmTOF500QX4.exe", "Fit2DFunctDD.dat", "UserDefaults_TOF_4pol.ent"],
                            "m_0_m": ["Mult500x0d3Gr.exe", "FitFunct.dat", "UserDefaults_nopol_multi.ent"],
                            "m_2_m": ["Mult500x2d4Gr.exe", "Fit2DFunctDD.dat", "UserDefaults_2pol_multi.ent"],
                            "m_4_m": ["Mult500x4d4Gr.exe", "Fit2DFunctDD.dat", "UserDefaults_4pol_multi.ent"],
                            "m_0_f": ["Film500x0Nfrac.exe", "FitFunct.dat", "UserDefaults_nopol_frac.ent"],
                            "m_2_f": ["Film500x2Nfrac.exe", "Fit2DFunctDD.dat", "UserDefaults_2pol_frac.ent"],
                            "m_4_f": ["Film500x4Nfrac.exe", "Fit2DFunctDD.dat", "UserDefaults_4pol_frac.ent"],
                            "m_0_sl": ["Film500x0.exe", "FitFunct.dat", "UserDefaults_nopol_sl.ent"],
                            "t_0_sl": ["FilmTOF500QX0.exe", "FitFunct.dat", "UserDefaults_TOF_nopol_sl.ent"]}

        DICT_MODES = {"action_Mono_No_polarisation": "m_0", "action_Mono_2_polarisations": "m_2", "action_Mono_4_polarisations": "m_4",
                      "action_Tof_No_polarisation": "t_0", "action_Tof_2_polarisations": "t_2", "action_Tof_4_polarisations": "t_4",
                      "action_Mono_No_polarisation_frac": "m_0_f", "action_Mono_2_polarisations_frac": "m_2_f", "action_Mono_4_polarisations_frac": "m_4_f",
                      "action_Mono_No_polarisation_multi": "m_0_m", "action_Mono_2_polarisations_multi": "m_2_m", "action_Mono_4_polarisations_multi": "m_4_m",
                      "action_Mono_No_polarisation_SL": "m_0_sl", "action_Tof_No_polarisation_SL": "t_0_sl", }

        # Step 1: define desired mode
        try: # check where we came from and change the interface accordingly
            self.BoToFit_mode = DICT_MODES[self.sender().objectName()]
            # Step 2: make sure that only one mode is checked in the mode menu
            for mode in [self.action_Mono_No_polarisation, self.action_Mono_2_polarisations, self.action_Mono_4_polarisations, self.action_Tof_No_polarisation, self.action_Tof_2_polarisations, self.action_Tof_4_polarisations, self.action_Mono_No_polarisation_multi, self.action_Mono_2_polarisations_multi, self.action_Mono_4_polarisations_multi, self.action_Mono_No_polarisation_SL, self.action_Tof_No_polarisation_SL, self.action_Mono_No_polarisation_frac, self.action_Mono_2_polarisations_frac, self.action_Mono_4_polarisations_frac]: mode.setChecked(True if mode.objectName() == self.sender().objectName() else False)
        except AttributeError: # first run of the program will have no "self.sender()"
            self.BoToFit_mode = DICT_MODES["action_Mono_No_polarisation"]
            self.action_Mono_No_polarisation.setChecked(True)

        # Step 3: reformat table(s) and show/hide available parameters for specific modes
        # show/hide tabs in the tabWidget
        TABS_AND_NAMES = [[self.tab_Film_description, ("Fraction 1" if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"] else "Film description")], [self.tab_Film_description_2, "Fraction 2"], [self.tab_Scan_parameters, "Scan parameters"]]
        for i in reversed(range(0, self.tabWidget_Start_fit_with.count())): self.tabWidget_Start_fit_with.removeTab(i)
        for index, tab in enumerate(TABS_AND_NAMES):
            if index == 1 and self.BoToFit_mode not in ["m_0_f", "m_2_f", "m_4_f"]: continue
            self.tabWidget_Start_fit_with.addTab(tab[0], tab[1])

        # show/hide frac parameters
        PARAMS_FRAC = [self.label_Scan_parameters_Fraction_amount, self.lineEdit_Scan_parameters_Fraction_amount, self.checkBox_Scan_parameters_Fraction_amount, self.label_Scan_parameters_Cg_2, self.lineEdit_Scan_parameters_Cg_2, self.checkBox_Scan_parameters_Cg_2, self.label_Scan_parameters_Sg_2, self.lineEdit_Scan_parameters_Sg_2, self.checkBox_Scan_parameters_Sg_2, self.label_Scan_parameters_Sg2_2, self.lineEdit_Scan_parameters_Sg2_2, self.checkBox_Scan_parameters_Sg2_2]
        for param in PARAMS_FRAC[0:3]: param.setVisible(True if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"] else False)
        for param in PARAMS_FRAC[3:]: param.setVisible(True if self.BoToFit_mode in ["m_2_f", "m_4_f"] else False)

        # show/hide polarisation parameters
        PARAMS_POL = [self.label_Scan_parameters_Piy, self.lineEdit_Scan_parameters_Piy, self.checkBox_Scan_parameters_Piy, self.label_Scan_parameters_Pfy, self.lineEdit_Scan_parameters_Pfy, self.checkBox_Scan_parameters_Pfy, self.label_Scan_parameters_Pfy, self.lineEdit_Scan_parameters_Pfy, self.checkBox_Scan_parameters_Pfy, self.label_Scan_parameters_Cg, self.lineEdit_Scan_parameters_Cg, self.checkBox_Scan_parameters_Cg, self.label_Scan_parameters_Sg, self.lineEdit_Scan_parameters_Sg, self.checkBox_Scan_parameters_Sg, self.label_Scan_parameters_Sg2, self.lineEdit_Scan_parameters_Sg2, self.checkBox_Scan_parameters_Sg2]

        if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl"]: enable, col_width = False, [102, 107, 32, 107, 32, 107, 32, 0, 0, 0, 0, 107, 32]
        elif self.BoToFit_mode in ["m_2", "m_4", "t_2", "t_4", "m_2_m", "m_4_m", "m_0_f", "m_2_f", "m_4_f"]:
            col_width =  [57, 66, 32, 65, 32, 65, 32, 65, 32, 76, 32, 72, 32]
            enable = False if self.BoToFit_mode == "m_0_f" else True
        for param in PARAMS_POL: param.setVisible(enable)
        for i in range(0, 13):
            self.tableWidget_Film_description.setColumnWidth(i, col_width[i])
            self.tableWidget_Film_description_2.setColumnWidth(i, col_width[i])

        # show/hide multi parameters
        PARAM_MULTI = [self.label_Scan_parameters_Gradient_period, self.lineEdit_Scan_parameters_Gradient_period, self.checkBox_Scan_parameters_Gradient_period, self.label_Scan_parameters_Gradient_roughness, self.lineEdit_Scan_parameters_Gradient_roughness, self.checkBox_Scan_parameters_Gradient_roughness, self.label_Scan_parameters_Gradient_sld, self.lineEdit_Scan_parameters_Gradient_sld, self.checkBox_Scan_parameters_Gradient_sld, self.label_Scan_parameters_Gradient_msld, self.lineEdit_Scan_parameters_Gradient_msld, self.checkBox_Scan_parameters_Gradient_msld]

        enable = [True if self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"] else False][0]
        for param in PARAM_MULTI: param.setVisible(enable)
        if self.BoToFit_mode == "m_0_m": # no mSLD gradient for NoPol_multi
            for param in PARAM_MULTI[9:13]: param.setVisible(False)

        # reformat checkboxes (I, dI, Qz, rad) and Wavelength/Inc.angle field
        CHECKBOXES = [self.comboBox_Data_file_Column_1, self.comboBox_Data_file_Column_2, self.comboBox_Data_file_Column_3]

        if self.BoToFit_mode in ["m_0", "m_2", "m_4", "m_0_m", "m_2_m", "m_4_m", "m_0_sl", "m_0_f", "m_2_f", "m_4_f"]:
            if self.comboBox_Data_file_Column_1.count() < 4:
                for checkbox in CHECKBOXES:
                    checkbox.addItem("")
                    checkbox.setItemText(3, "ang(rad)")
            self.label_Scan_parameters_Wavelength.setText("Wavelength (A)")

        elif self.BoToFit_mode in ["t_0", "t_2", "t_4", "t_0_sl"]:
            for checkbox in CHECKBOXES: checkbox.removeItem(3)
            self.label_Scan_parameters_Wavelength.setText("Inc. ang. (mrad)")

        if self.checkBox_Data_file_preformatted.isChecked(): self.comboBox_Data_file_Column_3.setCurrentIndex(0 if self.BoToFit_mode in ["t_0", "t_2", "t_4", "t_0_sl"] else 3)

        # clean up lineEdits and checkboxes when we switch to the mode with less parameters
        for i in ([1, 2], [4, 5], [7, 8], [10, 11], [13, 14], [16, 17]): # PARAMS_POL
            PARAMS_POL[i[0]].setText("")
            PARAMS_POL[i[1]].setChecked(False)
        for i in ([1, 2], [4, 5], [7, 8], [10, 11]): # PARAM_MULTI
            PARAM_MULTI[i[0]].setText("")
            PARAM_MULTI[i[1]].setChecked(False)

        # Step 4: reformat table if SL mode is needed
        self.table_add_sl_layer()

        # Step 5: load UserDefaults if such are presented
        try:
            if self.MODE_SPECS[self.BoToFit_mode][2] in os.listdir(self.current_dir + "/User_Defaults"):
                self.lineEdit_Scan_parameters_Wavelength.setText("")
                self.load_entry_file(entry_func_param=self.current_dir + "/User_Defaults/" + self.MODE_SPECS[self.BoToFit_mode][2])
        except: True

        # clear stuff, just in case
        self.clear_stuff()
        self.lineEdit_Data_file.clear()
        self.DATA_FOLDER = ""
    ##<--

    ##--> buttons and triggers
    def button_data_file(self):
        ''' if {NoPolarisation} and {toolButton_Data_file} is pressed: [user can choose only one file]
        elif {toolButton_Data_file} is pressed: [user can choose several file] '''

        self.input_structure = [self.comboBox_Data_file_Column_1.currentText(), self.comboBox_Data_file_Column_2.currentText(), self.comboBox_Data_file_Column_3.currentText()]

        if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]: data_files = QtWidgets.QFileDialog().getOpenFileName(None, "Data file", self.current_dir if len(self.lineEdit_Save_at_Dir_1.text()) < 1 else self.lineEdit_Save_at_Dir_1.text())[0]
        else: data_files = QtWidgets.QFileDialog().getOpenFileNames(None, "Data files", self.current_dir if len(self.lineEdit_Save_at_Dir_1.text()) < 1 else self.lineEdit_Save_at_Dir_1.text())[0]

        if data_files in ["", []]: return

        self.lineEdit_Data_file.setText(str(data_files))

        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]: data_files = data_files[0]

        data_file_input_name = data_files[data_files.rfind("/") + 1: data_files.rfind(".")].replace(" ", "_")
        self.lineEdit_Save_at_Dir_2.setText(data_file_input_name + "/")

        # clear stuff after last run
        self.clear_stuff()

        if self.BoToFit_mode in ["m_0", "m_2", "m_4", "m_0_m", "m_2_m", "m_4_m", "m_0_sl", "m_0_f", "m_2_f", "m_4_f"] and self.lineEdit_Scan_parameters_Wavelength.text() == "": self.statusbar.showMessage("Input wavelength and reimport the file")
        else: self.parse_data_files()

    def buttons_add_remove_layer(self):
        ''' We work with "Film description" table here'''

        # Step 1: check where we came here from (other function of button)
        try:
            sender_name = self.sender().objectName()
        except AttributeError: sender_name = "None" # if we come here from another function, we have no "self.sender()"

        # Step 2: Remove rows if user asked, otherwice - add
        if sender_name == "pushButton_Film_description_Remove_layer": # remove lines from {tableWidget_Film_description}
            if not self.tableWidget_Film_description.rowCount() == self.tableWidget_Film_description.currentRow() + 1:
                self.tableWidget_Film_description.removeRow(self.tableWidget_Film_description.currentRow())
                self.tableWidget_Film_description_2.removeRow(self.tableWidget_Film_description_2.currentRow())
        else: # add lines into {tableWidget_Film_description}
            i = self.tableWidget_Film_description.currentRow() if self.tableWidget_Film_description.currentRow() >= 0 else 0

            for index, tabWidget in enumerate([self.tableWidget_Film_description, self.tableWidget_Film_description_2]):
                tabWidget.insertRow(i)
                tabWidget.setRowHeight(i, 21)
                for j in range(0, 13):
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    if j in (1, 2) and index == 1: item.setFlags(QtCore.Qt.NoItemFlags) # leave "thickness" only in the first table
                    if j in (4, 6, 8, 10, 12):
                        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        item.setCheckState(QtCore.Qt.Checked if j == 6 else QtCore.Qt.Unchecked)

                    tabWidget.setItem(i, j, item)

    def button_save_at(self):
        ''' default {save_at_dit} folder is the one where "BoToFit.exe" is located
        otherwice: defined by user '''

        dir = QtWidgets.QFileDialog().getExistingDirectory(None, "FileNames", self.current_dir)
        if dir: self.lineEdit_Save_at_Dir_1.setText(str(dir) + "/")

    def button_copy_to_start_with(self):
        COLUMNS = {"Thickness" : 1, "SLD" : 3, "iSLD" : 5, "mSLD" : 7, "Cos(d-gamma)" : 9, "Roughness" : 11}
        PARAMETERS = {'Scaling_factor': self.lineEdit_Scan_parameters_Scaling_factor, 'Overillumination': self.lineEdit_Scan_parameters_Crossover_overillumination, 'Background': self.lineEdit_Scan_parameters_Background, 'Pi(y)': self.lineEdit_Scan_parameters_Piy, 'Pf(y)': self.lineEdit_Scan_parameters_Pfy, 'grad.Period': self.lineEdit_Scan_parameters_Gradient_period, 'grad.Roughness': self.lineEdit_Scan_parameters_Gradient_roughness, 'grad.SLD': self.lineEdit_Scan_parameters_Gradient_sld, 'grad.mSLD': self.lineEdit_Scan_parameters_Gradient_msld, "[F1]_amount" : self.lineEdit_Scan_parameters_Fraction_amount, '<cos(gamma)>':self.lineEdit_Scan_parameters_Cg, '<sin(gamma)>': self.lineEdit_Scan_parameters_Sg, '<sin2(gamma)>': self.lineEdit_Scan_parameters_Sg2, '<cos(gamma)>_F2':self.lineEdit_Scan_parameters_Cg_2, '<sin(gamma)>_F2': self.lineEdit_Scan_parameters_Sg_2, '<sin2(gamma)>_F2': self.lineEdit_Scan_parameters_Sg2_2}

        for i in range(0, self.tableWidget_Fit_results.rowCount()):
            if not self.tableWidget_Fit_results.item(i,0).checkState() == 2: continue

            parameter = self.tableWidget_Fit_results.item(i, 2).text().split()

            if not len(parameter) == 1: # table
                if "(La" in parameter[0]: row = int(parameter[0][3 : parameter[0].find(")")]) - (0 if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] else 1)
                elif "(Su)" in parameter[0]: row = self.tableWidget_Film_description.rowCount() - 1
                # in FRAC modes we have one more parameter [Fr1]/[Fr2]
                table = self.tableWidget_Film_description_2 if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"] and "[F2]" in parameter[0] else self.tableWidget_Film_description
                table.item(row, COLUMNS[parameter[1]]).setText(str(float(self.tableWidget_Fit_results.item(i, 3).text())))
            else: # other parameters
                PARAMETERS[parameter[0]].setText(str(float(self.tableWidget_Fit_results.item(i, 3).text())))

    def button_load_fitbag_file(self):
        ''' if user decided to terminate fitting routine, uncompleted FitBag file will still be recorded in SaveAt directory. Lets allow user to load last iteration from that FitBag file. '''

        if self.pushButton_Start_fitting.text() == "Stop fitting": # this means we came here while user wanted to stop BoToFit manually
            fitbag_file = self.DATA_FOLDER + ("Fit2DBag.dat" if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"] else "FitBag.dat")
        elif not self.DATA_FOLDER == "":   # otherwice user wants to open FitBag file manually (case 1)
            dir = self.DATA_FOLDER
            fitbag_file = QtWidgets.QFileDialog().getOpenFileName(None, "FitBag file", dir)[0]
        else: # (case 2)
            if not self.lineEdit_Save_at_Dir_1.text() == "": dir = self.lineEdit_Save_at_Dir_1.text()
            elif not self.lineEdit_Data_file.text() in ["", "[]"]:
                data_file = [file for file in self.lineEdit_Data_file.text().split("'") if len(file) > 2][0]
                dir = data_file[:data_file.rfind("/") + 1]
            else: dir = self.current_dir if len(self.lineEdit_Save_at_Dir_1.text()) < 1 else self.lineEdit_Save_at_Dir_1.text()
            fitbag_file = QtWidgets.QFileDialog().getOpenFileName(None, "FitBag file", dir)[0]
            self.DATA_FOLDER = fitbag_file[:fitbag_file.rfind("/")+1]

        if not fitbag_file: return

        self.create_entry_for_multiGrPr(fitbag_file) # read FitBag file
        self.multyGrPr_run()

        # run multiGrPr and wait until it finished to work
        while "SLD_profile.dat" not in os.listdir(self.DATA_FOLDER): QtTest.QTest.qWait(1000)
        while os.path.getsize(self.DATA_FOLDER + 'SLD_profile.dat') < 1: QtTest.QTest.qWait(1000)

        self.draw_sld() # draw SLD

    def button_start_fitting(self):
        ''' When user press "Start fitting" I start 2 threads: "BoToFit" and "Killer".
        If user press "Stop fitting" - I kill "BoToFit" process prematurely and try "start fitting" again with all parameters fixed, so I can get fitfunct file '''

        if self.lineEdit_Data_file.text() == "": return

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
                    [self.tableWidget_Film_description, self.tableWidget_Film_description_2] if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"] else [
                        self.tableWidget_Film_description]):
                for i in range(0, tabWidget.rowCount()):
                    if self.tableWidget_Film_description.item(i, 8).checkState() == 0 and self.tableWidget_Film_description.item(i, 10).checkState() == 0:
                        self.statusbar.showMessage("mSLD and cos(d-gamma) can not be fitted together for the same layer")
                        return

        start_time = time.time()

        # CLEANUP - delete some files and clear graphs before start
        self.FITBAG_df = ""
        self.lineEdit_Fit_results_Chi_square_Previous.setText(self.lineEdit_Fit_results_Chi_square_Actual.text())
        self.checkBox_Fit_results_Select_all.setChecked(False)
        self.clear_stuff(chi_prev=False)
        self.draw_reflectivity()
        self.statusbar.clearMessage()
        # delete files from previous run
        for SLD_multigrpr_file in [self.MODE_SPECS[self.BoToFit_mode][1], 'SLD_profile.dat', 'SLD_profile_F1.dat', 'SLD_profile_F2.dat', 'multiGrPr.ent',
                                   'multiGrPr_2.ent', 'multiGrPr_F1.ent', 'multiGrPr_F2.ent']:
            try:
                os.remove(self.DATA_FOLDER + SLD_multigrpr_file)
            except:
                True

        # RUN - step 1 - create new directory or rewrite files if they already exists
        if not self.lineEdit_Save_at_Dir_1.text(): self.lineEdit_Save_at_Dir_1.setText(self.current_dir + "/")
        self.DATA_FOLDER = self.lineEdit_Save_at_Dir_1.text() + self.lineEdit_Save_at_Dir_2.text() + (
            "/" if self.lineEdit_Save_at_Dir_2.text()[-1] == "/" else "")
        if not os.path.exists(self.DATA_FOLDER): os.makedirs(self.DATA_FOLDER)

        # RUN - step 2 - get ready to start BoToFit
        self.create_input_data_file()
        self.create_entry_for_BoToFit()

        # CHECKUP - dont run if Error in Statusbar
        if self.statusbar.currentMessage().find("Error") == 0: return

        # RUN - step 3 - Start BoToFit with its "killer" in 2 threads
        module = '"' + self.current_dir + '/BoToFit_Modules/' + self.MODE_SPECS[self.BoToFit_mode][0] + '"'
        entry = '"' + self.DATA_FOLDER + "boto.ent" + '"'
        data = '"' + self.DATA_FOLDER + "data_file_reformatted.dat" + '"'

        self.pushButton_Start_fitting.setText("Stop fitting")
        self.statusbar.showMessage("Running...")

        # start BoToFit module with Threading
        for i in range(2):
            t = threading.Thread(target=self.BoToFit_calc_run, args=(
            self.DATA_FOLDER, i, module, entry, data, self.lineEdit_Scan_parameters_Points_to_exclude_First.text(),
            self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()))
            t.start()

        # wait until "killer" is done or BoToFit has crashed
        BoToFit_calc_thread_are_done = 0
        while BoToFit_calc_thread_are_done == 0:
            QtTest.QTest.qWait(1000)
            proc_list = [proc.name() for proc in psutil.process_iter() if proc.name() == self.MODE_SPECS[self.BoToFit_mode][0]]
            ''' Button "Stop fitting" will kill "BoToFit" process, so we can move on '''
            if len(proc_list) == 0: BoToFit_calc_thread_are_done = 1

        # RUN - step 4 - analize the results depending on "how BoToFit was stopped"
        if self.MODE_SPECS[self.BoToFit_mode][1] not in os.listdir(self.DATA_FOLDER):
            ''' If BoToFit stops prematurely '''
            # self.clear_stuff(chi_prev=False)
            self.draw_reflectivity()
            self.statusbar.showMessage("BoToFit crashed or has been stopped by user. Anyway, consider using more reasonable 'Start fit' values.")
            self.button_load_fitbag_file()

            ''' Threading - Complimentary BoToFit - all params fixed (needed to get fitfunct) '''
            for i in range(2):
                t = threading.Thread(target=self.BoToFit_calc_run,
                                     args=(self.DATA_FOLDER + "temp/", i, module, '"' + self.DATA_FOLDER + "temp/boto.ent" + '"', data,
                                           self.lineEdit_Scan_parameters_Points_to_exclude_First.text(),
                                           self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()))
                t.start()

            # wait until "killer" is done or "BoToFit" has crashed
            BoToFit_calc_thread_are_done = 0
            while BoToFit_calc_thread_are_done == 0:
                QtTest.QTest.qWait(1000)
                proc_list = []
                for proc in psutil.process_iter(): proc_list.append(proc.name())
                if self.MODE_SPECS[self.BoToFit_mode][0] not in proc_list: BoToFit_calc_thread_are_done = 1

            if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]: fit_funct_files = ["FitFunct.dat"]
            elif self.BoToFit_mode in ["m_2", "t_2", "m_2_m", "m_2_f"]: fit_funct_files = ["Fit2DFunctUU.dat", "Fit2DFunctDD.dat"]
            elif self.BoToFit_mode in ["m_4", "t_4", "m_4_m", "m_4_f"]: fit_funct_files = ["Fit2DFunctUU.dat", "Fit2DFunctDD.dat", "Fit2DFunctUD.dat", "Fit2DFunctDU.dat"]

            # Mono_0_multy mode takes time to write a lot of points, so wait
            if self.BoToFit_mode == "m_0_m": QtTest.QTest.qWait(2000)

            for fit_func_file in fit_funct_files:
                os.replace(self.DATA_FOLDER + "temp/" + fit_func_file, self.DATA_FOLDER + fit_func_file)
            shutil.rmtree(self.DATA_FOLDER + "temp", ignore_errors=True)

            self.draw_and_export_reform_FitFunct()
            self.draw_diff()
            self.pushButton_Start_fitting.setText("Start fitting")
            return

        else:
            ''' If BoToFit stops as it should '''
            self.pushButton_Start_fitting.setText("Start fitting")

            # wait until fitting is done -> fill the table, draw graphs and create multiGrPr.ent using FitBag.dat file
            self.graphicsView_Reflectivity_profile.getPlotItem().clear()
            self.draw_reflectivity()
            self.draw_and_export_reform_FitFunct()
            self.draw_diff()

            self.create_entry_for_multiGrPr(
                self.DATA_FOLDER + ["Fit2DBag.dat" if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"] else "FitBag.dat"][0])

            self.multyGrPr_run()
            self.draw_sld()  # draw SLD

            self.statusbar.showMessage("Finished in " + str(round(float(time.time() - start_time), 1)) + " seconds")
    ##<--

    ##--> menu options
    def menu_info(self):

        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(self.iconpath))
        msgBox.setText( "BoToFit " + self.actionVersion.text() + "\n\n"
                        "Algorithm: Boris.Toperverg@ruhr-uni-bochum.de\n"
                        "GUI: Alexey.Klechikov@gmail.com\n\n"
                        "Check for newer version at https://github.com/Alexey-Klechikov/BoToFit/releases")
        msgBox.exec_()
    ##<--

    ##--> "input file"
    def parse_data_files(self):
        ''' I write data points into self.DATA_FILES_DATA variable in [*angle, *I, *dI] format to avoid multiple parsings of the same file
            inside the self.DATA_FILES_DATA, the data are ordered as self.DATA_FILES_DATA[File, polarization][Parameter][Point number]
            polarisation order in self.DATA_FILES_DATA = [UU, (DD), (UD), DU]
        '''
        # change comboboxes if required
        if self.checkBox_Data_file_preformatted.isChecked():
            comboboxes = [self.comboBox_Data_file_Column_1, self.comboBox_Data_file_Column_2, self.comboBox_Data_file_Column_3]
            for i, combobox in enumerate(comboboxes): combobox.setCurrentIndex([1, 2, 0 if self.BoToFit_mode in ["t_0", "t_2", "t_4", "t_0_sl"] else 3][i])

        self.DATA_FILES_DATA = []
        self.clear_stuff(fit_res=False)

        # parse data files if none of comboboxes are the same
        self.input_structure = [self.comboBox_Data_file_Column_1.currentText(), self.comboBox_Data_file_Column_2.currentText(), self.comboBox_Data_file_Column_3.currentText()]
        if not ([x for n, x in enumerate(self.input_structure) if x in self.input_structure[:n]] == [] and not self.lineEdit_Data_file.text() in ["", "[]"] and "I" in self.input_structure and "dI" in self.input_structure):
            self.statusbar.showMessage("Error: recheck 'Data file structure' comboboxes.")
            return

        # preformatted BoToFit data file should contain all polarisations in the format "I dI (ang(Qz) if TOF else ang(rad))"
        if self.checkBox_Data_file_preformatted.isChecked():
            with open([self.lineEdit_Data_file.text() if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"] else self.lineEdit_Data_file.text().split("'")[1]][0], "r") as preformatted_data_file:

                lines = [line for line in preformatted_data_file.readlines() if line.strip()]
                self.lineEdit_Number_of_points = len(lines) if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"] else [len(lines)/2 if self.BoToFit_mode in ["m_2", "t_2", "m_2_m", "m_2_f"] else len(lines)/4][0]

                data_angle, data_I, data_dI = [], [], []
                for i, line in enumerate(lines):
                    for ind, dat in enumerate((data_I, data_dI, data_angle)): dat.append(float(line.split()[ind]))
                    if (i + 1) % self.lineEdit_Number_of_points == 0:
                        self.DATA_FILES_DATA.append((data_angle, data_I, data_dI))
                        data_angle, data_I, data_dI = [], [], []

        # otherwice we analize several files with chosen structure
        else:
            files = [""] if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_m", "m_0_f"] else ["", "", "", ""]

            # reformat data to *I *dI *angle(rad) in Mono mode
            if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]:
                files[0] = self.lineEdit_Data_file.text()
            else:
                for i in self.lineEdit_Data_file.text().split("'"):
                    if i.rfind("_uu") > 0 or i.rfind("_UU") > 0 or i.rfind("_u_") > 0 or i.rfind("_U_") > 0: files[0] = i
                    elif i.rfind("_dd") > 0 or i.rfind("_DD") > 0: files[1] = i
                    elif i.rfind("_ud") > 0 or i.rfind("_UD") > 0: files[2] = i
                    elif i.rfind("_du") > 0 or i.rfind("_DU") > 0 or i.rfind("_d_") > 0 or i.rfind("_D_") > 0: files[-1] = i

            for file in [i for i in files if len(i) > 0]:
                self.lineEdit_Number_of_points, data_angle, data_I, data_dI = 0, [], [], []

                with open(file, 'r') as data_file_input:
                    for i, line in enumerate([line for line in data_file_input.readlines() if line.strip()]):
                        if file[-4:] == '.mft' and i < 23: continue # for Figaro

                        data_angle.append(float(line.split()[self.input_structure.index("ang(Qz)" if "ang(Qz)" in self.input_structure else "ang(rad)")]))
                        data_I.append(float(line.split()[self.input_structure.index("I")]))
                        data_dI.append(float(line.split()[self.input_structure.index("dI")]))
                        self.lineEdit_Number_of_points += 1

                self.DATA_FILES_DATA.append((data_angle, data_I, data_dI))

        # perform checkups of the data files
        self.statusbar.clearMessage()
        # 1 - missing files
        if (self.BoToFit_mode in ["m_2", "t_2", "m_2_m", "m_2_f"] and not len(self.DATA_FILES_DATA) == 2) or (self.BoToFit_mode in ["m_4", "t_4", "m_4_m", "m_4_f"] and not len(self.DATA_FILES_DATA) == 4):
            self.statusbar.showMessage("Error: Not enough Data files or missing points in the preformatted file.")
        # 2 - missing points
        elif (len(self.DATA_FILES_DATA) == 2 and not len(self.DATA_FILES_DATA[0]) == len(self.DATA_FILES_DATA[1])) or (len(self.DATA_FILES_DATA) == 4 and not len(self.DATA_FILES_DATA[0]) == len(self.DATA_FILES_DATA[1]) == len(self.DATA_FILES_DATA[2]) == len(self.DATA_FILES_DATA[3])):
            self.statusbar.showMessage("Error: Your input data files have different numbers of points.")
        # 3 - points aren't consistent
        else:
            for pol in self.DATA_FILES_DATA:
                for i in range(1, len(pol[0])):
                    if pol[0][i] < pol[0][i-1]: self.statusbar.showMessage("Warning: Your point order is not consistent. Recheck the point at the angle " + str(pol[0][i-1]))

        if self.statusbar.currentMessage().find("Error") == 0: return

        self.draw_reflectivity()

    def create_input_data_file(self):
        ''' input data files for BoToFit should have [*I *dI *angle(rad)] format in Mono mode and [*I *dI *Qz] in TOF mode '''

        with open(self.DATA_FOLDER + "data_file_reformatted.dat", 'w') as data_file_output:
            # check hidden table with experimental points already reformatted in Q I dI format
            for i in range(0, len(self.DATA_FILES_DATA)):
                data_angle, data_I, data_dI = self.DATA_FILES_DATA[i]

                for j in range(0, len(data_angle)):
                    if self.BoToFit_mode in ["t_0", "t_2", "t_4", "t_0_sl"]: data_file_output.write(str(data_I[j]) + "  " + str(data_dI[j]) + "    " + str(data_angle[j]) + "\n")
                    else: data_file_output.write(str(data_I[j]) + "  " + str(data_dI[j]) + "    " + str(data_angle[j] if not "ang(Qz)" in self.input_structure else self.angle_convert("Qz", "rad", float(data_angle[j]))) + "\n")
    ##<--

    ##--> "BoToFit entry"
    def load_entry_file(self, entry_func_param=""):
        ''' I use this function both at first run of the program to load "default" values and to import user's entry file '''
        if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: self.importing = True
        # remove cursor from the table for import
        self.tableWidget_Film_description.setCurrentCell(-1, -1)

        # Step 1: either we use entry sent as the parameter, or we allow user to open one manually
        entry_file = QtWidgets.QFileDialog().getOpenFileName(None, "Entry file", self.current_dir if len(self.lineEdit_Save_at_Dir_1.text()) < 1 else self.lineEdit_Save_at_Dir_1.text())[0] if not entry_func_param else entry_func_param
        if entry_file == "": return

        ENTRY = pd.read_csv(entry_file, header=None, squeeze=True)

        # Step 2: fill the form with parameters from the entry
        index_reference = 0
        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]:
            self.lineEdit_Scan_parameters_Piy.setText(ENTRY[2].split()[0]) # Piy incident polarization (polariser)
            self.__set_checked(self.checkBox_Scan_parameters_Piy, ENTRY[3].split()[0])
            self.lineEdit_Scan_parameters_Pfy.setText(ENTRY[8].split()[0]) # Pfy outgoing polarization (analyser)
            self.__set_checked(self.checkBox_Scan_parameters_Pfy, ENTRY[9].split()[0])
            index_reference = 12

        self.lineEdit_Scan_parameters_Wavelength.setText(ENTRY[index_reference].split()[0]) # wavelength or incident angle
        self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function.setText(ENTRY[index_reference+2].split()[0]) # number of experimental points in alpha
        self.lineEdit_Scan_parameters_Step_for_resolution_function.setText(ENTRY[index_reference+3].split()[0]) # step for resolution function (in mrad)
        self.lineEdit_Scan_parameters_Sigma.setText(ENTRY[index_reference+4].split()[0]) # "sigma" of resolution function (in mrad)

        # Check if we input proper Entry file by checkup for number of layers (should be int, not float)
        try:
            self.statusbar.clearMessage()
            _ = int(ENTRY[index_reference + 5].split()[0])
            if self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"]: _, _, _ = int(ENTRY[index_reference + 6].split()[0]), int(ENTRY[index_reference + 7].split()[0]), int(ENTRY[index_reference + 8].split()[0])
        except:
            self.statusbar.showMessage("Error: Incompatible entry format.")
            return

        if self.BoToFit_mode in ["m_0", "m_2", "m_4", "t_0", "t_2", "t_4", "m_0_sl", "t_0_sl", "m_0_f", "m_2_f", "m_4_f"]: number_of_layers, index_reference = int(ENTRY[index_reference+5].split()[0]), index_reference + 6   # no multi modules
        elif self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"]: # multi modules
            number_of_layers_cap = int(ENTRY[index_reference + 5].split()[0]) # "ncap" number of cap layers
            number_of_layers_sub = int(ENTRY[index_reference + 6].split()[0]) # "nsub" number of sub-ayers in a superstructure
            number_of_layers_repetitions = int(ENTRY[index_reference + 7].split()[0]) # "nrep" number of repetitions
            number_of_layers_buffer = int(ENTRY[index_reference + 8].split()[0]) # "nbuf" number of buffer layers
            number_of_layers, index_reference = number_of_layers_cap + number_of_layers_sub + number_of_layers_buffer, index_reference + 9

        # delete all layers except substrate from the table
        while not self.tableWidget_Film_description.rowCount() == 1: self.tableWidget_Film_description.removeRow(0)
        while not self.tableWidget_Film_description_2.rowCount() == 1:self.tableWidget_Film_description_2.removeRow(0)
        # add layers to the table
        for i in range(0, number_of_layers):
            self.buttons_add_remove_layer()
            self.tableWidget_Film_description.item(0, 0).setText(str(number_of_layers - i))
            self.tableWidget_Film_description_2.item(0, 0).setText(str(number_of_layers - i))

        # reformat the table in multi modes
        if self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"]:
            self.tableWidget_Film_description.setSpan(number_of_layers_cap, 0, number_of_layers_sub, 1)

            for row in range(0, number_of_layers):
                if row < number_of_layers_cap: self.tableWidget_Film_description.item(row, 0).setText(str(row+1))
                elif row < number_of_layers_cap + number_of_layers_sub: self.tableWidget_Film_description.item(row, 0).setText(str(row+1) + " x " + str(number_of_layers_repetitions))
                else: self.tableWidget_Film_description.item(row, 0).setText(str(row+2-number_of_layers_sub))

        # check if user wants to import SL entry, while SL checkbox isnt True
        if ENTRY[index_reference + 2].split()[1] == "+" and self.BoToFit_mode not in ["m_0_sl", "t_0_sl"]: self.statusbar.showMessage("Use 'Solid-Liquid' mode with this entry.")

        row, col, SL_sld_offset = 0, 1, ""
        for row in range(0, number_of_layers+1):
            if not row == number_of_layers:
                self.tableWidget_Film_description.item(row, col).setText(ENTRY[index_reference].split()[0].replace("d", "e")) # Thickness
                self.__set_checked(self.tableWidget_Film_description.item(row, col + 1), ENTRY[index_reference+1].split()[0])
                self.tableWidget_Film_description_2.item(row, col).setText(ENTRY[index_reference].split()[0].replace("d", "e"))  # Thickness
                self.__set_checked(self.tableWidget_Film_description_2.item(row, col + 1), ENTRY[index_reference + 1].split()[0])
            else: index_reference -= 2
            if self.BoToFit_mode not in ["m_0_f", "m_2_f", "m_4_f"]: # fill the table (not a FRAC mode)
                if SL_sld_offset == "": SL_sld_offset = float(ENTRY[index_reference + 2].split()[2]) if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] else 0
                self.tableWidget_Film_description.item(row, col + 2).setText(str(round(float(ENTRY[index_reference + 2].split()[0].replace("d", "e")) + SL_sld_offset, 5)))  # SLD
                self.__set_checked(self.tableWidget_Film_description.item(row, col + 3), ENTRY[index_reference+3].split()[0])
                self.tableWidget_Film_description.item(row, col + 4).setText(ENTRY[index_reference + 4].split()[0].replace("d", "e"))  # iSLD
                self.__set_checked(self.tableWidget_Film_description.item(row, col + 5), ENTRY[index_reference+5].split()[0])
                if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl"]:
                    self.tableWidget_Film_description.item(row, col + 10).setText(ENTRY[index_reference + 6].split()[0].replace("d", "e"))  # roughness
                    self.__set_checked(self.tableWidget_Film_description.item(row, col + 11), ENTRY[index_reference + 7].split()[0])
                    index_reference += 8
                else:
                    self.tableWidget_Film_description.item(row, col + 6).setText(ENTRY[index_reference + 6].split()[0].replace("d", "e"))  # mSLD
                    self.__set_checked(self.tableWidget_Film_description.item(row, col + 7), ENTRY[index_reference+7].split()[0])
                    self.tableWidget_Film_description.item(row, col + 8).setText(ENTRY[index_reference + 8].split()[0].replace("d", "e"))  # cos(d-gamma)
                    self.__set_checked(self.tableWidget_Film_description.item(row, col + 9), ENTRY[index_reference+9].split()[0])
                    self.tableWidget_Film_description.item(row, col + 10).setText(ENTRY[index_reference + 10].split()[0].replace("d", "e"))  # roughness
                    self.__set_checked(self.tableWidget_Film_description.item(row, col + 11), ENTRY[index_reference+11].split()[0])
                    index_reference += 12
            else:
                self.tableWidget_Film_description.item(row, col + 2).setText(str(round(float(ENTRY[index_reference + 2].split()[0].replace("d", "e")), 5)))  # SLD
                self.__set_checked(self.tableWidget_Film_description.item(row, col + 3), ENTRY[index_reference + 3].split()[0])
                self.tableWidget_Film_description_2.item(row, col + 2).setText(str(round(float(ENTRY[index_reference + 4].split()[0].replace("d", "e")), 5)))  # SLD 1
                self.__set_checked(self.tableWidget_Film_description_2.item(row, col + 3), ENTRY[index_reference + 5].split()[0])
                self.tableWidget_Film_description.item(row, col + 4).setText(ENTRY[index_reference + 6].split()[0].replace("d", "e"))  # iSLD
                self.__set_checked(self.tableWidget_Film_description.item(row, col + 5), ENTRY[index_reference + 7].split()[0])
                self.tableWidget_Film_description_2.item(row, col + 4).setText(ENTRY[index_reference + 8].split()[0].replace("d", "e"))  # iSLD 2
                self.__set_checked(self.tableWidget_Film_description_2.item(row, col + 5), ENTRY[index_reference + 9].split()[0])
                self.tableWidget_Film_description.item(row, col + 6).setText(ENTRY[index_reference + 10].split()[0].replace("d", "e"))  # mSLD
                self.__set_checked(self.tableWidget_Film_description.item(row, col + 7), ENTRY[index_reference + 11].split()[0])
                self.tableWidget_Film_description_2.item(row, col + 6).setText(ENTRY[index_reference + 12].split()[0].replace("d", "e"))  # mSLD 2
                self.__set_checked(self.tableWidget_Film_description_2.item(row, col + 7), ENTRY[index_reference + 13].split()[0])
                self.tableWidget_Film_description.item(row, col + 8).setText(ENTRY[index_reference + 14].split()[0].replace("d", "e"))  # cos(d-gamma)
                self.__set_checked(self.tableWidget_Film_description.item(row, col + 9), ENTRY[index_reference + 15].split()[0])
                self.tableWidget_Film_description_2.item(row, col + 8).setText(ENTRY[index_reference + 16].split()[0].replace("d", "e"))  # cos(d-gamma) 2
                self.__set_checked(self.tableWidget_Film_description_2.item(row, col + 9), ENTRY[index_reference + 17].split()[0])
                self.tableWidget_Film_description.item(row, col + 10).setText(ENTRY[index_reference + 18].split()[0].replace("d", "e"))  # roughness
                self.__set_checked(self.tableWidget_Film_description.item(row, col + 11), ENTRY[index_reference + 19].split()[0])
                self.tableWidget_Film_description_2.item(row, col + 10).setText(ENTRY[index_reference + 20].split()[0].replace("d", "e"))  # roughness 2
                self.__set_checked(self.tableWidget_Film_description_2.item(row, col + 11), ENTRY[index_reference + 21].split()[0])
                index_reference += 22

        if self.BoToFit_mode in ["m_0_sl", "t_0_sl"]: # Solid-Liquid
            self.table_add_sl_layer()
            self.tableWidget_Film_description.item(0, 3).setText(str(float(SL_sld_offset)))

        if self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"]: # periodical multilayers
            self.lineEdit_Scan_parameters_Gradient_period.setText(ENTRY[index_reference].split()[0])    # Gradient Period (-1 < "grad"< 1)
            self.__set_checked(self.checkBox_Scan_parameters_Gradient_period, ENTRY[index_reference + 1].split()[0])
            self.lineEdit_Scan_parameters_Gradient_roughness.setText(ENTRY[index_reference + 2].split()[0])     # Gradient Roughness (DW)  (-1 < "grad"< 1)
            self.__set_checked(self.checkBox_Scan_parameters_Gradient_roughness, ENTRY[index_reference + 3].split()[0])
            self.lineEdit_Scan_parameters_Gradient_sld.setText(ENTRY[index_reference + 4].split()[0])       # Gradient SLD (Nb) (-1 < "grad"< 1)
            self.__set_checked(self.checkBox_Scan_parameters_Gradient_sld, ENTRY[index_reference + 5].split()[0])
            if not self.BoToFit_mode == "m_0_m":
                self.lineEdit_Scan_parameters_Gradient_msld.setText(ENTRY[index_reference + 6].split()[0])      # Gradient mSLD (Np) (-1 < "grad"< 1)
                self.__set_checked(self.checkBox_Scan_parameters_Gradient_msld, ENTRY[index_reference + 7].split()[0])
                index_reference += 8
            else: index_reference += 6

        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]:
            self.lineEdit_Scan_parameters_Cg.setText(ENTRY[index_reference].split()[0])     # cg: mean value <cos(gamma)> over big domains
            self.__set_checked(self.checkBox_Scan_parameters_Cg, ENTRY[index_reference + 1].split()[0])
            if self.BoToFit_mode not in ["m_2_f", "m_4_f"]:
                self.lineEdit_Scan_parameters_Sg.setText(ENTRY[index_reference + 2].split()[0])     # sg: mean value <sin(gamma)> over big domains
                self.__set_checked(self.checkBox_Scan_parameters_Sg, ENTRY[index_reference + 3].split()[0])
                self.lineEdit_Scan_parameters_Sg2.setText(ENTRY[index_reference + 4].split()[0])    # sg2: mean value <sin^2(gamma)> over big domains
                self.__set_checked(self.checkBox_Scan_parameters_Sg2, ENTRY[index_reference + 5].split()[0])
                index_reference += 6
            else:
                self.lineEdit_Scan_parameters_Sg.setText(ENTRY[index_reference + 2].split()[0])  # sg: mean value <sin(gamma)> over big domains
                self.__set_checked(self.checkBox_Scan_parameters_Sg, ENTRY[index_reference + 3].split()[0])
                self.lineEdit_Scan_parameters_Sg2.setText(ENTRY[index_reference + 4].split()[0])  # sg2: mean value <sin^2(gamma)> over big domains
                self.__set_checked(self.checkBox_Scan_parameters_Sg2, ENTRY[index_reference + 5].split()[0])
                self.lineEdit_Scan_parameters_Cg_2.setText(ENTRY[index_reference + 6].split()[0])  # cg 2
                self.__set_checked(self.checkBox_Scan_parameters_Cg_2, ENTRY[index_reference + 7].split()[0])
                self.lineEdit_Scan_parameters_Sg_2.setText(ENTRY[index_reference + 8].split()[0])  # sg 2
                self.__set_checked(self.checkBox_Scan_parameters_Sg_2, ENTRY[index_reference + 9].split()[0])
                self.lineEdit_Scan_parameters_Sg2_2.setText(ENTRY[index_reference + 10].split()[0])    # sg2 2
                self.__set_checked(self.checkBox_Scan_parameters_Sg2_2, ENTRY[index_reference + 11].split()[0])
                index_reference += 12

        if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]:
            self.lineEdit_Scan_parameters_Fraction_amount.setText(ENTRY[index_reference].split()[0]) # fraction amount
            self.__set_checked(self.checkBox_Scan_parameters_Fraction_amount, ENTRY[index_reference + 1].split()[0])
            index_reference += 2

        self.lineEdit_Scan_parameters_Scaling_factor.setText(ENTRY[index_reference].split()[0])     # ct  total scaling factor
        self.__set_checked(self.checkBox_Scan_parameters_Scaling_factor, ENTRY[index_reference + 1].split()[0])
        self.lineEdit_Scan_parameters_Crossover_overillumination.setText(ENTRY[index_reference + 2].split()[0])     # alpha_0 crossover angle overillumination (in mrad)
        self.__set_checked(self.checkBox_Scan_parameters_Crossover_overillumination, ENTRY[index_reference + 3].split()[0])
        self.lineEdit_Scan_parameters_Background.setText(ENTRY[index_reference + 4].split()[0])    # bgr 'background'
        self.__set_checked(self.checkBox_Scan_parameters_Background, ENTRY[index_reference + 5].split()[0])
        self.lineEdit_Scan_parameters_Zero_correction.setText(ENTRY[index_reference + 6].split()[0])   # correction of the detector 'zero' (in mrad)

        if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: self.importing = False

        self.draw_resolution_function()

    def create_entry_for_BoToFit(self):
        ''' BoToFit needs its own entry file, so we make one using data from the table '''
        ENTRY, self.ncap, self.nsub, self.nrep, self.nbuf = [], 0, 0, 0, 0

        # polarisation
        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]:
            ENTRY.append("0     Pix incident polarization (polariser)\nf\n" + self.lineEdit_Scan_parameters_Piy.text() + '    Piy\n' + self.__check_checked(self.checkBox_Scan_parameters_Piy) + "\n" + "0     Piz\nf\n\n")
            ENTRY.append("0     Pfx outgoing polarization (analyser)\nf\n" + self.lineEdit_Scan_parameters_Pfy.text() + '    Pfy\n' + self.__check_checked(self.checkBox_Scan_parameters_Pfy) + "\n" + "0     Pfz\nf\n\n")
        # wavelength / inc.angle
        if self.BoToFit_mode not in ["t_0", "t_2", "t_4", "t_0_sl"]: ENTRY.append(self.lineEdit_Scan_parameters_Wavelength.text() + '        wavelength (in Angstrem)\n')
        else: ENTRY.append(self.lineEdit_Scan_parameters_Wavelength.text() + '        incident angle (in mrad)\n')
        # other parameters (header)
        ENTRY.append(str(self.lineEdit_Number_of_points) + "        *nn number of experimental points in alpha (<1001)\n")
        ENTRY.append(self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function.text() + "        *j0 number of points for resolution function (odd) (<102)\n")
        ENTRY.append(self.lineEdit_Scan_parameters_Step_for_resolution_function.text() + "        step for resolution function (in mrad)\n")
        ENTRY.append(self.lineEdit_Scan_parameters_Sigma.text() + "        *sigma of resolution function (in mrad)\n\n")
        # number of layers
        if self.BoToFit_mode in ["m_0", "m_2", "m_4", "t_0", "t_2", "t_4", "m_0_f", "m_2_f", "m_4_f"]: ENTRY.append(str(self.tableWidget_Film_description.rowCount() - 1) + "        number of layers (excluding substrate) (<21)\n\n")
        elif self.BoToFit_mode in ["m_0_sl", "t_0_sl"]: ENTRY.append(str(self.tableWidget_Film_description.rowCount() - 2) + "        number of layers (excluding substrate_sl) (<21)\n\n")
        else:
            for row, span in enumerate([self.tableWidget_Film_description.rowSpan(row, 0) for row in range(0, self.tableWidget_Film_description.rowCount() - 1)]):
                if self.nsub == 0 and self.nrep == 0 and span == 1 and not "x" in self.tableWidget_Film_description.item(row, 0).text(): self.ncap += 1
                elif self.nsub == 0 and (span > 1 or "x" in self.tableWidget_Film_description.item(row, 0).text()):
                    self.nsub, self.nrep = span, int(self.tableWidget_Film_description.item(row, 0).text()[self.tableWidget_Film_description.item(row, 0).text().find("x") + 1:])
                elif self.nrep > 0 and span == 1: self.nbuf += 1
            ENTRY.append(str(self.ncap) + "        \"ncap\" number of cap layers\n")
            ENTRY.append(str(self.nsub) + "        \"nsub\" number of sub-layers in a superstructure\n")
            ENTRY.append(str(self.nrep) + "        \"nrep\" number of repetitions\n")
            ENTRY.append(str(self.nbuf) + "        \"nbuf\" number of buffer layers\n\n")
        # read the table
        for i in range(1 if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] else 0, self.tableWidget_Film_description.rowCount()):
            comment = ""
            # Thickness
            if not self.tableWidget_Film_description.item(i, 0).text() in ["Substrate", "Liquid"]:
                if self.BoToFit_mode in ["m_0", "m_2", "m_4", "t_0", "t_2", "t_4", "m_0_f", "m_2_f", "m_4_f"]: layer = str(i+1)
                elif self.BoToFit_mode in ["m_0_sl", "t_0_sl"]: layer = str(i)
                elif self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"]:
                    if i < self.ncap: layer = "Cap " + str(i+1)
                    elif i < self.ncap + self.nsub: layer = "Sub " + str(i+1-self.ncap)
                    elif i < self.ncap + self.nsub + self.nbuf: layer = "Buffer " + str(i+1-self.ncap-self.nsub)

                ENTRY.append(self.tableWidget_Film_description.item(i, 1).text() + "        layer " + layer + " - thickness (in A)\n" + self.__check_checked(self.tableWidget_Film_description.item(i, 2)) + "\n")
            else: comment = "substrate's"
            # SLD: In Solid-Liquid mode we subtract buffer SLD from all other SLD's.
            sld = self.tableWidget_Film_description.item(i, 3).text() if self.BoToFit_mode not in ["m_0_sl", "t_0_sl"] else str(str(float(self.tableWidget_Film_description.item(i, 3).text()) - float(self.tableWidget_Film_description.item(0, 3).text())) + " + " + self.tableWidget_Film_description.item(0, 3).text())
            ENTRY.append(sld + "        "+ comment + " nbr nuclear SLD Nb'  (in A**-2) *1e-6\n" + self.__check_checked(self.tableWidget_Film_description.item(i, 4)) + "\n")
            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]:
                ENTRY.append(self.tableWidget_Film_description_2.item(i, 3).text() + "        "+ comment + "    nbr2 nuclear SLD Nb'  (in A**-2) *1e-6\n" + self.__check_checked(self.tableWidget_Film_description_2.item(i, 4)) + "\n")
            # iSLD
            ENTRY.append(self.tableWidget_Film_description.item(i, 5).text() + "        " + comment + "    nbi nuclear SLD Nb'' (in A**-2) *1e-6\n" + self.__check_checked(self.tableWidget_Film_description.item(i, 6)) + "\n")
            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]:
                ENTRY.append(self.tableWidget_Film_description_2.item(i, 5).text() + "        "+ comment + "    nbi2 nuclear SLD Nb'' (in A**-2) *1e-6\n" + self.__check_checked(self.tableWidget_Film_description_2.item(i, 6)) + "\n")
            # mSLD, <cos(delta_gamma)>
            if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl"]:
                # mSLD
                ENTRY.append(self.tableWidget_Film_description.item(i, 7).text() + "        " + comment + "   Np magnetic SLD (in A**-2)*1e-6\n" + self.__check_checked(self.tableWidget_Film_description.item(i, 8)) + "\n")
                if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]:
                    ENTRY.append(self.tableWidget_Film_description_2.item(i, 7).text() + "        " + comment + "   Np2 magnetic SLD (in A**-2)*1e-6\n" + self.__check_checked(self.tableWidget_Film_description_2.item(i, 8)) + "\n")
                # <cos(delta_gamma)>
                ENTRY.append(self.tableWidget_Film_description.item(i, 9).text() + "        " + comment + "   c=<cos(delta_gamma)>\n" + self.__check_checked(self.tableWidget_Film_description.item(i, 10)) + "\n")
                if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]:
                    ENTRY.append(self.tableWidget_Film_description_2.item(i, 9).text() + "        " + comment + "   c2=<cos(delta_gamma)>\n" + self.__check_checked(self.tableWidget_Film_description_2.item(i, 10)) + "\n")
            # roughness
            ENTRY.append(self.tableWidget_Film_description.item(i, 11).text() + "        " + comment + "  dw Debye-Waller in [AA]\n" + self.__check_checked(self.tableWidget_Film_description.item(i, 12)) + "\n")
            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]:
                ENTRY.append(self.tableWidget_Film_description_2.item(i, 11).text() + "        " + comment + "  dw2 Debye-Waller in [AA]\n" + self.__check_checked(self.tableWidget_Film_description_2.item(i, 12)) + "\n\n")
            else: ENTRY.append("\n")
        # gradients
        if self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"]:
            ENTRY.append(self.lineEdit_Scan_parameters_Gradient_period.text() + '        Period gradient (-1 < "grad"< 1)\n' + self.__check_checked(self.checkBox_Scan_parameters_Gradient_period) + "\n")
            ENTRY.append(self.lineEdit_Scan_parameters_Gradient_roughness.text() + '        DW gradient (-1 < "grad"< 1)\n' + self.__check_checked(self.checkBox_Scan_parameters_Gradient_roughness) + "\n")
            ENTRY.append(self.lineEdit_Scan_parameters_Gradient_sld.text() + '        Nb gradient (-1 < "grad"< 1)\n' + self.__check_checked(self.checkBox_Scan_parameters_Gradient_sld) + "\n")
            ENTRY.append(self.lineEdit_Scan_parameters_Gradient_msld.text() + '        Np gradient (-1 < "grad"< 1)\n' + self.__check_checked(self.checkBox_Scan_parameters_Gradient_msld) + "\n\n" if not self.BoToFit_mode == "m_0_m" else "\n")
        # <cos(gamma)>, <sin(gamma)>, <sin^2(gamma)>
        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]:
            ENTRY.append(self.lineEdit_Scan_parameters_Cg.text() + '        cg: mean value <cos(gamma)> over big domains\n' + self.__check_checked(self.checkBox_Scan_parameters_Cg) + "\n")
            ENTRY.append(self.lineEdit_Scan_parameters_Sg.text() + '        sg: mean value <sin(gamma)> over big domains\n' + self.__check_checked(self.checkBox_Scan_parameters_Sg) + "\n")
            ENTRY.append(self.lineEdit_Scan_parameters_Sg2.text() + '        sg2: mean value <sin^2(gamma)> over big domains\n' + self.__check_checked(self.checkBox_Scan_parameters_Sg2) + "\n")
            if self.BoToFit_mode in ["m_2_f", "m_4_f"]:
                ENTRY.append(self.lineEdit_Scan_parameters_Cg_2.text() + '        cg_2: mean value <cos(gamma)> over big domains\n' + self.__check_checked(self.checkBox_Scan_parameters_Cg_2) + "\n")
                ENTRY.append(self.lineEdit_Scan_parameters_Sg_2.text() + '        sg_2: mean value <sin(gamma)> over big domains\n' + self.__check_checked(self.checkBox_Scan_parameters_Sg_2) + "\n")
                ENTRY.append(self.lineEdit_Scan_parameters_Sg2_2.text() + '        sg2_2: mean value <sin^2(gamma)> over big domains\n' + self.__check_checked(self.checkBox_Scan_parameters_Sg2_2) + "\n")
        # fraction amount
        if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]:
            ENTRY.append(self.lineEdit_Scan_parameters_Fraction_amount.text() + '        fraction of 1-st type of domains\n' + self.__check_checked(self.checkBox_Scan_parameters_Fraction_amount) + "\n\n")
        elif self.BoToFit_mode not in ["m_0_f", "m_0", "t_0"]: ENTRY.append("\n")
        # other parameters (footer)
        ENTRY.append(self.lineEdit_Scan_parameters_Scaling_factor.text() + "        *ct  total scaling factor\n" + self.__check_checked(self.checkBox_Scan_parameters_Scaling_factor) + "\n")
        ENTRY.append(self.lineEdit_Scan_parameters_Crossover_overillumination.text() + "        *alpha_0 crossover angle overillumination (in mrad)\n" + self.__check_checked(self.checkBox_Scan_parameters_Crossover_overillumination) + "\n")
        ENTRY.append(self.lineEdit_Scan_parameters_Background.text() + "        *bgr background\n" + self.__check_checked(self.checkBox_Scan_parameters_Background) + "\n")
        ENTRY.append("\n" + self.lineEdit_Scan_parameters_Zero_correction.text() + "        correction of the detector 'zero' (in mrad)")

        with open(self.DATA_FOLDER + 'boto.ent', 'w') as entry_file:
            for i in ENTRY:
                try:
                    _ = float(i.split()[0])
                except:
                    if not i in [" ", "\n"]: self.statusbar.showMessage("Error: recheck the field <" + i + "> for the proper input.")
                entry_file.write(i)

    def create_entry_for_BoToFit_from_fitbag(self, FITBAG):
        ''' You come here from "create_entry_for_multiGrPr" function. This is needed to create simulated reflectivity curve even when BoToFit crashed or has been stopped '''
        TEMP_ENTRY, self.ncap, self.nsub, self.nrep, self.nbuf = [], 0, 0, 0, 0

        # polarisation
        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]:
            TEMP_ENTRY.append("0     Pix incident polarization (polariser)\nf\n" + str(float(FITBAG[FITBAG["Name"] == "Pi(y)"]['Value'])) + "    Piy\nf\n" + "0     Piz\nf\n\n")
            TEMP_ENTRY.append("0     Pfx outgoing polarization (analyser)\nf\n" + str(float(FITBAG[FITBAG["Name"] == "Pf(y)"]['Value'])) + "    Pfy\nf\n" + "0     Pfz\nf\n\n")

        # wavelength / inc.angle
        if self.BoToFit_mode not in ["t_0", "t_2", "t_4", "t_0_sl"]: TEMP_ENTRY.append(self.lineEdit_Scan_parameters_Wavelength.text() + '    wavelength (in Angstrem)\n')
        else: TEMP_ENTRY.append(self.lineEdit_Scan_parameters_Wavelength.text() + '    incident angle (in mrad)\n')

        # other parameters (header)
        TEMP_ENTRY.append(str(self.lineEdit_Number_of_points) + "        *nn number of experimental points in alpha (<1001)\n")
        TEMP_ENTRY.append(self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function.text() + "        *j0 number of points for resolution function (odd) (<102)\n")
        TEMP_ENTRY.append(self.lineEdit_Scan_parameters_Step_for_resolution_function.text() + "        step for resolution function (in mrad)\n")
        TEMP_ENTRY.append(self.lineEdit_Scan_parameters_Sigma.text() + "        *sigma of resolution function (in mrad)\n\n")

        # number of layers
        if self.BoToFit_mode in ["m_0", "m_2", "m_4", "t_0", "t_2", "t_4", "m_0_f", "m_2_f", "m_4_f"]:
            TEMP_ENTRY.append(str(self.tableWidget_Film_description.rowCount() - 1) + "        number of layers (excluding substrate) (<21)\n\n")
        elif self.BoToFit_mode in ["m_0_sl", "t_0_sl"]:
            TEMP_ENTRY.append(str(self.tableWidget_Film_description.rowCount() - 2) + "        number of layers (excluding substrate_sl) (<21)\n\n")
        else:
            for row, span in enumerate([self.tableWidget_Film_description.rowSpan(row, 0) for row in range(0, self.tableWidget_Film_description.rowCount() - 1)]):
                if self.nsub == 0 and self.nrep == 0 and span == 1 and not "x" in self.tableWidget_Film_description.item(row, 0).text(): self.ncap += 1
                elif self.nsub == 0 and (span > 1 or "x" in self.tableWidget_Film_description.item(row, 0).text()):
                    self.nsub, self.nrep = span, int(self.tableWidget_Film_description.item(row, 0).text()[self.tableWidget_Film_description.item(row, 0).text().find("x") + 1:])
                elif self.nrep > 0 and span == 1: self.nbuf += 1
            TEMP_ENTRY.append(str(self.ncap) + "        \"ncap\" number of cap layers\n")
            TEMP_ENTRY.append(str(self.nsub) + "        \"nsub\" number of sub-layers in a superstructure\n")
            TEMP_ENTRY.append(str(self.nrep) + "        \"nrep\" number of repetitions\n")
            TEMP_ENTRY.append(str(self.nbuf) + "        \"nbuf\" number of buffer layers\n\n")

        # table
        for layer_number in range(0, self.tableWidget_Film_description.rowCount() - (1 if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] else 0)):
            comment = ""

            # Thickness
            if not layer_number == self.tableWidget_Film_description.rowCount() - (1 if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] else 0) - 1:
                if self.BoToFit_mode not in ["m_0_m", "m_2_m", "m_4_m"]: layer = str(layer_number + 1)
                else:
                    if layer_number < self.ncap: layer = "Cap " + str(layer_number + 1)
                    elif layer_number < self.ncap + self.nsub: layer = "Sub " + str(layer_number + 1 - self.ncap)
                    elif layer_number < self.ncap + self.nsub + self.nbuf: layer = "Buffer " + str(layer_number + 1 - self.ncap - self.nsub)

                TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "Thickness"].iloc[layer_number]['Value'])) + "        layer " + layer + " - thickness (in A)\nf\n")

            else: comment = "substrate's"

            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: iloc_index = layer_number * 2
            else: iloc_index = layer_number
            # SLD: In Solid-Liquid mode we subtract buffer SLD from all other SLD's.
            TEMP_ENTRY.append(str((float(FITBAG[FITBAG["Name"] == "SLD"].iloc[iloc_index]['Value']) * 1e6)) + (" + " + self.tableWidget_Film_description.item(0, 3).text() if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] else "") + "        " + comment + " nbr nuclear SLD Nb'  (in A**-2) *1e-6\nf\n")
            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "SLD"].iloc[iloc_index + 1]['Value']) * 1e6) + "        " + comment + "    nbr2 nuclear SLD Nb'  (in A**-2) *1e-6\nf\n")
            # iSLD
            TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "iSLD"].iloc[iloc_index]['Value']) * 1e6) + "        " + comment + "    nbi nuclear SLD Nb'' (in A**-2) *1e-6\nf\n")
            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "iSLD"].iloc[iloc_index + 1]['Value']) * 1e6) + "        " + comment + "    nbi2 nuclear SLD Nb'' (in A**-2) *1e-6\nf\n")
            # mSLD, <cos(delta_gamma)>
            if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl"]:
                # mSLD
                TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "mSLD"].iloc[iloc_index]['Value']) * 1e6) + "        " + comment + "   Np magnetic SLD (in A**-2)*1e-6\nf\n")
                if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "mSLD"].iloc[iloc_index + 1]['Value'])  * 1e6) + "        " + comment + "   Np2 magnetic SLD (in A**-2)*1e-6\nf\n")
                # <cos(delta_gamma)>
                TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "Cos(d-gamma)"].iloc[iloc_index]['Value'])) + "        " + comment + "   c=<cos(delta_gamma)>\nf\n")
                if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "Cos(d-gamma)"].iloc[iloc_index + 1]['Value'])) + "        " + comment + "   c2=<cos(delta_gamma)>\nf\n")
            # roughness
            TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "Roughness"].iloc[iloc_index]['Value'])) + "        " + comment + "  dw Debye-Waller in [AA]\nf\n")
            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "Roughness"].iloc[iloc_index + 1]['Value'])) + "        " + comment + "  dw2 Debye-Waller in [AA]\nf\n\n")
            else: TEMP_ENTRY.append("\n")

        # gradients
        if self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"]:
            TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "grad.Period"]['Value'])) + "        Period gradient (-1 < 'grad'< 1)\nf\n")
            TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "grad.Roughness"]['Value'])) + "        DW gradient (-1 < 'grad'< 1)\nf\n")
            TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "grad.SLD"]['Value'])) + "        Nb gradient (-1 < 'grad'< 1)\nf\n")
            TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "grad.mSLD"]['Value'])) + "        Np gradient (-1 < 'grad'< 1)\nf\n\n" if not self.BoToFit_mode == "m_0_m" else "\n")
        # <cos(gamma)>, <sin(gamma)>, <sin^2(gamma)>
        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]:
            TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "<cos(gamma)>"]['Value'])) + "        cg: mean value <cos(gamma)> over big domains\nf\n")
            TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "<sin(gamma)>"]['Value'])) + "        sg: mean value <sin(gamma)> over big domains\nf\n")
            TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "<sin2(gamma)>"]['Value'])) + "        sg2: mean value <sin^2(gamma)> over big domains\nf\n")
            if self.BoToFit_mode in ["m_2_f", "m_4_f"]:
                TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "<cos(gamma)>_F2"]['Value'])) + "        cg_2: mean value <cos(gamma)> over big domains\nf\n")
                TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "<sin(gamma)>_F2"]['Value'])) + "        sg_2: mean value <sin(gamma)> over big domains\nf\n")
                TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "<sin2(gamma)>_F2"]['Value'])) + "        sg2_2: mean value <sin^2(gamma)> over big domains\nf\n")
        # fraction amount
        if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: TEMP_ENTRY.append(self.lineEdit_Scan_parameters_Fraction_amount.text() + "        fraction of 1-st type of domains\nf\n\n")
        elif self.BoToFit_mode not in ["m_0_f", "m_0", "t_0"]: TEMP_ENTRY.append("\n")
        # other parameters (footer)
        TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "Scaling_factor"]['Value'])) + "        *ct  total scaling factor\nf\n")
        TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "Overillumination"]['Value'])) + "        *alpha_0 crossover angle overillumination (in mrad)\nf\n")
        TEMP_ENTRY.append(str(float(FITBAG[FITBAG["Name"] == "Background"]['Value'])) + "        *bgr background\nf\n")
        TEMP_ENTRY.append("\n" + self.lineEdit_Scan_parameters_Zero_correction.text() + "        correction of the detector 'zero' (in mrad)")

        if not os.path.exists(self.DATA_FOLDER + "temp/"): os.makedirs(self.DATA_FOLDER + "temp/")

        with open(self.DATA_FOLDER + 'temp/boto.ent', 'w') as entry_file:
            for i in TEMP_ENTRY: entry_file.write(i)
    ##<--

    ##--> "Results table" and "multiGrPr entry"
    def create_entry_for_multiGrPr(self, FITBAG_FILE, frac=False):
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
        non_inf_layers_index = [1 if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] else 0, self.tableWidget_Film_description.rowCount() - 1]
        for i in range(non_inf_layers_index[0] + 1, non_inf_layers_index[1]):
            multiGrPr_data.insert(5, [0, 0, 0, 0, 0, 0])
            multiGrPr_info.insert(5, ["Layer " + str(self.tableWidget_Film_description.rowCount() - i) + " thickness in (A)", "real part of nuclear SLD Nb'  (in A**-2) *1e-6",
                                      "imaginary part of nuclear SLD Nb'' (in A**-2) *1e-6", "magn. scatt. length density (SLD) Np (in A**-2) *1e-6", "c=<cos(delta_gamma)>_{over small domains}", "dw Debye-Waller in [AA]", "Gradient Period", "Gradient SLD", "Gradient mSLD", "Gradient Roughness"])

        # Step 2: reformat FitBag file and create Pandas dataframe "self.FITBAG_df"
        dict_replace = {"total scaling": "Scaling_factor", "alpha_0": "Overillumination", "Re{Nb1}": "SLD", "Re{Nb2}": "SLD", "Re{Nb}": "SLD", "Im{Nb1}": "iSLD", "Im{Nb2}": "iSLD", "Im{Nb}": "iSLD", "N_p1": "mSLD", "N_p2": "mSLD", "N_p": "mSLD",  "Debye-Waller1": "Roughness", "Debye-Waller2": "Roughness", "Debye-Waller": "Roughness", "background": "Background", "<Cos(delta_gamma": "Cos(d-gamma)", "<Cos(d_gamma)>":"Cos(d-gamma)", "<Cos(gamma)>":"<cos(gamma)>", "<Cos(gamma1)>":"<cos(gamma)>", "<Cos(gamma2)>":"<cos(gamma)>_F2", "<Sin(gamma)>":"<sin(gamma)>", "<Sin(gamma1)>":"<sin(gamma)>", "<Sin(gamma2)>":"<sin(gamma)>_F2", "<Sin^2(gamma)>":"<sin2(gamma)>", "<Sin^2(gamma1)>":"<sin2(gamma)>", "<Sin^2(gamma2)>":"<sin2(gamma)>_F2", "+/-": "", "on bound": "", "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%": "skip", "<grad>":"grad.Period", "<gradDw>":"grad.Roughness", "<gradDW>":"grad.Roughness", "<gradNb>":"grad.SLD", "<gradNp>":"grad.mSLD", "thickness":"Thickness", "<frac>":"[F1]_amount"}
        fitbag_data = []
        with open(FITBAG_FILE, "r") as fit_file:
            for line_number, line in reversed(list(enumerate(fit_file.readlines()))):
                for i in dict_replace.keys(): line = line.replace(i, dict_replace[i])

                line_arr = line.split()
                if len(line_arr) == 0 or line_arr[0] in ['skip', "sqrt(D):", "D=<Cos(gam)^2>-<Cos(gam)>^2:"]: continue

                fitbag_data.append(line_arr)
                if line.find(" iterate ") > 0: break

        self.FITBAG_df = pd.DataFrame(fitbag_data[::-1], columns=["Number", "Name", "Value", "Error", "Factor"]).fillna("None")
        
        # Step 3: fill multiGrPr_data
        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]:
            multiGrPr_data[0][1] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "Pi(y)"]['Value'])
            multiGrPr_data[1][1] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "Pf(y)"]['Value'])
        multiGrPr_data[2][0] = self.lineEdit_Scan_parameters_Wavelength.text()

        if self.BoToFit_mode not in ["m_0_m", "m_2_m", "m_4_m"]: multiGrPr_data[3][3] = non_inf_layers_index[1] - non_inf_layers_index[0]
        else: multiGrPr_data[3] = self.ncap, self.nsub, self.nrep, self.nbuf
        # layers
        for layer_number in range(0, non_inf_layers_index[1] - non_inf_layers_index[0]):
            multiGrPr_data[4 + layer_number][0] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "Thickness"].iloc[layer_number]['Value'])
            
            # by changing iloc_index we will create 2 different multiGrPr.ent for 2 FRACs
            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]: iloc_index = layer_number*2 + (1 if frac else 0)
            else: iloc_index = layer_number
            
            multiGrPr_data[4 + layer_number][1] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "SLD"].iloc[iloc_index]['Value']) * 1e+6 + (float(self.tableWidget_Film_description.item(0, 3).text()) if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] else 0)
            multiGrPr_data[4 + layer_number][2] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "iSLD"].iloc[iloc_index]['Value']) * 1e+6
            if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl"]:
                multiGrPr_data[4 + layer_number][3] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "mSLD"].iloc[iloc_index]['Value']) * 1e+6
                multiGrPr_data[4 + layer_number][4] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "Cos(d-gamma)"].iloc[iloc_index]['Value'])
            multiGrPr_data[4 + layer_number][5] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "Roughness"].iloc[iloc_index]['Value'])
        # gradients
        if self.BoToFit_mode in ["m_0_m", "m_2_m", "m_4_m"]:
            multiGrPr_data[-4][0] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "grad.Period"]['Value'])
            multiGrPr_data[-4][1] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "grad.SLD"]['Value'])
            if not self.BoToFit_mode == "m_0_m": multiGrPr_data[-3][2] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "grad.mSLD"]['Value'])
            multiGrPr_data[-4][3] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "grad.Roughness"]['Value'])
        # substrate
        iloc_index_substrate = (non_inf_layers_index[1] - non_inf_layers_index[0]) * (2 if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"] else 1)  + (1 if frac else 0)
        multiGrPr_data[-3][0] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "SLD"].iloc[iloc_index_substrate]['Value']) * 1e+6
        multiGrPr_data[-3][1] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "iSLD"].iloc[iloc_index_substrate]['Value']) * 1e+6
        if self.BoToFit_mode not in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl"]:
            multiGrPr_data[-3][2] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "mSLD"].iloc[iloc_index_substrate]['Value']) * 1e+6
            multiGrPr_data[-3][3] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "Cos(d-gamma)"].iloc[iloc_index_substrate]['Value'])
        multiGrPr_data[-3][4] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "Roughness"].iloc[iloc_index_substrate]['Value'])
        # estimate total thickness
        if self.BoToFit_mode not in ["m_0_m", "m_2_m", "m_4_m"]:
            for layer_number in range(0, non_inf_layers_index[1] - non_inf_layers_index[0]): multiGrPr_data[2][6] += float(self.FITBAG_df[self.FITBAG_df["Name"] == "Thickness"].iloc[layer_number]['Value'])
        else:
            for layer_number in range(0, non_inf_layers_index[1] - non_inf_layers_index[0]):
                multiGrPr_data[2][6] += float(self.FITBAG_df[self.FITBAG_df["Name"] == "Thickness"].iloc[layer_number]['Value'])
                if layer_number + 1 > self.ncap and layer_number < self.ncap + self.nsub:
                    multiGrPr_data[2][6] += float(self.FITBAG_df[self.FITBAG_df["Name"] == "Thickness"].iloc[layer_number]['Value']) * self.nrep

        if self.BoToFit_mode in ["m_2", "m_4", "t_2", "t_4", "m_2_m", "m_4_m", "m_2_f", "m_4_f"]:
            multiGrPr_data[-2][0] = float(self.FITBAG_df[self.FITBAG_df["Name"] == ("<cos(gamma)>_F2" if frac else "<cos(gamma)>")]['Value'])
            multiGrPr_data[-2][1] = float(self.FITBAG_df[self.FITBAG_df["Name"] == ("<sin(gamma)>_F2" if frac else "<sin(gamma)>")]['Value'])
            multiGrPr_data[-2][2] = float(self.FITBAG_df[self.FITBAG_df["Name"] == ("<sin2(gamma)>_F2" if frac else "<sin2(gamma)>")]['Value'])
        multiGrPr_data[-1][0] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "Scaling_factor"]['Value'])
        multiGrPr_data[-1][1] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "Overillumination"]['Value'])
        multiGrPr_data[-1][2] = float(self.FITBAG_df[self.FITBAG_df["Name"] == "Background"]['Value'])

        # Write file
        with open(self.DATA_FOLDER + ('multiGrPr.ent' if not frac else 'multiGrPr_2.ent'), 'w') as multiGrPr:
            for i in range(0, len(multiGrPr_data)):
                for j in range(0, len(multiGrPr_data[i])):
                    multiGrPr.write(str(round(float(multiGrPr_data[i][j]), 6)) + "     " + str(multiGrPr_info[i][j]) + "\n")
                multiGrPr.write("\n")

        if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"] and frac == False:
            self.create_entry_for_multiGrPr(FITBAG_FILE, frac=True)
        else:
            self.fill_Fit_results_table()

            if self.statusbar.currentMessage() == "BoToFit crashed or has been stopped by user. Anyway, consider using more reasonable 'Start fit' values.": self.create_entry_for_BoToFit_from_fitbag(self.FITBAG_df)

    def fill_Fit_results_table(self):
        if not self.FITBAG_df.__class__ == pd.core.frame.DataFrame: return
        # clear results_table before another fit
        for i in range(0, self.tableWidget_Fit_results.rowCount()): self.tableWidget_Fit_results.removeRow(0)

        self.lineEdit_Fit_results_Chi_square_Actual.setText(str(float(self.FITBAG_df[self.FITBAG_df["Number"] == "hi_sq.norm:"]["Name"])))
        self.lineEdit_Fit_results_Number_of_iterations.setText(str(int(self.FITBAG_df[self.FITBAG_df["Name"] == "iterate"]['Number'])))

        layer_name, counter_i, prefix_frac = "", 0, " "

        for row_df in self.FITBAG_df.iterrows():
            # define prefix & layer name for parameters
            if row_df[1]["Number"] in ["Layer", "Substrate", "hi_sq.norm:"] or row_df[1]["Name"] == "iterate":
                layer_name = ("(La" if row_df[1]["Number"] == "Layer" else "(Su") + (row_df[1]["Name"] if row_df[1]["Number"] == "Layer" else "") + ")"
                continue

            if not row_df[1]["Name"] in ['Thickness', 'SLD', 'iSLD', 'mSLD', 'Cos(d-gamma)', 'Roughness']: layer_name = ""

            if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"]:
                if row_df[1]["Name"] in ['SLD', 'iSLD', 'mSLD', 'Cos(d-gamma)', 'Roughness']: prefix_frac = "[F1] " if not prefix_frac == "[F1] " else "[F2] "
                else: prefix_frac = "    "

            # show fixed values
            if row_df[1]["Error"] == "fixed" and not self.checkBox_Show_fixed.isChecked(): continue

            # create table rows and set their properties
            self.tableWidget_Fit_results.insertRow(self.tableWidget_Fit_results.rowCount())
            self.tableWidget_Fit_results.setRowHeight(counter_i, 22)
            for j in range(0, 6):
                item = QtWidgets.QTableWidgetItem()
                if not j == 2: item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
                if j == 0:
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    item.setCheckState(QtCore.Qt.Unchecked)
                self.tableWidget_Fit_results.setItem(counter_i, j, item)

            # fill the row
            self.tableWidget_Fit_results.item(counter_i, 1).setText(str(counter_i + 1))
            self.tableWidget_Fit_results.item(counter_i, 2).setText(layer_name + (prefix_frac if row_df[1]["Name"] in ['SLD', 'iSLD', 'mSLD', 'Cos(d-gamma)', 'Roughness'] else " ") + str(row_df[1]["Name"]))
            self.tableWidget_Fit_results.item(counter_i, 3).setText(str(round(float(row_df[1]["Value"]) * (1e6 if row_df[1]["Name"] in ['SLD', 'iSLD', 'mSLD'] else 1) + (float(self.tableWidget_Film_description.item(0,3).text()) if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] and row_df[1]["Name"] == 'SLD' else 0), 8)))
            if row_df[1]["Error"] == "fixed": self.tableWidget_Fit_results.item(counter_i, 4).setText("fixed")
            elif not "infinite" in [row_df[1]["Value"], row_df[1]["Error"], row_df[1]["Factor"]]:
                self.tableWidget_Fit_results.item(counter_i, 4).setText(str(round(float(row_df[1]["Error"]) * (1e6 if row_df[1]["Name"] in ['SLD', 'iSLD', 'mSLD'] else 1), 8)))
                self.tableWidget_Fit_results.item(counter_i, 5).setText(str(round(float(row_df[1]["Factor"]), 8)))
            else: self.tableWidget_Fit_results.item(counter_i, 4).setText(str(row_df[1]["Error"]))

            counter_i += 1
    ##<--

    ##--> draw graphs
    def draw_reflectivity(self):
        ''' draw reflectivity in Angle vs. lg(I) scale using data from hidden table '''
        color = [0, 0, 0]

        if "ang(Qz)" in self.input_structure: self.label_Reflectivity_profile_and_Diff.setText("Reflectivity profile (I[              ] vs. Qz[Å**-1]) and Difference (Exper/Fit):")
        elif "ang(rad)" in self.input_structure: self.label_Reflectivity_profile_and_Diff.setText("Reflectivity profile (I[              ] vs. Angle[mrad]) and Difference (Exper/Fit):")

        self.graphicsView_Reflectivity_profile.getPlotItem().clear()

        for i in range(0, len(self.DATA_FILES_DATA)):
            data_angle, data_I, data_dI = self.DATA_FILES_DATA[i]

            # change color from black when 2 or 4 polarisations
            if self.BoToFit_mode in ["m_2", "t_2", "m_2_m", "m_2_f"] and i == 1: color = [255, 0, 0]
            elif self.BoToFit_mode in ["m_4", "t_4", "m_4_m", "m_4_f"]: color = [255, 0, 0] if i == 1 else ([0, 255, 0] if i == 2 else ([0, 0, 255] if i == 3 else [0, 0, 0]))

            # pyqtgraph can not rescale data in log scale, so we do it manually if needed
            plot_I, plot_angle, plot_dI_err_bottom, plot_dI_err_top = [], [], [], []

            for j in range(0, len(data_angle)):
                if float(data_I[j]) > 0:
                    plot_angle.append(float(data_angle[j]))
                    if self.comboBox_Reflectivity_profile_Scale.currentText() == "log":
                        plot_I.append(math.log10(float(data_I[j])))
                        plot_dI_err_top.append(abs(math.log10(float(data_I[j]) + float(data_dI[j])) - math.log10(float(data_I[j]))))

                        if float(data_I[j]) > float(data_dI[j]): plot_dI_err_bottom.append(math.log10(float(data_I[j])) - math.log10(float(data_I[j]) - float(data_dI[j])))
                        else: plot_dI_err_bottom.append(0)
                    else:
                        plot_I.append(float(data_I[j]))
                        plot_dI_err_top.append(float(data_dI[j]))
                        plot_dI_err_bottom.append(float(data_dI[j]))

            s1 = pg.ErrorBarItem(x=np.array(plot_angle[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1]), y=np.array(plot_I[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1]), top=np.array(plot_dI_err_top[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1]), bottom=np.array(plot_dI_err_bottom[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1]), pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
            self.graphicsView_Reflectivity_profile.addItem(s1)

            s2 = pg.ScatterPlotItem(x=plot_angle[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1], y=plot_I[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1], symbol="o", size=2, pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
            self.graphicsView_Reflectivity_profile.addItem(s2)

    def draw_and_export_reform_FitFunct(self):
        ''' draw BoToFit final fit function on top of the graph with experimental points '''

        if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]: fit_funct_files = [["FitFunct.dat", [0, 0, 0]], []]
        elif self.BoToFit_mode in ["m_2", "t_2", "m_2_m", "m_2_f"]: fit_funct_files = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]]]
        elif self.BoToFit_mode in ["m_4", "t_4", "m_4_m", "m_4_f"]: fit_funct_files = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]], ["Fit2DFunctUD.dat", [0, 255, 0]], ["Fit2DFunctDU.dat", [0, 0, 255]]]

        for file in fit_funct_files:
            plot_I, plot_angle = [], []

            # check if we have file to work with
            try:
                if fit_funct_files[0][0] not in os.listdir(self.DATA_FOLDER) or file == []: return
            except FileNotFoundError: return

            with open(self.DATA_FOLDER + file[0], 'r') as fit_funct_file:
                for line in fit_funct_file.readlines():
                    try:
                        if str(line.split()[1]) == "-Infinity": continue

                        if self.comboBox_Reflectivity_profile_Scale.currentText() == "log": plot_I.append(math.log10(float(line.split()[1])))
                        else: plot_I.append(float(line.split()[1]))

                        if self.BoToFit_mode in ["t_0", "t_2", "t_4", "t_0_sl"]: plot_angle.append(float(line.split()[0]))
                        else: plot_angle.append(self.angle_convert("rad", "Qz", float(line.split()[0])) if "ang(Qz)" in self.input_structure else float(line.split()[0]))
                    except: True

                s3 = pg.PlotDataItem(plot_angle, plot_I, pen = pg.mkPen(color=(file[1][0], file[1][1], file[1][2]), width=2))
                self.graphicsView_Reflectivity_profile.addItem(s3)

    def draw_sld(self):
        ''' draw SLD profiles, calculated in multiGrPr.exe '''

        self.graphicsView_Sld_profile.getPlotItem().clear()

        for index, SLD_profile in enumerate(['SLD_profile.dat', 'SLD_profile_F2.dat'] if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"] else ['SLD_profile.dat']):
            dist, sld_1, sld_2 = [], [], []
            points, cut_1_l, cut_2_l, cut_1_r, cut_2_r = -1, [-1, -1], [-1, -1], [-1, -1], [-1, -1]

            with open(self.DATA_FOLDER + SLD_profile, 'r') as sld_file:
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
                self.graphicsView_Sld_profile.addItem(s4)

                s5 = pg.PlotDataItem(dist[left_lim:right_lim], sld_2[left_lim:right_lim], pen=pg.mkPen(color=(0,0,0), width=2, style=(QtCore.Qt.SolidLine if SLD_profile == 'SLD_profile.dat' else QtCore.Qt.DashLine)))
                self.graphicsView_Sld_profile.addItem(s5)

    def draw_diff(self):
        '''
        Here I compare experimental points with fitting curves
        polarisation order in self.DATA_FILES_DATA = [UU, (DD), (UD), DU]
        '''

        self.graphicsView_Diff.getPlotItem().clear()

        if self.BoToFit_mode in ["m_0", "t_0", "m_0_m", "m_0_sl", "t_0_sl", "m_0_f"]: fit_funct_files = [["FitFunct.dat", [0, 0, 0]], []]
        elif self.BoToFit_mode in ["m_2", "t_2", "m_2_m", "m_2_f"]: fit_funct_files = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]]]
        elif self.BoToFit_mode in ["m_4", "t_4", "m_4_m", "m_4_f"]: fit_funct_files = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]], ["Fit2DFunctUD.dat", [0, 255, 0]], ["Fit2DFunctDU.dat", [0, 0, 255]]]

        for i, file in enumerate(fit_funct_files):
            fit_funct_I, fit_funct_angle, diff_I, scale_angle, zero_I = [], [], [], [], []

            if file == []: return

            with open(self.DATA_FOLDER + file[0], 'r') as fit_funct_file:
                for line in fit_funct_file.readlines():
                    if line.split()[1] == "-Infinity": continue

                    try:
                        if self.BoToFit_mode in ["t_0", "t_2", "t_4", "t_0_sl"]: fit_funct_angle.append((float(line.split()[0])))
                        else:
                            if "ang(rad)" in self.input_structure:
                                fit_funct_angle.append((float(line.split()[0])))
                            else: fit_funct_angle.append((4 * math.pi / float(self.lineEdit_Scan_parameters_Wavelength.text())) * math.sin(float(line.split()[0])))
                        fit_funct_I.append(float(line.split()[1]))
                    except: True

                s = InterpolatedUnivariateSpline(np.array(fit_funct_angle), np.array(fit_funct_I), k=1)

            scale_angle = self.DATA_FILES_DATA[i][0][int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()) : -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text())-1]
            data_I = self.DATA_FILES_DATA[i][1][int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()) : -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text())-1]

            for i in range(0, len(scale_angle)):
                if data_I[i] != 0: diff_I.append(data_I[i] / s(scale_angle[i]))
                else: zero_I.append(i)

            s6 = pg.PlotDataItem(np.delete(scale_angle, zero_I), diff_I, pen = pg.mkPen(color=(file[1][0], file[1][1], file[1][2]), width=2))
            self.graphicsView_Diff.addItem(s6)

    def draw_resolution_function(self):
        if self.sender().text() == "Show resolution function view":
            self.graphicsView_Resolution_function.setGeometry(QtCore.QRect(300, -10, 380, 150))
            self.pushButton_Resolution_function_Show.setText("Hide resolution function view")
        elif self.sender().text() == "Hide resolution function view":
            self.graphicsView_Resolution_function.setGeometry(QtCore.QRect(0, 0, 0, 0))
            self.pushButton_Resolution_function_Show.setText("Show resolution function view")

        scaler, collX, collY = 0, [], []
        self.graphicsView_Resolution_function.getPlotItem().clear()

        # Credits for resolution function calculation: Anton Devishvili
        for i in range(0, int(self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function.text()) + 2):
            x = float(self.lineEdit_Scan_parameters_Step_for_resolution_function.text()) * (i - (float(self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function.text()) + 1) / 2)
            y = np.exp(-((x / float(self.lineEdit_Scan_parameters_Sigma.text()))**2) / 2)
            if i in [0, int(self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function.text()) + 1]: y = 0
            scaler += y

            collX.append(x)
            collY.append(y)

        collY = collY / scaler

        srf = pg.PlotDataItem(collX, collY, pen=pg.mkPen(color=(255, 0, 0), width=2))
        self.graphicsView_Resolution_function.addItem(srf)
    ##<--

    ##--> extra functions to shorten the code
    def clear_stuff(self, graphs=True, fit_res=True, chi_prev=True):
        if graphs:
            for item in (self.graphicsView_Reflectivity_profile.getPlotItem(), self.graphicsView_Sld_profile.getPlotItem(), self.graphicsView_Diff.getPlotItem()): item.clear()

        if fit_res:
            for item in (self.lineEdit_Fit_results_Number_of_iterations, self.lineEdit_Fit_results_Chi_square_Actual): item.clear()
            for i in range(0, self.tableWidget_Fit_results.rowCount()): self.tableWidget_Fit_results.removeRow(0)

        if chi_prev: self.lineEdit_Fit_results_Chi_square_Previous.clear()

    def angle_convert(self, input_unit, output_unit, input_value):
        if output_unit == "Qz": output_value = float(input_value) if input_unit == "Qz" else (4 * math.pi / float(self.lineEdit_Scan_parameters_Wavelength.text())) * math.sin(float(input_value))
        elif output_unit == "rad": output_value = float(input_value) if input_unit == "rad" else math.asin(float(input_value) * float(self.lineEdit_Scan_parameters_Wavelength.text()) / (4 * math.pi))

        return output_value

    def fit_results_select_all(self):
        for i in range(0, self.tableWidget_Fit_results.rowCount()):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Checked if self.checkBox_Fit_results_Select_all.isChecked() else QtCore.Qt.Unchecked)
            self.tableWidget_Fit_results.setItem(i, 0, item)

    def BoToFit_calc_run(self, data_folder, thread, module, entry, data, pts_to_skip_left, pts_to_skip_right):
        if thread == 0:
            '''
            define that BoToFit is done by checking the folder for "self.MODE_SPECS[self.BoToFit_mode][1]"
            '''

            # check every second if BoToFit is done
            while self.MODE_SPECS[self.BoToFit_mode][1] not in os.listdir(data_folder):
                QtTest.QTest.qWait(1000)

                # check if BoToFit crashed
                proc_list = []
                for proc in psutil.process_iter(): proc_list.append(proc.name())
                if self.MODE_SPECS[self.BoToFit_mode][0] not in proc_list: return

            # wait 5 sec more to make sure that FitFunct file is ready
            QtTest.QTest.qWait(5000)

            # when its done, kill BoToFit process
            for proc in psutil.process_iter():
                if proc.name() == self.MODE_SPECS[self.BoToFit_mode][0]:
                    proc.kill()
        else:
            communicate_string = str(entry) + '\r\n' + str(data) + '\r\n' + str(pts_to_skip_left) + '\r\n' + str(pts_to_skip_right) + '\r\n'
            file = subprocess.Popen(str(module), stdin=subprocess.PIPE, cwd=data_folder)
            file.communicate(input=bytes(communicate_string, 'utf-8'))

    def multyGrPr_run(self):
        # run multiGrPr.exe (twice for FRAC modules)
        # multiGrPr.exe can process only the 'multiGrPr.ent' file. So when we have 2 FRACtions, we do some renaiming
        for index in range(2 if self.BoToFit_mode in ["m_0_f", "m_2_f", "m_4_f"] else 1):
            if index == 1:
                for i, f in zip(['SLD_profile.dat', 'multiGrPr.ent', 'multiGrPr_2.ent'], ['SLD_profile_F1.dat', 'multiGrPr_F1.ent', 'multiGrPr.ent']):
                    try:
                        os.rename(self.DATA_FOLDER + i, self.DATA_FOLDER + f)
                    except: True

            subprocess.Popen(str(self.current_dir + '/BoToFit_Modules/multiGrPr.exe'), cwd=str(self.DATA_FOLDER))

            # run multiGrPr and wait until it finished to work
            while "SLD_profile.dat" not in os.listdir(self.DATA_FOLDER): QtTest.QTest.qWait(1000)
            while os.path.getsize(self.DATA_FOLDER + 'SLD_profile.dat') < 1: QtTest.QTest.qWait(1000)

            # SLD needs correction for Solid-Liquid mode
            if self.BoToFit_mode in ["m_0_sl", "t_0_sl"]:
                with open(self.DATA_FOLDER + "SLD_profile.dat", "r") as SLD_file_original: SLD = SLD_file_original.readlines()
                with open(self.DATA_FOLDER + "SLD_profile.dat", "w") as SLD_file_new:
                    for i in SLD:
                        dist, sld1, sld2 = i.replace("-", "D-").replace("D", "E").replace("EE", "E").replace(" E", " ").split()
                        SLD_file_new.write(dist + " " + str(float(sld1) + float(self.tableWidget_Film_description.item(0, 3).text())) + " " + str(float(sld2) + float(self.tableWidget_Film_description.item(0, 3).text())) + "\n")

            if index == 1:
                for i, f in zip(['SLD_profile.dat', 'multiGrPr.ent', 'SLD_profile_F1.dat', 'multiGrPr_F1.ent'],
                                ['SLD_profile_F2.dat', 'multiGrPr_F2.ent', 'SLD_profile.dat', 'multiGrPr.ent']):
                    try:
                        os.rename(self.DATA_FOLDER + i, self.DATA_FOLDER + f)
                    except: True

                for SLD_multigrpr_file in ['SLD_profile_F1.dat', 'SLD_profile_F1.dat', 'multiGrPr_2.ent', 'multiGrPr_F1.ent']:
                    try:
                        os.remove(self.DATA_FOLDER + SLD_multigrpr_file)
                    except: True
    
    def table_add_sl_layer(self):
        if self.BoToFit_mode in ["m_0_sl", "t_0_sl"] and not self.tableWidget_Film_description.item(0, 0).text() == "Substrate (Solid)":
            self.buttons_add_remove_layer()

            column_names = ["Substrate (Solid)", "inf", "", "0", "", "-", "", "", "", "", "", "-", ""]
            for i in range(0, 13):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                if not i == 3: item.setFlags(QtCore.Qt.NoItemFlags)
                self.tableWidget_Film_description.setItem(0, i, item)
                self.tableWidget_Film_description.item(0, i).setText(column_names[i])

            self.tableWidget_Film_description.item(self.tableWidget_Film_description.rowCount() - 1, 0).setText("Liquid")

        elif self.BoToFit_mode not in ["m_0_sl", "t_0_sl"] and self.tableWidget_Film_description.item(self.tableWidget_Film_description.rowCount() - 1, 0).text() == "Liquid":
            self.tableWidget_Film_description.item(self.tableWidget_Film_description.rowCount() - 1, 0).setText("Substrate")
            if self.tableWidget_Film_description.item(0, 0).text() == "Substrate (Solid)" and self.tableWidget_Film_description.item(0, 1).text() == "inf":
                self.tableWidget_Film_description.removeRow(0)

    def synchronize_frac_thickness(self):
        # this function is used only for FRAC
        if self.BoToFit_mode not in ["m_0_f", "m_2_f", "m_4_f"] or self.importing: return

        for index, value in enumerate([self.tableWidget_Film_description.item(row, 1).text() for row in range(self.tableWidget_Film_description.rowCount()-1)]):
            self.tableWidget_Film_description_2.item(index, 1).setText(value)
            self.tableWidget_Film_description_2.item(index, 2).setCheckState(0 if self.tableWidget_Film_description.item(index, 2).checkState() == 0 else 2)

    def __set_checked(self, parameter, checked):
        parameter.setCheckState(0 if checked == "n" else 2)

    def __check_checked(self, parameter):
        checked = "n" if parameter.checkState() == 0 else "f"
        return checked

if __name__ == "__main__":
    import sys
    QtWidgets.QApplication.setStyle("Fusion")
    app = QtWidgets.QApplication(sys.argv)
    prog = GUI()
    prog.show()
    sys.exit(app.exec_())

