from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
import os, psutil, time, math, threading, subprocess
import pyqtgraph as pg
import numpy as np
import pandas as pd
from scipy.interpolate import InterpolatedUnivariateSpline

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Ui_MainWindow(QtGui.QMainWindow):

    def __create_element(self, object, geometry, object_name, text=None, font=None, placeholder=None, visible=None, stylesheet=None, checked=None, checkable=None, title=None, combo=None, enabled=None):


        object.setObjectName(object_name)

        if not geometry == [999, 999, 999, 999]:
            object.setGeometry(QtCore.QRect(geometry[0], geometry[1], geometry[2], geometry[3]))

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
        MainWindow_size = [1090, 751]
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(MainWindow_size[0], MainWindow_size[1])
        MainWindow.setMinimumSize(QtCore.QSize(MainWindow_size[0], MainWindow_size[1]))
        MainWindow.setMaximumSize(QtCore.QSize(MainWindow_size[0], MainWindow_size[1]))
        MainWindow.setFont(font_ee)
        MainWindow.setWindowIcon(QtGui.QIcon(self.current_dir + "\icon.png"))
        MainWindow.setIconSize(QtCore.QSize(30, 30))
        MainWindow.setWindowTitle("BoToFit")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Block: Data file and structure
        self.label_Data_file = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Data_file, [20, 0, 191, 16], "label_Data_file", text="Data file and structure:", font=font_headline)
        self.groupBox_Data_file = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_Data_file, [10, 0, 661, 50], "groupBox_Data_file", font=font_ee)
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

        # Block: Start fit with
        self.label_Start_fit_with = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Start_fit_with, [20, 50, 141, 16], "label_Start_fit_with", text="Start fit with:", font=font_headline)
        self.groupBox_Start_fit_with = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_Start_fit_with, [10, 50, 661, 289], "groupBox_Start_fit_with", font=font_ee)
        self.tabWidget_Start_fit_with = QtWidgets.QTabWidget(self.groupBox_Start_fit_with)
        self.__create_element(self.tabWidget_Start_fit_with, [1, 18, 660, 272], "tabWidget_Start_fit_with", font=font_ee)

        # - tab "Film description"
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
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_Film_description.setVerticalHeaderItem(0, item)
        column_names = ["name", "thickness", "", "SLD", "", "iSLD", "", "mSLD", "", "cos(d-gamma)", "", "roughness", ""]
        
        for i in range(0, 13):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget_Film_description.setHorizontalHeaderItem(i, item)
            self.tableWidget_Film_description.horizontalHeaderItem(i).setText(column_names[i])

        self.tableWidget_Film_description.verticalHeaderItem(0).setText("substrate")

        self.tableWidget_Film_description.horizontalHeaderItem(4).setFont(font_headline)

        column_names = ["substrate", "inf", "", "2.07", "", "0", "", "", "", "", "", "10", ""]
        for i in range(0, 13):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            if i in (0, 1, 2): item.setFlags(QtCore.Qt.NoItemFlags)
            if i in (4, 6, 8, 10, 12):
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
        self.__create_element(self.pushButton_Film_description_Load_entry, [1, 223, 111, 20], "pushButton_Film_description_Load_entry", text="Load entry file", font=font_ee)
        self.pushButton_Film_description_Add_layer = QtWidgets.QPushButton(self.tab_Film_description)
        self.__create_element(self.pushButton_Film_description_Add_layer, [491, 223, 80, 20], "pushButton_Film_description_Add_layer", text="Add layer", font=font_ee)
        self.pushButton_Film_description_Remove_layer = QtWidgets.QPushButton(self.tab_Film_description)
        self.__create_element(self.pushButton_Film_description_Remove_layer, [575, 223, 80, 20], "pushButton_Film_description_Remove_layer", text="Remove layer", font=font_ee)

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
        self.__create_element(self.label_Scan_parameters_Points_to_exclude_First, [8, 93, 191, 16], "label_Scan_parameters_Points_to_exclude_First", text="Number of first points to exclude")
        self.lineEdit_Scan_parameters_Points_to_exclude_First = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Points_to_exclude_First, [188, 93, 60, 17], "lineEdit_Scan_parameters_Points_to_exclude_First", text="5")
        self.label_Scan_parameters_Points_to_exclude_Last = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Points_to_exclude_Last, [8, 111, 191, 17], "label_Scan_parameters_Points_to_exclude_Last", text="Number of last points to exclude")
        self.lineEdit_Scan_parameters_Points_to_exclude_Last = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Points_to_exclude_Last, [188, 111, 60, 17], "lineEdit_Scan_parameters_Points_to_exclude_Last", text="5")
        self.pushButton_Scan_parameters_Redraw_reflectivity = QtWidgets.QPushButton(self.tab_Scan_parameters)
        self.__create_element(self.pushButton_Scan_parameters_Redraw_reflectivity, [256, 93, 121, 34], "pushButton_Scan_parameters_Redraw_reflectivity", text="Redraw reflectivity")

        self.label_Scan_parameters_Piy = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Piy, [8, 144, 291, 17], "label_Scan_parameters_Piy", text="Piy incident polarization (polariser)", font=font_ee)
        self.lineEdit_Scan_parameters_Piy = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Piy, [268, 144, 60, 17], "lineEdit_Scan_parameters_Piy", font=font_ee)
        self.checkBox_Scan_parameters_Piy = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Piy, [332, 144, 21, 18], "checkBox_Scan_parameters_Piy")
        self.label_Scan_parameters_Pfy = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Pfy, [8, 162, 251, 17], "label_Scan_parameters_Pfy", text="Pfy outgoing polarization (analyser)", font=font_ee)
        self.lineEdit_Scan_parameters_Pfy = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Pfy, [268, 162, 60, 17], "lineEdit_Scan_parameters_Pfy", font=font_ee)
        self.checkBox_Scan_parameters_Pfy = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Pfy, [332, 162, 21, 18], "checkBox_Scan_parameters_Pfy")
        self.label_Scan_parameters_Cg = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Cg, [8, 180, 291, 17], "label_Scan_parameters_Cg", text="cg: mean value <cos(gamma)> of big domains", font=font_ee)
        self.lineEdit_Scan_parameters_Cg = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Cg, [268, 180, 60, 17], "lineEdit_Scan_parameters_Cg", font=font_ee)
        self.checkBox_Scan_parameters_Cg = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Cg, [332, 180, 21, 18], "checkBox_Scan_parameters_Cg")
        self.label_Scan_parameters_Sg = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Sg, [8, 198, 291, 17], "label_Scan_parameters_Sg", text="sg: mean value <sin(gamma)> of big domains", font=font_ee)
        self.lineEdit_Scan_parameters_Sg = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Sg, [268, 198, 60, 17], "lineEdit_Scan_parameters_Sg", font=font_ee)
        self.checkBox_Scan_parameters_Sg = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Sg, [332, 198, 21, 18], "checkBox_Scan_parameters_Sg")
        self.label_Scan_parameters_Sg2 = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.__create_element(self.label_Scan_parameters_Sg2, [8, 216, 291, 17], "label_Scan_parameters_Sg2", text="sg2: mean value <sin^2(gamma)> of big domains", font=font_ee)
        self.lineEdit_Scan_parameters_Sg2 = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Scan_parameters_Sg2, [268, 216, 60, 17], "lineEdit_Scan_parameters_Sg2", font=font_ee)
        self.checkBox_Scan_parameters_Sg2 = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.__create_element(self.checkBox_Scan_parameters_Sg2, [332, 216, 21, 18], "checkBox_Scan_parameters_Sg2")

        self.tabWidget_Start_fit_with.setCurrentIndex(0)

        # Block: Save results at
        self.label_Save_at = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Save_at, [20, 340, 151, 16], "label_Save_at", text="Save results at:", font=font_headline)
        self.groupBox_Save_at = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_Save_at, [10, 340, 531, 50], "groupBox_Save_at", font=font_ee)
        self.lineEdit_Save_at = QtWidgets.QLineEdit(self.groupBox_Save_at)
        self.__create_element(self.lineEdit_Save_at, [5, 23, 491, 21], "lineEdit_Save_at", font=font_ee)
        self.toolButton_Save_at = QtWidgets.QToolButton(self.groupBox_Save_at)
        self.__create_element(self.toolButton_Save_at, [500, 23, 26, 21], "toolButton_Save_at", text="...", font=font_ee)

        # Button: Start fitting
        self.pushButton_Start_fitting = QtWidgets.QPushButton(self.centralwidget)
        self.__create_element(self.pushButton_Start_fitting, [550, 358, 121, 32], "pushButton_Start_fitting", text="Start Fitting", font=font_headline)

        # Block: Fit results
        self.label_Fit_results = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Fit_results, [690, 0, 101, 16], "label_Fit_results", text="Fit results:", font=font_headline)
        self.label_Fit_results.setFont(font_headline)
        self.label_Fit_results.setGeometry(QtCore.QRect(690, 0, 101, 16))
        self.label_Fit_results.setObjectName("label_Fit_results")
        self.label_Fit_results.setText("Fit results:")
        self.groupBox_Fit_results = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_Fit_results, [680, 0, 401, 390], "groupBox_Fit_results", font=font_headline)
        self.groupBox_Fit_results.setGeometry(QtCore.QRect(680, 0, 401, 390))
        self.groupBox_Fit_results.setObjectName("groupBox_Fit_results")
        self.tableWidget_Fit_results = QtWidgets.QTableWidget(self.groupBox_Fit_results)
        self.__create_element(self.tableWidget_Fit_results, [1, 48, 400, 318], "tableWidget_Fit_results", font=font_ee)
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
        column_widths = [15, 20, 100, 78, 78, 78]
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
        self.__create_element(self.label_Fit_results_Number_of_iterations, [10, 18, 161, 31], "label_Fit_results_Number_of_iterations", text="Number of iterations:", font=font_ee)
        self.lineEdit_Fit_results_Number_of_iterations = QtWidgets.QLineEdit(self.groupBox_Fit_results)
        self.__create_element(self.lineEdit_Fit_results_Number_of_iterations, [120, 23, 40, 21], "lineEdit_Fit_results_Number_of_iterations", font=font_ee)
        self.lineEdit_Fit_results_Number_of_iterations.setReadOnly(True)
        self.label_Fit_results_Chi_square = QtWidgets.QLabel(self.groupBox_Fit_results)
        self.__create_element(self.label_Fit_results_Chi_square, [255, 18, 151, 31], "label_Fit_results_Chi_square", text="Chi_sq.norm:", font=font_ee)
        self.lineEdit_Fit_results_Chi_square = QtWidgets.QLineEdit(self.groupBox_Fit_results)
        self.__create_element(self.lineEdit_Fit_results_Chi_square, [326, 23, 70, 21], "lineEdit_Fit_results_Chi_square", font=font_ee)
        self.lineEdit_Fit_results_Chi_square.setReadOnly(True)
        self.pushButton_Fit_results_Copy_to_Start_fit_with = QtWidgets.QPushButton(self.groupBox_Fit_results)
        self.__create_element(self.pushButton_Fit_results_Copy_to_Start_fit_with, [5, 368, 392, 19], "pushButton_Fit_results_Copy_to_Start_fit_with", text="Use selected (#) values as 'Start fit with' parameters", font=font_ee)

        # Block: Reflectivity profile and Difference
        self.label_Reflectivity_profile_and_Diff = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Reflectivity_profile_and_Diff, [20, 393, 541, 16], "label_Reflectivity_profile_and_Diff", text="Reflectivity profile (I[10e] vs. Qz[Å**-1]) and Difference (Exper/Fit):", font=font_headline)
        self.groupBox_Reflectivity_profile = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_Reflectivity_profile, [10, 393, 660, 316], "groupBox_Reflectivity_profile")
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
        self.graphicsView_Diff = pg.PlotWidget(self.groupBox_Reflectivity_profile, viewBox=pg.ViewBox())
        self.__create_element(self.graphicsView_Diff, [2, 224, 657, 91], "graphicsView_Diff")
        self.graphicsView_Diff.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_Diff.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_Diff.getAxis("left").tickFont = font_graphs
        self.graphicsView_Diff.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_Diff.showAxis("top")
        self.graphicsView_Diff.getAxis("top").setTicks([])
        self.graphicsView_Diff.showAxis("right")
        self.graphicsView_Diff.getAxis("right").setTicks([])
        self.graphicsView_Diff.getViewBox().setXLink(self.graphicsView_Reflectivity_profile)

        # Block: SLD profile
        self.label_Sld_profile = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Sld_profile, [690, 393, 481, 16], "label_Sld_profile", text="SLD profile (SLD [in Å**-2, *10e6] vs. Distance from interface [Å]:", font=font_headline)
        self.groupBox_Sld_profile = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_Sld_profile, [680, 393, 401, 316], "groupBox_Sld_profile")
        MainWindow.setCentralWidget(self.centralwidget)
        self.graphicsView_Sld_profile = pg.PlotWidget(self.groupBox_Sld_profile)
        self.__create_element(self.graphicsView_Sld_profile, [2, 19, 398, 296], "graphicsView_Sld_profile")
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
        self.__create_element(self.actionVersion, [999, 999, 999, 999], "actionVersion", text="V1.2")
        self.menuHelp.addAction(self.actionVersion)
        MainWindow.setMenuBar(self.menuBar)
        self.menu_Mono = QtWidgets.QMenu(self.menu_MenuBar)
        self.__create_element(self.menu_Mono, [999, 999, 999, 999], "menu_Mono", title="Mono")
        self.menu_MenuBar.addAction(self.menu_Mono.menuAction())
        self.menu_Tof = QtWidgets.QMenu(self.menu_MenuBar)
        self.__create_element(self.menu_Tof, [999, 999, 999, 999], "menu_Tof", title="No TOF")
        self.menu_MenuBar.addAction(self.menu_Tof.menuAction())
        self.action_Mono_No_polarisation = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_No_polarisation, [999, 999, 999, 999], "action_Mono_No_polarisation", checked=True, checkable=True, text="No polarisation") # Mode 0
        self.menu_Mono.addAction(self.action_Mono_No_polarisation)
        self.action_Mono_No_polarisation_multi = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_No_polarisation_multi, [999, 999, 999, 999], "action_Mono_No_polarisation_multi", checked=True, checkable=True, enabled=False, text="No polarisation (Multi)") # Mode 6
        self.menu_Mono.addAction(self.action_Mono_No_polarisation_multi)
        self.action_Mono_2_polarisations = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_2_polarisations, [999, 999, 999, 999], "action_Mono_2_polarisations", checked=True, checkable=True, text="2 polarisation") # Mode 1
        self.menu_Mono.addAction(self.action_Mono_2_polarisations)
        self.action_Mono_2_polarisations_multi = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_2_polarisations_multi, [999, 999, 999, 999], "action_Mono_2_polarisations_multi", checked=True, checkable=True, enabled=False, text="2 polarisation (Multi)") # Mode 7
        self.menu_Mono.addAction(self.action_Mono_2_polarisations_multi)
        self.action_Mono_4_polarisations = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_4_polarisations, [999, 999, 999, 999], "action_Mono_4_polarisations", checked=True, checkable=True, text="4 polarisation") # Mode 2
        self.menu_Mono.addAction(self.action_Mono_4_polarisations)
        self.action_Mono_4_polarisations_multi = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Mono_4_polarisations_multi, [999, 999, 999, 999], "action_Mono_4_polarisations_multi", checked=True, checkable=True, text="4 polarisation (Multi)") # Mode 8
        self.menu_Mono.addAction(self.action_Mono_4_polarisations_multi)
        self.action_Tof_No_polarisation = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Tof_No_polarisation, [999, 999, 999, 999], "action_Tof_No_polarisation", checked=True, checkable=True, text="No polarisation") # Mode 3
        self.menu_Tof.addAction(self.action_Tof_No_polarisation)
        self.action_Tof_2_polarisations = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Tof_2_polarisations, [999, 999, 999, 999], "action_Tof_2_polarisations", checked=True, checkable=True, text="2 polarisation") # Mode 4
        self.menu_Tof.addAction(self.action_Tof_2_polarisations)
        self.action_Tof_4_polarisations = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Tof_4_polarisations, [999, 999, 999, 999], "action_Tof_4_polarisations", checked=True, checkable=True, text="4 polarisation") # Mode 5
        self.menu_Tof.addAction(self.action_Tof_4_polarisations)

        # Statusbar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # lineEdit_Number_of_points and tableWidget_Data_points are hidden from the user. Used to avoid reopenning data file multiple times
        self.lineEdit_Number_of_points = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.__create_element(self.lineEdit_Number_of_points, [570, 290, 0, 0], "lineEdit_Number_of_points", enabled=False)

        self.tableWidget_Data_points = QtWidgets.QTableWidget(self.tab_Scan_parameters)
        self.__create_element(self.tableWidget_Data_points, [460, 200, 0, 0], "tableWidget_Data_points", enabled=False)
        self.tableWidget_Data_points.setColumnCount(3)
        self.tableWidget_Data_points.setRowCount(4)
        for i in range(0, 4):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_Data_points.setVerticalHeaderItem(i, item)
        for i in range(0, 3):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_Data_points.setHorizontalHeaderItem(i, item)
        self.tableWidget_Data_points.horizontalHeader().setVisible(False)
        self.tableWidget_Data_points.verticalHeader().setVisible(False)
        item = self.tableWidget_Data_points.horizontalHeaderItem(0)
        item.setText("Q")
        item = self.tableWidget_Data_points.horizontalHeaderItem(1)
        item.setText("I")
        item = self.tableWidget_Data_points.horizontalHeaderItem(2)
        item.setText("dI")

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

