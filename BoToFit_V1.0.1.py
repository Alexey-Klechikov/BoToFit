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
        font_ee.setPointSize(7)
        font_ee.setBold(False)

        # Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(910, 751)
        MainWindow.setMinimumSize(QtCore.QSize(910, 751))
        MainWindow.setMaximumSize(QtCore.QSize(910, 751))
        MainWindow.setFont(font_ee)
        MainWindow.setWindowIcon(QtGui.QIcon(self.current_dir + "\icon.png"))
        MainWindow.setIconSize(QtCore.QSize(30, 30))
        MainWindow.setWindowTitle("BoToFit")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Block: Data file and structure
        self.label_data_file = QtWidgets.QLabel(self.centralwidget)
        self.label_data_file.setGeometry(QtCore.QRect(20, 0, 191, 16))
        self.label_data_file.setFont(font_headline)
        self.label_data_file.setObjectName("label_data_file")
        self.label_data_file.setText("Data file and structure:")
        self.groupBox_data_file = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_data_file.setGeometry(QtCore.QRect(10, 0, 551, 50))
        self.groupBox_data_file.setObjectName("groupBox_data_file")
        self.toolButton_data_file = QtWidgets.QToolButton(self.groupBox_data_file)
        self.toolButton_data_file.setGeometry(QtCore.QRect(318, 23, 26, 21))
        self.toolButton_data_file.setObjectName("toolButton_data_file")
        self.toolButton_data_file.setText("...")
        self.lineEdit_data_file = QtWidgets.QLineEdit(self.groupBox_data_file)
        self.lineEdit_data_file.setGeometry(QtCore.QRect(5, 23, 310, 21))
        self.lineEdit_data_file.setFont(font_ee)
        self.lineEdit_data_file.setObjectName("lineEdit_data_file")
        self.comboBox_data_file_column_1 = QtWidgets.QComboBox(self.groupBox_data_file)
        self.comboBox_data_file_column_1.setGeometry(QtCore.QRect(355, 23, 61, 21))
        self.comboBox_data_file_column_1.setFont(font_ee)
        self.comboBox_data_file_column_1.setObjectName("comboBox_data_file_column_1")
        for i in range(0, 4): self.comboBox_data_file_column_1.addItem("")
        self.comboBox_data_file_column_1.setItemText(0, "ang(Qz)")
        self.comboBox_data_file_column_1.setItemText(1, "I")
        self.comboBox_data_file_column_1.setItemText(2, "dI")
        self.comboBox_data_file_column_1.setItemText(3, "ang(rad)")
        self.comboBox_data_file_column_2 = QtWidgets.QComboBox(self.groupBox_data_file)
        self.comboBox_data_file_column_2.setGeometry(QtCore.QRect(420, 23, 61, 21))
        self.comboBox_data_file_column_2.setFont(font_ee)
        self.comboBox_data_file_column_2.setObjectName("comboBox_data_file_column_2")
        for i in range(0, 4): self.comboBox_data_file_column_2.addItem("")
        self.comboBox_data_file_column_2.setItemText(0, "I")
        self.comboBox_data_file_column_2.setItemText(1, "dI")
        self.comboBox_data_file_column_2.setItemText(2, "ang(Qz)")
        self.comboBox_data_file_column_2.setItemText(3, "ang(rad)")
        self.comboBox_data_file_column_3 = QtWidgets.QComboBox(self.groupBox_data_file)
        self.comboBox_data_file_column_3.setGeometry(QtCore.QRect(485, 23, 61, 21))
        self.comboBox_data_file_column_3.setFont(font_ee)
        self.comboBox_data_file_column_3.setObjectName("comboBox_data_file_column_3")
        for i in range(0, 4): self.comboBox_data_file_column_3.addItem("")
        self.comboBox_data_file_column_3.setItemText(0, "dI")
        self.comboBox_data_file_column_3.setItemText(1, "I")
        self.comboBox_data_file_column_3.setItemText(2, "ang(Qz)")
        self.comboBox_data_file_column_3.setItemText(3, "ang(rad)")

        # Block: Start fit with
        self.label_start_fit_with = QtWidgets.QLabel(self.centralwidget)
        self.label_start_fit_with.setGeometry(QtCore.QRect(20, 50, 141, 16))
        self.label_start_fit_with.setFont(font_headline)
        self.label_start_fit_with.setObjectName("label_start_fit_with")
        self.label_start_fit_with.setText("Start fit with:")
        self.groupBox_start_fit_with = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_start_fit_with.setGeometry(QtCore.QRect(10, 50, 551, 289))
        self.groupBox_start_fit_with.setObjectName("groupBox_start_fit_with")
        self.tabWidget_start_fit_with = QtWidgets.QTabWidget(self.groupBox_start_fit_with)
        self.tabWidget_start_fit_with.setGeometry(QtCore.QRect(1, 18, 550, 272))
        self.tabWidget_start_fit_with.setFont(font_ee)
        self.tabWidget_start_fit_with.setObjectName("tabWidget_start_fit_with")

        # - tab "Film description"
        self.tab_film_description = QtWidgets.QWidget()
        self.tab_film_description.setObjectName("tab_film_description")
        self.tabWidget_start_fit_with.addTab(self.tab_film_description, "")
        self.tabWidget_start_fit_with.setTabText(self.tabWidget_start_fit_with.indexOf(self.tab_film_description),
                                                   "Film description")
        self.pushButton_film_description_add_layer = QtWidgets.QPushButton(self.tab_film_description)
        self.pushButton_film_description_add_layer.setGeometry(QtCore.QRect(377, 225, 80, 20))
        self.pushButton_film_description_add_layer.setObjectName("pushButton_film_description_add_layer")
        self.pushButton_film_description_add_layer.setText("Add layer")
        self.pushButton_film_description_remove_layer = QtWidgets.QPushButton(self.tab_film_description)
        self.pushButton_film_description_remove_layer.setGeometry(QtCore.QRect(463, 225, 80, 20))
        self.pushButton_film_description_remove_layer.setObjectName("pushButton_film_description_remove_layer")
        self.pushButton_film_description_remove_layer.setText("Remove layer")
        self.tableWidget_film_description = QtWidgets.QTableWidget(self.tab_film_description)
        self.tableWidget_film_description.setGeometry(QtCore.QRect(-2, -1, 550, 224))
        self.tableWidget_film_description.setFont(font_ee)
        self.tableWidget_film_description.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableWidget_film_description.setObjectName("tableWidget_film_description")
        self.tableWidget_film_description.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_film_description.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_film_description.setColumnCount(13)
        self.tableWidget_film_description.setRowCount(1)
        # reform the table if Pol/NoPol mode is chosen
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_film_description.setVerticalHeaderItem(0, item)
        for i in range(0, 13):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget_film_description.setHorizontalHeaderItem(i, item)
        item = self.tableWidget_film_description.verticalHeaderItem(0)
        item.setText("substrate")
        item = self.tableWidget_film_description.horizontalHeaderItem(0)
        item.setText("name")
        item = self.tableWidget_film_description.horizontalHeaderItem(1)
        item.setText("thickness")
        item = self.tableWidget_film_description.horizontalHeaderItem(3)
        item.setText("SLD")
        item = self.tableWidget_film_description.horizontalHeaderItem(5)
        item.setText("iSLD")
        item = self.tableWidget_film_description.horizontalHeaderItem(7)
        item.setText("mSLD")
        item = self.tableWidget_film_description.horizontalHeaderItem(9)
        item.setText("cos(d-gamma)")
        item = self.tableWidget_film_description.horizontalHeaderItem(11)
        item.setText("roughness")
        self.tableWidget_film_description.horizontalHeaderItem(4).setFont(font_headline)
        for i in range(0, 13):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            if i in (0, 1, 2): item.setFlags(QtCore.Qt.NoItemFlags)
            if i in (4, 6, 8, 10, 12):
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                if i == 8:
                    item.setCheckState(QtCore.Qt.Unchecked)
                else:
                    item.setCheckState(QtCore.Qt.Checked)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget_film_description.setItem(0, i, item)

        item = self.tableWidget_film_description.item(0, 0)
        item.setText("substrate")
        item = self.tableWidget_film_description.item(0, 1)
        item.setText("inf")
        item = self.tableWidget_film_description.item(0, 3)
        item.setText("2.07")
        item = self.tableWidget_film_description.item(0, 5)
        item.setText("0")
        item = self.tableWidget_film_description.item(0, 11)
        item.setText("10")
        self.tableWidget_film_description.setRowHeight(0, 21)
        self.tableWidget_film_description.horizontalHeader().setDefaultSectionSize(23)
        self.tableWidget_film_description.verticalHeader().setVisible(False)

        self.pushButton_film_description_load_entry = QtWidgets.QPushButton(self.tab_film_description)
        self.pushButton_film_description_load_entry.setGeometry(QtCore.QRect(0, 225, 111, 20))
        self.pushButton_film_description_load_entry.setObjectName("pushButton_film_description_load_entry")
        self.pushButton_film_description_load_entry.setText("Load entry file")

        # - tab "Scan parameters"
        self.tab_scan_parameters = QtWidgets.QWidget()
        self.tab_scan_parameters.setObjectName("tab_scan_parameters")
        self.tabWidget_start_fit_with.addTab(self.tab_scan_parameters, "")
        self.tabWidget_start_fit_with.setTabText(self.tabWidget_start_fit_with.indexOf(self.tab_scan_parameters),
                                                   "Scan parameters")
        self.label_scan_parameters_num_of_pts_for_res_function = QtWidgets.QLabel(self.tab_scan_parameters)
        self.label_scan_parameters_num_of_pts_for_res_function.setGeometry(QtCore.QRect(8, 9, 311, 17))
        self.label_scan_parameters_num_of_pts_for_res_function.setFont(font_ee)
        self.label_scan_parameters_num_of_pts_for_res_function.setObjectName("label_scan_parameters_num_of_pts_for_res_function")
        self.label_scan_parameters_num_of_pts_for_res_function.setText("Number of points for resolution function")
        self.lineEdit_scan_parameters_num_of_pts_for_res_function = QtWidgets.QLineEdit(self.tab_scan_parameters)
        self.lineEdit_scan_parameters_num_of_pts_for_res_function.setGeometry(QtCore.QRect(188, 9, 60, 17))
        self.lineEdit_scan_parameters_num_of_pts_for_res_function.setFont(font_ee)
        self.lineEdit_scan_parameters_num_of_pts_for_res_function.setObjectName("lineEdit_scan_parameters_num_of_pts_for_res_function")
        self.label_scan_parameters_step_for_res_function = QtWidgets.QLabel(self.tab_scan_parameters)
        self.label_scan_parameters_step_for_res_function.setGeometry(QtCore.QRect(8, 27, 291, 17))
        self.label_scan_parameters_step_for_res_function.setFont(font_ee)
        self.label_scan_parameters_step_for_res_function.setObjectName("label_scan_parameters_step_for_res_function")
        self.label_scan_parameters_step_for_res_function.setText("Step for resolution function (mrad)")
        self.lineEdit_scan_parameters_step_for_res_function = QtWidgets.QLineEdit(self.tab_scan_parameters)
        self.lineEdit_scan_parameters_step_for_res_function.setGeometry(QtCore.QRect(188, 27, 60, 17))
        self.lineEdit_scan_parameters_step_for_res_function.setFont(font_ee)
        self.lineEdit_scan_parameters_step_for_res_function.setObjectName("lineEdit_scan_parameters_step_for_res_function")
        self.label_scan_parameters_sigma = QtWidgets.QLabel(self.tab_scan_parameters)
        self.label_scan_parameters_sigma.setGeometry(QtCore.QRect(8, 45, 291, 17))
        self.label_scan_parameters_sigma.setFont(font_ee)
        self.label_scan_parameters_sigma.setObjectName("label_scan_parameters_sigma")
        self.label_scan_parameters_sigma.setText("\"Sigma\" of resolution function (mrad)")
        self.lineEdit_scan_parameters_sigma = QtWidgets.QLineEdit(self.tab_scan_parameters)
        self.lineEdit_scan_parameters_sigma.setGeometry(QtCore.QRect(188, 45, 60, 17))
        self.lineEdit_scan_parameters_sigma.setFont(font_ee)
        self.lineEdit_scan_parameters_sigma.setObjectName("lineEdit_scan_parameters_sigma")
        self.label_scan_parameters_zero_correction = QtWidgets.QLabel(self.tab_scan_parameters)
        self.label_scan_parameters_zero_correction.setGeometry(QtCore.QRect(8, 63, 281, 17))
        self.label_scan_parameters_zero_correction.setFont(font_ee)
        self.label_scan_parameters_zero_correction.setObjectName("label_scan_parameters_zero_correction")
        self.label_scan_parameters_zero_correction.setText("Correction of the detector \"zero\"")
        self.lineEdit_scan_parameters_zero_correction = QtWidgets.QLineEdit(self.tab_scan_parameters)
        self.lineEdit_scan_parameters_zero_correction.setGeometry(QtCore.QRect(188, 63, 60, 17))
        self.lineEdit_scan_parameters_zero_correction.setFont(font_ee)
        self.lineEdit_scan_parameters_zero_correction.setObjectName("lineEdit_scan_parameters_zero_correction")

        self.label_scan_parameters_cross_overill = QtWidgets.QLabel(self.tab_scan_parameters)
        self.label_scan_parameters_cross_overill.setGeometry(QtCore.QRect(280, 63, 311, 17))
        self.label_scan_parameters_cross_overill.setFont(font_ee)
        self.label_scan_parameters_cross_overill.setObjectName("label_scan_parameters_cross_overill")
        self.label_scan_parameters_cross_overill.setText("Crossover angle overillumination (mrad)")
        self.lineEdit_scan_parameters_cross_overill = QtWidgets.QLineEdit(self.tab_scan_parameters)
        self.lineEdit_scan_parameters_cross_overill.setGeometry(QtCore.QRect(460, 63, 60, 17))
        self.lineEdit_scan_parameters_cross_overill.setFont(font_ee)
        self.lineEdit_scan_parameters_cross_overill.setObjectName("lineEdit_scan_parameters_cross_overill")
        self.checkBox_scan_parameters_cross_overill = QtWidgets.QCheckBox(self.tab_scan_parameters)
        self.checkBox_scan_parameters_cross_overill.setGeometry(QtCore.QRect(523, 63, 21, 18))
        self.checkBox_scan_parameters_cross_overill.setObjectName("checkBox_scan_parameters_cross_overill")

        self.label_scan_parameters_wavelength = QtWidgets.QLabel(self.tab_scan_parameters)
        self.label_scan_parameters_wavelength.setGeometry(QtCore.QRect(280, 9, 131, 17))
        self.label_scan_parameters_wavelength.setFont(font_ee)
        self.label_scan_parameters_wavelength.setObjectName("label_scan_parameters_wavelength")
        self.label_scan_parameters_wavelength.setText("Wavelength (A)")
        self.lineEdit_scan_parameters_wavelength = QtWidgets.QLineEdit(self.tab_scan_parameters)
        self.lineEdit_scan_parameters_wavelength.setGeometry(QtCore.QRect(460, 9, 60, 17))
        self.lineEdit_scan_parameters_wavelength.setFont(font_ee)
        self.lineEdit_scan_parameters_wavelength.setObjectName("lineEdit_scan_parameters_wavelength")
        self.label_scan_parameters_scaling_factor = QtWidgets.QLabel(self.tab_scan_parameters)
        self.label_scan_parameters_scaling_factor.setGeometry(QtCore.QRect(280, 27, 101, 17))
        self.label_scan_parameters_scaling_factor.setFont(font_ee)
        self.label_scan_parameters_scaling_factor.setObjectName("label_scan_parameters_scaling_factor")
        self.label_scan_parameters_scaling_factor.setText("Scaling factor")
        self.lineEdit_scan_parameters_scaling_factor = QtWidgets.QLineEdit(self.tab_scan_parameters)
        self.lineEdit_scan_parameters_scaling_factor.setGeometry(QtCore.QRect(460, 27, 60, 17))
        self.lineEdit_scan_parameters_scaling_factor.setFont(font_ee)
        self.lineEdit_scan_parameters_scaling_factor.setPlaceholderText("")
        self.lineEdit_scan_parameters_scaling_factor.setObjectName("lineEdit_scan_parameters_scaling_factor")
        self.checkBox_scan_parameters_scaling_factor = QtWidgets.QCheckBox(self.tab_scan_parameters)
        self.checkBox_scan_parameters_scaling_factor.setGeometry(QtCore.QRect(523, 27, 20, 18))
        self.checkBox_scan_parameters_scaling_factor.setObjectName("checkBox_scan_parameters_scaling_factor")
        self.label_scan_parameters_background = QtWidgets.QLabel(self.tab_scan_parameters)
        self.label_scan_parameters_background.setGeometry(QtCore.QRect(280, 45, 91, 17))
        self.label_scan_parameters_background.setFont(font_ee)
        self.label_scan_parameters_background.setObjectName("label_scan_parameters_background")
        self.label_scan_parameters_background.setText("Background")
        self.lineEdit_scan_parameters_background = QtWidgets.QLineEdit(self.tab_scan_parameters)
        self.lineEdit_scan_parameters_background.setGeometry(QtCore.QRect(460, 45, 60, 17))
        self.lineEdit_scan_parameters_background.setFont(font_ee)
        self.lineEdit_scan_parameters_background.setObjectName("lineEdit_scan_parameters_background")
        self.checkBox_scan_parameters_background = QtWidgets.QCheckBox(self.tab_scan_parameters)
        self.checkBox_scan_parameters_background.setGeometry(QtCore.QRect(523, 45, 21, 18))
        self.checkBox_scan_parameters_background.setObjectName("checkBox_scan_parameters_background")

        self.label_scan_parameters_points_to_exclude_first = QtWidgets.QLabel(self.tab_scan_parameters)
        self.label_scan_parameters_points_to_exclude_first.setGeometry(QtCore.QRect(8, 93, 191, 16))
        self.label_scan_parameters_points_to_exclude_first.setObjectName("label_scan_parameters_points_to_exclude_first")
        self.label_scan_parameters_points_to_exclude_first.setText("Number of first points to exclude")
        self.lineEdit_scan_parameters_points_to_exclude_first = QtWidgets.QLineEdit(self.tab_scan_parameters)
        self.lineEdit_scan_parameters_points_to_exclude_first.setGeometry(QtCore.QRect(188, 93, 60, 17))
        self.lineEdit_scan_parameters_points_to_exclude_first.setObjectName("lineEdit_scan_parameters_points_to_exclude_first")
        self.lineEdit_scan_parameters_points_to_exclude_first.setText("5")
        self.label_scan_parameters_points_to_exclude_last = QtWidgets.QLabel(self.tab_scan_parameters)
        self.label_scan_parameters_points_to_exclude_last.setGeometry(QtCore.QRect(8, 111, 191, 17))
        self.label_scan_parameters_points_to_exclude_last.setObjectName("label_scan_parameters_points_to_exclude_last")
        self.label_scan_parameters_points_to_exclude_last.setText("Number of last points to exclude")
        self.lineEdit_scan_parameters_points_to_exclude_last = QtWidgets.QLineEdit(self.tab_scan_parameters)
        self.lineEdit_scan_parameters_points_to_exclude_last.setGeometry(QtCore.QRect(188, 111, 60, 17))
        self.lineEdit_scan_parameters_points_to_exclude_last.setObjectName("lineEdit_scan_parameters_points_to_exclude_last")
        self.lineEdit_scan_parameters_points_to_exclude_last.setText("5")
        self.pushButton_scan_parameters_redraw_reflectivity = QtWidgets.QPushButton(self.tab_scan_parameters)
        self.pushButton_scan_parameters_redraw_reflectivity.setGeometry(QtCore.QRect(256, 93, 121, 34))
        self.pushButton_scan_parameters_redraw_reflectivity.setObjectName("pushButton_scan_parameters_redraw_reflectivity")
        self.pushButton_scan_parameters_redraw_reflectivity.setText("Redraw reflectivity")

        self.label_scan_parameters_piy = QtWidgets.QLabel(self.tab_scan_parameters)
        self.label_scan_parameters_piy.setGeometry(QtCore.QRect(8, 144, 291, 17))
        self.label_scan_parameters_piy.setObjectName("label_scan_parameters_piy")
        self.label_scan_parameters_piy.setText("Piy incident polarization (polariser)")
        self.lineEdit_scan_parameters_piy = QtWidgets.QLineEdit(self.tab_scan_parameters)
        self.lineEdit_scan_parameters_piy.setGeometry(QtCore.QRect(228, 144, 60, 17))
        self.lineEdit_scan_parameters_piy.setObjectName("lineEdit_scan_parameters_piy")
        self.checkBox_scan_parameters_piy = QtWidgets.QCheckBox(self.tab_scan_parameters)
        self.checkBox_scan_parameters_piy.setGeometry(QtCore.QRect(292, 144, 21, 18))
        self.checkBox_scan_parameters_piy.setObjectName("checkBox_scan_parameters_piy")
        self.label_scan_parameters_pfy = QtWidgets.QLabel(self.tab_scan_parameters)
        self.label_scan_parameters_pfy.setGeometry(QtCore.QRect(8, 162, 251, 17))
        self.label_scan_parameters_pfy.setObjectName("label_scan_parameters_pfy")
        self.label_scan_parameters_pfy.setText("Pfy outgoing polarization (analyser)")
        self.lineEdit_scan_parameters_pfy = QtWidgets.QLineEdit(self.tab_scan_parameters)
        self.lineEdit_scan_parameters_pfy.setGeometry(QtCore.QRect(228, 162, 60, 17))
        self.lineEdit_scan_parameters_pfy.setObjectName("lineEdit_scan_parameters_pfy")
        self.checkBox_scan_parameters_pfy = QtWidgets.QCheckBox(self.tab_scan_parameters)
        self.checkBox_scan_parameters_pfy.setGeometry(QtCore.QRect(292, 162, 21, 18))
        self.checkBox_scan_parameters_pfy.setObjectName("checkBox_scan_parameters_pfy")
        self.label_scan_parameters_cg = QtWidgets.QLabel(self.tab_scan_parameters)
        self.label_scan_parameters_cg.setGeometry(QtCore.QRect(8, 180, 291, 17))
        self.label_scan_parameters_cg.setObjectName("label_scan_parameters_cg")
        self.label_scan_parameters_cg.setText("cg: mean value <cos(gamma)> of big domains")
        self.lineEdit_scan_parameters_cg = QtWidgets.QLineEdit(self.tab_scan_parameters)
        self.lineEdit_scan_parameters_cg.setGeometry(QtCore.QRect(228, 180, 60, 17))
        self.lineEdit_scan_parameters_cg.setObjectName("lineEdit_scan_parameters_cg")
        self.checkBox_scan_parameters_cg = QtWidgets.QCheckBox(self.tab_scan_parameters)
        self.checkBox_scan_parameters_cg.setGeometry(QtCore.QRect(292, 180, 21, 18))
        self.checkBox_scan_parameters_cg.setObjectName("checkBox_scan_parameters_cg")
        self.label_scan_parameters_sg = QtWidgets.QLabel(self.tab_scan_parameters)
        self.label_scan_parameters_sg.setGeometry(QtCore.QRect(8, 198, 291, 17))
        self.label_scan_parameters_sg.setObjectName("label_scan_parameters_sg")
        self.label_scan_parameters_sg.setText("sg: mean value <sin(gamma)> of big domains")
        self.lineEdit_scan_parameters_sg = QtWidgets.QLineEdit(self.tab_scan_parameters)
        self.lineEdit_scan_parameters_sg.setGeometry(QtCore.QRect(228, 198, 60, 17))
        self.lineEdit_scan_parameters_sg.setObjectName("lineEdit_scan_parameters_sg")
        self.checkBox_scan_parameters_sg = QtWidgets.QCheckBox(self.tab_scan_parameters)
        self.checkBox_scan_parameters_sg.setGeometry(QtCore.QRect(292, 198, 21, 18))
        self.checkBox_scan_parameters_sg.setObjectName("checkBox_scan_parameters_sg")
        self.label_scan_parameters_sg2 = QtWidgets.QLabel(self.tab_scan_parameters)
        self.label_scan_parameters_sg2.setGeometry(QtCore.QRect(8, 216, 291, 17))
        self.label_scan_parameters_sg2.setObjectName("label_scan_parameters_sg2")
        self.label_scan_parameters_sg2.setText("sg2: mean value <sin^2(gamma)> of big domains")
        self.lineEdit_scan_parameters_sg2 = QtWidgets.QLineEdit(self.tab_scan_parameters)
        self.lineEdit_scan_parameters_sg2.setGeometry(QtCore.QRect(228, 216, 60, 17))
        self.lineEdit_scan_parameters_sg2.setObjectName("lineEdit_scan_parameters_sg2")
        self.checkBox_scan_parameters_sg2 = QtWidgets.QCheckBox(self.tab_scan_parameters)
        self.checkBox_scan_parameters_sg2.setGeometry(QtCore.QRect(292, 216, 21, 18))
        self.checkBox_scan_parameters_sg2.setObjectName("checkBox_scan_parameters_sg2")

        self.tabWidget_start_fit_with.setCurrentIndex(0)

        # Block: Save results at
        self.label_save_at = QtWidgets.QLabel(self.centralwidget)
        self.label_save_at.setFont(font_headline)
        self.label_save_at.setGeometry(QtCore.QRect(20, 340, 151, 16))
        self.label_save_at.setObjectName("label_save_at")
        self.label_save_at.setText("Save results at:")
        self.groupBox_save_at = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_save_at.setGeometry(QtCore.QRect(10, 340, 421, 50))
        self.groupBox_save_at.setObjectName("groupBox_save_at")
        self.lineEdit_save_at = QtWidgets.QLineEdit(self.groupBox_save_at)
        self.lineEdit_save_at.setGeometry(QtCore.QRect(5, 23, 381, 21))
        self.lineEdit_save_at.setFont(font_ee)
        self.lineEdit_save_at.setObjectName("lineEdit_save_at")
        self.toolButton_save_at = QtWidgets.QToolButton(self.groupBox_save_at)
        self.toolButton_save_at.setGeometry(QtCore.QRect(390, 23, 26, 21))
        self.toolButton_save_at.setObjectName("toolButton_save_at")
        self.toolButton_save_at.setText("...")

        # Button: Start fitting
        self.pushButton_start_fitting = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start_fitting.setGeometry(QtCore.QRect(440, 358, 121, 32))
        self.pushButton_start_fitting.setFont(font_headline)
        self.pushButton_start_fitting.setObjectName("pushButton_start_fitting")
        self.pushButton_start_fitting.setText("Start Fitting")

        # Block: Fit results
        self.label_fit_results = QtWidgets.QLabel(self.centralwidget)
        self.label_fit_results.setFont(font_headline)
        self.label_fit_results.setGeometry(QtCore.QRect(580, 0, 101, 16))
        self.label_fit_results.setObjectName("label_fit_results")
        self.label_fit_results.setText("Fit results:")
        self.groupBox_fit_results = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_fit_results.setGeometry(QtCore.QRect(570, 0, 331, 390))
        self.groupBox_fit_results.setObjectName("groupBox_fit_results")
        self.tableWidget_fit_results = QtWidgets.QTableWidget(self.groupBox_fit_results)
        self.tableWidget_fit_results.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_fit_results.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_fit_results.setGeometry(QtCore.QRect(1, 48, 329, 322))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.tableWidget_fit_results.setPalette(palette)
        self.tableWidget_fit_results.setFont(font_ee)
        self.tableWidget_fit_results.setObjectName("tableWidget_fit_results")
        self.tableWidget_fit_results.setColumnCount(6)
        self.tableWidget_fit_results.setRowCount(0)
        for i in range(0, 6):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_fit_results.setHorizontalHeaderItem(i, item)

        self.tableWidget_fit_results.horizontalHeaderItem(0).setFont(font_headline)
        item = self.tableWidget_fit_results.horizontalHeaderItem(1)
        item.setText("No")
        item = self.tableWidget_fit_results.horizontalHeaderItem(2)
        item.setText("Parameter")
        item = self.tableWidget_fit_results.horizontalHeaderItem(3)
        item.setText("Value")
        item = self.tableWidget_fit_results.horizontalHeaderItem(4)
        item.setText("Error")
        item = self.tableWidget_fit_results.horizontalHeaderItem(5)
        item.setText("Factor")
        self.tableWidget_fit_results.setColumnWidth(0, 15)
        self.tableWidget_fit_results.setColumnWidth(1, 20)
        self.tableWidget_fit_results.setColumnWidth(2, 100)
        self.tableWidget_fit_results.setColumnWidth(3, 60)
        self.tableWidget_fit_results.setColumnWidth(4, 60)
        self.tableWidget_fit_results.setColumnWidth(5, int(self.tableWidget_fit_results.width() - int(
            self.tableWidget_fit_results.columnWidth(0)) - int(self.tableWidget_fit_results.columnWidth(1)) - int(self.tableWidget_fit_results.columnWidth(2)) - int(
                self.tableWidget_fit_results.columnWidth(3)) - int(self.tableWidget_fit_results.columnWidth(4) - 5)))
        self.tableWidget_fit_results.verticalHeader().setVisible(False)
        self.checkBox_fit_results_select_all = QtWidgets.QCheckBox(self.tableWidget_fit_results.horizontalHeader())
        self.checkBox_fit_results_select_all.setGeometry(QtCore.QRect(self.tableWidget_fit_results.columnWidth(0) / 9, 1, 14, 14))
        self.checkBox_fit_results_select_all.setObjectName("checkBox_fit_results_select_all")
        self.label_fit_results_number_of_iterations = QtWidgets.QLabel(self.groupBox_fit_results)
        self.label_fit_results_number_of_iterations.setGeometry(QtCore.QRect(10, 18, 161, 31))
        self.label_fit_results_number_of_iterations.setObjectName("label_fit_results_number_of_iterations")
        self.label_fit_results_number_of_iterations.setText("Number of iterations:")
        self.lineEdit_fit_results_number_of_iterations = QtWidgets.QLineEdit(self.groupBox_fit_results)
        self.lineEdit_fit_results_number_of_iterations.setGeometry(QtCore.QRect(104, 23, 31, 21))
        self.lineEdit_fit_results_number_of_iterations.setFont(font_ee)
        self.lineEdit_fit_results_number_of_iterations.setReadOnly(True)
        self.lineEdit_fit_results_number_of_iterations.setObjectName("lineEdit_fit_results_number_of_iterations")
        self.label_fit_results_chi_square = QtWidgets.QLabel(self.groupBox_fit_results)
        self.label_fit_results_chi_square.setGeometry(QtCore.QRect(205, 18, 151, 31))
        self.label_fit_results_chi_square.setObjectName("label_fit_results_chi_square")
        self.label_fit_results_chi_square.setText("Chi_sq.norm:")
        self.lineEdit_fit_results_chi_square = QtWidgets.QLineEdit(self.groupBox_fit_results)
        self.lineEdit_fit_results_chi_square.setGeometry(QtCore.QRect(268, 23, 58, 21))
        self.lineEdit_fit_results_chi_square.setFont(font_ee)
        self.lineEdit_fit_results_chi_square.setReadOnly(True)
        self.lineEdit_fit_results_chi_square.setObjectName("lineEdit_fit_results_chi_square")
        self.pushButton_fit_results_copy_to_start_fit_with = QtWidgets.QPushButton(self.groupBox_fit_results)
        self.pushButton_fit_results_copy_to_start_fit_with.setGeometry(QtCore.QRect(5, 372, 322, 15))
        self.pushButton_fit_results_copy_to_start_fit_with.setObjectName("pushButton_fit_results_copy_to_start_fit_with")
        self.pushButton_fit_results_copy_to_start_fit_with.setText("Use selected (#) values as 'Start fit with' parameters")

        # Block: Reflectivity profile and Difference
        self.label_reflectivity_profile_and_diff = QtWidgets.QLabel(self.centralwidget)
        self.label_reflectivity_profile_and_diff.setFont(font_headline)
        self.label_reflectivity_profile_and_diff.setGeometry(QtCore.QRect(20, 393, 541, 16))
        self.label_reflectivity_profile_and_diff.setObjectName("label_reflectivity_profile_and_diff")
        self.label_reflectivity_profile_and_diff.setText("Reflectivity profile (I[10e] vs. Qz[Å**-1]) and Difference (Exper/Fit):")
        self.groupBox_reflectivity_profile = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_reflectivity_profile.setGeometry(QtCore.QRect(10, 393, 491, 316))
        self.groupBox_reflectivity_profile.setObjectName("groupBox_reflectivity_profile")
        self.graphicsView_reflectivity_profile = pg.PlotWidget(self.centralwidget, viewBox=pg.ViewBox())
        self.graphicsView_reflectivity_profile.setGeometry(QtCore.QRect(12, 412, 488, 205))
        self.graphicsView_reflectivity_profile.setObjectName("graphicsView_reflectivity_profile")
        self.graphicsView_reflectivity_profile.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_reflectivity_profile.getAxis("bottom").setStyle(showValues=False)
        self.graphicsView_reflectivity_profile.getAxis("left").tickFont = font_graphs
        self.graphicsView_reflectivity_profile.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_reflectivity_profile.showAxis("top")
        self.graphicsView_reflectivity_profile.getAxis("top").setTicks([])
        self.graphicsView_reflectivity_profile.showAxis("right")
        self.graphicsView_reflectivity_profile.getAxis("right").setTicks([])
        self.graphicsView_diff = pg.PlotWidget(self.centralwidget, viewBox=pg.ViewBox())
        self.graphicsView_diff.setGeometry(QtCore.QRect(12, 617, 488, 91))
        self.graphicsView_diff.setObjectName("graphicsView_diff")
        self.graphicsView_diff.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_diff.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_diff.getAxis("left").tickFont = font_graphs
        self.graphicsView_diff.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_diff.showAxis("top")
        self.graphicsView_diff.getAxis("top").setTicks([])
        self.graphicsView_diff.showAxis("right")
        self.graphicsView_diff.getAxis("right").setTicks([])
        self.graphicsView_diff.getViewBox().setXLink(self.graphicsView_reflectivity_profile)

        # Block: SLD profile
        self.label_sld_profile = QtWidgets.QLabel(self.centralwidget)
        self.label_sld_profile.setFont(font_headline)
        self.label_sld_profile.setGeometry(QtCore.QRect(520, 393, 481, 16))
        self.label_sld_profile.setObjectName("label_sld_profile")
        self.label_sld_profile.setText("SLD profile (SLD [in Å**-2, *10e6] vs. Distance from interface [Å]:")
        self.groupBox_sld_profile = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_sld_profile.setGeometry(QtCore.QRect(510, 393, 391, 316))
        self.groupBox_sld_profile.setObjectName("groupBox_sld_profile")
        MainWindow.setCentralWidget(self.centralwidget)
        self.graphicsView_sld_profile = pg.PlotWidget(self.centralwidget)
        self.graphicsView_sld_profile.setGeometry(QtCore.QRect(512, 412, 388, 296))
        self.graphicsView_sld_profile.setObjectName("graphicsView_sld_profile")
        self.graphicsView_sld_profile.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_sld_profile.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_sld_profile.getAxis("left").tickFont = font_graphs
        self.graphicsView_sld_profile.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_sld_profile.showAxis("top")
        self.graphicsView_sld_profile.getAxis("top").setTicks([])
        self.graphicsView_sld_profile.showAxis("right")
        self.graphicsView_sld_profile.getAxis("right").setTicks([])

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
        self.actionVersion.setText("V1.0.1")
        self.menuHelp.addAction(self.actionVersion)
        MainWindow.setMenuBar(self.menuBar)
        self.menu_mono = QtWidgets.QMenu(self.menu_MenuBar)
        self.menu_mono.setObjectName("menu_mono")
        self.menu_mono.setTitle("Mono")
        self.menu_MenuBar.addAction(self.menu_mono.menuAction())
        self.menu_tof = QtWidgets.QMenu(self.menu_MenuBar)
        self.menu_tof.setObjectName("menu_tof")
        self.menu_tof.setTitle("TOF")
        self.menu_MenuBar.addAction(self.menu_tof.menuAction())
        self.action_mono_no_polarisation = QtWidgets.QAction(MainWindow)
        self.action_mono_no_polarisation.setCheckable(True)
        self.action_mono_no_polarisation.setChecked(True)
        self.action_mono_no_polarisation.setObjectName("action_mono_no_polarisation")
        self.action_mono_no_polarisation.setText("No polarisation")
        self.menu_mono.addAction(self.action_mono_no_polarisation)
        self.action_mono_2_polarisations = QtWidgets.QAction(MainWindow)
        self.action_mono_2_polarisations.setCheckable(True)
        self.action_mono_2_polarisations.setEnabled(True)
        self.action_mono_2_polarisations.setObjectName("action_mono_2_polarisations")
        self.action_mono_2_polarisations.setText("2 polarisations")
        self.menu_mono.addAction(self.action_mono_2_polarisations)
        self.action_mono_4_polarisations = QtWidgets.QAction(MainWindow)
        self.action_mono_4_polarisations.setCheckable(True)
        self.action_mono_4_polarisations.setEnabled(True)
        self.action_mono_4_polarisations.setObjectName("action_mono_4_polarisations")
        self.action_mono_4_polarisations.setText("4 polarisations")
        self.menu_mono.addAction(self.action_mono_4_polarisations)
        self.action_tof_no_polarisation = QtWidgets.QAction(MainWindow)
        self.action_tof_no_polarisation.setCheckable(True)
        self.action_tof_no_polarisation.setEnabled(True)
        self.action_tof_no_polarisation.setObjectName("action_tof_no_polarisation")
        self.action_tof_no_polarisation.setText("No polarisation")
        self.menu_tof.addAction(self.action_tof_no_polarisation)
        self.action_tof_2_polarisations = QtWidgets.QAction(MainWindow)
        self.action_tof_2_polarisations.setCheckable(True)
        self.action_tof_2_polarisations.setEnabled(True)
        self.action_tof_2_polarisations.setObjectName("action_tof_2_polarisations")
        self.action_tof_2_polarisations.setText("2 polarisations")
        self.menu_tof.addAction(self.action_tof_2_polarisations)
        self.action_tof_4_polarisations = QtWidgets.QAction(MainWindow)
        self.action_tof_4_polarisations.setCheckable(True)
        self.action_tof_4_polarisations.setEnabled(True)
        self.action_tof_4_polarisations.setObjectName("action_tof_4_polarisations")
        self.action_tof_4_polarisations.setText("4 polarisations")
        self.menu_tof.addAction(self.action_tof_4_polarisations)

        # Statusbar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # lineEdit_number_of_points and tableWidget_data_points are hidden from the user. Used to avoid reopenning data file multiple times
        self.lineEdit_number_of_points = QtWidgets.QLineEdit(self.tab_scan_parameters)
        self.lineEdit_number_of_points.setEnabled(False)
        self.lineEdit_number_of_points.setGeometry(QtCore.QRect(570, 290, 0, 0))
        self.lineEdit_number_of_points.setObjectName("lineEdit_number_of_points")

        self.tableWidget_data_points = QtWidgets.QTableWidget(self.tab_scan_parameters)
        self.tableWidget_data_points.setEnabled(False)
        self.tableWidget_data_points.setGeometry(QtCore.QRect(460, 200, 0, 0))
        self.tableWidget_data_points.setObjectName("tableWidget_data_points")
        self.tableWidget_data_points.setColumnCount(3)
        self.tableWidget_data_points.setRowCount(4)
        for i in range(0, 4):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_data_points.setVerticalHeaderItem(i, item)
        for i in range(0, 3):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_data_points.setHorizontalHeaderItem(i, item)
        self.tableWidget_data_points.horizontalHeader().setVisible(False)
        self.tableWidget_data_points.verticalHeader().setVisible(False)
        item = self.tableWidget_data_points.horizontalHeaderItem(0)
        item.setText("Q")
        item = self.tableWidget_data_points.horizontalHeaderItem(1)
        item.setText("I")
        item = self.tableWidget_data_points.horizontalHeaderItem(2)
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
        self.toolButton_data_file.clicked.connect(self.button_data_file)
        self.toolButton_save_at.clicked.connect(self.button_save_at)
        self.pushButton_film_description_add_layer.clicked.connect(self.buttons_add_remove_layer)
        self.pushButton_film_description_remove_layer.clicked.connect(self.buttons_add_remove_layer)
        self.pushButton_start_fitting.clicked.connect(self.button_start_fitting)
        self.pushButton_scan_parameters_redraw_reflectivity.clicked.connect(self.draw_reflectivity)
        self.pushButton_fit_results_copy_to_start_fit_with.clicked.connect(self.button_copy_to_start_with)
        self.pushButton_film_description_load_entry.clicked.connect(self.load_entry_file)
        self.action_mono_no_polarisation.triggered.connect(self.program_mode)
        self.action_mono_2_polarisations.triggered.connect(self.program_mode)
        self.action_mono_4_polarisations.triggered.connect(self.program_mode)
        self.action_tof_no_polarisation.triggered.connect(self.program_mode)
        self.action_tof_2_polarisations.triggered.connect(self.program_mode)
        self.action_tof_4_polarisations.triggered.connect(self.program_mode)
        self.actionVersion.triggered.connect(self.menu_info)
        self.checkBox_fit_results_select_all.clicked.connect(self.fit_results_select_all)
        #
        self.lineEdit_save_at.setPlaceholderText("default [" + str(self.current_dir) + "]")

    ##--> redefine user interface elements if TOF/Mono is selected and if polarisation is needed
    def program_mode(self):

        # check where we came from and change the interface accordingly
        # select mono_nopol by default
        try:
            action_mode = self.sender().objectName()
        except:
            action_mode = "action_mono_no_polarisation"

        if action_mode == "action_mono_no_polarisation":
            self.BoToFit_mode = 0
            self.BoToFit_exe = "Film500x0.exe"
            self.file_to_wait = "FitFunct.dat"
            self.default_entry = "UserDefaults_nopol.dat"

            self.action_mono_no_polarisation.setChecked(True)
            self.action_mono_2_polarisations.setChecked(False)
            self.action_mono_4_polarisations.setChecked(False)
            self.action_tof_no_polarisation.setChecked(False)
            self.action_tof_2_polarisations.setChecked(False)
            self.action_tof_4_polarisations.setChecked(False)

        elif action_mode == "action_mono_2_polarisations":
            self.BoToFit_mode = 1
            self.BoToFit_exe = "Film500x2.exe"
            self.file_to_wait = "Fit2DFunctDD.dat"
            self.default_entry = "UserDefaults_2pol.dat"

            self.action_mono_no_polarisation.setChecked(False)
            self.action_mono_2_polarisations.setChecked(True)
            self.action_mono_4_polarisations.setChecked(False)
            self.action_tof_no_polarisation.setChecked(False)
            self.action_tof_2_polarisations.setChecked(False)
            self.action_tof_4_polarisations.setChecked(False)

        elif action_mode == "action_mono_4_polarisations":
            self.BoToFit_mode = 2
            self.BoToFit_exe = "Film500x4.exe"
            self.file_to_wait = "Fit2DFunctDD.dat"
            self.default_entry = "UserDefaults_4pol.dat"

            self.action_mono_no_polarisation.setChecked(False)
            self.action_mono_2_polarisations.setChecked(False)
            self.action_mono_4_polarisations.setChecked(True)
            self.action_tof_no_polarisation.setChecked(False)
            self.action_tof_2_polarisations.setChecked(False)
            self.action_tof_4_polarisations.setChecked(False)

        elif action_mode == "action_tof_no_polarisation":
            self.BoToFit_mode = 3
            self.BoToFit_exe = "FilmTOF500QX0.exe"
            self.file_to_wait = "FitFunct.dat"
            self.default_entry = "UserDefaults_TOF_nopol.dat"

            self.action_mono_no_polarisation.setChecked(False)
            self.action_mono_2_polarisations.setChecked(False)
            self.action_mono_4_polarisations.setChecked(False)
            self.action_tof_no_polarisation.setChecked(True)
            self.action_tof_2_polarisations.setChecked(False)
            self.action_tof_4_polarisations.setChecked(False)

        elif action_mode == "action_tof_2_polarisations":
            self.BoToFit_mode = 4
            self.BoToFit_exe = "FilmTOF500QX2.exe"
            self.file_to_wait = "Fit2DFunctDD.dat"
            self.default_entry = "UserDefaults_TOF_2pol.dat"

            self.action_mono_no_polarisation.setChecked(False)
            self.action_mono_2_polarisations.setChecked(False)
            self.action_mono_4_polarisations.setChecked(False)
            self.action_tof_no_polarisation.setChecked(False)
            self.action_tof_2_polarisations.setChecked(True)
            self.action_tof_4_polarisations.setChecked(False)

        elif action_mode == "action_tof_4_polarisations":
            self.BoToFit_mode = 5
            self.BoToFit_exe = "FilmTOF500QX4.exe"
            self.file_to_wait = "Fit2DFunctDD.dat"
            self.default_entry = "UserDefaults_TOF_4pol.dat"

            self.action_mono_no_polarisation.setChecked(False)
            self.action_mono_2_polarisations.setChecked(False)
            self.action_mono_4_polarisations.setChecked(False)
            self.action_tof_no_polarisation.setChecked(False)
            self.action_tof_2_polarisations.setChecked(False)
            self.action_tof_4_polarisations.setChecked(True)

        # reformat table and polarisation parameters
        if self.BoToFit_mode in [0, 3]:
            self.label_scan_parameters_piy.setEnabled(False)
            self.lineEdit_scan_parameters_piy.setEnabled(False)
            self.checkBox_scan_parameters_piy.setEnabled(False)

            self.label_scan_parameters_pfy.setEnabled(False)
            self.lineEdit_scan_parameters_pfy.setEnabled(False)
            self.checkBox_scan_parameters_pfy.setEnabled(False)

            self.label_scan_parameters_pfy.setEnabled(False)
            self.lineEdit_scan_parameters_pfy.setEnabled(False)
            self.checkBox_scan_parameters_pfy.setEnabled(False)

            self.label_scan_parameters_cg.setEnabled(False)
            self.lineEdit_scan_parameters_cg.setEnabled(False)
            self.checkBox_scan_parameters_cg.setEnabled(False)

            self.label_scan_parameters_sg.setEnabled(False)
            self.lineEdit_scan_parameters_sg.setEnabled(False)
            self.checkBox_scan_parameters_sg.setEnabled(False)

            self.label_scan_parameters_sg2.setEnabled(False)
            self.lineEdit_scan_parameters_sg2.setEnabled(False)
            self.checkBox_scan_parameters_sg2.setEnabled(False)

            # columns with checkboxes can change their width depends on Windows scaling settings, so we correct our table
            col_width = round((int(self.tableWidget_film_description.width()) - 4 * int(self.tableWidget_film_description.columnWidth(2))) / 5, 0)

            self.tableWidget_film_description.setColumnWidth(0, col_width)
            self.tableWidget_film_description.setColumnWidth(1, col_width)
            self.tableWidget_film_description.setColumnWidth(2, 1)
            self.tableWidget_film_description.setColumnWidth(3, col_width)
            self.tableWidget_film_description.setColumnWidth(4, 1)
            self.tableWidget_film_description.setColumnWidth(5, col_width)
            self.tableWidget_film_description.setColumnWidth(6, 1)
            self.tableWidget_film_description.setColumnWidth(7, 0)
            self.tableWidget_film_description.setColumnWidth(8, 0)
            self.tableWidget_film_description.setColumnWidth(9, 0)
            self.tableWidget_film_description.setColumnWidth(10, 0)
            self.tableWidget_film_description.setColumnWidth(11, int(self.tableWidget_film_description.width()) - 4 * int(self.tableWidget_film_description.columnWidth(2)) - 4 * col_width - 2)
            self.tableWidget_film_description.setColumnWidth(12, 1)

        elif self.BoToFit_mode in [1, 2, 4, 5]:
            self.label_scan_parameters_piy.setEnabled(True)
            self.lineEdit_scan_parameters_piy.setEnabled(True)
            self.checkBox_scan_parameters_piy.setEnabled(True)

            self.label_scan_parameters_pfy.setEnabled(True)
            self.lineEdit_scan_parameters_pfy.setEnabled(True)
            self.checkBox_scan_parameters_pfy.setEnabled(True)

            self.label_scan_parameters_pfy.setEnabled(True)
            self.lineEdit_scan_parameters_pfy.setEnabled(True)
            self.checkBox_scan_parameters_pfy.setEnabled(True)

            self.label_scan_parameters_cg.setEnabled(True)
            self.lineEdit_scan_parameters_cg.setEnabled(True)
            self.checkBox_scan_parameters_cg.setEnabled(True)

            self.label_scan_parameters_sg.setEnabled(True)
            self.lineEdit_scan_parameters_sg.setEnabled(True)
            self.checkBox_scan_parameters_sg.setEnabled(True)

            self.label_scan_parameters_sg2.setEnabled(True)
            self.lineEdit_scan_parameters_sg2.setEnabled(True)
            self.checkBox_scan_parameters_sg2.setEnabled(True)

            # columns with checkboxes can change their width depends on Windows scaling settings, so we correct our table
            col_width = round((int(self.tableWidget_film_description.width()) - 6 * int(self.tableWidget_film_description.columnWidth(2))) / 7, 0)

            self.tableWidget_film_description.setColumnWidth(0, col_width)
            self.tableWidget_film_description.setColumnWidth(1, col_width + 6)
            self.tableWidget_film_description.setColumnWidth(2, 1)
            self.tableWidget_film_description.setColumnWidth(3, col_width - 7)
            self.tableWidget_film_description.setColumnWidth(4, 1)
            self.tableWidget_film_description.setColumnWidth(5, col_width - 7)
            self.tableWidget_film_description.setColumnWidth(6, 1)
            self.tableWidget_film_description.setColumnWidth(7, col_width - 7)
            self.tableWidget_film_description.setColumnWidth(8, 1)
            self.tableWidget_film_description.setColumnWidth(9, col_width + 9)
            self.tableWidget_film_description.setColumnWidth(10, 1)
            self.tableWidget_film_description.setColumnWidth(11, int(self.tableWidget_film_description.width()) - 6 * int(self.tableWidget_film_description.columnWidth(2)) - 6 * col_width + 4)
            self.tableWidget_film_description.setColumnWidth(12, 1)

        # reformat checkboxes (I, dI, Qz, rad) and Wavelength/Inc.angle field
        if self.BoToFit_mode in [0, 1, 2]:
            if self.comboBox_data_file_column_1.count() < 4:
                self.comboBox_data_file_column_1.addItem("")
                self.comboBox_data_file_column_1.setItemText(3, "ang(rad)")
                self.comboBox_data_file_column_2.addItem("")
                self.comboBox_data_file_column_2.setItemText(3, "ang(rad)")
                self.comboBox_data_file_column_3.addItem("")
                self.comboBox_data_file_column_3.setItemText(3, "ang(rad)")
            self.label_scan_parameters_wavelength.setText("Wavelength (A)")

        elif self.BoToFit_mode in [3, 4, 5]:
            self.comboBox_data_file_column_1.removeItem(3)
            self.comboBox_data_file_column_2.removeItem(3)
            self.comboBox_data_file_column_3.removeItem(3)
            self.label_scan_parameters_wavelength.setText("Inc. ang. (mrad)")

        # load UserDefaults if such are presented
        try:
            if self.default_entry in os.listdir(self.current_dir + "/User_Defaults"):
                self.lineEdit_scan_parameters_wavelength.setText("")
                self.load_entry_file()
        except:
            print("No 'User Defaults' found")

        # clear stuff, just in case
        self.clear_stuff()
        self.lineEdit_data_file.clear()
    ##<--

    ##--> buttons
    def button_data_file(self):
        '''
        if {NoPolarisation} and {toolButton_data_file} is pressed: [user can choose only one file]
        elif {toolButton_data_file} is pressed: [user can choose several file]
        '''

        self.input_structure = [self.comboBox_data_file_column_1.currentText(), self.comboBox_data_file_column_2.currentText(), self.comboBox_data_file_column_3.currentText()]

        if self.BoToFit_mode in [0, 3]:
            data_files = QtWidgets.QFileDialog().getOpenFileName(None, "FileNames", self.current_dir)
        else: data_files = QtWidgets.QFileDialog().getOpenFileNames(None, "FileNames", self.current_dir)

        if data_files[0] == "": return

        self.lineEdit_data_file.setText(str(data_files[0]))

        # clear stuff after last run
        self.clear_stuff()
        self.tableWidget_data_points.clear()
        self.lineEdit_number_of_points.clear()

        if self.BoToFit_mode in [0, 1, 2] and self.lineEdit_scan_parameters_wavelength.text() == "":
            self.statusbar.showMessage("Input wavelength and reimport the file")
        else:
            self.parse_data_files()
            self.draw_reflectivity()

    def buttons_add_remove_layer(self):

        # check where we came from do required action
        try:
            sender_name = self.sender().objectName()
        except:
            sender_name = "None"

        if sender_name == "pushButton_film_description_remove_layer":
            # remove lines from {tableWidget_film_description}
            if not self.tableWidget_film_description.rowCount() == self.tableWidget_film_description.currentRow() + 1:
                self.tableWidget_film_description.removeRow(self.tableWidget_film_description.currentRow())

        else:
            # add lines into {tableWidget_film_description}
            if self.tableWidget_film_description.currentRow() >= 0:
                i = self.tableWidget_film_description.currentRow()
            else:
                i = 0

            self.tableWidget_film_description.insertRow(i)
            self.tableWidget_film_description.setRowHeight(i, 21)

            for j in range(0, 13):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                if j in (2, 4, 6, 8, 10, 12):
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    if j == 6:
                        item.setCheckState(QtCore.Qt.Checked)
                    else:
                        item.setCheckState(QtCore.Qt.Unchecked)

                self.tableWidget_film_description.setItem(i, j, item)

    def button_save_at(self):
        '''
        default {save_at_dit} folder is the one where "BoToFit.exe" is located
        otherwice: defined by user
        '''
        dir = QtWidgets.QFileDialog().getExistingDirectory(None, "FileNames", self.current_dir)
        if dir: self.lineEdit_save_at.setText(str(dir))

    def button_copy_to_start_with(self):

        for i in range(0, self.tableWidget_fit_results.rowCount()):
            if not self.tableWidget_fit_results.item(i,0).checkState() == 2: continue

            parameter = self.tableWidget_fit_results.item(i, 2).text().split()

            # Fill in the table:
            # Substrate has 2 parameters, Layers have 3
            if not len(parameter) == 1:
                start_fit_table_row = self.tableWidget_film_description.rowCount() - 1
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

                self.tableWidget_film_description.item(start_fit_table_row, start_fit_table_column).setText(self.tableWidget_fit_results.item(i, 3).text())

            if parameter[0] == 'Scaling_factor': self.lineEdit_scan_parameters_scaling_factor.setText(self.tableWidget_fit_results.item(i, 3).text())
            if parameter[0] == 'Overillumination': self.lineEdit_scan_parameters_cross_overill.setText(self.tableWidget_fit_results.item(i, 3).text())
            if parameter[0] == 'Background': self.lineEdit_scan_parameters_background.setText(self.tableWidget_fit_results.item(i, 3).text())
            if parameter[0] == '<Cos(gamma)>': self.lineEdit_scan_parameters_cg.setText(self.tableWidget_fit_results.item(i, 3).text())
            if parameter[0] == '<Sin(gamma)>': self.lineEdit_scan_parameters_sg.setText(self.tableWidget_fit_results.item(i, 3).text())
            if parameter[0] == '<Sin^2(gamma)>': self.lineEdit_scan_parameters_sg2.setText(self.tableWidget_fit_results.item(i, 3).text())
            if parameter[0] == 'Pi(y)': self.lineEdit_scan_parameters_piy.setText(self.tableWidget_fit_results.item(i, 3).text())
            if parameter[0] == 'Pf(y)': self.lineEdit_scan_parameters_pfy.setText(self.tableWidget_fit_results.item(i, 3).text())

    def button_start_fitting(self):

        start_time = time.time()

        # for Polarisation - check if User selected to fit both mSLD and cos(d-gamma) for the same layer
        if not self.BoToFit_mode in [0, 3]:
            for i in range(0, self.tableWidget_film_description.rowCount()):
                if self.tableWidget_film_description.item(i, 8).checkState() == 0 and self.tableWidget_film_description.item(i, 10).checkState() == 0:
                    self.statusbar.showMessage("mSLD and cos(d-gamma) can not be fitted together for the same layer")
                    return

        self.checkBox_fit_results_select_all.setChecked(False)

        self.statusbar.showMessage("Running...")

        data_files = []
        for file in self.lineEdit_data_file.text().split("'"):
            if len(file) > 2: data_files.append(file)

        # check if we have file to work with
        if not self.lineEdit_data_file.text(): return

        self.clear_stuff()
        self.draw_reflectivity()

        data_file_input_name = data_files[0][data_files[0].rfind("/") + 1: data_files[0].rfind(".")].replace(" ", "_")

        # create new directory or rewrite files if they already exists
        if not self.lineEdit_save_at.text():
            self.lineEdit_save_at.setText(self.current_dir)

        self.data_folder_name = self.lineEdit_save_at.text() + "/" + data_file_input_name + "/"

        if not os.path.exists(self.data_folder_name):
            os.makedirs(self.data_folder_name)

        # create entry for BoToFit
        self.create_input_data_file()
        self.create_entry_for_BoToFit()

        # Start BoToFit with its "killer" in 2 threads
        module = '"' + self.current_dir + '/BoToFit_Modules/' + self.BoToFit_exe + '"'
        entry = '"' + self.data_folder_name + "entry.dat" + '"'
        data = '"' + self.data_folder_name + "data_file_reformatted.dat" + '"'

        for i in range(2):
            t = threading.Thread(target=self.BoToFit_calc_run, args=(i, module, entry, data, self.lineEdit_scan_parameters_points_to_exclude_first.text(), self.lineEdit_scan_parameters_points_to_exclude_last.text()))
            t.start()

        # wait until "killer" is done or "BoToFit" has crashed
        BoToFit_calc_threads_are_done = 0
        while BoToFit_calc_threads_are_done == 0:
            QtTest.QTest.qWait(1000)
            proc_list = []
            for proc in psutil.process_iter(): proc_list.append(proc.name())

            if self.BoToFit_exe not in proc_list: BoToFit_calc_threads_are_done = 1

        if self.file_to_wait not in os.listdir(self.data_folder_name):
            self.clear_stuff()
            self.draw_reflectivity()
            self.statusbar.showMessage("BoToFit crashed. Consider using more reasonable 'Start fit' values.")
            return

        # wait until fitting is done -> fill the table, draw graphs and create multiGrPr.ent using FitBag.dat file
        self.graphicsView_reflectivity_profile.getPlotItem().clear()
        self.draw_reflectivity()
        self.draw_and_export_reform_FitFunct()
        self.create_fit_results_table_and_multiGrPr_entry()

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
    def parse_data_files(self):
        '''
        I write files with experimental data points into hidden table [tableWidget_data_points] at MainWindow in [*angle, *I, *dI] format to avoid multiple parsings of the same file

        if {we have only one file with experimental points (in case of NoPolarisation)}: {we write it to the first line of the (hidden) table}
        elif {we have 2 polarisations}: {we write files as "uu", "du" in first 2 lines of the (hidden) table}
        elif {we have 4 polarisations}: {we write files as "uu", "dd", "ud", "du" in first 4 lines of the (hidden) table}
        '''

        files = []

        # reformat data to *I *dI *angle(rad) in Mono mode

        if self.BoToFit_mode in [0, 3]:
            files.append(self.lineEdit_data_file.text())
        else:
            for i in self.lineEdit_data_file.text().split("'"):
                if i.rfind("_uu") > 0 or i.rfind("_UU") > 0: files.append(i)

            if self.BoToFit_mode in [2, 5]:

                for i in self.lineEdit_data_file.text().split("'"):
                    if i.rfind("_dd") > 0 or i.rfind("_DD") > 0: files.append(i)

                for i in self.lineEdit_data_file.text().split("'"):
                    if i.rfind("_ud") > 0 or i.rfind("_UD") > 0: files.append(i)

            for i in self.lineEdit_data_file.text().split("'"):
                if i.rfind("_du") > 0 or i.rfind("_DU") > 0: files.append(i)

        for i in range(0, 4):
            for j in range(0, 3):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget_data_points.setItem(i, j, item)

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

            self.lineEdit_number_of_points.setText(str(exper_points_number))
            self.tableWidget_data_points.item(j, 0).setText(str(data_angle))
            self.tableWidget_data_points.item(j, 1).setText(str(data_I))
            self.tableWidget_data_points.item(j, 2).setText(str(data_dI))

            j += 1

    def create_input_data_file(self):
        '''
        input data files for BoToFit should have [*I *dI *angle(rad)] format in Mono mode and [*I *dI *Qz] in TOF mode
        '''

        with open(self.data_folder_name + "data_file_reformatted.dat", 'w') as data_file_output:
            # check hidden table with experimental points already reformatted in Q I dI format
            for i in range(0, 4):
                if self.tableWidget_data_points.item(i, 0).text() not in ("", "[]"):
                    data_angle = self.tableWidget_data_points.item(i, 0).text()[1: -1].replace(",", "").split()
                    data_I = self.tableWidget_data_points.item(i, 1).text()[1: -1].replace(",", "").split()
                    data_dI = self.tableWidget_data_points.item(i, 2).text()[1: -1].replace(",", "").split()

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
        self.tableWidget_film_description.setCurrentCell(-1, -1)

        if self.lineEdit_scan_parameters_wavelength.text() == "":
            if self.default_entry in os.listdir(self.current_dir + "/User_Defaults"):
                entry_file = self.current_dir + "/User_Defaults/" + self.default_entry
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
                        self.lineEdit_scan_parameters_piy.setText(line.split()[0])
                        piy_line = line_number + 1
                    if line_number == piy_line:
                        if line.split()[0] == "n": self.checkBox_scan_parameters_piy.setCheckState(0)
                        elif line.split()[0] == "f": self.checkBox_scan_parameters_piy.setCheckState(2)

                    # Pfy outgoing polarization (analyser)
                    if line.rfind("Pfy") > 0:
                        self.lineEdit_scan_parameters_pfy.setText(line.split()[0])
                        pfy_line = line_number + 1
                    if line_number == pfy_line:
                        if line.split()[0] == "n": self.checkBox_scan_parameters_pfy.setCheckState(0)
                        elif line.split()[0] == "f": self.checkBox_scan_parameters_pfy.setCheckState(2)

                    # cg: mean value <cos(gamma)> over big domains
                    if line.rfind("cos(gamma)") > 0:
                        self.lineEdit_scan_parameters_cg.setText(line.split()[0])
                        cg_line = line_number + 1
                    if line_number == cg_line:
                        if line.split()[0] == "n": self.checkBox_scan_parameters_cg.setCheckState(0)
                        elif line.split()[0] == "f": self.checkBox_scan_parameters_cg.setCheckState(2)
                    # sg: mean value <sin(gamma)> over big domains
                    if line_number == cg_line + 1: self.lineEdit_scan_parameters_sg.setText(line.split()[0])
                    if line_number == cg_line + 2:
                        if line.split()[0] == "n": self.checkBox_scan_parameters_sg.setCheckState(0)
                        elif line.split()[0] == "f": self.checkBox_scan_parameters_sg.setCheckState(2)
                    # sg2: mean value <sin^2(gamma)> over big domains
                    if line_number == cg_line + 3: self.lineEdit_scan_parameters_sg2.setText(line.split()[0])
                    if line_number == cg_line + 4:
                        if line.split()[0] == "n": self.checkBox_scan_parameters_sg2.setCheckState(0)
                        elif line.split()[0] == "f": self.checkBox_scan_parameters_sg2.setCheckState(2)

                # wavelength or incident angle
                '''
                BoToFit entry is almost the same for Mono and TOF modes.
                The only difference is that "incident angle" is used instead of "wavelength".
                '''
                if line.rfind("wavelength") > 0 or line.rfind("incident angle") > 0:
                    self.lineEdit_scan_parameters_wavelength.setText(line.split()[0])
                    wavelength_line = line_number

                # number of experimental points in alpha
                if line_number == wavelength_line + 2: self.lineEdit_scan_parameters_num_of_pts_for_res_function.setText(
                    line.split()[0])
                # step for resolution function (in mrad)
                if line_number == wavelength_line + 3: self.lineEdit_scan_parameters_step_for_res_function.setText(line.split()[0])
                # "sigma" of resolution function (in mrad)
                if line_number == wavelength_line + 4: self.lineEdit_scan_parameters_sigma.setText(line.split()[0])
                # correction of the detector 'zero' (in mrad): alpha-da
                if line.rfind("correction of the") > 0: self.lineEdit_scan_parameters_zero_correction.setText(
                    line.split()[0])

                # ct  total scaling factor
                if line.rfind("scaling factor") > 0:
                    self.lineEdit_scan_parameters_scaling_factor.setText(line.split()[0])
                    scaling_fact_line = line_number + 1
                if line_number == scaling_fact_line:
                    if line.split()[0] == "n":
                        self.checkBox_scan_parameters_scaling_factor.setCheckState(0)
                    elif line.split()[0] == "f":
                        self.checkBox_scan_parameters_scaling_factor.setCheckState(2)
                # alpha_0 crossover angle overillumination (in mrad)
                if line_number == scaling_fact_line + 1: self.lineEdit_scan_parameters_cross_overill.setText(line.split()[0])
                if line_number == scaling_fact_line + 2:
                    if line.split()[0] == "n":
                        self.checkBox_scan_parameters_cross_overill.setCheckState(0)
                    elif line.split()[0] == "f":
                        self.checkBox_scan_parameters_cross_overill.setCheckState(2)
                # bgr 'background'
                if line_number == scaling_fact_line + 3: self.lineEdit_scan_parameters_background.setText(line.split()[0])
                if line_number == scaling_fact_line + 4:
                    if line.split()[0] == "n":
                        self.checkBox_scan_parameters_background.setCheckState(0)
                    elif line.split()[0] == "f":
                        self.checkBox_scan_parameters_background.setCheckState(2)

                if line.rfind("number of layers") > 0:
                    number_of_layers = int(line.split()[0])  # excluding substrate
                    layers_description_line = line_number
                    # delete all layers except substrate
                    while not self.tableWidget_film_description.item(0, 0).text() == "substrate":
                        self.tableWidget_film_description.removeRow(0)
                    # add i layers
                    for i in range(0, number_of_layers):
                        self.buttons_add_remove_layer()
                        self.tableWidget_film_description.item(0, 0).setText("Layer " + str(number_of_layers - i))

                try:
                    if line_number > layers_description_line + 1 and not line == "":

                        # I hide 4 columns in NoPol mode, so we skip them
                        if self.BoToFit_mode in [0, 3] and col == 7: col = 11

                        if col <= 12 and row <= number_of_layers:
                            if line.split()[0] == "n":
                                self.tableWidget_film_description.item(row, col).setCheckState(0)
                            elif line.split()[0] == "f":
                                self.tableWidget_film_description.item(row, col).setCheckState(2)
                            else:
                                self.tableWidget_film_description.item(row, col).setText(line.split()[0].replace("d", "e"))

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
                entry_file.write(self.lineEdit_scan_parameters_piy.text() + '    Piy\n')
                if self.checkBox_scan_parameters_piy.isChecked(): entry_file.write("f" + "   \n")
                else: entry_file.write("n" + "   \n")
                entry_file.write("0     Piz\nf\n\n")

                # outgoing polarization (analyser)
                entry_file.write("0     Pfx outgoing polarization (analyser)\nf\n")
                entry_file.write(self.lineEdit_scan_parameters_pfy.text() + '    Pfy\n')
                if self.checkBox_scan_parameters_pfy.isChecked():
                    entry_file.write("f" + "   \n")
                else:
                    entry_file.write("n" + "   \n")
                entry_file.write("0     Pfz\nf\n\n")

            if not self.BoToFit_mode in [3, 4, 5]:
                entry_file.write(self.lineEdit_scan_parameters_wavelength.text() + '    wavelength (in Angstrem)\n')
            else:
                entry_file.write(self.lineEdit_scan_parameters_wavelength.text() + '    incident angle (in mrad)\n')

            entry_file.write(self.lineEdit_number_of_points.text() + "   *nn number of experimental points in alpha (<1001)\n")
            entry_file.write(self.lineEdit_scan_parameters_num_of_pts_for_res_function.text() + "    *j0 number of points for resolution function (odd) (<102)\n")
            entry_file.write(self.lineEdit_scan_parameters_step_for_res_function.text() + "    step for resolution function (in mrad)\n")
            entry_file.write(self.lineEdit_scan_parameters_sigma.text() + "     *sigma of resolution function (in mrad)\n\n")
            entry_file.write(str(self.tableWidget_film_description.rowCount() - 1) + "   number of layers (excluding substrate) (<21)\n\n")
            # read the table
            for i in range(0, self.tableWidget_film_description.rowCount()):
                comment = ""
                # Thickness
                if not self.tableWidget_film_description.item(i, 0).text() == "substrate":
                    entry_file.write(self.tableWidget_film_description.item(i, 1).text() + "    layer " + str(i+1) + " ("+ self.tableWidget_film_description.item(i, 0).text() + ") thickness (in A)\n")
                    if self.tableWidget_film_description.item(i, 2).checkState() == 2: entry_file.write("f" + "   \n")
                    else: entry_file.write("n" + "   \n")
                else: comment = "substrate's"
                # SLD
                entry_file.write(self.tableWidget_film_description.item(i, 3).text() + "    " + comment + " nbr nuclear SLD Nb'  (in A**-2) *1e6\n")
                if self.tableWidget_film_description.item(i, 4).checkState() == 2: entry_file.write("f" + "   \n")
                else: entry_file.write("n" + "   \n")
                # iSDL
                entry_file.write(self.tableWidget_film_description.item(i, 5).text() + "    " + comment + " nbi nuclear SLD Nb'' (in A**-2) *1e6\n")
                if self.tableWidget_film_description.item(i, 6).checkState() == 2: entry_file.write("f" + "   \n")
                else: entry_file.write("n" + "   \n")

                if self.BoToFit_mode not in [0, 3]:
                    # magnetic SLD
                    entry_file.write(self.tableWidget_film_description.item(i, 7).text() + "    magnetic SLD Np (in A**-2)*1e6\n")
                    if self.tableWidget_film_description.item(i, 8).checkState() == 2: entry_file.write("f\n")
                    else: entry_file.write("n\n")
                    # c=<cos(delta_gamma)>
                    entry_file.write(self.tableWidget_film_description.item(i, 9).text() + "    c=<cos(delta_gamma)>\n")
                    if self.tableWidget_film_description.item(i, 10).checkState() == 2: entry_file.write("f\n")
                    else: entry_file.write("n\n")

                # roughness
                entry_file.write(self.tableWidget_film_description.item(i, 11).text() + "    dw Debye-Waller in [AA]\n")
                if self.tableWidget_film_description.item(i, 12).checkState() == 2: entry_file.write("f\n\n")
                else: entry_file.write("n\n\n")

            if self.BoToFit_mode not in [0, 3]:
                # cg
                entry_file.write(self.lineEdit_scan_parameters_cg.text() + '    cg: mean value <cos(gamma)> over big domains\n')
                if self.checkBox_scan_parameters_cg.isChecked(): entry_file.write("f" + "   \n")
                else: entry_file.write("n" + "   \n")
                # sg
                entry_file.write(self.lineEdit_scan_parameters_sg.text() + '    sg: mean value <sin(gamma)> over big domains\n')
                if self.checkBox_scan_parameters_sg.isChecked(): entry_file.write("f" + "   \n")
                else: entry_file.write("n" + "   \n")
                # sg2
                entry_file.write(self.lineEdit_scan_parameters_sg2.text() + '    sg2: mean value <sin^2(gamma)> over big domains\n')
                if self.checkBox_scan_parameters_sg2.isChecked(): entry_file.write("f" + "  \n\n")
                else: entry_file.write("n" + "   \n\n")

            # ct - total scaling factor
            entry_file.write(self.lineEdit_scan_parameters_scaling_factor.text() + "   *ct  total scaling factor\n")
            if self.checkBox_scan_parameters_scaling_factor.isChecked(): entry_file.write("f" + "   \n")
            else: entry_file.write("n" + "   \n")
            # alpha_0 crossover angle overillumination
            entry_file.write(self.lineEdit_scan_parameters_cross_overill.text() + "   *alpha_0 crossover angle overillumination (in mrad)\n")
            if self.checkBox_scan_parameters_cross_overill.isChecked(): entry_file.write("f" + "   \n")
            else: entry_file.write("n" + "   \n")
            # background
            entry_file.write(self.lineEdit_scan_parameters_background.text() + "   *bgr background\n")
            if self.checkBox_scan_parameters_background.isChecked(): entry_file.write("f" + "   \n")
            else: entry_file.write("n" + "   \n")
            # correction of the detector 'zero'
            entry_file.write("\n" + self.lineEdit_scan_parameters_zero_correction.text() + "   correction of the detector 'zero' (in mrad)\n")
    ##<--

    ##--> "Results table" and "multiGrPr entry"
    def create_fit_results_table_and_multiGrPr_entry(self):
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

        for i in range(1, self.tableWidget_film_description.rowCount() - 1):
            multiGrPr_data.insert(5, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            multiGrPr_info.insert(5, ["Layer " + str(self.tableWidget_film_description.rowCount() - i) + " thickness in (A)", "real part of nuclear SLD Nb'  (in A**-2) *1e-6", "imaginary part of nuclear SLD Nb'' (in A**-2) *1e-6", "magn. scatt. length density (SLD) Np (in A**-2) *1e-6", "c=<cos(delta_gamma)>_{over small domains}", "dw Debye-Waller in [AA]", "grad_d", "grad_Nb", "grad_Np", "grad_DW"])

        last_itr_loc = 0

        multiGrPr = open(self.data_folder_name + 'multiGrPr.ent', 'w')

        multiGrPr_data[2][0] = self.lineEdit_scan_parameters_wavelength.text()
        multiGrPr_data[3][3] = self.tableWidget_film_description.rowCount() - 1

        # clear results_table before another fit
        for i in range(0, self.tableWidget_fit_results.rowCount()): self.tableWidget_fit_results.removeRow(0)

        # do fast run to find last iteration location
        fit_file_name = "FitBag.dat" if not self.BoToFit_mode == 3 else "FitBag.dat"

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

                        if line.split()[0] == "hi_sq.norm:": self.lineEdit_fit_results_chi_square.setText(str("0") + str(line.split()[1]))

                        if line.split()[1] == "iterate": self.lineEdit_fit_results_number_of_iterations.setText(str(line.split()[0]))

                        # Fill table
                        if line.split()[1] in ['thickness', 'SLD', 'iSLD', 'roughness', 'mSLD', 'cos(d-gamma)', 'Scaling_factor',
                                               'Overillumination', 'Background', '<Cos(gamma)>', '<Sin(gamma)>', '<Sin^2(gamma)>', 'Pi(x)', 'Pi(y)', 'Pi(z)', 'Pf(x)', 'Pf(y)', 'Pf(z)'] and not line.split()[3] == "fixed":

                            self.tableWidget_fit_results.insertRow(self.tableWidget_fit_results.rowCount())

                            try:
                                self.tableWidget_fit_results.setRowHeight(i, 22)
                                for j in range(0, 6):
                                    item = QtWidgets.QTableWidgetItem()
                                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                                    item.setFlags(
                                        QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
                                    if j == 0:
                                        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                                        item.setCheckState(QtCore.Qt.Unchecked)
                                    self.tableWidget_fit_results.setItem(i, j, item)

                                self.tableWidget_fit_results.item(i, 1).setText(str(i + 1))
                                self.tableWidget_fit_results.item(i, 2).setText(layer_name + " " + line.split()[1])
                                if line.split()[1] in ['SLD', 'iSLD', 'mSLD']:
                                    self.tableWidget_fit_results.item(i, 3).setText(str(round(float(line.split()[2]) * 10e5, 4)))
                                else:
                                    self.tableWidget_fit_results.item(i, 3).setText(str(float(line.split()[2])))

                                if str(line.split()[3]) == "fixed": table_error = "fixed"
                                elif str(line.split()[4]) == "infinite": table_error = "infinite"
                                else:
                                    if line.split()[1] in ['SLD', 'iSLD', 'mSLD']:
                                        table_error = str(line.split()[3]) + str(round(float(line.split()[4])* 10e5, 4))
                                    else: table_error = str(line.split()[3]) + str(float(line.split()[4]))

                                self.tableWidget_fit_results.item(i, 4).setText(table_error)
                                self.tableWidget_fit_results.item(i, 5).setText(str(float(line.split()[5])))

                            except: a = 1 # print("create_fit_results_table_error_1")
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
                            if line.split()[1] == '<Cos(gamma)>': multiGrPr_data[4+self.tableWidget_film_description.rowCount()][0] = float(line.split()[2])
                            if line.split()[1] == '<Sin(gamma)>': multiGrPr_data[4 + self.tableWidget_film_description.rowCount()][1] = float(line.split()[2])
                            if line.split()[1] == '<Sin^2(gamma)>': multiGrPr_data[4 + self.tableWidget_film_description.rowCount()][2] = float(line.split()[2])
                            if line.split()[1] == 'Scaling_factor': multiGrPr_data[4 + self.tableWidget_film_description.rowCount()+1][0] = float(line.split()[2])
                            if line.split()[1] == 'Overillumination': multiGrPr_data[4 + self.tableWidget_film_description.rowCount()+1][1] = float(line.split()[2])
                            if line.split()[1] == 'Background': multiGrPr_data[4 + self.tableWidget_film_description.rowCount()+1][2] = float(line.split()[2])

                        elif line.split()[1] == 'Pi(y)': multiGrPr_data[0][1] = float(line.split()[2])
                        elif line.split()[1] == 'Pf(y)': multiGrPr_data[1][1] = float(line.split()[2])

                    except: a = 1 #print("create_fit_results_table_error_2 - skip this : " + line)

        for i in range(0, len(multiGrPr_data)):
            for j in range(0, len(multiGrPr_data[i])):
                multiGrPr.write(str(multiGrPr_data[i][j]) + "     " + str(multiGrPr_info[i][j]) + "\n")
            multiGrPr.write("\n")

        multiGrPr.close()
    ##<--

    ##--> draw graphs
    def draw_reflectivity(self):

        if self.sender().objectName() == "pushButton_scan_parameters_redraw_reflectivity":
            self.graphicsView_reflectivity_profile.getPlotItem().clear()

        '''
        draw reflectivity in Angle vs. lg(I) scale using data from hidden table
        '''
        color = [0, 0, 0]

        if "ang(Qz)" in self.input_structure:
            self.label_reflectivity_profile_and_diff.setText("Reflectivity profile (I[10e] vs. Qz[Å**-1]) and Difference (Exper/Fit):")
        elif "ang(rad)" in self.input_structure:
            self.label_reflectivity_profile_and_diff.setText("Reflectivity profile (I[10e] vs. Angle[mrad]) and Difference (Exper/Fit):")

        # if tableWidget_data_points is empty - do nothing
        try:
            self.tableWidget_data_points.item(0, 0).text()
        except:
            return

        for i in range(0, 4):
            if self.tableWidget_data_points.item(i, 0).text() not in ("", "[]"):
                data_angle = self.tableWidget_data_points.item(i, 0).text()[1: -1].replace(",", "").split()
                data_I = self.tableWidget_data_points.item(i, 1).text()[1: -1].replace(",", "").split()
                data_dI = self.tableWidget_data_points.item(i, 2).text()[1: -1].replace(",", "").split()

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

                s1 = pg.ErrorBarItem(x=numpy.array(plot_angle[int(self.lineEdit_scan_parameters_points_to_exclude_first.text()): -int(self.lineEdit_scan_parameters_points_to_exclude_last.text()) - 1]), y=numpy.array(plot_I[int(self.lineEdit_scan_parameters_points_to_exclude_first.text()): -int(self.lineEdit_scan_parameters_points_to_exclude_last.text()) - 1]), top=numpy.array(plot_dI_err_top[int(self.lineEdit_scan_parameters_points_to_exclude_first.text()): -int(self.lineEdit_scan_parameters_points_to_exclude_last.text()) - 1]), bottom=numpy.array(plot_dI_err_bottom[int(self.lineEdit_scan_parameters_points_to_exclude_first.text()): -int(self.lineEdit_scan_parameters_points_to_exclude_last.text()) - 1]), pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                self.graphicsView_reflectivity_profile.addItem(s1)

                s2 = pg.ScatterPlotItem(x=plot_angle[int(self.lineEdit_scan_parameters_points_to_exclude_first.text()): -int(self.lineEdit_scan_parameters_points_to_exclude_last.text()) - 1], y=plot_I[int(self.lineEdit_scan_parameters_points_to_exclude_first.text()): -int(self.lineEdit_scan_parameters_points_to_exclude_last.text()) - 1], symbol="o", size=2, pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                self.graphicsView_reflectivity_profile.addItem(s2)

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
                    if not self.BoToFit_mode in [3, 4, 5] and "ang(Qz)" in self.input_structure: export_fit_funct_file.write(str((4 * math.pi / float(self.lineEdit_scan_parameters_wavelength.text())) * math.sin(float(line.split()[0]))) + "    " + str((line.split()[1])) + "\n")

                s3 = pg.PlotDataItem(plot_angle, plot_I, pen = pg.mkPen(color=(file[1][0], file[1][1], file[1][2]), width=2))
                self.graphicsView_reflectivity_profile.addItem(s3)

    def draw_SLD(self):
        '''
        draw SLD profiles, calculated in multiGrPr.exe
        '''

        self.graphicsView_sld_profile.getPlotItem().clear()

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
            self.graphicsView_sld_profile.addItem(s4)

            s5 = pg.PlotDataItem(dist[:max(cut_1, cut_2)+ 50], sld_2[:max(cut_1, cut_2) + 50], pen=pg.mkPen(color=(0,0,0), width=2))
            self.graphicsView_sld_profile.addItem(s5)

    def draw_diff(self):
        '''
        Here I compare experimental points with fitting curves

        data in [tableWidget_data_points] order:
            0pol = line 0
            2pol = line 0 (uu), line 1(du)
            4pol = line 0 (uu), line 1(dd), line 2 (ud), line 3(du)
        '''

        self.graphicsView_diff.getPlotItem().clear()

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
                            else: fit_funct_angle.append((4 * math.pi / float(self.lineEdit_scan_parameters_wavelength.text())) * math.sin(float(line.split()[0])))
                        fit_funct_I.append(float(line.split()[1]))
                    except:
                        a = 1

                s = InterpolatedUnivariateSpline(numpy.array(fit_funct_angle), numpy.array(fit_funct_I), k=1)

            if self.tableWidget_data_points.item(i, 0).text() not in ("", "[]"):
                scale_angle = numpy.array(self.tableWidget_data_points.item(i, 0).text()[1: -1].replace(",", "").split()).astype(float)[int(self.lineEdit_scan_parameters_points_to_exclude_first.text()) : -int(self.lineEdit_scan_parameters_points_to_exclude_last.text())-1]
                data_I = numpy.array(self.tableWidget_data_points.item(i, 1).text()[1: -1].replace(",", "").split()).astype(float)[int(self.lineEdit_scan_parameters_points_to_exclude_first.text()) : -int(self.lineEdit_scan_parameters_points_to_exclude_last.text())-1]

                for i in range(0, len(scale_angle)):
                    if data_I[i] != 0:
                        diff_I.append(data_I[i] / s(scale_angle[i]))
                    else: zero_I.append(i)

            s6 = pg.PlotDataItem(numpy.delete(scale_angle, zero_I), diff_I, pen = pg.mkPen(color=(file[1][0], file[1][1], file[1][2]), width=2))
            self.graphicsView_diff.addItem(s6)
    ##<--

    ##--> reformat data for user in Mono modes if he uses Qz as an angle
    def export_for_user(self):

        # create reformatted files (in Qz I dI) named "Export"
        if self.BoToFit_mode == 0: num_rows = 1
        elif self.BoToFit_mode == 1: num_rows = 2
        elif self.BoToFit_mode == 2: num_rows = 4

        for i in range(0, num_rows):
            if num_rows == 1:
                file_name_export_data_points = "/EXPORT - Qz_I_dI - data points.dat"
            elif num_rows == 2:
                if i == 0:
                    file_name_export_data_points = "/EXPORT - Qz_I_dI - data points - U.dat"
                else:
                    file_name_export_data_points = "/EXPORT - Qz_I_dI - data points - D.dat"
            elif num_rows == 4:
                if i == 0:
                    file_name_export_data_points = "/EXPORT - Qz_I_dI - data points - UU.dat"
                elif i == 1:
                    file_name_export_data_points = "/EXPORT - Qz_I_dI - data points - DD.dat"
                elif i == 2:
                    file_name_export_data_points = "/EXPORT - Qz_I_dI - data points - UD.dat"
                else:
                    file_name_export_data_points = "/EXPORT - Qz_I_dI - data points - DU.dat"

            with open(self.data_folder_name + file_name_export_data_points, "w") as export_data_points:
                data_Qz = self.tableWidget_data_points.item(i, 0).text()[1: -1].replace(",", "").split()
                data_I = self.tableWidget_data_points.item(i, 1).text()[1: -1].replace(",", "").split()
                data_dI = self.tableWidget_data_points.item(i, 2).text()[1: -1].replace(",", "").split()

                for j in range(0, len(data_I)):
                    export_data_points.write(str(data_Qz[j]) + "    " + str(data_I[j]) + "    " + str(data_dI[j]) + "\n")
    ##<--

    ##--> extra functions to shorten the code
    def clear_stuff(self):
        self.graphicsView_reflectivity_profile.getPlotItem().clear()
        self.graphicsView_sld_profile.getPlotItem().clear()
        self.graphicsView_diff.getPlotItem().clear()
        self.lineEdit_fit_results_number_of_iterations.clear()
        self.lineEdit_fit_results_chi_square.clear()
        for i in range(0, self.tableWidget_fit_results.rowCount()): self.tableWidget_fit_results.removeRow(0)

    def angle_convert(self, input_unit, output_unit, input_value):

        if output_unit == "Qz":
            if input_unit == "Qz": output_value = float(input_value)
            elif input_unit == "rad": output_value = (4 * math.pi / float(self.lineEdit_scan_parameters_wavelength.text())) * math.sin(float(input_value))

        elif output_unit == "rad":
            if input_unit == "Qz": output_value = math.asin(float(input_value) * float(self.lineEdit_scan_parameters_wavelength.text()) / (4 * math.pi))
            elif input_unit == "rad": output_value = float(input_value)

        return output_value

    def fit_results_select_all(self):
        if self.checkBox_fit_results_select_all.isChecked():
            for i in range(0, self.tableWidget_fit_results.rowCount()):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setCheckState(QtCore.Qt.Checked)
                self.tableWidget_fit_results.setItem(i, 0, item)

        else:
            for i in range(0, self.tableWidget_fit_results.rowCount()):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setCheckState(QtCore.Qt.Unchecked)
                self.tableWidget_fit_results.setItem(i, 0, item)

    def BoToFit_calc_run(self, thread, module, entry, data, pts_to_skip_left, pts_to_skip_right):

        if thread == 0:
            # define that BoToFit is done by checking the folder for "self.file_to_wait"

            # delete old FitFunct.dat file
            try:
                os.remove(self.data_folder_name + self.file_to_wait)
            except:
                print("Nothing to delete (FitFunct)")

            # check every second if BoToFit is done
            while self.file_to_wait not in os.listdir(self.data_folder_name):

                QtTest.QTest.qWait(1000)

                # check if BoToFit crashed
                proc_list = []
                for proc in psutil.process_iter(): proc_list.append(proc.name())
                if self.BoToFit_exe not in proc_list: return

            # wait 5 sec more to make sure that FitFunct file is ready
            QtTest.QTest.qWait(5000)

            # when its done, kill BoToFit process
            for proc in psutil.process_iter():
                if proc.name() == self.BoToFit_exe:
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

