from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
import os, psutil, time, math, numpy, threading, subprocess
import pyqtgraph as pg
from scipy.interpolate import InterpolatedUnivariateSpline

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Ui_MainWindow(QtGui.QMainWindow):

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
        window_dimentions = [1090, 751]
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(window_dimentions[0], window_dimentions[1])
        MainWindow.setMinimumSize(QtCore.QSize(window_dimentions[0], window_dimentions[1]))
        MainWindow.setMaximumSize(QtCore.QSize(window_dimentions[0], window_dimentions[1]))
        MainWindow.setFont(font_ee)
        MainWindow.setWindowIcon(QtGui.QIcon(self.current_dir + "\icon.png"))
        MainWindow.setIconSize(QtCore.QSize(30, 30))
        MainWindow.setWindowTitle("BoToFit")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Block: Data file and structure
        self.label_Data_file = QtWidgets.QLabel(self.centralwidget)
        self.label_Data_file.setGeometry(QtCore.QRect(20, 0, 191, 16))
        self.label_Data_file.setFont(font_headline)
        self.label_Data_file.setObjectName("label_Data_file")
        self.label_Data_file.setText("Data file and structure:")
        self.groupBox_Data_file = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Data_file.setGeometry(QtCore.QRect(10, 0, 661, 50))
        self.groupBox_Data_file.setObjectName("groupBox_Data_file")
        self.lineEdit_Data_file = QtWidgets.QLineEdit(self.groupBox_Data_file)
        self.lineEdit_Data_file.setGeometry(QtCore.QRect(5, 23, 370, 21))
        self.lineEdit_Data_file.setFont(font_ee)
        self.lineEdit_Data_file.setObjectName("lineEdit_Data_file")
        self.toolButton_Data_file = QtWidgets.QToolButton(self.groupBox_Data_file)
        self.toolButton_Data_file.setGeometry(QtCore.QRect(378, 23, 26, 21))
        self.toolButton_Data_file.setObjectName("toolButton_Data_file")
        self.toolButton_Data_file.setText("...")
        self.comboBox_Data_file_Column_1 = QtWidgets.QComboBox(self.groupBox_Data_file)
        self.comboBox_Data_file_Column_1.setGeometry(QtCore.QRect(435, 23, 71, 21))
        self.comboBox_Data_file_Column_1.setFont(font_ee)
        self.comboBox_Data_file_Column_1.setObjectName("comboBox_Data_file_Column_1")
        self.comboBox_Data_file_Column_2 = QtWidgets.QComboBox(self.groupBox_Data_file)
        self.comboBox_Data_file_Column_2.setGeometry(QtCore.QRect(510, 23, 71, 21))
        self.comboBox_Data_file_Column_2.setFont(font_ee)
        self.comboBox_Data_file_Column_2.setObjectName("comboBox_Data_file_Column_2")
        self.comboBox_Data_file_Column_3 = QtWidgets.QComboBox(self.groupBox_Data_file)
        self.comboBox_Data_file_Column_3.setGeometry(QtCore.QRect(585, 23, 71, 21))
        self.comboBox_Data_file_Column_3.setFont(font_ee)
        self.comboBox_Data_file_Column_3.setObjectName("comboBox_Data_file_Column_3")
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
        self.label_Start_fit_with.setGeometry(QtCore.QRect(20, 50, 141, 16))
        self.label_Start_fit_with.setFont(font_headline)
        self.label_Start_fit_with.setObjectName("label_Start_fit_with")
        self.label_Start_fit_with.setText("Start fit with:")
        self.groupBox_Start_fit_with = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Start_fit_with.setGeometry(QtCore.QRect(10, 50, 661, 289))
        self.groupBox_Start_fit_with.setObjectName("groupBox_Start_fit_with")
        self.tabWidget_Start_fit_with = QtWidgets.QTabWidget(self.groupBox_Start_fit_with)
        self.tabWidget_Start_fit_with.setGeometry(QtCore.QRect(1, 18, 660, 272))
        self.tabWidget_Start_fit_with.setFont(font_ee)
        self.tabWidget_Start_fit_with.setObjectName("tabWidget_Start_fit_with")

        # - tab "Film description"
        self.tab_Film_description = QtWidgets.QWidget()
        self.tab_Film_description.setObjectName("tab_Film_description")
        self.tabWidget_Start_fit_with.addTab(self.tab_Film_description, "")
        self.tabWidget_Start_fit_with.setTabText(self.tabWidget_Start_fit_with.indexOf(self.tab_Film_description), "Film description")
        self.tableWidget_Film_description = QtWidgets.QTableWidget(self.tab_Film_description)
        self.tableWidget_Film_description.setGeometry(QtCore.QRect(-2, -1, 660, 222))
        self.tableWidget_Film_description.setFont(font_ee)
        self.tableWidget_Film_description.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableWidget_Film_description.setObjectName("tableWidget_Film_description")
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
        self.pushButton_Film_description_Load_entry.setGeometry(QtCore.QRect(1, 223, 111, 20))
        self.pushButton_Film_description_Load_entry.setObjectName("pushButton_Film_description_Load_entry")
        self.pushButton_Film_description_Load_entry.setText("Load entry file")
        self.pushButton_Film_description_Add_layer = QtWidgets.QPushButton(self.tab_Film_description)
        self.pushButton_Film_description_Add_layer.setGeometry(QtCore.QRect(491, 223, 80, 20))
        self.pushButton_Film_description_Add_layer.setObjectName("pushButton_Film_description_Add_layer")
        self.pushButton_Film_description_Add_layer.setText("Add layer")
        self.pushButton_Film_description_Remove_layer = QtWidgets.QPushButton(self.tab_Film_description)
        self.pushButton_Film_description_Remove_layer.setGeometry(QtCore.QRect(575, 223, 80, 20))
        self.pushButton_Film_description_Remove_layer.setObjectName("pushButton_Film_description_Remove_layer")
        self.pushButton_Film_description_Remove_layer.setText("Remove layer")

        # - tab "Scan parameters"
        self.tab_Scan_parameters = QtWidgets.QWidget()
        self.tab_Scan_parameters.setObjectName("tab_Scan_parameters")
        self.tabWidget_Start_fit_with.addTab(self.tab_Scan_parameters, "")
        self.tabWidget_Start_fit_with.setTabText(self.tabWidget_Start_fit_with.indexOf(self.tab_Scan_parameters), "Scan parameters")
        self.label_Scan_parameters_Number_of_pts_for_resolution_function = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.label_Scan_parameters_Number_of_pts_for_resolution_function.setGeometry(QtCore.QRect(8, 9, 311, 17))
        self.label_Scan_parameters_Number_of_pts_for_resolution_function.setFont(font_ee)
        self.label_Scan_parameters_Number_of_pts_for_resolution_function.setObjectName("label_Scan_parameters_Number_of_pts_for_resolution_function")
        self.label_Scan_parameters_Number_of_pts_for_resolution_function.setText("Number of points for resolution function")
        self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function.setGeometry(QtCore.QRect(223, 9, 60, 17))
        self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function.setFont(font_ee)
        self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function.setObjectName("lineEdit_Scan_parameters_Number_of_pts_for_resolution_function")
        self.label_Scan_parameters_Step_for_resolution_function = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.label_Scan_parameters_Step_for_resolution_function.setGeometry(QtCore.QRect(8, 27, 291, 17))
        self.label_Scan_parameters_Step_for_resolution_function.setFont(font_ee)
        self.label_Scan_parameters_Step_for_resolution_function.setObjectName("label_Scan_parameters_Step_for_resolution_function")
        self.label_Scan_parameters_Step_for_resolution_function.setText("Step for resolution function (mrad)")
        self.lineEdit_Scan_parameters_Step_for_resolution_function = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.lineEdit_Scan_parameters_Step_for_resolution_function.setGeometry(QtCore.QRect(223, 27, 60, 17))
        self.lineEdit_Scan_parameters_Step_for_resolution_function.setFont(font_ee)
        self.lineEdit_Scan_parameters_Step_for_resolution_function.setObjectName("lineEdit_Scan_parameters_Step_for_resolution_function")
        self.label_Scan_parameters_Sigma = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.label_Scan_parameters_Sigma.setGeometry(QtCore.QRect(8, 45, 291, 17))
        self.label_Scan_parameters_Sigma.setFont(font_ee)
        self.label_Scan_parameters_Sigma.setObjectName("label_Scan_parameters_Sigma")
        self.label_Scan_parameters_Sigma.setText("\"Sigma\" of resolution function (mrad)")
        self.lineEdit_Scan_parameters_Sigma = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.lineEdit_Scan_parameters_Sigma.setGeometry(QtCore.QRect(223, 45, 60, 17))
        self.lineEdit_Scan_parameters_Sigma.setFont(font_ee)
        self.lineEdit_Scan_parameters_Sigma.setObjectName("lineEdit_Scan_parameters_Sigma")
        self.label_Scan_parameters_Zero_correction = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.label_Scan_parameters_Zero_correction.setGeometry(QtCore.QRect(8, 63, 281, 17))
        self.label_Scan_parameters_Zero_correction.setFont(font_ee)
        self.label_Scan_parameters_Zero_correction.setObjectName("label_Scan_parameters_Zero_correction")
        self.label_Scan_parameters_Zero_correction.setText("Correction of the detector \"zero\"")
        self.lineEdit_Scan_parameters_Zero_correction = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.lineEdit_Scan_parameters_Zero_correction.setGeometry(QtCore.QRect(223, 63, 60, 17))
        self.lineEdit_Scan_parameters_Zero_correction.setFont(font_ee)
        self.lineEdit_Scan_parameters_Zero_correction.setObjectName("lineEdit_Scan_parameters_Zero_correction")

        self.label_Scan_parameters_Wavelength = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.label_Scan_parameters_Wavelength.setGeometry(QtCore.QRect(350, 9, 131, 17))
        self.label_Scan_parameters_Wavelength.setFont(font_ee)
        self.label_Scan_parameters_Wavelength.setObjectName("label_Scan_parameters_Wavelength")
        self.label_Scan_parameters_Wavelength.setText("Wavelength (A)")
        self.lineEdit_Scan_parameters_Wavelength = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.lineEdit_Scan_parameters_Wavelength.setGeometry(QtCore.QRect(560, 9, 60, 17))
        self.lineEdit_Scan_parameters_Wavelength.setFont(font_ee)
        self.lineEdit_Scan_parameters_Wavelength.setObjectName("lineEdit_Scan_parameters_Wavelength")
        self.label_Scan_parameters_Scaling_factor = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.label_Scan_parameters_Scaling_factor.setGeometry(QtCore.QRect(350, 27, 101, 17))
        self.label_Scan_parameters_Scaling_factor.setFont(font_ee)
        self.label_Scan_parameters_Scaling_factor.setObjectName("label_Scan_parameters_Scaling_factor")
        self.label_Scan_parameters_Scaling_factor.setText("Scaling factor")
        self.lineEdit_Scan_parameters_Scaling_factor = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.lineEdit_Scan_parameters_Scaling_factor.setGeometry(QtCore.QRect(560, 27, 60, 17))
        self.lineEdit_Scan_parameters_Scaling_factor.setFont(font_ee)
        self.lineEdit_Scan_parameters_Scaling_factor.setPlaceholderText("")
        self.lineEdit_Scan_parameters_Scaling_factor.setObjectName("lineEdit_Scan_parameters_Scaling_factor")
        self.checkBox_Scan_parameters_Scaling_factor = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.checkBox_Scan_parameters_Scaling_factor.setGeometry(QtCore.QRect(623, 27, 20, 18))
        self.checkBox_Scan_parameters_Scaling_factor.setObjectName("checkBox_Scan_parameters_Scaling_factor")
        self.label_Scan_parameters_Background = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.label_Scan_parameters_Background.setGeometry(QtCore.QRect(350, 45, 91, 17))
        self.label_Scan_parameters_Background.setFont(font_ee)
        self.label_Scan_parameters_Background.setObjectName("label_Scan_parameters_Background")
        self.label_Scan_parameters_Background.setText("Background")
        self.lineEdit_Scan_parameters_Background = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.lineEdit_Scan_parameters_Background.setGeometry(QtCore.QRect(560, 45, 60, 17))
        self.lineEdit_Scan_parameters_Background.setFont(font_ee)
        self.lineEdit_Scan_parameters_Background.setObjectName("lineEdit_Scan_parameters_Background")
        self.checkBox_Scan_parameters_Background = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.checkBox_Scan_parameters_Background.setGeometry(QtCore.QRect(623, 45, 21, 18))
        self.checkBox_Scan_parameters_Background.setObjectName("checkBox_Scan_parameters_Background")
        self.label_Scan_parameters_Crossover_overillumination = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.label_Scan_parameters_Crossover_overillumination.setGeometry(QtCore.QRect(350, 63, 311, 17))
        self.label_Scan_parameters_Crossover_overillumination.setFont(font_ee)
        self.label_Scan_parameters_Crossover_overillumination.setObjectName("label_Scan_parameters_Crossover_overillumination")
        self.label_Scan_parameters_Crossover_overillumination.setText("Crossover angle overillumination (mrad)")
        self.lineEdit_Scan_parameters_Crossover_overillumination = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.lineEdit_Scan_parameters_Crossover_overillumination.setGeometry(QtCore.QRect(560, 63, 60, 17))
        self.lineEdit_Scan_parameters_Crossover_overillumination.setFont(font_ee)
        self.lineEdit_Scan_parameters_Crossover_overillumination.setObjectName("lineEdit_Scan_parameters_Crossover_overillumination")
        self.checkBox_Scan_parameters_Crossover_overillumination = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.checkBox_Scan_parameters_Crossover_overillumination.setGeometry(QtCore.QRect(623, 63, 21, 18))
        self.checkBox_Scan_parameters_Crossover_overillumination.setObjectName("checkBox_Scan_parameters_Crossover_overillumination")

        self.label_Scan_parameters_Points_to_exclude_First = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.label_Scan_parameters_Points_to_exclude_First.setGeometry(QtCore.QRect(8, 93, 191, 16))
        self.label_Scan_parameters_Points_to_exclude_First.setObjectName("label_Scan_parameters_Points_to_exclude_First")
        self.label_Scan_parameters_Points_to_exclude_First.setText("Number of first points to exclude")
        self.lineEdit_Scan_parameters_Points_to_exclude_First = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.lineEdit_Scan_parameters_Points_to_exclude_First.setGeometry(QtCore.QRect(188, 93, 60, 17))
        self.lineEdit_Scan_parameters_Points_to_exclude_First.setObjectName("lineEdit_Scan_parameters_Points_to_exclude_First")
        self.lineEdit_Scan_parameters_Points_to_exclude_First.setText("5")
        self.label_Scan_parameters_Points_to_exclude_Last = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.label_Scan_parameters_Points_to_exclude_Last.setGeometry(QtCore.QRect(8, 111, 191, 17))
        self.label_Scan_parameters_Points_to_exclude_Last.setObjectName("label_Scan_parameters_Points_to_exclude_Last")
        self.label_Scan_parameters_Points_to_exclude_Last.setText("Number of last points to exclude")
        self.lineEdit_Scan_parameters_Points_to_exclude_Last = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.lineEdit_Scan_parameters_Points_to_exclude_Last.setGeometry(QtCore.QRect(188, 111, 60, 17))
        self.lineEdit_Scan_parameters_Points_to_exclude_Last.setObjectName("lineEdit_Scan_parameters_Points_to_exclude_Last")
        self.lineEdit_Scan_parameters_Points_to_exclude_Last.setText("5")
        self.pushButton_Scan_parameters_Redraw_reflectivity = QtWidgets.QPushButton(self.tab_Scan_parameters)
        self.pushButton_Scan_parameters_Redraw_reflectivity.setGeometry(QtCore.QRect(256, 93, 121, 34))
        self.pushButton_Scan_parameters_Redraw_reflectivity.setObjectName("pushButton_Scan_parameters_Redraw_reflectivity")
        self.pushButton_Scan_parameters_Redraw_reflectivity.setText("Redraw reflectivity")

        self.label_Scan_parameters_Piy = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.label_Scan_parameters_Piy.setGeometry(QtCore.QRect(8, 144, 291, 17))
        self.label_Scan_parameters_Piy.setObjectName("label_Scan_parameters_Piy")
        self.label_Scan_parameters_Piy.setText("Piy incident polarization (polariser)")
        self.lineEdit_Scan_parameters_Piy = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.lineEdit_Scan_parameters_Piy.setGeometry(QtCore.QRect(268, 144, 60, 17))
        self.lineEdit_Scan_parameters_Piy.setObjectName("lineEdit_Scan_parameters_Piy")
        self.checkBox_Scan_parameters_Piy = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.checkBox_Scan_parameters_Piy.setGeometry(QtCore.QRect(332, 144, 21, 18))
        self.checkBox_Scan_parameters_Piy.setObjectName("checkBox_Scan_parameters_Piy")
        self.label_Scan_parameters_Pfy = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.label_Scan_parameters_Pfy.setGeometry(QtCore.QRect(8, 162, 251, 17))
        self.label_Scan_parameters_Pfy.setObjectName("label_Scan_parameters_Pfy")
        self.label_Scan_parameters_Pfy.setText("Pfy outgoing polarization (analyser)")
        self.lineEdit_Scan_parameters_Pfy = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.lineEdit_Scan_parameters_Pfy.setGeometry(QtCore.QRect(268, 162, 60, 17))
        self.lineEdit_Scan_parameters_Pfy.setObjectName("lineEdit_Scan_parameters_Pfy")
        self.checkBox_Scan_parameters_Pfy = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.checkBox_Scan_parameters_Pfy.setGeometry(QtCore.QRect(332, 162, 21, 18))
        self.checkBox_Scan_parameters_Pfy.setObjectName("checkBox_Scan_parameters_Pfy")
        self.label_Scan_parameters_Cg = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.label_Scan_parameters_Cg.setGeometry(QtCore.QRect(8, 180, 291, 17))
        self.label_Scan_parameters_Cg.setObjectName("label_Scan_parameters_Cg")
        self.label_Scan_parameters_Cg.setText("cg: mean value <cos(gamma)> of big domains")
        self.lineEdit_Scan_parameters_Cg = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.lineEdit_Scan_parameters_Cg.setGeometry(QtCore.QRect(268, 180, 60, 17))
        self.lineEdit_Scan_parameters_Cg.setObjectName("lineEdit_Scan_parameters_Cg")
        self.checkBox_Scan_parameters_Cg = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.checkBox_Scan_parameters_Cg.setGeometry(QtCore.QRect(332, 180, 21, 18))
        self.checkBox_Scan_parameters_Cg.setObjectName("checkBox_Scan_parameters_Cg")
        self.label_Scan_parameters_Sg = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.label_Scan_parameters_Sg.setGeometry(QtCore.QRect(8, 198, 291, 17))
        self.label_Scan_parameters_Sg.setObjectName("label_Scan_parameters_Sg")
        self.label_Scan_parameters_Sg.setText("sg: mean value <sin(gamma)> of big domains")
        self.lineEdit_Scan_parameters_Sg = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.lineEdit_Scan_parameters_Sg.setGeometry(QtCore.QRect(268, 198, 60, 17))
        self.lineEdit_Scan_parameters_Sg.setObjectName("lineEdit_Scan_parameters_Sg")
        self.checkBox_Scan_parameters_Sg = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.checkBox_Scan_parameters_Sg.setGeometry(QtCore.QRect(332, 198, 21, 18))
        self.checkBox_Scan_parameters_Sg.setObjectName("checkBox_Scan_parameters_Sg")
        self.label_Scan_parameters_Sg2 = QtWidgets.QLabel(self.tab_Scan_parameters)
        self.label_Scan_parameters_Sg2.setGeometry(QtCore.QRect(8, 216, 291, 17))
        self.label_Scan_parameters_Sg2.setObjectName("label_Scan_parameters_Sg2")
        self.label_Scan_parameters_Sg2.setText("sg2: mean value <sin^2(gamma)> of big domains")
        self.lineEdit_Scan_parameters_Sg2 = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.lineEdit_Scan_parameters_Sg2.setGeometry(QtCore.QRect(268, 216, 60, 17))
        self.lineEdit_Scan_parameters_Sg2.setObjectName("lineEdit_Scan_parameters_Sg2")
        self.checkBox_Scan_parameters_Sg2 = QtWidgets.QCheckBox(self.tab_Scan_parameters)
        self.checkBox_Scan_parameters_Sg2.setGeometry(QtCore.QRect(332, 216, 21, 18))
        self.checkBox_Scan_parameters_Sg2.setObjectName("checkBox_Scan_parameters_Sg2")

        self.tabWidget_Start_fit_with.setCurrentIndex(0)

        # Block: Save results at
        self.label_Save_at = QtWidgets.QLabel(self.centralwidget)
        self.label_Save_at.setFont(font_headline)
        self.label_Save_at.setGeometry(QtCore.QRect(20, 340, 151, 16))
        self.label_Save_at.setObjectName("label_Save_at")
        self.label_Save_at.setText("Save results at:")
        self.groupBox_Save_at = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Save_at.setGeometry(QtCore.QRect(10, 340, 531, 50))
        self.groupBox_Save_at.setObjectName("groupBox_Save_at")
        self.lineEdit_Save_at = QtWidgets.QLineEdit(self.groupBox_Save_at)
        self.lineEdit_Save_at.setGeometry(QtCore.QRect(5, 23, 491, 21))
        self.lineEdit_Save_at.setFont(font_ee)
        self.lineEdit_Save_at.setObjectName("lineEdit_Save_at")
        self.toolButton_Save_at = QtWidgets.QToolButton(self.groupBox_Save_at)
        self.toolButton_Save_at.setGeometry(QtCore.QRect(500, 23, 26, 21))
        self.toolButton_Save_at.setObjectName("toolButton_Save_at")
        self.toolButton_Save_at.setText("...")

        # Button: Start fitting
        self.pushButton_Start_fitting = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Start_fitting.setGeometry(QtCore.QRect(550, 358, 121, 32))
        self.pushButton_Start_fitting.setFont(font_headline)
        self.pushButton_Start_fitting.setObjectName("pushButton_Start_fitting")
        self.pushButton_Start_fitting.setText("Start Fitting")

        # Block: Fit results
        self.label_Fit_results = QtWidgets.QLabel(self.centralwidget)
        self.label_Fit_results.setFont(font_headline)
        self.label_Fit_results.setGeometry(QtCore.QRect(690, 0, 101, 16))
        self.label_Fit_results.setObjectName("label_Fit_results")
        self.label_Fit_results.setText("Fit results:")
        self.groupBox_Fit_results = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Fit_results.setGeometry(QtCore.QRect(680, 0, 401, 390))
        self.groupBox_Fit_results.setObjectName("groupBox_Fit_results")
        self.tableWidget_Fit_results = QtWidgets.QTableWidget(self.groupBox_Fit_results)
        self.tableWidget_Fit_results.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_Fit_results.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_Fit_results.setGeometry(QtCore.QRect(1, 48, 400, 318))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.tableWidget_Fit_results.setPalette(palette)
        self.tableWidget_Fit_results.setFont(font_ee)
        self.tableWidget_Fit_results.setObjectName("tableWidget_Fit_results")
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
        self.checkBox_Fit_results_Select_all.setGeometry(QtCore.QRect(self.tableWidget_Fit_results.columnWidth(0) / 9, 1, 14, 14))
        self.checkBox_Fit_results_Select_all.setObjectName("checkBox_Fit_results_Select_all")
        self.label_Fit_results_Number_of_iterations = QtWidgets.QLabel(self.groupBox_Fit_results)
        self.label_Fit_results_Number_of_iterations.setGeometry(QtCore.QRect(10, 18, 161, 31))
        self.label_Fit_results_Number_of_iterations.setObjectName("label_Fit_results_Number_of_iterations")
        self.label_Fit_results_Number_of_iterations.setText("Number of iterations:")
        self.lineEdit_Fit_results_Number_of_iterations = QtWidgets.QLineEdit(self.groupBox_Fit_results)
        self.lineEdit_Fit_results_Number_of_iterations.setGeometry(QtCore.QRect(120, 23, 40, 21))
        self.lineEdit_Fit_results_Number_of_iterations.setFont(font_ee)
        self.lineEdit_Fit_results_Number_of_iterations.setReadOnly(True)
        self.lineEdit_Fit_results_Number_of_iterations.setObjectName("lineEdit_Fit_results_Number_of_iterations")
        self.label_Fit_results_Chi_square = QtWidgets.QLabel(self.groupBox_Fit_results)
        self.label_Fit_results_Chi_square.setGeometry(QtCore.QRect(255, 18, 151, 31))
        self.label_Fit_results_Chi_square.setObjectName("label_Fit_results_Chi_square")
        self.label_Fit_results_Chi_square.setText("Chi_sq.norm:")
        self.lineEdit_Fit_results_Chi_square = QtWidgets.QLineEdit(self.groupBox_Fit_results)
        self.lineEdit_Fit_results_Chi_square.setGeometry(QtCore.QRect(326, 23, 70, 21))
        self.lineEdit_Fit_results_Chi_square.setFont(font_ee)
        self.lineEdit_Fit_results_Chi_square.setReadOnly(True)
        self.lineEdit_Fit_results_Chi_square.setObjectName("lineEdit_Fit_results_Chi_square")
        self.pushButton_Fit_results_Copy_to_Start_fit_with = QtWidgets.QPushButton(self.groupBox_Fit_results)
        self.pushButton_Fit_results_Copy_to_Start_fit_with.setGeometry(QtCore.QRect(5, 368, 392, 19))
        self.pushButton_Fit_results_Copy_to_Start_fit_with.setObjectName("pushButton_Fit_results_Copy_to_Start_fit_with")
        self.pushButton_Fit_results_Copy_to_Start_fit_with.setText("Use selected (#) values as 'Start fit with' parameters")

        # Block: Reflectivity profile and Difference
        self.label_Reflectivity_profile_and_Diff = QtWidgets.QLabel(self.centralwidget)
        self.label_Reflectivity_profile_and_Diff.setFont(font_headline)
        self.label_Reflectivity_profile_and_Diff.setGeometry(QtCore.QRect(20, 393, 541, 16))
        self.label_Reflectivity_profile_and_Diff.setObjectName("label_Reflectivity_profile_and_Diff")
        self.label_Reflectivity_profile_and_Diff.setText("Reflectivity profile (I[10e] vs. Qz[Å**-1]) and Difference (Exper/Fit):")
        self.groupBox_Reflectivity_profile = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Reflectivity_profile.setGeometry(QtCore.QRect(10, 393, 660, 316))
        self.groupBox_Reflectivity_profile.setObjectName("groupBox_Reflectivity_profile")
        self.graphicsView_Reflectivity_profile = pg.PlotWidget(self.groupBox_Reflectivity_profile, viewBox=pg.ViewBox())
        self.graphicsView_Reflectivity_profile.setGeometry(QtCore.QRect(2, 19, 657, 205))
        self.graphicsView_Reflectivity_profile.setObjectName("graphicsView_Reflectivity_profile")
        self.graphicsView_Reflectivity_profile.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_Reflectivity_profile.getAxis("bottom").setStyle(showValues=False)
        self.graphicsView_Reflectivity_profile.getAxis("left").tickFont = font_graphs
        self.graphicsView_Reflectivity_profile.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_Reflectivity_profile.showAxis("top")
        self.graphicsView_Reflectivity_profile.getAxis("top").setTicks([])
        self.graphicsView_Reflectivity_profile.showAxis("right")
        self.graphicsView_Reflectivity_profile.getAxis("right").setTicks([])
        self.graphicsView_Diff = pg.PlotWidget(self.groupBox_Reflectivity_profile, viewBox=pg.ViewBox())
        self.graphicsView_Diff.setGeometry(QtCore.QRect(2, 224, 657, 91))
        self.graphicsView_Diff.setObjectName("graphicsView_Diff")
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
        self.label_Sld_profile.setFont(font_headline)
        self.label_Sld_profile.setGeometry(QtCore.QRect(690, 393, 481, 16))
        self.label_Sld_profile.setObjectName("label_Sld_profile")
        self.label_Sld_profile.setText("SLD profile (SLD [in Å**-2, *10e6] vs. Distance from interface [Å]:")
        self.groupBox_Sld_profile = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Sld_profile.setGeometry(QtCore.QRect(680, 393, 401, 316))
        self.groupBox_Sld_profile.setObjectName("groupBox_Sld_profile")
        MainWindow.setCentralWidget(self.centralwidget)
        self.graphicsView_Sld_profile = pg.PlotWidget(self.groupBox_Sld_profile)
        self.graphicsView_Sld_profile.setGeometry(QtCore.QRect(2, 19, 398, 296))
        self.graphicsView_Sld_profile.setObjectName("graphicsView_Sld_profile")
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
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1229, 29))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1228, 26))
        self.menuBar.setObjectName("menuBar")
        self.menu_MenuBar = QtWidgets.QMenu(self.menuBar)
        self.menu_MenuBar.setObjectName("menu_MenuBar")
        self.menu_MenuBar.setTitle("Mode")
        self.menuBar.addAction(self.menu_MenuBar.menuAction())
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuHelp.setTitle("Help")
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.actionVersion = QtWidgets.QAction(MainWindow)
        self.actionVersion.setCheckable(False)
        self.actionVersion.setObjectName("actionVersion")
        self.actionVersion.setText("V1.1")
        self.menuHelp.addAction(self.actionVersion)
        MainWindow.setMenuBar(self.menuBar)
        self.menu_Mono = QtWidgets.QMenu(self.menu_MenuBar)
        self.menu_Mono.setObjectName("menu_Mono")
        self.menu_Mono.setTitle("Mono")
        self.menu_MenuBar.addAction(self.menu_Mono.menuAction())
        self.menu_Tof = QtWidgets.QMenu(self.menu_MenuBar)
        self.menu_Tof.setObjectName("menu_Tof")
        self.menu_Tof.setTitle("TOF")
        self.menu_MenuBar.addAction(self.menu_Tof.menuAction())
        self.action_Mono_No_polarisation = QtWidgets.QAction(MainWindow)
        self.action_Mono_No_polarisation.setCheckable(True)
        self.action_Mono_No_polarisation.setChecked(True)
        self.action_Mono_No_polarisation.setObjectName("action_Mono_No_polarisation")
        self.action_Mono_No_polarisation.setText("No polarisation")
        self.menu_Mono.addAction(self.action_Mono_No_polarisation)
        self.action_Mono_2_polarisations = QtWidgets.QAction(MainWindow)
        self.action_Mono_2_polarisations.setCheckable(True)
        self.action_Mono_2_polarisations.setEnabled(True)
        self.action_Mono_2_polarisations.setObjectName("action_Mono_2_polarisations")
        self.action_Mono_2_polarisations.setText("2 polarisations")
        self.menu_Mono.addAction(self.action_Mono_2_polarisations)
        self.action_Mono_4_polarisations = QtWidgets.QAction(MainWindow)
        self.action_Mono_4_polarisations.setCheckable(True)
        self.action_Mono_4_polarisations.setEnabled(True)
        self.action_Mono_4_polarisations.setObjectName("action_Mono_4_polarisations")
        self.action_Mono_4_polarisations.setText("4 polarisations")
        self.menu_Mono.addAction(self.action_Mono_4_polarisations)
        self.action_Tof_No_polarisation = QtWidgets.QAction(MainWindow)
        self.action_Tof_No_polarisation.setCheckable(True)
        self.action_Tof_No_polarisation.setEnabled(True)
        self.action_Tof_No_polarisation.setObjectName("action_Tof_No_polarisation")
        self.action_Tof_No_polarisation.setText("No polarisation")
        self.menu_Tof.addAction(self.action_Tof_No_polarisation)
        self.action_Tof_2_polarisations = QtWidgets.QAction(MainWindow)
        self.action_Tof_2_polarisations.setCheckable(True)
        self.action_Tof_2_polarisations.setEnabled(True)
        self.action_Tof_2_polarisations.setObjectName("action_Tof_2_polarisations")
        self.action_Tof_2_polarisations.setText("2 polarisations")
        self.menu_Tof.addAction(self.action_Tof_2_polarisations)
        self.action_Tof_4_polarisations = QtWidgets.QAction(MainWindow)
        self.action_Tof_4_polarisations.setCheckable(True)
        self.action_Tof_4_polarisations.setEnabled(True)
        self.action_Tof_4_polarisations.setObjectName("action_Tof_4_polarisations")
        self.action_Tof_4_polarisations.setText("4 polarisations")
        self.menu_Tof.addAction(self.action_Tof_4_polarisations)

        # Statusbar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # lineEdit_Number_of_points and tableWidget_Data_points are hidden from the user. Used to avoid reopenning data file multiple times
        self.lineEdit_Number_of_points = QtWidgets.QLineEdit(self.tab_Scan_parameters)
        self.lineEdit_Number_of_points.setEnabled(False)
        self.lineEdit_Number_of_points.setGeometry(QtCore.QRect(570, 290, 0, 0))
        self.lineEdit_Number_of_points.setObjectName("lineEdit_Number_of_points")

        self.tableWidget_Data_points = QtWidgets.QTableWidget(self.tab_Scan_parameters)
        self.tableWidget_Data_points.setEnabled(False)
        self.tableWidget_Data_points.setGeometry(QtCore.QRect(460, 200, 0, 0))
        self.tableWidget_Data_points.setObjectName("tableWidget_Data_points")
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
        self.MODE_SPECS = [["Film500x0.exe", "FitFunct.dat", "UserDefaults_nopol.dat"],
                      ["Film500x2.exe", "Fit2DFunctDD.dat", "UserDefaults_2pol.dat"],
                      ["Film500x4.exe", "Fit2DFunctDD.dat", "UserDefaults_4pol.dat"],
                      ["FilmTOF500QX0.exe", "FitFunct.dat", "UserDefaults_TOF_nopol.dat"],
                      ["FilmTOF500QX2.exe", "Fit2DFunctDD.dat", "UserDefaults_TOF_2pol.dat"],
                      ["FilmTOF500QX4.exe", "Fit2DFunctDD.dat", "UserDefaults_TOF_4pol.dat"]
                      ]

        if action_mode == "action_Mono_No_polarisation":
            self.BoToFit_mode = 0

            self.action_Mono_No_polarisation.setChecked(True)
            self.action_Mono_2_polarisations.setChecked(False)
            self.action_Mono_4_polarisations.setChecked(False)
            self.action_Tof_No_polarisation.setChecked(False)
            self.action_Tof_2_polarisations.setChecked(False)
            self.action_Tof_4_polarisations.setChecked(False)

        elif action_mode == "action_Mono_2_polarisations":
            self.BoToFit_mode = 1

            self.action_Mono_No_polarisation.setChecked(False)
            self.action_Mono_2_polarisations.setChecked(True)
            self.action_Mono_4_polarisations.setChecked(False)
            self.action_Tof_No_polarisation.setChecked(False)
            self.action_Tof_2_polarisations.setChecked(False)
            self.action_Tof_4_polarisations.setChecked(False)

        elif action_mode == "action_Mono_4_polarisations":
            self.BoToFit_mode = 2

            self.action_Mono_No_polarisation.setChecked(False)
            self.action_Mono_2_polarisations.setChecked(False)
            self.action_Mono_4_polarisations.setChecked(True)
            self.action_Tof_No_polarisation.setChecked(False)
            self.action_Tof_2_polarisations.setChecked(False)
            self.action_Tof_4_polarisations.setChecked(False)

        elif action_mode == "action_Tof_No_polarisation":
            self.BoToFit_mode = 3

            self.action_Mono_No_polarisation.setChecked(False)
            self.action_Mono_2_polarisations.setChecked(False)
            self.action_Mono_4_polarisations.setChecked(False)
            self.action_Tof_No_polarisation.setChecked(True)
            self.action_Tof_2_polarisations.setChecked(False)
            self.action_Tof_4_polarisations.setChecked(False)

        elif action_mode == "action_Tof_2_polarisations":
            self.BoToFit_mode = 4

            self.action_Mono_No_polarisation.setChecked(False)
            self.action_Mono_2_polarisations.setChecked(False)
            self.action_Mono_4_polarisations.setChecked(False)
            self.action_Tof_No_polarisation.setChecked(False)
            self.action_Tof_2_polarisations.setChecked(True)
            self.action_Tof_4_polarisations.setChecked(False)

        elif action_mode == "action_Tof_4_polarisations":
            self.BoToFit_mode = 5

            self.action_Mono_No_polarisation.setChecked(False)
            self.action_Mono_2_polarisations.setChecked(False)
            self.action_Mono_4_polarisations.setChecked(False)
            self.action_Tof_No_polarisation.setChecked(False)
            self.action_Tof_2_polarisations.setChecked(False)
            self.action_Tof_4_polarisations.setChecked(True)

        # reformat table and polarisation parameters
        if self.BoToFit_mode in [0, 3]:
            self.label_Scan_parameters_Piy.setEnabled(False)
            self.lineEdit_Scan_parameters_Piy.setEnabled(False)
            self.checkBox_Scan_parameters_Piy.setEnabled(False)

            self.label_Scan_parameters_Pfy.setEnabled(False)
            self.lineEdit_Scan_parameters_Pfy.setEnabled(False)
            self.checkBox_Scan_parameters_Pfy.setEnabled(False)

            self.label_Scan_parameters_Pfy.setEnabled(False)
            self.lineEdit_Scan_parameters_Pfy.setEnabled(False)
            self.checkBox_Scan_parameters_Pfy.setEnabled(False)

            self.label_Scan_parameters_Cg.setEnabled(False)
            self.lineEdit_Scan_parameters_Cg.setEnabled(False)
            self.checkBox_Scan_parameters_Cg.setEnabled(False)

            self.label_Scan_parameters_Sg.setEnabled(False)
            self.lineEdit_Scan_parameters_Sg.setEnabled(False)
            self.checkBox_Scan_parameters_Sg.setEnabled(False)

            self.label_Scan_parameters_Sg2.setEnabled(False)
            self.lineEdit_Scan_parameters_Sg2.setEnabled(False)
            self.checkBox_Scan_parameters_Sg2.setEnabled(False)

            # columns with checkboxes can change their width depends on Windows scaling settings, so we correct our table
            col_width = [106, 106, 1, 106, 1, 106, 1, 0, 0, 0, 0, 106, 1]
            for i in range(0, 13):
                self.tableWidget_Film_description.setColumnWidth(i, col_width[i])

        elif self.BoToFit_mode in [1, 2, 4, 5]:
            self.label_Scan_parameters_Piy.setEnabled(True)
            self.lineEdit_Scan_parameters_Piy.setEnabled(True)
            self.checkBox_Scan_parameters_Piy.setEnabled(True)

            self.label_Scan_parameters_Pfy.setEnabled(True)
            self.lineEdit_Scan_parameters_Pfy.setEnabled(True)
            self.checkBox_Scan_parameters_Pfy.setEnabled(True)

            self.label_Scan_parameters_Pfy.setEnabled(True)
            self.lineEdit_Scan_parameters_Pfy.setEnabled(True)
            self.checkBox_Scan_parameters_Pfy.setEnabled(True)

            self.label_Scan_parameters_Cg.setEnabled(True)
            self.lineEdit_Scan_parameters_Cg.setEnabled(True)
            self.checkBox_Scan_parameters_Cg.setEnabled(True)

            self.label_Scan_parameters_Sg.setEnabled(True)
            self.lineEdit_Scan_parameters_Sg.setEnabled(True)
            self.checkBox_Scan_parameters_Sg.setEnabled(True)

            self.label_Scan_parameters_Sg2.setEnabled(True)
            self.lineEdit_Scan_parameters_Sg2.setEnabled(True)
            self.checkBox_Scan_parameters_Sg2.setEnabled(True)

            # columns with checkboxes can change their width depends on Windows scaling settings, so we correct our table
            col_width = [65, 73, 1, 59, 1, 59, 1, 59, 1, 81, 1, 75, 1]
            for i in range(0, 13):
                self.tableWidget_Film_description.setColumnWidth(i, col_width[i])

        # reformat checkboxes (I, dI, Qz, rad) and Wavelength/Inc.angle field
        if self.BoToFit_mode in [0, 1, 2]:
            if self.comboBox_Data_file_Column_1.count() < 4:
                self.comboBox_Data_file_Column_1.addItem("")
                self.comboBox_Data_file_Column_1.setItemText(3, "ang(rad)")
                self.comboBox_Data_file_Column_2.addItem("")
                self.comboBox_Data_file_Column_2.setItemText(3, "ang(rad)")
                self.comboBox_Data_file_Column_3.addItem("")
                self.comboBox_Data_file_Column_3.setItemText(3, "ang(rad)")
            self.label_Scan_parameters_Wavelength.setText("Wavelength (A)")

        elif self.BoToFit_mode in [3, 4, 5]:
            self.comboBox_Data_file_Column_1.removeItem(3)
            self.comboBox_Data_file_Column_2.removeItem(3)
            self.comboBox_Data_file_Column_3.removeItem(3)
            self.label_Scan_parameters_Wavelength.setText("Inc. ang. (mrad)")

        # load UserDefaults if such are presented
        try:
            if self.MODE_SPECS[self.BoToFit_mode][2] in os.listdir(self.current_dir + "/User_Defaults"):
                self.lineEdit_Scan_parameters_Wavelength.setText("")
                self.load_entry_file()
        except:
            print("No 'User Defaults' found")

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

        if self.BoToFit_mode in [0, 3]:
            data_files = QtWidgets.QFileDialog().getOpenFileName(None, "FileNames", self.current_dir)
        else: data_files = QtWidgets.QFileDialog().getOpenFileNames(None, "FileNames", self.current_dir)

        if data_files[0] == "": return

        self.lineEdit_Data_file.setText(str(data_files[0]))

        # clear stuff after last run
        self.clear_stuff()
        self.tableWidget_Data_points.clear()
        self.lineEdit_Number_of_points.clear()

        if self.BoToFit_mode in [0, 1, 2] and self.lineEdit_Scan_parameters_Wavelength.text() == "":
            self.statusbar.showMessage("Input wavelength and reimport the file")
        else:
            self.parse_Data_files()
            self.draw_reflectivity()

    def buttons_add_remove_layer(self):

        # check where we came from do required action
        try:
            sender_name = self.sender().objectName()
        except:
            sender_name = "None"

        if sender_name == "pushButton_Film_description_Remove_layer":
            # remove lines from {tableWidget_Film_description}
            if not self.tableWidget_Film_description.rowCount() == self.tableWidget_Film_description.currentRow() + 1:
                self.tableWidget_Film_description.removeRow(self.tableWidget_Film_description.currentRow())

        else:
            # add lines into {tableWidget_Film_description}
            if self.tableWidget_Film_description.currentRow() >= 0:
                i = self.tableWidget_Film_description.currentRow()
            else:
                i = 0

            self.tableWidget_Film_description.insertRow(i)
            self.tableWidget_Film_description.setRowHeight(i, 21)

            for j in range(0, 13):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                if j in (2, 4, 6, 8, 10, 12):
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    if j == 6:
                        item.setCheckState(QtCore.Qt.Checked)
                    else:
                        item.setCheckState(QtCore.Qt.Unchecked)

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
                start_fit_table_row = self.tableWidget_Film_description.rowCount() - 1
                index = 1
                if len(parameter) == 3:
                    start_fit_table_row = int(parameter[1]) - 1
                    index = 2

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
        if not self.BoToFit_mode in [0, 3]:
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
        except:
            print("Nothing to delete (SLD_profile.dat)")

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

        if "ang(Qz)" in self.input_structure and self.BoToFit_mode in [0, 1, 2]: self.export_for_user()
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

        if self.BoToFit_mode in [0, 3]:
            files.append(self.lineEdit_Data_file.text())
        else:
            for i in self.lineEdit_Data_file.text().split("'"):
                if i.rfind("_uu") > 0 or i.rfind("_UU") > 0: files.append(i)

            if self.BoToFit_mode in [2, 5]:

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
            exper_points_number = 0
            data_angle = []
            data_I = []
            data_dI = []

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

        row = 0
        col = 1
        scaling_fact_line = piy_line = pfy_line = wavelength_line = cg_line = -1000

        with open(str(entry_file), "r") as file:
            for line_number, line in enumerate(file.readlines()):
                if not self.BoToFit_mode == 0 and not self.BoToFit_mode == 3 :
                    # Piy incident polarization (polariser)
                    if line.rfind("Piy") > 0:
                        self.lineEdit_Scan_parameters_Piy.setText(line.split()[0])
                        piy_line = line_number + 1
                    if line_number == piy_line:
                        if line.split()[0] == "n": self.checkBox_Scan_parameters_Piy.setCheckState(0)
                        elif line.split()[0] == "f": self.checkBox_Scan_parameters_Piy.setCheckState(2)

                    # Pfy outgoing polarization (analyser)
                    if line.rfind("Pfy") > 0:
                        self.lineEdit_Scan_parameters_Pfy.setText(line.split()[0])
                        pfy_line = line_number + 1
                    if line_number == pfy_line:
                        if line.split()[0] == "n": self.checkBox_Scan_parameters_Pfy.setCheckState(0)
                        elif line.split()[0] == "f": self.checkBox_Scan_parameters_Pfy.setCheckState(2)

                    # cg: mean value <cos(gamma)> over big domains
                    if line.rfind("cos(gamma)") > 0:
                        self.lineEdit_Scan_parameters_Cg.setText(line.split()[0])
                        cg_line = line_number + 1
                    if line_number == cg_line:
                        if line.split()[0] == "n": self.checkBox_Scan_parameters_Cg.setCheckState(0)
                        elif line.split()[0] == "f": self.checkBox_Scan_parameters_Cg.setCheckState(2)
                    # sg: mean value <sin(gamma)> over big domains
                    if line_number == cg_line + 1: self.lineEdit_Scan_parameters_Sg.setText(line.split()[0])
                    if line_number == cg_line + 2:
                        if line.split()[0] == "n": self.checkBox_Scan_parameters_Sg.setCheckState(0)
                        elif line.split()[0] == "f": self.checkBox_Scan_parameters_Sg.setCheckState(2)
                    # sg2: mean value <sin^2(gamma)> over big domains
                    if line_number == cg_line + 3: self.lineEdit_Scan_parameters_Sg2.setText(line.split()[0])
                    if line_number == cg_line + 4:
                        if line.split()[0] == "n": self.checkBox_Scan_parameters_Sg2.setCheckState(0)
                        elif line.split()[0] == "f": self.checkBox_Scan_parameters_Sg2.setCheckState(2)

                # wavelength or incident angle
                '''
                BoToFit entry is almost the same for Mono and TOF modes.
                The only difference is that "incident angle" is used instead of "wavelength".
                '''
                if line.rfind("wavelength") > 0 or line.rfind("incident angle") > 0:
                    self.lineEdit_Scan_parameters_Wavelength.setText(line.split()[0])
                    wavelength_line = line_number

                # number of experimental points in alpha
                if line_number == wavelength_line + 2: self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function.setText(
                    line.split()[0])
                # step for resolution function (in mrad)
                if line_number == wavelength_line + 3: self.lineEdit_Scan_parameters_Step_for_resolution_function.setText(line.split()[0])
                # "sigma" of resolution function (in mrad)
                if line_number == wavelength_line + 4: self.lineEdit_Scan_parameters_Sigma.setText(line.split()[0])
                # correction of the detector 'zero' (in mrad): alpha-da
                if line.rfind("correction of the") > 0: self.lineEdit_Scan_parameters_Zero_correction.setText(
                    line.split()[0])

                # ct  total scaling factor
                if line.rfind("scaling factor") > 0:
                    self.lineEdit_Scan_parameters_Scaling_factor.setText(line.split()[0])
                    scaling_fact_line = line_number + 1
                if line_number == scaling_fact_line:
                    if line.split()[0] == "n":
                        self.checkBox_Scan_parameters_Scaling_factor.setCheckState(0)
                    elif line.split()[0] == "f":
                        self.checkBox_Scan_parameters_Scaling_factor.setCheckState(2)
                # alpha_0 crossover angle overillumination (in mrad)
                if line_number == scaling_fact_line + 1: self.lineEdit_Scan_parameters_Crossover_overillumination.setText(line.split()[0])
                if line_number == scaling_fact_line + 2:
                    if line.split()[0] == "n":
                        self.checkBox_Scan_parameters_Crossover_overillumination.setCheckState(0)
                    elif line.split()[0] == "f":
                        self.checkBox_Scan_parameters_Crossover_overillumination.setCheckState(2)
                # bgr 'background'
                if line_number == scaling_fact_line + 3: self.lineEdit_Scan_parameters_Background.setText(line.split()[0])
                if line_number == scaling_fact_line + 4:
                    if line.split()[0] == "n":
                        self.checkBox_Scan_parameters_Background.setCheckState(0)
                    elif line.split()[0] == "f":
                        self.checkBox_Scan_parameters_Background.setCheckState(2)

                if line.rfind("number of layers") > 0:
                    number_of_layers = int(line.split()[0])  # excluding substrate
                    layers_description_line = line_number
                    # delete all layers except substrate
                    while not self.tableWidget_Film_description.item(0, 0).text() == "substrate":
                        self.tableWidget_Film_description.removeRow(0)
                    # add i layers
                    for i in range(0, number_of_layers):
                        self.buttons_add_remove_layer()
                        self.tableWidget_Film_description.item(0, 0).setText("Layer " + str(number_of_layers - i))

                try:
                    if line_number > layers_description_line + 1 and not line == "":

                        # I hide 4 columns in NoPol mode, so we skip them
                        if self.BoToFit_mode in [0, 3] and col == 7: col = 11

                        if col <= 12 and row <= number_of_layers:
                            if line.split()[0] == "n":
                                self.tableWidget_Film_description.item(row, col).setCheckState(0)
                            elif line.split()[0] == "f":
                                self.tableWidget_Film_description.item(row, col).setCheckState(2)
                            else:
                                self.tableWidget_Film_description.item(row, col).setText(line.split()[0].replace("d", "e"))

                            col += 1
                            if col > 12 and row < number_of_layers:  # every layer has 12 rows to fill
                                col = 1
                                row += 1

                            if col == 1 and row == number_of_layers:  # then we fill substrate layer
                                col = 3

                except:
                    a = 1  # print("load_entry_file - skip this : " + line)

    def create_entry_for_BoToFit(self):
        '''
        BoToFit needs its own entry file, so we make one using data from the table
        '''

        with open(self.data_folder_name + 'entry.dat', 'w') as entry_file:

            if self.BoToFit_mode not in [0, 3]:
                # incident polarization (polariser)
                entry_file.write("0     Pix incident polarization (polariser)\nf\n")
                entry_file.write(self.lineEdit_Scan_parameters_Piy.text() + '    Piy\n')
                if self.checkBox_Scan_parameters_Piy.isChecked(): entry_file.write("f" + "   \n")
                else: entry_file.write("n" + "   \n")
                entry_file.write("0     Piz\nf\n\n")

                # outgoing polarization (analyser)
                entry_file.write("0     Pfx outgoing polarization (analyser)\nf\n")
                entry_file.write(self.lineEdit_Scan_parameters_Pfy.text() + '    Pfy\n')
                if self.checkBox_Scan_parameters_Pfy.isChecked():
                    entry_file.write("f" + "   \n")
                else:
                    entry_file.write("n" + "   \n")
                entry_file.write("0     Pfz\nf\n\n")

            if not self.BoToFit_mode in [3, 4, 5]:
                entry_file.write(self.lineEdit_Scan_parameters_Wavelength.text() + '    wavelength (in Angstrem)\n')
            else:
                entry_file.write(self.lineEdit_Scan_parameters_Wavelength.text() + '    incident angle (in mrad)\n')

            entry_file.write(self.lineEdit_Number_of_points.text() + "   *nn number of experimental points in alpha (<1001)\n")
            entry_file.write(self.lineEdit_Scan_parameters_Number_of_pts_for_resolution_function.text() + "    *j0 number of points for resolution function (odd) (<102)\n")
            entry_file.write(self.lineEdit_Scan_parameters_Step_for_resolution_function.text() + "    step for resolution function (in mrad)\n")
            entry_file.write(self.lineEdit_Scan_parameters_Sigma.text() + "     *sigma of resolution function (in mrad)\n\n")
            entry_file.write(str(self.tableWidget_Film_description.rowCount() - 1) + "   number of layers (excluding substrate) (<21)\n\n")
            # read the table
            for i in range(0, self.tableWidget_Film_description.rowCount()):
                comment = ""
                # Thickness
                if not self.tableWidget_Film_description.item(i, 0).text() == "substrate":
                    entry_file.write(self.tableWidget_Film_description.item(i, 1).text() + "    layer " + str(i+1) + " ("+ self.tableWidget_Film_description.item(i, 0).text() + ") thickness (in A)\n")
                    if self.tableWidget_Film_description.item(i, 2).checkState() == 2: entry_file.write("f" + "   \n")
                    else: entry_file.write("n" + "   \n")
                else: comment = "substrate's"
                # SLD
                entry_file.write(self.tableWidget_Film_description.item(i, 3).text() + "    " + comment + " nbr nuclear SLD Nb'  (in A**-2) *1e6\n")
                if self.tableWidget_Film_description.item(i, 4).checkState() == 2: entry_file.write("f" + "   \n")
                else: entry_file.write("n" + "   \n")
                # iSDL
                entry_file.write(self.tableWidget_Film_description.item(i, 5).text() + "    " + comment + " nbi nuclear SLD Nb'' (in A**-2) *1e6\n")
                if self.tableWidget_Film_description.item(i, 6).checkState() == 2: entry_file.write("f" + "   \n")
                else: entry_file.write("n" + "   \n")

                if self.BoToFit_mode not in [0, 3]:
                    # magnetic SLD
                    entry_file.write(self.tableWidget_Film_description.item(i, 7).text() + "    magnetic SLD Np (in A**-2)*1e6\n")
                    if self.tableWidget_Film_description.item(i, 8).checkState() == 2: entry_file.write("f\n")
                    else: entry_file.write("n\n")
                    # c=<cos(delta_gamma)>
                    entry_file.write(self.tableWidget_Film_description.item(i, 9).text() + "    c=<cos(delta_gamma)>\n")
                    if self.tableWidget_Film_description.item(i, 10).checkState() == 2: entry_file.write("f\n")
                    else: entry_file.write("n\n")

                # roughness
                entry_file.write(self.tableWidget_Film_description.item(i, 11).text() + "    dw Debye-Waller in [AA]\n")
                if self.tableWidget_Film_description.item(i, 12).checkState() == 2: entry_file.write("f\n\n")
                else: entry_file.write("n\n\n")

            if self.BoToFit_mode not in [0, 3]:
                # cg
                entry_file.write(self.lineEdit_Scan_parameters_Cg.text() + '    cg: mean value <cos(gamma)> over big domains\n')
                if self.checkBox_Scan_parameters_Cg.isChecked(): entry_file.write("f" + "   \n")
                else: entry_file.write("n" + "   \n")
                # sg
                entry_file.write(self.lineEdit_Scan_parameters_Sg.text() + '    sg: mean value <sin(gamma)> over big domains\n')
                if self.checkBox_Scan_parameters_Sg.isChecked(): entry_file.write("f" + "   \n")
                else: entry_file.write("n" + "   \n")
                # sg2
                entry_file.write(self.lineEdit_Scan_parameters_Sg2.text() + '    sg2: mean value <sin^2(gamma)> over big domains\n')
                if self.checkBox_Scan_parameters_Sg2.isChecked(): entry_file.write("f" + "  \n\n")
                else: entry_file.write("n" + "   \n\n")

            # ct - total scaling factor
            entry_file.write(self.lineEdit_Scan_parameters_Scaling_factor.text() + "   *ct  total scaling factor\n")
            if self.checkBox_Scan_parameters_Scaling_factor.isChecked(): entry_file.write("f" + "   \n")
            else: entry_file.write("n" + "   \n")
            # alpha_0 crossover angle overillumination
            entry_file.write(self.lineEdit_Scan_parameters_Crossover_overillumination.text() + "   *alpha_0 crossover angle overillumination (in mrad)\n")
            if self.checkBox_Scan_parameters_Crossover_overillumination.isChecked(): entry_file.write("f" + "   \n")
            else: entry_file.write("n" + "   \n")
            # background
            entry_file.write(self.lineEdit_Scan_parameters_Background.text() + "   *bgr background\n")
            if self.checkBox_Scan_parameters_Background.isChecked(): entry_file.write("f" + "   \n")
            else: entry_file.write("n" + "   \n")
            # correction of the detector 'zero'
            entry_file.write("\n" + self.lineEdit_Scan_parameters_Zero_correction.text() + "   correction of the detector 'zero' (in mrad)\n")
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
        fit_file_name = "Fit2DBag.dat" if not self.BoToFit_mode in [0, 3] else "FitBag.dat"

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

                            except: a = 1 # print("create_Fit_results_table_error_1")
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

                    except: a = 1 #print("create_Fit_results_table_error_2 - skip this : " + line)

        for i in range(0, len(multiGrPr_data)):
            for j in range(0, len(multiGrPr_data[i])):
                multiGrPr.write(str(multiGrPr_data[i][j]) + "     " + str(multiGrPr_info[i][j]) + "\n")
            multiGrPr.write("\n")

        multiGrPr.close()
    ##<--

    ##--> draw graphs
    def draw_reflectivity(self):

        if self.sender().objectName() == "pushButton_Scan_parameters_Redraw_reflectivity":
            self.graphicsView_Reflectivity_profile.getPlotItem().clear()

        '''
        draw reflectivity in Angle vs. lg(I) scale using data from hidden table
        '''
        color = [0, 0, 0]

        if "ang(Qz)" in self.input_structure:
            self.label_Reflectivity_profile_and_Diff.setText("Reflectivity profile (I[10e] vs. Qz[Å**-1]) and Difference (Exper/Fit):")
        elif "ang(rad)" in self.input_structure:
            self.label_Reflectivity_profile_and_Diff.setText("Reflectivity profile (I[10e] vs. Angle[mrad]) and Difference (Exper/Fit):")

        # if tableWidget_Data_points is empty - do nothing
        try:
            self.tableWidget_Data_points.item(0, 0).text()
        except:
            return

        for i in range(0, 4):
            if self.tableWidget_Data_points.item(i, 0).text() not in ("", "[]"):
                data_angle = self.tableWidget_Data_points.item(i, 0).text()[1: -1].replace(",", "").split()
                data_I = self.tableWidget_Data_points.item(i, 1).text()[1: -1].replace(",", "").split()
                data_dI = self.tableWidget_Data_points.item(i, 2).text()[1: -1].replace(",", "").split()

                # change color from black when 2 or 4 polarisations
                if self.BoToFit_mode in [1, 4]:
                    if i == 1: color = [255, 0, 0]
                elif self.BoToFit_mode in [2, 5]:
                    if i == 1: color = [255, 0, 0]
                    if i == 2: color = [0, 255, 0]
                    if i == 3: color = [0, 0, 255]

                # pyqtgraph can not rescale data in log scale, so we do it manually
                plot_I = []
                plot_angle = []
                plot_dI_err_bottom = []
                plot_dI_err_top = []

                for j in range(0, len(data_angle)):
                    if float(data_I[j]) > 0:
                        plot_angle.append(float(data_angle[j]))
                        plot_I.append(math.log10(float(data_I[j])))
                        plot_dI_err_top.append(abs(math.log10(float(data_I[j]) + float(data_dI[j])) - math.log10(float(data_I[j]))))

                        if float(data_I[j]) > float(data_dI[j]):
                            plot_dI_err_bottom.append(math.log10(float(data_I[j])) - math.log10(float(data_I[j]) - float(data_dI[j])))
                        else: plot_dI_err_bottom.append(0)

                s1 = pg.ErrorBarItem(x=numpy.array(plot_angle[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1]), y=numpy.array(plot_I[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1]), top=numpy.array(plot_dI_err_top[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1]), bottom=numpy.array(plot_dI_err_bottom[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1]), pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                self.graphicsView_Reflectivity_profile.addItem(s1)

                s2 = pg.ScatterPlotItem(x=plot_angle[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1], y=plot_I[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()): -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text()) - 1], symbol="o", size=2, pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                self.graphicsView_Reflectivity_profile.addItem(s2)

    def draw_and_export_reform_FitFunct(self):
        '''
        draw BoToFit final fit function on top of the graph with experimental points
        '''

        if self.BoToFit_mode in [0, 3]: fit_funct_files = [["FitFunct.dat", [0, 0, 0]], []]
        elif self.BoToFit_mode in [1, 4]: fit_funct_files = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]]]
        elif self.BoToFit_mode in [2, 5]: fit_funct_files = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]], ["Fit2DFunctUD.dat", [0, 255, 0]], ["Fit2DFunctDU.dat", [0, 0, 255]]]

        for file in fit_funct_files:
            plot_I = []
            plot_angle = []

            if file == []: return

            # if user wants to work with data in Qz, he will get additional files during export
            if not self.BoToFit_mode in [3, 4, 5] and "ang(Qz)" in self.input_structure:
                export_fit_funct_file_name = self.data_folder_name + "EXPORT - Qz_I - " + file[0]
                if self.BoToFit_mode == 1:
                    export_fit_funct_file_name = self.data_folder_name + "EXPORT - Qz_I - " + file[0][:-5] + ".dat"

                export_fit_funct_file = open(export_fit_funct_file_name, "w")

            with open(self.data_folder_name + file[0], 'r') as fit_funct_file:
                for line in fit_funct_file.readlines():
                    try:
                        plot_I.append(math.log10(float(line.split()[1])))
                        if self.BoToFit_mode in [3, 4, 5]: plot_angle.append(float(line.split()[0]))
                        else:
                            if "ang(Qz)" in self.input_structure: plot_angle.append(self.angle_convert("rad", "Qz", float(line.split()[0])))
                            elif "ang(rad)" in self.input_structure: plot_angle.append(float(line.split()[0]))
                    except: a = 1

                    # export data for user in (Qz I) format if needed
                    if not self.BoToFit_mode in [3, 4, 5] and "ang(Qz)" in self.input_structure: export_fit_funct_file.write(str((4 * math.pi / float(self.lineEdit_Scan_parameters_Wavelength.text())) * math.sin(float(line.split()[0]))) + "    " + str((line.split()[1])) + "\n")

                s3 = pg.PlotDataItem(plot_angle, plot_I, pen = pg.mkPen(color=(file[1][0], file[1][1], file[1][2]), width=2))
                self.graphicsView_Reflectivity_profile.addItem(s3)

    def draw_SLD(self):
        '''
        draw SLD profiles, calculated in multiGrPr.exe
        '''

        self.graphicsView_Sld_profile.getPlotItem().clear()

        dist = []
        sld_1 = []
        sld_2 = []
        points = -1
        cut_1 = -1
        cut_2 = -1

        with open(self.data_folder_name + 'SLD_profile.dat', 'r') as sld_file:
            for line_number, line in enumerate(sld_file.readlines()):
                try:
                    sld_1.append((float(line.split()[1].replace("D", "E"))))
                    sld_2.append((float(line.split()[2].replace("D", "E"))))
                    dist.append(float(line.split()[0].replace("D", "E")))
                except: a = 1
                points = line_number

            try:
                for i in range(points-100, 0, -1):
                    if not round(sld_1[i], 3) == round(sld_1[points - 100], 3) and cut_1 == -1: cut_1 = i
                for i in range(points-100, 0, -1):
                    if not round(sld_2[i], 3) == round(sld_2[points - 100], 3) and cut_2 == -1: cut_2 = i
            except:
                print("No cut")
                cut_1 = cut_2 = points

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

        if self.BoToFit_mode in [0, 3]: fit_funct_files = [["FitFunct.dat", [0, 0, 0]], []]
        elif self.BoToFit_mode in [1, 4]: fit_funct_files = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]]]
        elif self.BoToFit_mode in [2, 5]: fit_funct_files = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]], ["Fit2DFunctUD.dat", [0, 255, 0]], ["Fit2DFunctDU.dat", [0, 0, 255]]]

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
                    except:
                        a = 1

                s = InterpolatedUnivariateSpline(numpy.array(fit_funct_angle), numpy.array(fit_funct_I), k=1)

            if self.tableWidget_Data_points.item(i, 0).text() not in ("", "[]"):
                scale_angle = numpy.array(self.tableWidget_Data_points.item(i, 0).text()[1: -1].replace(",", "").split()).astype(float)[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()) : -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text())-1]
                data_I = numpy.array(self.tableWidget_Data_points.item(i, 1).text()[1: -1].replace(",", "").split()).astype(float)[int(self.lineEdit_Scan_parameters_Points_to_exclude_First.text()) : -int(self.lineEdit_Scan_parameters_Points_to_exclude_Last.text())-1]

                for i in range(0, len(scale_angle)):
                    if data_I[i] != 0:
                        diff_I.append(data_I[i] / s(scale_angle[i]))
                    else: zero_I.append(i)

            s6 = pg.PlotDataItem(numpy.delete(scale_angle, zero_I), diff_I, pen = pg.mkPen(color=(file[1][0], file[1][1], file[1][2]), width=2))
            self.graphicsView_Diff.addItem(s6)
    ##<--

    ##--> reformat data for user in Mono modes if he uses Qz as an angle
    def export_for_user(self):

        # create reformatted files (in Qz I dI) named "Export"
        if self.BoToFit_mode == 0: num_rows = 1
        elif self.BoToFit_mode == 1: num_rows = 2
        elif self.BoToFit_mode == 2: num_rows = 4

        for i in range(0, num_rows):
            if num_rows == 1:
                file_name_export_Data_points = "/EXPORT - Qz_I_dI - data points.dat"
            elif num_rows == 2:
                if i == 0:
                    file_name_export_Data_points = "/EXPORT - Qz_I_dI - data points - U.dat"
                else:
                    file_name_export_Data_points = "/EXPORT - Qz_I_dI - data points - D.dat"
            elif num_rows == 4:
                if i == 0:
                    file_name_export_Data_points = "/EXPORT - Qz_I_dI - data points - UU.dat"
                elif i == 1:
                    file_name_export_Data_points = "/EXPORT - Qz_I_dI - data points - DD.dat"
                elif i == 2:
                    file_name_export_Data_points = "/EXPORT - Qz_I_dI - data points - UD.dat"
                else:
                    file_name_export_Data_points = "/EXPORT - Qz_I_dI - data points - DU.dat"

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
            except:
                print("Nothing to delete (FitFunct)")

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

if __name__ == "__main__":
    import sys
    QtWidgets.QApplication.setStyle("Fusion")
    app = QtWidgets.QApplication(sys.argv)
    prog = GUI()
    prog.show()
    sys.exit(app.exec_())