class GUI(Ui_MainWindow):

    current_dir = os.getcwd().replace("\\", "/") + "/"

    def __init__(self):

        super(GUI, self).__init__()
        self.setupUi(self)

        # structure of the data file
        self.input_structure = []

        # No polarisation by default
        self.program_mode()

        # Actions for buttons
        self.toolButton_Data_file.clicked.connect(self.button_Data_file)
        self.toolButton_Save_at.clicked.connect(self.button_Save_at)
        self.pushButton_Film_description_Add_layer.clicked.connect(self.buttons_add_remove_layer)
        self.pushButton_Film_description_Remove_layer.clicked.connect(self.buttons_add_remove_layer)
        self.pushButton_Start_fitting.clicked.connect(self.button_Start_fitting)
        self.pushButton_Scan_parameters_Redraw_reflectivity.clicked.connect(self.draw_reflectivity)
        self.pushButton_Fit_results_Copy_to_Start_fit_with.clicked.connect(self.button_copy_to_start_with)
        self.pushButton_Film_description_Load_entry.clicked.connect(self.load_entry_file)
        self.action_Mono_No_polarisation.triggered.connect(self.program_mode)
        self.action_Mono_2_polarisations.triggered.connect(self.program_mode)
        self.action_Mono_4_polarisations.triggered.connect(self.program_mode)
        self.action_Tof_No_polarisation.triggered.connect(self.program_mode)
        self.action_Tof_2_polarisations.triggered.connect(self.program_mode)
        self.action_Tof_4_polarisations.triggered.connect(self.program_mode)
        self.action_Mono_No_polarisation_multi.triggered.connect(self.program_mode)
        self.action_Mono_2_polarisations_multi.triggered.connect(self.program_mode)
        self.action_Mono_4_polarisations_multi.triggered.connect(self.program_mode)
        self.actionVersion.triggered.connect(self.menu_info)
        self.checkBox_Fit_results_Select_all.clicked.connect(self.fit_results_Select_all)
        #
        self.lineEdit_Save_at.setPlaceholderText("default [" + str(self.current_dir) + "]")

    ##--> redefine user interface elements if TOF/Mono is selected and if polarisation is needed
    def program_mode(self):

        # check where we came from and change the interface accordingly
        # select mono_nopol by default
        try:
            action_mode = self.sender().objectName()
        except:
            action_mode = "action_Mono_No_polarisation"

        # program name, file to wait, default entry
        self.MODE_SPECS = [ ["Film500x0.exe", "FitFunct.dat", "UserDefaults_nopol.dat"],
                            ["Film500x2.exe", "Fit2DFunctDD.dat", "UserDefaults_2pol.dat"],
                            ["Film500x4.exe", "Fit2DFunctDD.dat", "UserDefaults_4pol.dat"],
                            ["FilmTOF500QX0.exe", "FitFunct.dat", "UserDefaults_TOF_nopol.dat"],
                            ["FilmTOF500QX2.exe", "Fit2DFunctDD.dat", "UserDefaults_TOF_2pol.dat"],
                            ["FilmTOF500QX4.exe", "Fit2DFunctDD.dat", "UserDefaults_TOF_4pol.dat"],
                            ["XXXXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXXXX"],
                            ["XXXXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXXXX"],
                            ["Mult500x4d4Gr.exe", "Fit2DFunctDD.dat", "UserDefaults_4pol_multi.dat"]]

        MODES = [self.action_Mono_No_polarisation, self.action_Mono_2_polarisations, self.action_Mono_4_polarisations, self.action_Tof_No_polarisation, self.action_Tof_2_polarisations, self.action_Tof_4_polarisations,
                 self.action_Mono_No_polarisation_multi, self.action_Mono_2_polarisations_multi, self.action_Mono_4_polarisations_multi]

        if action_mode == "action_Mono_No_polarisation": self.BoToFit_mode = 0
        elif action_mode == "action_Mono_2_polarisations": self.BoToFit_mode = 1
        elif action_mode == "action_Mono_4_polarisations": self.BoToFit_mode = 2
        elif action_mode == "action_Tof_No_polarisation": self.BoToFit_mode = 3
        elif action_mode == "action_Tof_2_polarisations": self.BoToFit_mode = 4
        elif action_mode == "action_Tof_4_polarisations": self.BoToFit_mode = 5
        elif action_mode == "action_Mono_No_polarisation_multi": self.BoToFit_mode = 6
        elif action_mode == "action_Mono_2_polarisations_multi": self.BoToFit_mode = 7
        elif action_mode == "action_Mono_4_polarisations_multi": self.BoToFit_mode = 8

        for index, mode in enumerate(MODES):
            if index == self.BoToFit_mode: MODES[index].setChecked(True)
            else: MODES[index].setChecked(False)

        # reformat table and polarisation parameters
        PARAMS_POL = [self.label_Scan_parameters_Piy, self.lineEdit_Scan_parameters_Piy, self.checkBox_Scan_parameters_Piy, self.label_Scan_parameters_Pfy, self.lineEdit_Scan_parameters_Pfy, self.checkBox_Scan_parameters_Pfy, self.label_Scan_parameters_Pfy, self.lineEdit_Scan_parameters_Pfy, self.checkBox_Scan_parameters_Pfy, self.label_Scan_parameters_Cg, self.lineEdit_Scan_parameters_Cg, self.checkBox_Scan_parameters_Cg, self.label_Scan_parameters_Sg, self.lineEdit_Scan_parameters_Sg, self.checkBox_Scan_parameters_Sg, self.label_Scan_parameters_Sg2, self.lineEdit_Scan_parameters_Sg2, self.checkBox_Scan_parameters_Sg2]
        if self.BoToFit_mode in [0, 3, 6]:
            for param in PARAMS_POL: param.setEnabled(False)
            # columns with checkboxes can change their width depends on Windows scaling settings, so we correct our table
            col_width = [106, 106, 1, 106, 1, 106, 1, 0, 0, 0, 0, 106, 1]
            for i in range(0, 13): self.tableWidget_Film_description.setColumnWidth(i, col_width[i])

        elif self.BoToFit_mode in [1, 2, 4, 5, 7, 8]:
            for param in PARAMS_POL: param.setEnabled(True)
            # columns with checkboxes can change their width depends on Windows scaling settings, so we correct our table
            col_width = [65, 73, 1, 59, 1, 59, 1, 59, 1, 81, 1, 75, 1]
            for i in range(0, 13):
                self.tableWidget_Film_description.setColumnWidth(i, col_width[i])

        # reformat checkboxes (I, dI, Qz, rad) and Wavelength/Inc.angle field
        CHECKBOXES = [self.comboBox_Data_file_Column_1, self.comboBox_Data_file_Column_2, self.comboBox_Data_file_Column_3]

        if self.BoToFit_mode in [0, 1, 2, 6, 7, 8]:
            if self.comboBox_Data_file_Column_1.count() < 4:
                for checkbox in CHECKBOXES:
                    checkbox.addItem("")
                    checkbox.setItemText(3, "ang(rad)")
            self.label_Scan_parameters_Wavelength.setText("Wavelength (A)")

        elif self.BoToFit_mode in [3, 4, 5]:
            for checkbox in CHECKBOXES: checkbox.removeItem(3)
            self.label_Scan_parameters_Wavelength.setText("Inc. ang. (mrad)")

        # load UserDefaults if such are presented
        try:
            if self.MODE_SPECS[self.BoToFit_mode][2] in os.listdir(self.current_dir + "/User_Defaults"):
                self.lineEdit_Scan_parameters_Wavelength.setText("")
                self.load_entry_file()
        except: True

        # clear stuff, just in case
        self.clear_stuff()
        self.lineEdit_Data_file.clear()
    ##<--

    ##--> buttons
    def button_Data_file(self):
        '''
        if {NoPolarisation} and {toolButton_Data_file} is pressed: [user can choose only one file]
        elif {toolButton_Data_file} is pressed: [user can choose several file]
        '''

        self.input_structure = [self.comboBox_Data_file_Column_1.currentText(), self.comboBox_Data_file_Column_2.currentText(), self.comboBox_Data_file_Column_3.currentText()]

        if self.BoToFit_mode in [0, 3, 6]:
            data_files = QtWidgets.QFileDialog().getOpenFileName(None, "FileNames", self.current_dir)
        else: data_files = QtWidgets.QFileDialog().getOpenFileNames(None, "FileNames", self.current_dir)

        if data_files[0] == "": return

        self.lineEdit_Data_file.setText(str(data_files[0]))

        # clear stuff after last run
        self.clear_stuff()
        self.tableWidget_Data_points.clear()
        self.lineEdit_Number_of_points.clear()

        if self.BoToFit_mode in [0, 1, 2, 6, 7, 8] and self.lineEdit_Scan_parameters_Wavelength.text() == "":
            self.statusbar.showMessage("Input wavelength and reimport the file")
        else:
            self.parse_Data_files()
            self.draw_reflectivity()

    def buttons_add_remove_layer(self):
        # check where we came from do required action
        try:
            sender_name = self.sender().objectName()
        except: sender_name = "None"

        if sender_name == "pushButton_Film_description_Remove_layer":
            # remove lines from {tableWidget_Film_description}
            if not self.tableWidget_Film_description.rowCount() == self.tableWidget_Film_description.currentRow() + 1:
                self.tableWidget_Film_description.removeRow(self.tableWidget_Film_description.currentRow())

        else:
            # add lines into {tableWidget_Film_description}
            if self.tableWidget_Film_description.currentRow() >= 0: i = self.tableWidget_Film_description.currentRow()
            else: i = 0

            self.tableWidget_Film_description.insertRow(i)
            self.tableWidget_Film_description.setRowHeight(i, 21)

            for j in range(0, 13):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                if j in (2, 4, 6, 8, 10, 12):
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    if j == 6: item.setCheckState(QtCore.Qt.Checked)
                    else: item.setCheckState(QtCore.Qt.Unchecked)

                self.tableWidget_Film_description.setItem(i, j, item)

    def button_Save_at(self):
        '''
        default {save_at_dit} folder is the one where "BoToFit.exe" is located
        otherwice: defined by user
        '''
        dir = QtWidgets.QFileDialog().getExistingDirectory(None, "FileNames", self.current_dir)
        if dir: self.lineEdit_Save_at.setText(str(dir))

    def button_copy_to_start_with(self):

        for i in range(0, self.tableWidget_Fit_results.rowCount()):
            if not self.tableWidget_Fit_results.item(i,0).checkState() == 2: continue

            parameter = self.tableWidget_Fit_results.item(i, 2).text().split()

            # Fill in the table:
            # Substrate has 2 parameters, Layers have 3
            if not len(parameter) == 1:
                index, start_fit_table_row = 1, self.tableWidget_Film_description.rowCount() - 1
                if len(parameter) == 3:
                    index, start_fit_table_row = 2, int(parameter[1]) - 1

                if parameter[index] == "thickness": start_fit_table_column = 1
                elif parameter[index] == "SLD": start_fit_table_column = 3
                elif parameter[index] == "iSLD": start_fit_table_column = 5
                elif parameter[index] == "mSLD": start_fit_table_column = 7
                elif parameter[index] == "cos(d-gamma)": start_fit_table_column = 9
                elif parameter[index] == "roughness": start_fit_table_column = 11

                self.tableWidget_Film_description.item(start_fit_table_row, start_fit_table_column).setText(self.tableWidget_Fit_results.item(i, 3).text())

            if parameter[0] == 'Scaling_factor': self.lineEdit_Scan_parameters_Scaling_factor.setText(self.tableWidget_Fit_results.item(i, 3).text())
            if parameter[0] == 'Overillumination': self.lineEdit_Scan_parameters_Crossover_overillumination.setText(self.tableWidget_Fit_results.item(i, 3).text())
            if parameter[0] == 'Background': self.lineEdit_Scan_parameters_Background.setText(self.tableWidget_Fit_results.item(i, 3).text())
            if parameter[0] == '<Cos(gamma)>': self.lineEdit_Scan_parameters_Cg.setText(self.tableWidget_Fit_results.item(i, 3).text())
            if parameter[0] == '<Sin(gamma)>': self.lineEdit_Scan_parameters_Sg.setText(self.tableWidget_Fit_results.item(i, 3).text())
            if parameter[0] == '<Sin^2(gamma)>': self.lineEdit_Scan_parameters_Sg2.setText(self.tableWidget_Fit_results.item(i, 3).text())
            if parameter[0] == 'Pi(y)': self.lineEdit_Scan_parameters_Piy.setText(self.tableWidget_Fit_results.item(i, 3).text())
            if parameter[0] == 'Pf(y)': self.lineEdit_Scan_parameters_Pfy.setText(self.tableWidget_Fit_results.item(i, 3).text())

    def button_Start_fitting(self):

        start_time = time.time()

        # for Polarisation - check if User selected to fit both mSLD and cos(d-gamma) for the same layer
        if not self.BoToFit_mode in [0, 3, 6]:
            for i in range(0, self.tableWidget_Film_description.rowCount()):
                if self.tableWidget_Film_description.item(i, 8).checkState() == 0 and self.tableWidget_Film_description.item(i, 10).checkState() == 0:
                    self.statusbar.showMessage("mSLD and cos(d-gamma) can not be fitted together for the same layer")
                    return

        self.checkBox_Fit_results_Select_all.setChecked(False)

        self.statusbar.showMessage("Running...")

        data_files = []
        for file in self.lineEdit_Data_file.text().split("'"):
            if len(file) > 2: data_files.append(file)

        # check if we have file to work with
        if not self.lineEdit_Data_file.text(): return

        self.clear_stuff()
        self.draw_reflectivity()

        data_file_input_name = data_files[0][data_files[0].rfind("/") + 1: data_files[0].rfind(".")].replace(" ", "_")

        # create new directory or rewrite files if they already exists
        if not self.lineEdit_Save_at.text():
            self.lineEdit_Save_at.setText(self.current_dir)

        self.data_folder_name = self.lineEdit_Save_at.text() + "/" + data_file_input_name + "/"

        if not os.path.exists(self.data_folder_name):
            os.makedirs(self.data_folder_name)

        # create entry for BoToFit
        self.create_input_Data_file()
        self.create_entry_for_BoToFit()

        # Start BoToFit with its "killer" in 2 threads
        module = '"' + self.current_dir + '/BoToFit_Modules/' + self.MODE_SPECS[self.BoToFit_mode][0] + '"'
        entry = '"' + self.data_folder_name + "entry.dat" + '"'
        data = '"' + self.data_folder_name + "data_file_reformatted.dat" + '"'

        for i in range(2):
            t = threading.Thread(target=self.BoToFit_calc_run, args=(i, module, entry, data, self.lineEdit_Scan_parameters_Points_to_exclude_First.text(), self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()))
            t.start()

        # wait until "killer" is done or "BoToFit" has crashed
        BoToFit_calc_threads_are_done = 0
        while BoToFit_calc_threads_are_done == 0:
            QtTest.QTest.qWait(1000)
            proc_list = []
            for proc in psutil.process_iter(): proc_list.append(proc.name())

            if self.MODE_SPECS[self.BoToFit_mode][0] not in proc_list: BoToFit_calc_threads_are_done = 1

        if self.MODE_SPECS[self.BoToFit_mode][1] not in os.listdir(self.data_folder_name):
            self.clear_stuff()
            self.draw_reflectivity()
            self.statusbar.showMessage("BoToFit crashed. Consider using more reasonable 'Start fit' values.")
            return

        # wait until fitting is done -> fill the table, draw graphs and create multiGrPr.ent using FitBag.dat file
        self.graphicsView_Reflectivity_profile.getPlotItem().clear()
        self.draw_reflectivity()
        self.draw_and_export_reform_FitFunct()
        self.create_Fit_results_table_and_multiGrPr_entry()

        self.draw_diff()

        try:
            os.remove(self.data_folder_name + 'SLD_profile.dat')
        except: True

        # run multiGrPr.exe
        subprocess.Popen(str(self.current_dir + '/BoToFit_Modules/multiGrPr.exe'), cwd=str(self.data_folder_name))

        # run multiGrPr and wait until it finished to work
        while "SLD_profile.dat" not in os.listdir(self.data_folder_name):
            QtTest.QTest.qWait(1000)

        while os.path.getsize(self.data_folder_name + 'SLD_profile.dat') < 1:
            QtTest.QTest.qWait(1000)

        # draw SLD
        self.draw_SLD()

        elapsed_time = time.time() - start_time
        self.statusbar.showMessage("Finished in " + str(round(float(elapsed_time), 1)) + " seconds")

        if "ang(Qz)" in self.input_structure and self.BoToFit_mode in [0, 1, 2, 6, 7, 8]: self.export_for_user()
    ##<--

    ##--> menu options
    def menu_info(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(self.current_dir + "\icon.png"))
        msgBox.setText( "BoToFit " + self.actionVersion.text() + "\n\n"
                        "Algorithm: Boris.Toperverg@ruhr-uni-bochum.de\n"
                        "GUI: Alexey.Klechikov@gmail.com\n\n"
                        
                        "Check for newer version at https://github.com/Alexey-Klechikov/BoToFit/releases")
        msgBox.exec_()
    ##<--

    ##--> "input file"
    def parse_Data_files(self):
        '''
        I write files with experimental data points into hidden table [tableWidget_Data_points] at MainWindow in [*angle, *I, *dI] format to avoid multiple parsings of the same file

        if {we have only one file with experimental points (in case of NoPolarisation)}: {we write it to the first line of the (hidden) table}
        elif {we have 2 polarisations}: {we write files as "uu", "du" in first 2 lines of the (hidden) table}
        elif {we have 4 polarisations}: {we write files as "uu", "dd", "ud", "du" in first 4 lines of the (hidden) table}
        '''

        files = []

        # reformat data to *I *dI *angle(rad) in Mono mode

        if self.BoToFit_mode in [0, 3, 6]:
            files.append(self.lineEdit_Data_file.text())
        else:
            for i in self.lineEdit_Data_file.text().split("'"):
                if i.rfind("_uu") > 0 or i.rfind("_UU") > 0: files.append(i)

            if self.BoToFit_mode in [2, 5, 8]:

                for i in self.lineEdit_Data_file.text().split("'"):
                    if i.rfind("_dd") > 0 or i.rfind("_DD") > 0: files.append(i)
                for i in self.lineEdit_Data_file.text().split("'"):
                    if i.rfind("_ud") > 0 or i.rfind("_UD") > 0: files.append(i)

            for i in self.lineEdit_Data_file.text().split("'"):
                if i.rfind("_du") > 0 or i.rfind("_DU") > 0: files.append(i)

        for i in range(0, 4):
            for j in range(0, 3):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget_Data_points.setItem(i, j, item)

        j = 0
        for file in files:
            exper_points_number, data_angle, data_I, data_dI = 0, [], [], []

            with open(file, 'r') as data_file_input:
                for i, line in enumerate(data_file_input.readlines()):

                    # for Figaro
                    if file[-4:] == '.mft':
                        if i < 23: continue

                    if "ang(Qz)" in self.input_structure: data_angle.append(float(line.split()[self.input_structure.index("ang(Qz)")]))
                    elif "ang(rad)" in self.input_structure: data_angle.append(float(line.split()[self.input_structure.index("ang(rad)")]))

                    data_I.append(float(line.split()[self.input_structure.index("I")]))
                    data_dI.append(float(line.split()[self.input_structure.index("dI")]))
                    exper_points_number += 1

            self.lineEdit_Number_of_points.setText(str(exper_points_number))
            self.tableWidget_Data_points.item(j, 0).setText(str(data_angle))
            self.tableWidget_Data_points.item(j, 1).setText(str(data_I))
            self.tableWidget_Data_points.item(j, 2).setText(str(data_dI))

            j += 1

    def create_input_Data_file(self):
        '''
        input data files for BoToFit should have [*I *dI *angle(rad)] format in Mono mode and [*I *dI *Qz] in TOF mode
        '''

        with open(self.data_folder_name + "data_file_reformatted.dat", 'w') as data_file_output:
            # check hidden table with experimental points already reformatted in Q I dI format
            for i in range(0, 4):
                if self.tableWidget_Data_points.item(i, 0).text() not in ("", "[]"):
                    data_angle = self.tableWidget_Data_points.item(i, 0).text()[1: -1].replace(",", "").split()
                    data_I = self.tableWidget_Data_points.item(i, 1).text()[1: -1].replace(",", "").split()
                    data_dI = self.tableWidget_Data_points.item(i, 2).text()[1: -1].replace(",", "").split()

                    for j in range(0, len(data_angle)):
                        if self.BoToFit_mode in [3, 4, 5]: data_file_output.write(data_I[j] + "  " + data_dI[j] + "    " + data_angle[j] + "\n")
                        else:
                            if "ang(Qz)" in self.input_structure:
                                data_file_output.write(data_I[j] + "  " + data_dI[j] + "    " + str(self.angle_convert("Qz", "rad", float(data_angle[j]))) + "\n")
                            else: data_file_output.write(data_I[j] + "  " + data_dI[j] + "    " + data_angle[j] + "\n")
    ##<--

    ##--> "BoToFit entry"
    def load_entry_file(self):
        '''
        I use this function both at first run of the program to load "default" values and to import user's entry file
        '''
        # remove cursor from the table for import
        self.tableWidget_Film_description.setCurrentCell(-1, -1)

        if self.lineEdit_Scan_parameters_Wavelength.text() == "":
            if self.MODE_SPECS[self.BoToFit_mode][2] in os.listdir(self.current_dir + "/User_Defaults"):
                entry_file = self.current_dir + "/User_Defaults/" + self.MODE_SPECS[self.BoToFit_mode][2]
        else:
            entry_file = QtWidgets.QFileDialog().getOpenFileName(None, "FileNames", self.current_dir)[0]

        if entry_file == "": return

        ENTRY = pd.read_csv(entry_file, header=None, squeeze=True)

        index_reference = 0
        if not self.BoToFit_mode in [0, 3, 6]:
            self.lineEdit_Scan_parameters_Piy.setText(ENTRY[2].split()[0]) # Piy incident polarization (polariser)
            self.__set_checked(self.checkBox_Scan_parameters_Piy, ENTRY[3].split()[0])
            self.lineEdit_Scan_parameters_Pfy.setText(ENTRY[8].split()[0]) # Pfy outgoing polarization (analyser)
            self.__set_checked(self.checkBox_Scan_parameters_Pfy, ENTRY[9].split()[0])
            index_reference = 12

        self.lineEdit_Scan_parameters_Wavelength.setText(ENTRY[index_reference].split()[0]) # wavelength or incident angle
        self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function.setText(ENTRY[index_reference+2].split()[0]) # number of experimental points in alpha
        self.lineEdit_Scan_parameters_Step_for_resolution_function.setText(ENTRY[index_reference+3].split()[0]) # step for resolution function (in mrad)
        self.lineEdit_Scan_parameters_Sigma.setText(ENTRY[index_reference+4].split()[0]) # "sigma" of resolution function (in mrad)

        number_of_layers = int(ENTRY[index_reference+5].split()[0])
        
        # delete all layers except substrate
        while not self.tableWidget_Film_description.rowCount() == 1:
            self.tableWidget_Film_description.removeRow(0)
        # add layers
        for i in range(0, number_of_layers):
            self.buttons_add_remove_layer()
            self.tableWidget_Film_description.item(0, 0).setText("Layer " + str(number_of_layers - i))
        # fill the table
        row, col, index_reference = 0, 1, index_reference+6
        for row in range(0, number_of_layers+1):
            if not row == number_of_layers:
                self.tableWidget_Film_description.item(row, col).setText(ENTRY[index_reference].split()[0].replace("d", "e")) # Thickness
                self.__set_checked(self.tableWidget_Film_description.item(row, col + 1), ENTRY[index_reference+1].split()[0])
            else: index_reference -= 2
            self.tableWidget_Film_description.item(row, col + 2).setText(ENTRY[index_reference + 2].split()[0].replace("d", "e"))  # SLD
            self.__set_checked(self.tableWidget_Film_description.item(row, col + 3), ENTRY[index_reference+3].split()[0])
            self.tableWidget_Film_description.item(row, col + 4).setText(ENTRY[index_reference + 4].split()[0].replace("d", "e"))  # iSLD
            self.__set_checked(self.tableWidget_Film_description.item(row, col + 5), ENTRY[index_reference+5].split()[0])
            if self.BoToFit_mode in [0, 3, 6]:
                self.tableWidget_Film_description.item(row, col + 10).setText(ENTRY[index_reference + 6].split()[0].replace("d", "e"))  # roughness
                self.__set_checked(self.tableWidget_Film_description.item(row, col + 11), ENTRY[index_reference + 7].split()[0])
                index_reference = index_reference + 8
            else:
                self.tableWidget_Film_description.item(row, col + 6).setText(ENTRY[index_reference + 6].split()[0].replace("d", "e"))  # mSLD
                self.__set_checked(self.tableWidget_Film_description.item(row, col + 7), ENTRY[index_reference+7].split()[0])
                self.tableWidget_Film_description.item(row, col + 8).setText(ENTRY[index_reference + 8].split()[0].replace("d", "e"))  # cos(d-gamma)
                self.__set_checked(self.tableWidget_Film_description.item(row, col + 9), ENTRY[index_reference+9].split()[0])
                self.tableWidget_Film_description.item(row, col + 10).setText(ENTRY[index_reference + 10].split()[0].replace("d", "e"))  # roughness
                self.__set_checked(self.tableWidget_Film_description.item(row, col + 11), ENTRY[index_reference+11].split()[0])
                index_reference = index_reference + 12

        if not self.BoToFit_mode in [0, 3, 6]:
            # cg: mean value <cos(gamma)> over big domains
            self.lineEdit_Scan_parameters_Cg.setText(ENTRY[index_reference].split()[0])
            self.__set_checked(self.checkBox_Scan_parameters_Cg, ENTRY[index_reference + 1].split()[0])
            # sg: mean value <sin(gamma)> over big domains
            self.lineEdit_Scan_parameters_Sg.setText(ENTRY[index_reference + 2].split()[0])
            self.__set_checked(self.checkBox_Scan_parameters_Sg, ENTRY[index_reference + 3].split()[0])
            # sg2: mean value <sin^2(gamma)> over big domains
            self.lineEdit_Scan_parameters_Sg2.setText(ENTRY[index_reference + 4].split()[0])
            self.__set_checked(self.checkBox_Scan_parameters_Sg2, ENTRY[index_reference + 5].split()[0])
        else: index_reference -= 6

        # ct  total scaling factor
        self.lineEdit_Scan_parameters_Scaling_factor.setText(ENTRY[index_reference + 6].split()[0])
        self.__set_checked(self.checkBox_Scan_parameters_Scaling_factor, ENTRY[index_reference + 7].split()[0])
        # alpha_0 crossover angle overillumination (in mrad)
        self.lineEdit_Scan_parameters_Crossover_overillumination.setText(ENTRY[index_reference + 8].split()[0])
        self.__set_checked(self.checkBox_Scan_parameters_Crossover_overillumination, ENTRY[index_reference + 9].split()[0])
        # bgr 'background'
        self.lineEdit_Scan_parameters_Background.setText(ENTRY[index_reference + 10].split()[0])
        self.__set_checked(self.checkBox_Scan_parameters_Background, ENTRY[index_reference + 11].split()[0])
        # correction of the detector 'zero' (in mrad)
        self.lineEdit_Scan_parameters_Zero_correction.setText(ENTRY[index_reference + 12].split()[0])

    def create_entry_for_BoToFit(self):
        '''
        BoToFit needs its own entry file, so we make one using data from the table
        '''

        ENTRY = []

        if self.BoToFit_mode not in [0, 3, 6]:
            # incident polarization (polariser)
            ENTRY.append("0     Pix incident polarization (polariser)\nf\n" + self.lineEdit_Scan_parameters_Piy.text() + '    Piy\n' + self.__check_checked(self.checkBox_Scan_parameters_Piy) + "\n" + "0     Piz\nf\n\n")
            # outgoing polarization (analyser)
            ENTRY.append("0     Pfx outgoing polarization (analyser)\nf\n" + self.lineEdit_Scan_parameters_Pfy.text() + '    Pfy\n' + self.__check_checked(self.checkBox_Scan_parameters_Pfy) + "\n" + "0     Pfz\nf\n\n")

        if not self.BoToFit_mode in [3, 4, 5]: ENTRY.append(self.lineEdit_Scan_parameters_Wavelength.text() + '    wavelength (in Angstrem)\n')
        else: ENTRY.append(self.lineEdit_Scan_parameters_Wavelength.text() + '    incident angle (in mrad)\n')

        ENTRY.append(self.lineEdit_Number_of_points.text() + "   *nn number of experimental points in alpha (<1001)\n")
        ENTRY.append(self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function.text() + "    *j0 number of points for resolution function (odd) (<102)\n")
        ENTRY.append(self.lineEdit_Scan_parameters_Step_for_resolution_function.text() + "    step for resolution function (in mrad)\n")
        ENTRY.append(self.lineEdit_Scan_parameters_Sigma.text() + "     *sigma of resolution function (in mrad)\n\n")
        ENTRY.append(str(self.tableWidget_Film_description.rowCount() - 1) + "   number of layers (excluding substrate) (<21)\n\n")
        # read the table
        for i in range(0, self.tableWidget_Film_description.rowCount()):
            comment = ""
            # Thickness
            if not self.tableWidget_Film_description.item(i, 0).text() == "substrate":
                ENTRY.append(self.tableWidget_Film_description.item(i, 1).text() + "    layer " + str(i+1) + " ("+ self.tableWidget_Film_description.item(i, 0).text() + ") thickness (in A)\n" + self.__check_checked(self.tableWidget_Film_description.item(i, 2)) + "\n")
            else: comment = "substrate's"
            # SLD
            ENTRY.append(self.tableWidget_Film_description.item(i, 3).text() + "    " + comment + " nbr nuclear SLD Nb'  (in A**-2) *1e6\n" + self.__check_checked(self.tableWidget_Film_description.item(i, 4)) + "\n")
            # iSDL
            ENTRY.append(self.tableWidget_Film_description.item(i, 5).text() + "    " + comment + " nbi nuclear SLD Nb'' (in A**-2) *1e6\n" + self.__check_checked(self.tableWidget_Film_description.item(i, 6)) + "\n")
            if self.BoToFit_mode not in [0, 3, 6]:
                # magnetic SLD
                ENTRY.append(self.tableWidget_Film_description.item(i, 7).text() + "    magnetic SLD Np (in A**-2)*1e6\n" + self.__check_checked(self.tableWidget_Film_description.item(i, 8)) + "\n")
                # c=<cos(delta_gamma)>
                ENTRY.append(self.tableWidget_Film_description.item(i, 9).text() + "    c=<cos(delta_gamma)>\n" + self.__check_checked(self.tableWidget_Film_description.item(i, 10)) + "\n")
            # roughness
            ENTRY.append(self.tableWidget_Film_description.item(i, 11).text() + "    dw Debye-Waller in [AA]\n" + self.__check_checked(self.tableWidget_Film_description.item(i, 12)) + "\n\n")

        if self.BoToFit_mode not in [0, 3, 6]:
            # cg
            ENTRY.append(self.lineEdit_Scan_parameters_Cg.text() + '    cg: mean value <cos(gamma)> over big domains\n' + self.__check_checked(self.checkBox_Scan_parameters_Cg) + "\n")
            # sg
            ENTRY.append(self.lineEdit_Scan_parameters_Sg.text() + '    sg: mean value <sin(gamma)> over big domains\n' + self.__check_checked(self.checkBox_Scan_parameters_Sg) + "\n")
            # sg2
            ENTRY.append(self.lineEdit_Scan_parameters_Sg2.text() + '    sg2: mean value <sin^2(gamma)> over big domains\n' + self.__check_checked(self.checkBox_Scan_parameters_Sg2) + "\n\n")

        # ct - total scaling factor
        ENTRY.append(self.lineEdit_Scan_parameters_Scaling_factor.text() + "   *ct  total scaling factor\n" + self.__check_checked(self.checkBox_Scan_parameters_Scaling_factor) + "\n")
        # alpha_0 crossover angle overillumination
        ENTRY.append(self.lineEdit_Scan_parameters_Crossover_overillumination.text() + "   *alpha_0 crossover angle overillumination (in mrad)\n" + self.__check_checked(self.checkBox_Scan_parameters_Crossover_overillumination) + "\n")
        # background
        ENTRY.append(self.lineEdit_Scan_parameters_Background.text() + "   *bgr background\n" + self.__check_checked(self.checkBox_Scan_parameters_Background) + "\n")

        # correction of the detector 'zero'
        ENTRY.append("\n" + self.lineEdit_Scan_parameters_Zero_correction.text() + "   correction of the detector 'zero' (in mrad)")

        with open(self.data_folder_name + 'entry.dat', 'w') as entry_file:
            for i in ENTRY: entry_file.write(i)
    ##<--

    ##--> "Results table" and "multiGrPr entry"
    def create_Fit_results_table_and_multiGrPr_entry(self):
        '''
        this is another entry, used for multiGrPr.exe. It is used to calculate SLD profile
        '''

        multiGrPr_data = [[0, 0.977836, 0],
                          [0, 0.985158, 0],
                          [0, 0, 30, 0, 30, -200, 3000, 1999, 0.36, 3],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [1, 0, 0],
                          [1, 0, 0]]

        multiGrPr_info = [["Pix incident polarization (polariser)", "Piy", "Piz"],
                          ["Pfx outgoing polarization (analyser)", "Pfy", "Pfz"],
                          ["wavelength lambda (in A)", "min. angle of incidence alphai  (in mrad)", "max. angle of incidence alhamax (in mrad)", "min. angle of exit  (in mrad)", "max. angle of exit  (in mrad)", "min. z  (in Angstrom)", "max. z  (in Angstrom)", "'nn' number of points in alphai (alphaf)", "'delta' width of Gaussian in (mrad)", "'nn0' number of withs averaged"],
                          ["number of cap layers", "number of sub-layers", "number of repetitions", "number of buffer layers"],
                          ["Layer 1  thickness in (A)", "real part of nuclear SLD Nb'  (in A**-2) *1e-6", "imaginary part of nuclear SLD Nb'' (in A**-2) *1e-6", "magn. scatt. length density (SLD) Np (in A**-2) *1e-6", "c=<cos(delta_gamma)>_{over small domains}", "dw Debye-Waller in [AA]", "grad_d", "grad_Nb", "grad_Np", "grad_DW"],
                          ["Substrate SLD Nb' (in A**-2) *1e-6", "Substrate   Nb'' im. part of nucl. SLD Nb'' (in A**-2) *1e-6", "magnetic scattering length density Np (in A**-2) *1e-6", "c=<cos(delta_phi)>_{over small domains}", "dw Debye-Waller in [AA]"],
                          ["cg: mean value <cos(gamma)>  of 'big domains'' ! cg^2<1-sg2", "sg: mean <sin(gamma)>", "sg2: mean value <sin^2(gamma)> of 'big domains'"],
                          ["ct  total scaling factor", "alpha_0 [mrad] crossover illumination angle", "bgr"]
                          ]

        for i in range(1, self.tableWidget_Film_description.rowCount() - 1):
            multiGrPr_data.insert(5, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            multiGrPr_info.insert(5, ["Layer " + str(self.tableWidget_Film_description.rowCount() - i) + " thickness in (A)", "real part of nuclear SLD Nb'  (in A**-2) *1e-6", "imaginary part of nuclear SLD Nb'' (in A**-2) *1e-6", "magn. scatt. length density (SLD) Np (in A**-2) *1e-6", "c=<cos(delta_gamma)>_{over small domains}", "dw Debye-Waller in [AA]", "grad_d", "grad_Nb", "grad_Np", "grad_DW"])

        last_itr_loc = 0

        multiGrPr = open(self.data_folder_name + 'multiGrPr.ent', 'w')

        multiGrPr_data[2][0] = self.lineEdit_Scan_parameters_Wavelength.text()
        multiGrPr_data[3][3] = self.tableWidget_Film_description.rowCount() - 1

        # clear results_table before another fit
        for i in range(0, self.tableWidget_Fit_results.rowCount()): self.tableWidget_Fit_results.removeRow(0)

        # do fast run to find last iteration location
        fit_file_name = "Fit2DBag.dat" if not self.BoToFit_mode in [0, 3, 6] else "FitBag.dat"

        with open(self.data_folder_name + fit_file_name, "r") as fit_file:
            for line_number, line in enumerate(fit_file.readlines()):
                if line.find(" iterate ") > 0:
                    last_itr_loc = line_number

        # show it in the table
        with open(self.data_folder_name + fit_file_name, "r") as fit_file:
            layer_name = 0
            layer_num = 0
            i = 0
            for line_number, line in enumerate(fit_file.readlines()):
                if line_number >= last_itr_loc:

                    try:
                        if line.split()[0] == "Layer": layer_name = "Layer " + str(line.split()[1]) + " "
                        elif line.split()[0] == "Substrate": layer_name = "Substrate "
                        elif line.split()[1] in ['<Cos(gamma)>', 'total', 'alpha_0', 'background']: layer_name = ""

                        if line.split()[1] == 'total': line = line.replace("total scaling", "Scaling_factor")
                        elif line.split()[1] == 'alpha_0': line = line.replace("alpha_0", "Overillumination")
                        elif line.split()[1] == 'Re{Nb}': line = line.replace("Re{Nb}", "SLD")
                        elif line.split()[1] == 'Im{Nb}': line = line.replace("Im{Nb}", "iSLD")
                        elif line.split()[1] == 'N_p': line = line.replace("N_p", "mSLD")
                        elif line.split()[1] == 'Debye-Waller': line = line.replace("Debye-Waller", "roughness")
                        elif line.split()[1] == 'background': line = line.replace("background", "Background")
                        elif line.split()[1] == '<Cos(delta_gamma': line = line.replace("<Cos(delta_gamma", "cos(d-gamma)")

                        if line.split()[0] == "hi_sq.norm:": self.lineEdit_Fit_results_Chi_square.setText(str("0") + str(line.split()[1]))

                        if line.split()[1] == "iterate": self.lineEdit_Fit_results_Number_of_iterations.setText(str(line.split()[0]))

                        # Fill table
                        if line.split()[1] in ['thickness', 'SLD', 'iSLD', 'roughness', 'mSLD', 'cos(d-gamma)', 'Scaling_factor',
                                               'Overillumination', 'Background', '<Cos(gamma)>', '<Sin(gamma)>', '<Sin^2(gamma)>', 'Pi(x)', 'Pi(y)', 'Pi(z)', 'Pf(x)', 'Pf(y)', 'Pf(z)'] and not line.split()[3] == "fixed":

                            self.tableWidget_Fit_results.insertRow(self.tableWidget_Fit_results.rowCount())

                            try:
                                self.tableWidget_Fit_results.setRowHeight(i, 22)
                                for j in range(0, 6):
                                    item = QtWidgets.QTableWidgetItem()
                                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                                    item.setFlags(
                                        QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
                                    if j == 0:
                                        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                                        item.setCheckState(QtCore.Qt.Unchecked)
                                    self.tableWidget_Fit_results.setItem(i, j, item)

                                self.tableWidget_Fit_results.item(i, 1).setText(str(i + 1))
                                self.tableWidget_Fit_results.item(i, 2).setText(layer_name + " " + line.split()[1])
                                if line.split()[1] in ['SLD', 'iSLD', 'mSLD']:
                                    self.tableWidget_Fit_results.item(i, 3).setText(str(round(float(line.split()[2]) * 10e5, 4)))
                                else:
                                    self.tableWidget_Fit_results.item(i, 3).setText(str(float(line.split()[2])))

                                if str(line.split()[3]) == "fixed": table_error = "fixed"
                                elif str(line.split()[4]) == "infinite": table_error = "infinite"
                                else:
                                    if line.split()[1] in ['SLD', 'iSLD', 'mSLD']:
                                        table_error = str(line.split()[3]) + str(round(float(line.split()[4])* 10e5, 4))
                                    else: table_error = str(line.split()[3]) + str(float(line.split()[4]))

                                self.tableWidget_Fit_results.item(i, 4).setText(table_error)
                                self.tableWidget_Fit_results.item(i, 5).setText(str(float(line.split()[5])))

                            except: True
                            i += 1

                        # Fill multiGrPr.ent
                        ## layers
                        if line.split()[1] in ['thickness', 'SLD', 'iSLD', 'roughness', 'mSLD', 'cos(d-gamma)'] and not layer_name == "Substrate ":
                            if line.split()[1] == 'thickness': multiGrPr_data[4+layer_num][0] = float(line.split()[2])
                            elif line.split()[1] == 'SLD': multiGrPr_data[4+layer_num][1] = float(line.split()[2]) * 10e+5
                            elif line.split()[1] == 'iSLD': multiGrPr_data[4+layer_num][2] = float(line.split()[2]) * 10e+5
                            elif line.split()[1] == 'mSLD': multiGrPr_data[4+layer_num][3] = float(line.split()[2]) * 10e+5
                            elif line.split()[1] == 'cos(d-gamma)': multiGrPr_data[4+layer_num][4] = float(line.split()[2])
                            elif line.split()[1] == 'roughness':
                                multiGrPr_data[4+layer_num][5] = float(line.split()[2])
                                layer_num += 1

                        ## substrate
                        elif line.split()[1] in ['SLD', 'iSLD', 'roughness', 'mSLD', 'cos(d-gamma)'] and layer_name == "Substrate ":
                            if line.split()[1] == 'SLD': multiGrPr_data[4+layer_num][0] = float(line.split()[2]) * 10e+5
                            elif line.split()[1] == 'iSLD': multiGrPr_data[4+layer_num][1] = float(line.split()[2]) * 10e+5
                            elif line.split()[1] == 'mSLD': multiGrPr_data[4 + layer_num][2] = float(line.split()[2]) * 10e+5
                            elif line.split()[1] == 'cos(d-gamma)': multiGrPr_data[4 + layer_num][3] = float(line.split()[2])
                            elif line.split()[1] == 'roughness': multiGrPr_data[4 + layer_num][4] = float(line.split()[2])

                        ## end of file
                        elif line.split()[1] in ['Scaling_factor', 'Overillumination', 'Background', '<Cos(gamma)>', '<Sin(gamma)>', '<Sin^2(gamma)>']:
                            if line.split()[1] == '<Cos(gamma)>': multiGrPr_data[4+self.tableWidget_Film_description.rowCount()][0] = float(line.split()[2])
                            if line.split()[1] == '<Sin(gamma)>': multiGrPr_data[4 + self.tableWidget_Film_description.rowCount()][1] = float(line.split()[2])
                            if line.split()[1] == '<Sin^2(gamma)>': multiGrPr_data[4 + self.tableWidget_Film_description.rowCount()][2] = float(line.split()[2])
                            if line.split()[1] == 'Scaling_factor': multiGrPr_data[4 + self.tableWidget_Film_description.rowCount()+1][0] = float(line.split()[2])
                            if line.split()[1] == 'Overillumination': multiGrPr_data[4 + self.tableWidget_Film_description.rowCount()+1][1] = float(line.split()[2])
                            if line.split()[1] == 'Background': multiGrPr_data[4 + self.tableWidget_Film_description.rowCount()+1][2] = float(line.split()[2])

                        elif line.split()[1] == 'Pi(y)': multiGrPr_data[0][1] = float(line.split()[2])
                        elif line.split()[1] == 'Pf(y)': multiGrPr_data[1][1] = float(line.split()[2])

                    except: True

        for i in range(0, len(multiGrPr_data)):
            for j in range(0, len(multiGrPr_data[i])):
                multiGrPr.write(str(multiGrPr_data[i][j]) + "     " + str(multiGrPr_info[i][j]) + "\n")
            multiGrPr.write("\n")

        multiGrPr.close()
    ##<--

    ##--> draw graphs
    def draw_reflectivity(self):

        if self.sender().objectName() == "pushButton_Scan_parameters_Redraw_reflectivity": self.graphicsView_Reflectivity_profile.getPlotItem().clear()

        '''
        draw reflectivity in Angle vs. lg(I) scale using data from hidden table
        '''
        color = [0, 0, 0]

        if "ang(Qz)" in self.input_structure: self.label_Reflectivity_profile_and_Diff.setText("Reflectivity profile (I[10e] vs. Qz[Å**-1]) and Difference (Exper/Fit):")
        elif "ang(rad)" in self.input_structure: self.label_Reflectivity_profile_and_Diff.setText("Reflectivity profile (I[10e] vs. Angle[mrad]) and Difference (Exper/Fit):")

        # if tableWidget_Data_points is empty - do nothing
        try:
            self.tableWidget_Data_points.item(0, 0).text()
        except: return

        for i in range(0, 4):
            if self.tableWidget_Data_points.item(i, 0).text() not in ("", "[]"):
                data_angle = self.tableWidget_Data_points.item(i, 0).text()[1: -1].replace(",", "").split()
                data_I = self.tableWidget_Data_points.item(i, 1).text()[1: -1].replace(",", "").split()
                data_dI = self.tableWidget_Data_points.item(i, 2).text()[1: -1].replace(",", "").split()

                # change color from black when 2 or 4 polarisations
                if self.BoToFit_mode in [1, 4, 7]:
                    if i == 1: color = [255, 0, 0]
                elif self.BoToFit_mode in [2, 5, 8]:
                    if i == 1: color = [255, 0, 0]
                    if i == 2: color = [0, 255, 0]
                    if i == 3: color = [0, 0, 255]

                # pyqtgraph can not rescale data in log scale, so we do it manually
                plot_I, plot_angle, plot_dI_err_bottom, plot_dI_err_top = [], [], [], []

                for j in range(0, len(data_angle)):
                    if float(data_I[j]) > 0:
                        plot_angle.append(float(data_angle[j]))
                        plot_I.append(math.log10(float(data_I[j])))
                        plot_dI_err_top.append(abs(math.log10(float(data_I[j]) + float(data_dI[j])) - math.log10(float(data_I[j]))))

                        if float(data_I[j]) > float(data_dI[j]):
                            plot_dI_err_bottom.append(math.log10(float(data_I[j])) - math.log10(float(data_I[j]) - float(data_dI[j])))
                        else: plot_dI_err_bottom.append(0)

                s1 = pg.ErrorBarItem(x=np.array(plot_angle[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1]), y=np.array(plot_I[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1]), top=np.array(plot_dI_err_top[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1]), bottom=np.array(plot_dI_err_bottom[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1]), pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                self.graphicsView_Reflectivity_profile.addItem(s1)

                s2 = pg.ScatterPlotItem(x=plot_angle[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1], y=plot_I[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1], symbol="o", size=2, pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                self.graphicsView_Reflectivity_profile.addItem(s2)

    def draw_and_export_reform_FitFunct(self):
        '''
        draw BoToFit final fit function on top of the graph with experimental points
        '''

        if self.BoToFit_mode in [0, 3, 6]: fit_funct_files = [["FitFunct.dat", [0, 0, 0]], []]
        elif self.BoToFit_mode in [1, 4, 7]: fit_funct_files = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]]]
        elif self.BoToFit_mode in [2, 5, 8]: fit_funct_files = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]], ["Fit2DFunctUD.dat", [0, 255, 0]], ["Fit2DFunctDU.dat", [0, 0, 255]]]

        for file in fit_funct_files:
            plot_I, plot_angle = [], []

            if file == []: return

            # if user wants to work with data in Qz, he will get additional files during export
            if not self.BoToFit_mode in [3, 4, 5] and "ang(Qz)" in self.input_structure:
                export_fit_funct_file_name = self.data_folder_name + "EXPORT - Qz_I - " + file[0]
                if self.BoToFit_mode in [1, 7]: export_fit_funct_file_name = self.data_folder_name + "EXPORT - Qz_I - " + file[0][:-5] + ".dat"

                export_fit_funct_file = open(export_fit_funct_file_name, "w")

            with open(self.data_folder_name + file[0], 'r') as fit_funct_file:
                for line in fit_funct_file.readlines():
                    try:
                        plot_I.append(math.log10(float(line.split()[1])))
                        if self.BoToFit_mode in [3, 4, 5]: plot_angle.append(float(line.split()[0]))
                        else:
                            if "ang(Qz)" in self.input_structure: plot_angle.append(self.angle_convert("rad", "Qz", float(line.split()[0])))
                            elif "ang(rad)" in self.input_structure: plot_angle.append(float(line.split()[0]))
                    except: True

                    # export data for user in (Qz I) format if needed
                    if not self.BoToFit_mode in [3, 4, 5] and "ang(Qz)" in self.input_structure: export_fit_funct_file.write(str((4 * math.pi / float(self.lineEdit_Scan_parameters_Wavelength.text())) * math.sin(float(line.split()[0]))) + "    " + str((line.split()[1])) + "\n")

                s3 = pg.PlotDataItem(plot_angle, plot_I, pen = pg.mkPen(color=(file[1][0], file[1][1], file[1][2]), width=2))
                self.graphicsView_Reflectivity_profile.addItem(s3)

    def draw_SLD(self):
        '''
        draw SLD profiles, calculated in multiGrPr.exe
        '''

        self.graphicsView_Sld_profile.getPlotItem().clear()

        dist, sld_1, sld_2 = [], [], []
        points, cut_1, cut_2 = -1, -1, -1

        with open(self.data_folder_name + 'SLD_profile.dat', 'r') as sld_file:
            for line_number, line in enumerate(sld_file.readlines()):
                try:
                    sld_1.append((float(line.split()[1].replace("D", "E"))))
                    sld_2.append((float(line.split()[2].replace("D", "E"))))
                    dist.append(float(line.split()[0].replace("D", "E")))
                except: True
                points = line_number

            try:
                for i in range(points-100, 0, -1):
                    if not round(sld_1[i], 3) == round(sld_1[points - 100], 3) and cut_1 == -1: cut_1 = i
                for i in range(points-100, 0, -1):
                    if not round(sld_2[i], 3) == round(sld_2[points - 100], 3) and cut_2 == -1: cut_2 = i
            except: cut_1 = cut_2 = points

            s4 = pg.PlotDataItem(dist[:max(cut_1, cut_2) + 50], sld_1[:max(cut_1, cut_2) + 50], pen=pg.mkPen(color=(255,0,0), width=2))
            self.graphicsView_Sld_profile.addItem(s4)

            s5 = pg.PlotDataItem(dist[:max(cut_1, cut_2)+ 50], sld_2[:max(cut_1, cut_2) + 50], pen=pg.mkPen(color=(0,0,0), width=2))
            self.graphicsView_Sld_profile.addItem(s5)

    def draw_diff(self):
        '''
        Here I compare experimental points with fitting curves

        data in [tableWidget_Data_points] order:
            0pol = line 0
            2pol = line 0 (uu), line 1(du)
            4pol = line 0 (uu), line 1(dd), line 2 (ud), line 3(du)
        '''

        self.graphicsView_Diff.getPlotItem().clear()

        if self.BoToFit_mode in [0, 3, 6]: fit_funct_files = [["FitFunct.dat", [0, 0, 0]], []]
        elif self.BoToFit_mode in [1, 4, 7]: fit_funct_files = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]]]
        elif self.BoToFit_mode in [2, 5, 8]: fit_funct_files = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]], ["Fit2DFunctUD.dat", [0, 255, 0]], ["Fit2DFunctDU.dat", [0, 0, 255]]]

        for i, file in enumerate(fit_funct_files):
            fit_funct_I = []
            fit_funct_angle = []
            diff_I = []
            scale_angle = []
            zero_I = []

            if file == []: return

            with open(self.data_folder_name + file[0], 'r') as fit_funct_file:
                for line in fit_funct_file.readlines():

                    if line.split()[1] == "-Infinity": continue

                    try:
                        if self.BoToFit_mode in [3, 4, 5]: fit_funct_angle.append((float(line.split()[0])))
                        else:
                            if "ang(rad)" in self.input_structure:
                                fit_funct_angle.append((float(line.split()[0])))
                            else: fit_funct_angle.append((4 * math.pi / float(self.lineEdit_Scan_parameters_Wavelength.text())) * math.sin(float(line.split()[0])))
                        fit_funct_I.append(float(line.split()[1]))
                    except: True

                s = InterpolatedUnivariateSpline(np.array(fit_funct_angle), np.array(fit_funct_I), k=1)

            if self.tableWidget_Data_points.item(i, 0).text() not in ("", "[]"):
                scale_angle = np.array(self.tableWidget_Data_points.item(i, 0).text()[1: -1].replace(",", "").split()).astype(float)[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()) : -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text())-1]
                data_I = np.array(self.tableWidget_Data_points.item(i, 1).text()[1: -1].replace(",", "").split()).astype(float)[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()) : -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text())-1]

                for i in range(0, len(scale_angle)):
                    if data_I[i] != 0: diff_I.append(data_I[i] / s(scale_angle[i]))
                    else: zero_I.append(i)

            s6 = pg.PlotDataItem(np.delete(scale_angle, zero_I), diff_I, pen = pg.mkPen(color=(file[1][0], file[1][1], file[1][2]), width=2))
            self.graphicsView_Diff.addItem(s6)
    ##<--

    ##--> reformat data for user in Mono modes if he uses Qz as an angle
    def export_for_user(self):

        # create reformatted files (in Qz I dI) named "Export"
        if self.BoToFit_mode in [0, 6]: num_rows = 1
        elif self.BoToFit_mode in [1, 7]: num_rows = 2
        elif self.BoToFit_mode in [2, 8]: num_rows = 4

        for i in range(0, num_rows):
            file_name_export_Data_points = "/EXPORT - Qz_I_dI - data points.dat"
            if num_rows == 2:
                file_name_export_Data_points = "/EXPORT - Qz_I_dI - data points - U.dat"
                if i == 1: file_name_export_Data_points = "/EXPORT - Qz_I_dI - data points - D.dat"
            elif num_rows == 4:
                file_name_export_Data_points = "/EXPORT - Qz_I_dI - data points - UU.dat"
                if i == 1: file_name_export_Data_points = "/EXPORT - Qz_I_dI - data points - DD.dat"
                elif i == 2: file_name_export_Data_points = "/EXPORT - Qz_I_dI - data points - UD.dat"
                elif i == 3: file_name_export_Data_points = "/EXPORT - Qz_I_dI - data points - DU.dat"

            with open(self.data_folder_name + file_name_export_Data_points, "w") as export_Data_points:
                data_Qz = self.tableWidget_Data_points.item(i, 0).text()[1: -1].replace(",", "").split()
                data_I = self.tableWidget_Data_points.item(i, 1).text()[1: -1].replace(",", "").split()
                data_dI = self.tableWidget_Data_points.item(i, 2).text()[1: -1].replace(",", "").split()

                for j in range(0, len(data_I)):
                    export_Data_points.write(str(data_Qz[j]) + "    " + str(data_I[j]) + "    " + str(data_dI[j]) + "\n")
    ##<--

    ##--> extra functions to shorten the code
    def clear_stuff(self):
        self.graphicsView_Reflectivity_profile.getPlotItem().clear()
        self.graphicsView_Sld_profile.getPlotItem().clear()
        self.graphicsView_Diff.getPlotItem().clear()
        self.lineEdit_Fit_results_Number_of_iterations.clear()
        self.lineEdit_Fit_results_Chi_square.clear()
        for i in range(0, self.tableWidget_Fit_results.rowCount()): self.tableWidget_Fit_results.removeRow(0)

    def angle_convert(self, input_unit, output_unit, input_value):

        if output_unit == "Qz":
            if input_unit == "Qz": output_value = float(input_value)
            elif input_unit == "rad": output_value = (4 * math.pi / float(self.lineEdit_Scan_parameters_Wavelength.text())) * math.sin(float(input_value))

        elif output_unit == "rad":
            if input_unit == "Qz": output_value = math.asin(float(input_value) * float(self.lineEdit_Scan_parameters_Wavelength.text()) / (4 * math.pi))
            elif input_unit == "rad": output_value = float(input_value)

        return output_value

    def fit_results_Select_all(self):
        if self.checkBox_Fit_results_Select_all.isChecked():
            for i in range(0, self.tableWidget_Fit_results.rowCount()):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setCheckState(QtCore.Qt.Checked)
                self.tableWidget_Fit_results.setItem(i, 0, item)

        else:
            for i in range(0, self.tableWidget_Fit_results.rowCount()):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setCheckState(QtCore.Qt.Unchecked)
                self.tableWidget_Fit_results.setItem(i, 0, item)

    def BoToFit_calc_run(self, thread, module, entry, data, pts_to_skip_left, pts_to_skip_right):

        if thread == 0:
            # define that BoToFit is done by checking the folder for "self.MODE_SPECS[self.BoToFit_mode][1]"

            # delete old FitFunct.dat file
            try:
                os.remove(self.data_folder_name + self.MODE_SPECS[self.BoToFit_mode][1])
            except: True

            # check every second if BoToFit is done
            while self.MODE_SPECS[self.BoToFit_mode][1] not in os.listdir(self.data_folder_name):

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
            file = subprocess.Popen(str(module), stdin=subprocess.PIPE, cwd=self.data_folder_name)
            file.communicate(input=bytes(communicate_string, 'utf-8'))

    def __set_checked(self, parameter, checked):
        if checked == "n": parameter.setCheckState(0)
        elif checked == "f": parameter.setCheckState(2)

    def __check_checked(self, parameter):
        checked = "f"
        if parameter.checkState() == 0: checked = "n"
        return checked

if __name__ == "__main__":
    import sys
    QtWidgets.QApplication.setStyle("Fusion")
    app = QtWidgets.QApplication(sys.argv)
    prog = GUI()
    prog.show()
    sys.exit(app.exec_())

