from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
import os, psutil, time, math, numpy, shutil
import pyqtgraph as pg
from scipy.interpolate import InterpolatedUnivariateSpline

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

current_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

class Ui_MainWindow(object):
    def __init__(self):

        # save_at directory
        self.save_dir = ""

        # structure of the data file
        self.input_structure = []

        # list of modes: "0" - Mono, No polarisation, "1" - Mono, 2 polarisations, "2" - Mono, 4 polarisations, "3" - TOF, No polarisations
        self.BoToFit_mode = 0

        # list of exe: "Film500x0.exe" - Mono, No polarisation, "Film500x2.exe" - Mono, 2 polarisations, "Film500x4.exe" - Mono, 4 polarisations, "FilmTOF500QX0.exe" - TOF, No polarisations
        self.BoToFit_exe = "Film500x0.exe"

    ##--> define user interface elements
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1228, 945)
        MainWindow.setMinimumSize(QtCore.QSize(1228, 945))
        MainWindow.setMaximumSize(QtCore.QSize(1228, 945))
        font = QtGui.QFont()
        font.setPointSize(8)
        MainWindow.setFont(font)
        MainWindow.setWindowIcon(QtGui.QIcon(current_dir + "\icon.png"))
        MainWindow.setIconSize(QtCore.QSize(30, 30))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_data_file = QtWidgets.QLabel(self.centralwidget)
        self.label_data_file.setGeometry(QtCore.QRect(20, 0, 191, 16))
        self.label_data_file.setFont(font)
        self.label_data_file.setObjectName("label_data_file")
        self.label_start_fit_with = QtWidgets.QLabel(self.centralwidget)
        self.label_start_fit_with.setGeometry(QtCore.QRect(20, 60, 141, 16))
        self.label_start_fit_with.setFont(font)
        self.label_start_fit_with.setObjectName("label_start_fit_with")
        self.label_save_at = QtWidgets.QLabel(self.centralwidget)
        self.label_save_at.setFont(font)
        self.label_save_at.setGeometry(QtCore.QRect(20, 460, 151, 16))
        self.label_save_at.setObjectName("label_save_at")
        self.label_graphs_refl_and_diff = QtWidgets.QLabel(self.centralwidget)
        self.label_graphs_refl_and_diff.setFont(font)
        self.label_graphs_refl_and_diff.setGeometry(QtCore.QRect(20, 520, 541, 16))
        self.label_graphs_refl_and_diff.setObjectName("label_graphs_refl_and_diff")
        self.label_sld_profile = QtWidgets.QLabel(self.centralwidget)
        self.label_sld_profile.setFont(font)
        self.label_sld_profile.setGeometry(QtCore.QRect(630, 520, 481, 16))
        self.label_sld_profile.setObjectName("label_sld_profile")
        self.label_fit_results = QtWidgets.QLabel(self.centralwidget)
        self.label_fit_results.setFont(font)
        self.label_fit_results.setGeometry(QtCore.QRect(730, 0, 101, 16))
        self.label_fit_results.setObjectName("label_fit_results")

        self.groupBox_data_file = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_data_file.setGeometry(QtCore.QRect(10, 0, 701, 60))
        self.groupBox_data_file.setObjectName("groupBox_data_file")
        self.toolButton_data_file = QtWidgets.QToolButton(self.groupBox_data_file)
        self.toolButton_data_file.setGeometry(QtCore.QRect(435, 26, 26, 26))
        self.toolButton_data_file.setObjectName("toolButton_data_file")
        self.lineEdit_data_file = QtWidgets.QLineEdit(self.groupBox_data_file)
        self.lineEdit_data_file.setGeometry(QtCore.QRect(10, 26, 421, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEdit_data_file.setFont(font)
        self.lineEdit_data_file.setObjectName("lineEdit_data_file")
        self.comboBox_1 = QtWidgets.QComboBox(self.groupBox_data_file)
        self.comboBox_1.setGeometry(QtCore.QRect(470, 26, 72, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.comboBox_1.setFont(font)
        self.comboBox_1.setObjectName("comboBox_1")
        for i in range(0, 4): self.comboBox_1.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(self.groupBox_data_file)
        self.comboBox_2.setGeometry(QtCore.QRect(545, 26, 72, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName("comboBox_2")
        for i in range(0, 4): self.comboBox_2.addItem("")
        self.comboBox_3 = QtWidgets.QComboBox(self.groupBox_data_file)
        self.comboBox_3.setGeometry(QtCore.QRect(620, 26, 72, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.comboBox_3.setFont(font)
        self.comboBox_3.setObjectName("comboBox_3")
        for i in range(0, 4): self.comboBox_3.addItem("")
        self.groupBox_start_fit_with = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_start_fit_with.setGeometry(QtCore.QRect(10, 60, 701, 371))
        self.groupBox_start_fit_with.setObjectName("groupBox_start_fit_with")
        self.tabWidget_data_for_fitting = QtWidgets.QTabWidget(self.groupBox_start_fit_with)
        self.tabWidget_data_for_fitting.setGeometry(QtCore.QRect(1, 18, 700, 354))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tabWidget_data_for_fitting.setFont(font)
        self.tabWidget_data_for_fitting.setObjectName("tabWidget_data_for_fitting")
        self.Tab_film_description = QtWidgets.QWidget()
        self.Tab_film_description.setObjectName("Tab_film_description")
        self.pushButton_add_layer = QtWidgets.QPushButton(self.Tab_film_description)
        self.pushButton_add_layer.setGeometry(QtCore.QRect(490, 295, 93, 30))
        self.pushButton_add_layer.setObjectName("pushButton_add_layer")
        self.pushButton_remove_layer = QtWidgets.QPushButton(self.Tab_film_description)
        self.pushButton_remove_layer.setGeometry(QtCore.QRect(590, 295, 105, 30))
        self.pushButton_remove_layer.setObjectName("pushButton_remove_layer")
        self.tableWidget_film = QtWidgets.QTableWidget(self.Tab_film_description)
        self.tableWidget_film.setGeometry(QtCore.QRect(-2, -1, 700, 294))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tableWidget_film.setFont(font)
        self.tableWidget_film.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget_film.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableWidget_film.setObjectName("tableWidget_film")
        self.tableWidget_film.setColumnCount(13)
        self.tableWidget_film.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_film.setVerticalHeaderItem(0, item)
        for i in range(0, 13):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget_film.setHorizontalHeaderItem(i, item)
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
            self.tableWidget_film.setItem(0, i, item)
        self.tableWidget_film.horizontalHeader().setDefaultSectionSize(23)
        self.tableWidget_film.verticalHeader().setVisible(False)

        self.pushButton_load_entry = QtWidgets.QPushButton(self.Tab_film_description)
        self.pushButton_load_entry.setGeometry(QtCore.QRect(0, 295, 131, 30))
        self.pushButton_load_entry.setObjectName("pushButton_load_entry")
        self.tabWidget_data_for_fitting.addTab(self.Tab_film_description, "")
        self.tab_scan_param = QtWidgets.QWidget()
        self.tab_scan_param.setObjectName("tab_scan_param")
        self.label_wavelength = QtWidgets.QLabel(self.tab_scan_param)
        self.label_wavelength.setGeometry(QtCore.QRect(410, 10, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_wavelength.setFont(font)
        self.label_wavelength.setObjectName("label_wavelength")
        self.label_n_of_pts_f_resol_funct = QtWidgets.QLabel(self.tab_scan_param)
        self.label_n_of_pts_f_resol_funct.setGeometry(QtCore.QRect(10, 10, 311, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_n_of_pts_f_resol_funct.setFont(font)
        self.label_n_of_pts_f_resol_funct.setObjectName("label_n_of_pts_f_resol_funct")
        self.label_step_f_resol_funct = QtWidgets.QLabel(self.tab_scan_param)
        self.label_step_f_resol_funct.setGeometry(QtCore.QRect(10, 30, 291, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_step_f_resol_funct.setFont(font)
        self.label_step_f_resol_funct.setObjectName("label_step_f_resol_funct")
        self.label_sigma = QtWidgets.QLabel(self.tab_scan_param)
        self.label_sigma.setGeometry(QtCore.QRect(10, 50, 291, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_sigma.setFont(font)
        self.label_sigma.setObjectName("label_sigma")
        self.label_zero_correction = QtWidgets.QLabel(self.tab_scan_param)
        self.label_zero_correction.setGeometry(QtCore.QRect(10, 70, 281, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_zero_correction.setFont(font)
        self.label_zero_correction.setObjectName("label_zero_correction")
        self.lineEdit_zero_correction = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_zero_correction.setGeometry(QtCore.QRect(260, 70, 101, 19))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEdit_zero_correction.setFont(font)
        self.lineEdit_zero_correction.setPlaceholderText("")
        self.lineEdit_zero_correction.setObjectName("lineEdit_zero_correction")
        self.label_cross_overill = QtWidgets.QLabel(self.tab_scan_param)
        self.label_cross_overill.setGeometry(QtCore.QRect(10, 90, 311, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_cross_overill.setFont(font)
        self.label_cross_overill.setObjectName("label_cross_overill")
        self.checkBox_scaling_factor = QtWidgets.QCheckBox(self.tab_scan_param)
        self.checkBox_scaling_factor.setGeometry(QtCore.QRect(640, 30, 20, 20))
        self.checkBox_scaling_factor.setText("")
        self.checkBox_scaling_factor.setChecked(True)
        self.checkBox_scaling_factor.setTristate(False)
        self.checkBox_scaling_factor.setObjectName("checkBox_scaling_factor")
        self.lineEdit_scaling_factor = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_scaling_factor.setGeometry(QtCore.QRect(530, 30, 101, 19))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEdit_scaling_factor.setFont(font)
        self.lineEdit_scaling_factor.setText("")
        self.lineEdit_scaling_factor.setPlaceholderText("")
        self.lineEdit_scaling_factor.setObjectName("lineEdit_scaling_factor")
        self.label_scaling_factor = QtWidgets.QLabel(self.tab_scan_param)
        self.label_scaling_factor.setGeometry(QtCore.QRect(410, 30, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_scaling_factor.setFont(font)
        self.label_scaling_factor.setObjectName("label_scaling_factor")
        self.label_background = QtWidgets.QLabel(self.tab_scan_param)
        self.label_background.setGeometry(QtCore.QRect(410, 50, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_background.setFont(font)
        self.label_background.setObjectName("label_background")
        self.lineEdit_background = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_background.setGeometry(QtCore.QRect(530, 50, 101, 19))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEdit_background.setFont(font)
        self.lineEdit_background.setPlaceholderText("")
        self.lineEdit_background.setObjectName("lineEdit_background")
        self.checkBox_background = QtWidgets.QCheckBox(self.tab_scan_param)
        self.checkBox_background.setGeometry(QtCore.QRect(640, 50, 21, 20))
        self.checkBox_background.setText("")
        self.checkBox_background.setChecked(True)
        self.checkBox_background.setObjectName("checkBox_background")
        self.checkBox_cross_overill = QtWidgets.QCheckBox(self.tab_scan_param)
        self.checkBox_cross_overill.setGeometry(QtCore.QRect(370, 90, 21, 20))
        self.checkBox_cross_overill.setText("")
        self.checkBox_cross_overill.setChecked(False)
        self.checkBox_cross_overill.setObjectName("checkBox_cross_overill")
        self.lineEdit_cross_overill = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_cross_overill.setGeometry(QtCore.QRect(260, 90, 101, 19))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEdit_cross_overill.setFont(font)
        self.lineEdit_cross_overill.setPlaceholderText("")
        self.lineEdit_cross_overill.setObjectName("lineEdit_cross_overill")
        self.lineEdit_wavelength = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_wavelength.setGeometry(QtCore.QRect(530, 10, 101, 19))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEdit_wavelength.setFont(font)
        self.lineEdit_wavelength.setPlaceholderText("")
        self.lineEdit_wavelength.setObjectName("lineEdit_wavelength")
        self.lineEdit_n_of_pts_f_resol_funct = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_n_of_pts_f_resol_funct.setGeometry(QtCore.QRect(260, 10, 101, 19))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEdit_n_of_pts_f_resol_funct.setFont(font)
        self.lineEdit_n_of_pts_f_resol_funct.setPlaceholderText("")
        self.lineEdit_n_of_pts_f_resol_funct.setObjectName("lineEdit_n_of_pts_f_resol_funct")
        self.lineEdit_step_f_resol_funct = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_step_f_resol_funct.setGeometry(QtCore.QRect(260, 30, 101, 19))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEdit_step_f_resol_funct.setFont(font)
        self.lineEdit_step_f_resol_funct.setPlaceholderText("")
        self.lineEdit_step_f_resol_funct.setObjectName("lineEdit_step_f_resol_funct")
        self.lineEdit_sigma = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_sigma.setGeometry(QtCore.QRect(260, 50, 101, 19))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEdit_sigma.setFont(font)
        self.lineEdit_sigma.setPlaceholderText("")
        self.lineEdit_sigma.setObjectName("lineEdit_sigma")
        self.lineEdit_piy = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_piy.setEnabled(True)
        self.lineEdit_piy.setGeometry(QtCore.QRect(310, 210, 101, 19))
        self.lineEdit_piy.setObjectName("lineEdit_piy")
        self.lineEdit_pfy = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_pfy.setGeometry(QtCore.QRect(310, 230, 101, 19))
        self.lineEdit_pfy.setObjectName("lineEdit_pfy")
        self.lineEdit_cg = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_cg.setGeometry(QtCore.QRect(310, 250, 101, 19))
        self.lineEdit_cg.setObjectName("lineEdit_cg")
        self.lineEdit_sg = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_sg.setGeometry(QtCore.QRect(310, 270, 101, 19))
        self.lineEdit_sg.setObjectName("lineEdit_sg")
        self.lineEdit_sg2 = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_sg2.setGeometry(QtCore.QRect(310, 290, 101, 19))
        self.lineEdit_sg2.setObjectName("lineEdit_sg2")
        self.checkBox_piy = QtWidgets.QCheckBox(self.tab_scan_param)
        self.checkBox_piy.setEnabled(True)
        self.checkBox_piy.setGeometry(QtCore.QRect(420, 210, 21, 20))
        self.checkBox_piy.setText("")
        self.checkBox_piy.setObjectName("checkBox_piy")
        self.checkBox_cg = QtWidgets.QCheckBox(self.tab_scan_param)
        self.checkBox_cg.setGeometry(QtCore.QRect(420, 250, 21, 20))
        self.checkBox_cg.setText("")
        self.checkBox_cg.setObjectName("checkBox_cg")
        self.checkBox_sg = QtWidgets.QCheckBox(self.tab_scan_param)
        self.checkBox_sg.setGeometry(QtCore.QRect(420, 270, 21, 20))
        self.checkBox_sg.setText("")
        self.checkBox_sg.setObjectName("checkBox_sg")
        self.checkBox_pfy = QtWidgets.QCheckBox(self.tab_scan_param)
        self.checkBox_pfy.setGeometry(QtCore.QRect(420, 230, 21, 20))
        self.checkBox_pfy.setText("")
        self.checkBox_pfy.setObjectName("checkBox_pfy")
        self.checkBox_sg2 = QtWidgets.QCheckBox(self.tab_scan_param)
        self.checkBox_sg2.setGeometry(QtCore.QRect(420, 290, 21, 20))
        self.checkBox_sg2.setText("")
        self.checkBox_sg2.setObjectName("checkBox_sg2")
        self.label_piy = QtWidgets.QLabel(self.tab_scan_param)
        self.label_piy.setEnabled(True)
        self.label_piy.setGeometry(QtCore.QRect(10, 210, 291, 16))
        self.label_piy.setObjectName("label_piy")
        self.label_pfy = QtWidgets.QLabel(self.tab_scan_param)
        self.label_pfy.setGeometry(QtCore.QRect(10, 230, 251, 16))
        self.label_pfy.setObjectName("label_pfy")
        self.label_cg = QtWidgets.QLabel(self.tab_scan_param)
        self.label_cg.setGeometry(QtCore.QRect(10, 250, 291, 16))
        self.label_cg.setObjectName("label_cg")
        self.label_sg = QtWidgets.QLabel(self.tab_scan_param)
        self.label_sg.setGeometry(QtCore.QRect(10, 270, 291, 16))
        self.label_sg.setObjectName("label_sg")
        self.label_sg2 = QtWidgets.QLabel(self.tab_scan_param)
        self.label_sg2.setGeometry(QtCore.QRect(10, 290, 291, 16))
        self.label_sg2.setObjectName("label_sg2")
        self.label_exclude_last = QtWidgets.QLabel(self.tab_scan_param)
        self.label_exclude_last.setGeometry(QtCore.QRect(10, 160, 191, 16))
        self.label_exclude_last.setObjectName("label_exclude_last")
        self.lineEdit_exclude_first = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_exclude_first.setGeometry(QtCore.QRect(260, 140, 101, 19))
        self.lineEdit_exclude_first.setObjectName("lineEdit_exclude_first")
        self.lineEdit_exclude_last = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_exclude_last.setGeometry(QtCore.QRect(260, 160, 101, 19))
        self.lineEdit_exclude_last.setObjectName("lineEdit_exclude_last")
        self.label_exclude_first = QtWidgets.QLabel(self.tab_scan_param)
        self.label_exclude_first.setGeometry(QtCore.QRect(10, 140, 191, 16))
        self.label_exclude_first.setObjectName("label_exclude_first")
        self.pushButton_redraw_refl = QtWidgets.QPushButton(self.tab_scan_param)
        self.pushButton_redraw_refl.setGeometry(QtCore.QRect(370, 140, 121, 39))
        self.pushButton_redraw_refl.setObjectName("pushButton_redraw_refl")
        self.tabWidget_data_for_fitting.addTab(self.tab_scan_param, "")
        self.groupBox_fit_results = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_fit_results.setGeometry(QtCore.QRect(720, 0, 501, 515))
        self.groupBox_fit_results.setObjectName("groupBox_fit_results")

        self.tableWidget_fit_results = QtWidgets.QTableWidget(self.groupBox_fit_results)
        self.tableWidget_fit_results.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_fit_results.setGeometry(QtCore.QRect(1, 50, 500, 465))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.tableWidget_fit_results.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tableWidget_fit_results.setFont(font)
        self.tableWidget_fit_results.setObjectName("tableWidget_fit_results")
        self.tableWidget_fit_results.setColumnCount(5)
        self.tableWidget_fit_results.setRowCount(0)
        for i in range(0, 5):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_fit_results.setHorizontalHeaderItem(i, item)
        self.tableWidget_fit_results.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget_fit_results.verticalHeader().setVisible(False)
        self.label_iter_numb = QtWidgets.QLabel(self.groupBox_fit_results)
        self.label_iter_numb.setGeometry(QtCore.QRect(10, 18, 161, 31))
        self.label_iter_numb.setObjectName("label_iter_numb")
        self.label_chi_sq_norm = QtWidgets.QLabel(self.groupBox_fit_results)
        self.label_chi_sq_norm.setGeometry(QtCore.QRect(342, 18, 151, 31))
        self.label_chi_sq_norm.setObjectName("label_chi_sq_norm")
        self.lineEdit_iter_number = QtWidgets.QLineEdit(self.groupBox_fit_results)
        self.lineEdit_iter_number.setGeometry(QtCore.QRect(120, 24, 41, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEdit_iter_number.setFont(font)
        self.lineEdit_iter_number.setReadOnly(True)
        self.lineEdit_iter_number.setObjectName("lineEdit_iter_number")
        self.lineEdit_chi_sq = QtWidgets.QLineEdit(self.groupBox_fit_results)
        self.lineEdit_chi_sq.setGeometry(QtCore.QRect(416, 24, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEdit_chi_sq.setFont(font)
        self.lineEdit_chi_sq.setReadOnly(True)
        self.lineEdit_chi_sq.setObjectName("lineEdit_chi_sq")

        # lineEdit_data_folder_name, lineEdit_pts_num and tableWidget_data_points are hidden from the user. Used to avoid reopenning data file multiple times
        self.lineEdit_pts_num = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_pts_num.setEnabled(False)
        self.lineEdit_pts_num.setGeometry(QtCore.QRect(570, 290, 0, 0))
        self.lineEdit_pts_num.setObjectName("lineEdit_pts_num")

        self.lineEdit_data_folder_name = QtWidgets.QLineEdit(self.tab_scan_param)
        self.lineEdit_data_folder_name.setEnabled(False)
        self.lineEdit_data_folder_name.setGeometry(QtCore.QRect(575, 290, 0, 0))
        self.lineEdit_data_folder_name.setObjectName("lineEdit_data_folder_name")

        self.tableWidget_data_points = QtWidgets.QTableWidget(self.tab_scan_param)
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

        self.label_botofit_crashed = QtWidgets.QLabel(self.groupBox_fit_results)
        self.label_botofit_crashed.setGeometry(QtCore.QRect(80, 260, 551, 20))
        self.label_botofit_crashed.setObjectName("label_botofit_crashed")

        self.label_need_wavelength = QtWidgets.QLabel(self.groupBox_fit_results)
        self.label_need_wavelength.setGeometry(QtCore.QRect(20, 260, 551, 20))
        self.label_need_wavelength.setObjectName("label_need_wavelength")

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.pushButton_start_fitting = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start_fitting.setGeometry(QtCore.QRect(480, 438, 231, 31))
        self.pushButton_start_fitting.setFont(font)
        self.pushButton_start_fitting.setObjectName("pushButton_start_fitting")
        self.groupBox_save_at_dir = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_save_at_dir.setGeometry(QtCore.QRect(10, 460, 701, 55))
        self.groupBox_save_at_dir.setObjectName("groupBox_save_at_dir")
        self.lineEdit_save_at_dir = QtWidgets.QLineEdit(self.groupBox_save_at_dir)
        self.lineEdit_save_at_dir.setGeometry(QtCore.QRect(10, 23, 651, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEdit_save_at_dir.setFont(font)
        self.lineEdit_save_at_dir.setObjectName("lineEdit_save_at_dir")
        self.toolButton_save_at_dir = QtWidgets.QToolButton(self.groupBox_save_at_dir)
        self.toolButton_save_at_dir.setGeometry(QtCore.QRect(670, 23, 26, 26))
        self.toolButton_save_at_dir.setObjectName("toolButton_save_at_dir")
        self.groupBox_refl_profile = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_refl_profile.setGeometry(QtCore.QRect(10, 520, 601, 381))
        self.groupBox_refl_profile.setObjectName("groupBox_refl_profile")

        self.groupBox_sld_profile = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_sld_profile.setGeometry(QtCore.QRect(620, 520, 601, 381))
        self.groupBox_sld_profile.setObjectName("groupBox_sld_profile")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1229, 29))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1228, 26))
        self.menuBar.setObjectName("menuBar")
        self.menu_MenuBar = QtWidgets.QMenu(self.menuBar)
        self.menu_MenuBar.setObjectName("menu_MenuBar")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.action_mono_no_polarisation = QtWidgets.QAction(MainWindow)
        self.action_mono_no_polarisation.setCheckable(True)
        self.action_mono_no_polarisation.setChecked(True)
        self.action_mono_no_polarisation.setObjectName("action_mono_no_polarisation")
        self.action_mono_2_polarisations = QtWidgets.QAction(MainWindow)
        self.action_mono_2_polarisations.setCheckable(True)
        self.action_mono_2_polarisations.setObjectName("action_mono_2_polarisations")
        self.action_mono_4_polarisations = QtWidgets.QAction(MainWindow)
        self.action_mono_4_polarisations.setCheckable(True)
        self.action_mono_4_polarisations.setObjectName("action_mono_4_polarisations")
        self.action_tof_no_polarisation = QtWidgets.QAction(MainWindow)
        self.action_tof_no_polarisation.setCheckable(True)
        self.action_tof_no_polarisation.setObjectName("action_tof_no_polarisation")
        self.actionAlgorithm_info = QtWidgets.QAction(MainWindow)
        self.actionAlgorithm_info.setObjectName("actionAlgorithm_info")
        self.actionVersion = QtWidgets.QAction(MainWindow)
        self.actionVersion.setCheckable(False)
        self.actionVersion.setObjectName("actionVersion")
        self.menu_MenuBar.addAction(self.action_mono_no_polarisation)
        self.menu_MenuBar.addAction(self.action_mono_2_polarisations)
        self.menu_MenuBar.addAction(self.action_mono_4_polarisations)
        self.menu_MenuBar.addAction(self.action_tof_no_polarisation)
        self.menuHelp.addAction(self.actionAlgorithm_info)
        self.menuHelp.addAction(self.actionVersion)
        self.menuBar.addAction(self.menu_MenuBar.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget_data_for_fitting.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BoToFit"))

        self.label_data_file.setText(_translate("MainWindow", "Data file and structure:"))
        self.label_start_fit_with.setText(_translate("MainWindow", "Start fit with:"))
        self.label_save_at.setText(_translate("MainWindow", "Save results at:"))
        self.label_graphs_refl_and_diff.setText(_translate("MainWindow", "Reflectivity profile (Reflectivity [10e] vs. Qz[Å**-1]) and Difference (Exper/Fit):"))
        self.label_sld_profile.setText(_translate("MainWindow", "SLD profile (SLD [in Å**-2, *10e6] vs. Distance from interface [Å]:"))
        self.label_fit_results.setText(_translate("MainWindow", "Fit results:"))

        self.toolButton_data_file.setText(_translate("MainWindow", "..."))
        self.comboBox_1.setItemText(0, _translate("MainWindow", "ang(Qz)"))
        self.comboBox_1.setItemText(1, _translate("MainWindow", "I"))
        self.comboBox_1.setItemText(2, _translate("MainWindow", "dI"))
        self.comboBox_1.setItemText(3, _translate("MainWindow", "ang(rad)"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "I"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "dI"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "ang(Qz)"))
        self.comboBox_2.setItemText(3, _translate("MainWindow", "ang(rad)"))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "dI"))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "I"))
        self.comboBox_3.setItemText(2, _translate("MainWindow", "ang(Qz)"))
        self.comboBox_3.setItemText(3, _translate("MainWindow", "ang(rad)"))
        self.pushButton_add_layer.setText(_translate("MainWindow", "Add layer"))
        self.pushButton_remove_layer.setText(_translate("MainWindow", "Remove layer"))

        item = self.tableWidget_film.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "substrate"))
        item = self.tableWidget_film.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "name"))
        item = self.tableWidget_film.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "thickness"))
        item = self.tableWidget_film.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "SLD"))
        item = self.tableWidget_film.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "iSLD"))
        item = self.tableWidget_film.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "mSLD"))
        item = self.tableWidget_film.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "cos(d-gamma)"))
        item = self.tableWidget_film.horizontalHeaderItem(11)
        item.setText(_translate("MainWindow", "roughness"))
        __sortingEnabled = self.tableWidget_film.isSortingEnabled()
        self.tableWidget_film.setSortingEnabled(False)
        item = self.tableWidget_film.item(0, 0)
        item.setText(_translate("MainWindow", "substrate"))
        item = self.tableWidget_film.item(0, 1)
        item.setText(_translate("MainWindow", "inf"))
        item = self.tableWidget_film.item(0, 3)
        item.setText(_translate("MainWindow", "2.07"))
        item = self.tableWidget_film.item(0, 5)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_film.item(0, 11)
        item.setText(_translate("MainWindow", "10"))
        self.tableWidget_film.setSortingEnabled(__sortingEnabled)
        self.pushButton_load_entry.setText(_translate("MainWindow", "Load entry file"))
        self.tabWidget_data_for_fitting.setTabText(self.tabWidget_data_for_fitting.indexOf(self.Tab_film_description),
                                                   _translate("MainWindow", "Film description"))
        self.label_wavelength.setText(_translate("MainWindow", "Wavelength (A)"))
        self.label_n_of_pts_f_resol_funct.setText(_translate("MainWindow", "Number of points for resolution function"))
        self.label_step_f_resol_funct.setText(_translate("MainWindow", "Step for resolution function (mrad)"))
        self.label_sigma.setText(_translate("MainWindow", "\"Sigma\" of resolution function (mrad)"))
        self.label_zero_correction.setText(_translate("MainWindow", "Correction of the detector \"zero\""))
        self.label_cross_overill.setText(_translate("MainWindow", "Crossover angle overillumination (mrad)"))
        self.label_scaling_factor.setText(_translate("MainWindow", "Scaling factor"))
        self.label_background.setText(_translate("MainWindow", "Background"))
        self.label_exclude_first.setText(_translate("MainWindow", "Number of first points to exclude"))
        self.label_exclude_last.setText(_translate("MainWindow", "Number of last points to exclude"))
        self.lineEdit_exclude_first.setText(_translate("MainWindow", "5"))
        self.lineEdit_exclude_last.setText(_translate("MainWindow", "5"))
        self.label_piy.setText(_translate("MainWindow", "Piy incident polarization (polariser)"))
        self.label_pfy.setText(_translate("MainWindow", "Pfy outgoing polarization (analyser)"))
        self.label_cg.setText(_translate("MainWindow", "cg: mean value <cos(gamma)> of big domains"))
        self.label_sg.setText(_translate("MainWindow", "sg: mean value <sin(gamma)> of big domains"))
        self.label_sg2.setText(_translate("MainWindow", "sg2: mean value <sin^2(gamma)> of big domains"))
        self.tabWidget_data_for_fitting.setTabText(self.tabWidget_data_for_fitting.indexOf(self.tab_scan_param),
                                                   _translate("MainWindow", "Scan parameters"))

        item = self.tableWidget_fit_results.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "No"))
        item = self.tableWidget_fit_results.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Parameter"))
        item = self.tableWidget_fit_results.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Value"))
        item = self.tableWidget_fit_results.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Error"))
        item = self.tableWidget_fit_results.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Factor"))

        self.label_iter_numb.setText(_translate("MainWindow", "Number of iterations:"))
        self.label_chi_sq_norm.setText(_translate("MainWindow", "Chi_sq.norm:"))
        self.pushButton_start_fitting.setText(_translate("MainWindow", "Start Fitting"))
        self.toolButton_save_at_dir.setText(_translate("MainWindow", "..."))
        self.label_botofit_crashed.setText(_translate("MainWindow", "BoToFit crashed. Consider using more reasonable 'Start fit' values."))
        self.label_need_wavelength.setText( _translate("MainWindow", "Input wavelength before importing files in Qz. Otherwice cant convert to ang(rad) for calculations."))
        self.menu_MenuBar.setTitle(_translate("MainWindow", "Mode"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.action_mono_no_polarisation.setText(_translate("MainWindow", "Mono - No polarisation"))
        self.action_mono_2_polarisations.setText(_translate("MainWindow", "Mono - 2 polarisations"))
        self.action_mono_4_polarisations.setText(_translate("MainWindow", "Mono - 4 polarisations"))
        self.action_tof_no_polarisation.setText(_translate("MainWindow", "TOF - No polarisation"))
        self.actionAlgorithm_info.setText(_translate("MainWindow", "Algorithm info"))
        self.actionVersion.setText(_translate("MainWindow", "Version 190511"))
        self.pushButton_redraw_refl.setText(_translate("MainWindow", "Redraw reflectivity"))

        item = self.tableWidget_data_points.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Q"))
        item = self.tableWidget_data_points.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "I"))
        item = self.tableWidget_data_points.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "dI"))
        __sortingEnabled = self.tableWidget_data_points.isSortingEnabled()
        self.tableWidget_data_points.setSortingEnabled(False)
        self.tableWidget_data_points.setSortingEnabled(__sortingEnabled)

        self.label_botofit_crashed.setVisible(0)
        self.label_need_wavelength.setVisible(0)

        pg.setConfigOption('background', (255, 255, 255))
        pg.setConfigOption('foreground', 'k')

        self.graphicsView_refl_profile = pg.PlotWidget(self.centralwidget)
        self.graphicsView_refl_profile.setGeometry(QtCore.QRect(15, 550, 581, 241))
        self.graphicsView_refl_profile.setObjectName("graphicsView_refl_profile")
        font = QtGui.QFont()
        font.setPixelSize(11)
        self.graphicsView_refl_profile.getAxis("bottom").tickFont = font
        self.graphicsView_refl_profile.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_refl_profile.getAxis("left").tickFont = font
        self.graphicsView_refl_profile.getAxis("left").setStyle(tickTextOffset=10)

        self.graphicsView_refl_diff = pg.PlotWidget(self.centralwidget)
        self.graphicsView_refl_diff.setGeometry(QtCore.QRect(15, 800, 581, 91))
        self.graphicsView_refl_diff.setObjectName("graphicsView_refl_diff")
        font = QtGui.QFont()
        font.setPixelSize(11)
        self.graphicsView_refl_diff.getAxis("bottom").tickFont = font
        self.graphicsView_refl_diff.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_refl_diff.getAxis("left").tickFont = font
        self.graphicsView_refl_diff.getAxis("left").setStyle(tickTextOffset=10)

        self.graphicsView_sld_profile = pg.PlotWidget(self.centralwidget)
        self.graphicsView_sld_profile.setGeometry(QtCore.QRect(625, 550, 581, 341))
        self.graphicsView_sld_profile.setObjectName("graphicsView_sld_profile")
        font = QtGui.QFont()
        font.setPixelSize(11)
        self.graphicsView_sld_profile.getAxis("bottom").tickFont = font
        self.graphicsView_sld_profile.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_sld_profile.getAxis("left").tickFont = font
        self.graphicsView_sld_profile.getAxis("left").setStyle(tickTextOffset=10)

        self.tableWidget_fit_results.setColumnWidth(0, 30)
        self.tableWidget_fit_results.setColumnWidth(1, 166)
        self.tableWidget_fit_results.setColumnWidth(2, 100)
        self.tableWidget_fit_results.setColumnWidth(3, 100)
        self.tableWidget_fit_results.setColumnWidth(4, int(self.tableWidget_fit_results.width()) - int(self.tableWidget_fit_results.columnWidth(0)) - int(self.tableWidget_fit_results.columnWidth(1)) - int(self.tableWidget_fit_results.columnWidth(2)) - int(self.tableWidget_fit_results.columnWidth(3)) - 2)

        self.toolButton_data_file.clicked.connect(self.button_data_file)
        self.pushButton_add_layer.clicked.connect(self.button_add_layer)
        self.pushButton_remove_layer.clicked.connect(self.button_remove_layer)
        self.pushButton_start_fitting.clicked.connect(self.button_start_fitting)
        self.pushButton_redraw_refl.clicked.connect(self.button_redraw_refl)

        self.lineEdit_save_at_dir.setPlaceholderText(_translate("MainWindow", "default [" + str(current_dir) + "]"))
        self.toolButton_save_at_dir.clicked.connect(self.button_save_at_dir)

        self.pushButton_load_entry.clicked.connect(self.load_entry_file)

        # No polarisation by default
        self.interface()

        self.action_mono_no_polarisation.triggered.connect(self.mode_mono_no_pol)
        self.action_mono_2_polarisations.triggered.connect(self.mode_mono_2_pol)
        self.action_mono_4_polarisations.triggered.connect(self.mode_mono_4_pol)
        self.action_tof_no_polarisation.triggered.connect(self.mode_tof_no_pol)

        self.actionVersion.triggered.connect(self.menu_info)
        self.actionAlgorithm_info.triggered.connect(self.menu_algorithm)

        # load user defaults if such are presented in the folder
        if "UserDefaults_nopol.dat" in os.listdir(current_dir):
            self.load_entry_file()
    ##<--

    ##--> redefine user interface elements if TOF/Mono is selected and if polarisation is needed
    def mode_mono_no_pol(self):
        #global BoToFit_mode
        self.BoToFit_mode = 0

        if self.action_mono_no_polarisation.isChecked():
            self.action_mono_2_polarisations.setChecked(False)
            self.action_mono_4_polarisations.setChecked(False)
            self.action_tof_no_polarisation.setChecked(False)
        elif not self.action_mono_2_polarisations.isChecked() and not self.action_mono_4_polarisations.isChecked() and not self.action_mono_no_polarisation.isChecked() and self.action_tof_no_polarisation.isChecked():
            self.action_mono_no_polarisation.setChecked(True)

        self.interface()

        # load UserDefaults if such are presented
        if "UserDefaults_nopol.dat" in os.listdir(current_dir):
            self.lineEdit_wavelength.setText("")
            self.load_entry_file()

        # clear stuff, just in case
        self.clear_stuff()
        self.lineEdit_data_file.clear()

        self.label_wavelength.setText("Wavelength (A)")

    def mode_mono_2_pol(self):
        self.BoToFit_mode = 1

        if self.action_mono_2_polarisations.isChecked():
            self.action_mono_no_polarisation.setChecked(False)
            self.action_mono_4_polarisations.setChecked(False)
            self.action_tof_no_polarisation.setChecked(False)
        elif not self.action_mono_2_polarisations.isChecked() and not self.action_mono_4_polarisations.isChecked() and not self.action_mono_no_polarisation.isChecked() and not self.action_tof_no_polarisation.isChecked():
            self.action_mono_2_polarisations.setChecked(True)

        self.interface()

        # load UserDefaults if such are presented
        if "UserDefaults_2pol.dat" in os.listdir(current_dir):
            self.lineEdit_wavelength.setText("")
            self.load_entry_file()

        # clear stuff, just in case
        self.clear_stuff()
        self.lineEdit_data_file.clear()

        self.label_wavelength.setText("Wavelength (A)")

    def mode_mono_4_pol(self):
        self.BoToFit_mode = 2

        if self.action_mono_4_polarisations.isChecked():
            self.action_mono_no_polarisation.setChecked(False)
            self.action_mono_2_polarisations.setChecked(False)
            self.action_tof_no_polarisation.setChecked(False)
        elif not self.action_mono_2_polarisations.isChecked() and not self.action_mono_4_polarisations.isChecked() and not self.action_mono_no_polarisation.isChecked() and not self.action_tof_no_polarisation.isChecked():
            self.action_mono_4_polarisations.setChecked(True)

        self.interface()

        # load UserDefaults if such are presented
        if "UserDefaults_4pol.dat" in os.listdir(current_dir):
            self.lineEdit_wavelength.setText("")
            self.load_entry_file()

        # clear stuff, just in case
        self.clear_stuff()
        self.lineEdit_data_file.clear()

        self.label_wavelength.setText("Wavelength (A)")

    def mode_tof_no_pol(self):
        self.BoToFit_mode = 3

        if self.action_tof_no_polarisation.isChecked():
            self.action_mono_no_polarisation.setChecked(False)
            self.action_mono_2_polarisations.setChecked(False)
            self.action_mono_4_polarisations.setChecked(False)
        elif not self.action_mono_2_polarisations.isChecked() and not self.action_mono_4_polarisations.isChecked() and not self.action_mono_no_polarisation.isChecked() and not self.action_tof_no_polarisation.isChecked():
            self.action_tof_no_polarisation.setChecked(True)

        self.interface()

        # load UserDefaults if such are presented
        if "UserDefaults_TOF_nopol.dat" in os.listdir(current_dir):
            self.lineEdit_wavelength.setText("")
            self.load_entry_file()

        # clear stuff, just in case
        self.clear_stuff()
        self.lineEdit_data_file.clear()

        # rename "wavelength" to "incident angle" on the form
        self.label_wavelength.setText("Incident angle (mrad)")

    def interface(self):
        # reformat table and polarisation parameters
        if self.BoToFit_mode in [0, 3]:
            self.label_piy.setEnabled(False)
            self.lineEdit_piy.setEnabled(False)
            self.checkBox_piy.setEnabled(False)

            self.label_pfy.setEnabled(False)
            self.lineEdit_pfy.setEnabled(False)
            self.checkBox_pfy.setEnabled(False)

            self.label_pfy.setEnabled(False)
            self.lineEdit_pfy.setEnabled(False)
            self.checkBox_pfy.setEnabled(False)

            self.label_cg.setEnabled(False)
            self.lineEdit_cg.setEnabled(False)
            self.checkBox_cg.setEnabled(False)

            self.label_sg.setEnabled(False)
            self.lineEdit_sg.setEnabled(False)
            self.checkBox_sg.setEnabled(False)

            self.label_sg2.setEnabled(False)
            self.lineEdit_sg2.setEnabled(False)
            self.checkBox_sg2.setEnabled(False)

            # columns with checkboxes can change their width depends on Windows scaling settings, so we correct our table
            col_width = round((int(self.tableWidget_film.width()) - 4 * int(self.tableWidget_film.columnWidth(2))) / 5, 0)

            self.tableWidget_film.setColumnWidth(0, col_width)
            self.tableWidget_film.setColumnWidth(1, col_width)
            self.tableWidget_film.setColumnWidth(2, 1)
            self.tableWidget_film.setColumnWidth(3, col_width)
            self.tableWidget_film.setColumnWidth(4, 1)
            self.tableWidget_film.setColumnWidth(5, col_width)
            self.tableWidget_film.setColumnWidth(6, 1)
            self.tableWidget_film.setColumnWidth(7, 0)
            self.tableWidget_film.setColumnWidth(8, 0)
            self.tableWidget_film.setColumnWidth(9, 0)
            self.tableWidget_film.setColumnWidth(10, 0)
            self.tableWidget_film.setColumnWidth(11, int(self.tableWidget_film.width()) - 4 * int(self.tableWidget_film.columnWidth(2)) - 4 * col_width - 2)
            self.tableWidget_film.setColumnWidth(12, 1)
        elif self.BoToFit_mode in [1, 2]:
            self.label_piy.setEnabled(True)
            self.lineEdit_piy.setEnabled(True)
            self.checkBox_piy.setEnabled(True)

            self.label_pfy.setEnabled(True)
            self.lineEdit_pfy.setEnabled(True)
            self.checkBox_pfy.setEnabled(True)

            self.label_pfy.setEnabled(True)
            self.lineEdit_pfy.setEnabled(True)
            self.checkBox_pfy.setEnabled(True)

            self.label_cg.setEnabled(True)
            self.lineEdit_cg.setEnabled(True)
            self.checkBox_cg.setEnabled(True)

            self.label_sg.setEnabled(True)
            self.lineEdit_sg.setEnabled(True)
            self.checkBox_sg.setEnabled(True)

            self.label_sg2.setEnabled(True)
            self.lineEdit_sg2.setEnabled(True)
            self.checkBox_sg2.setEnabled(True)

            # columns with checkboxes can change their width depends on Windows scaling settings, so we correct our table
            col_width = round((int(self.tableWidget_film.width()) - 6 * int(self.tableWidget_film.columnWidth(2))) / 7, 0)

            self.tableWidget_film.setColumnWidth(0, col_width)
            self.tableWidget_film.setColumnWidth(1, col_width + 6)
            self.tableWidget_film.setColumnWidth(2, 1)
            self.tableWidget_film.setColumnWidth(3, col_width - 6)
            self.tableWidget_film.setColumnWidth(4, 1)
            self.tableWidget_film.setColumnWidth(5, col_width - 6)
            self.tableWidget_film.setColumnWidth(6, 1)
            self.tableWidget_film.setColumnWidth(7, col_width - 6)
            self.tableWidget_film.setColumnWidth(8, 1)
            self.tableWidget_film.setColumnWidth(9, col_width + 6)
            self.tableWidget_film.setColumnWidth(10, 1)
            self.tableWidget_film.setColumnWidth(11, int(self.tableWidget_film.width()) - 6 * int(self.tableWidget_film.columnWidth(2)) - 6 * col_width + 4)
            self.tableWidget_film.setColumnWidth(12, 1)

        # reformat checkboxes (I, dI, Qz, rad)
        if self.BoToFit_mode in [0, 1, 2]:
            if self.comboBox_1.count() < 4:
                self.comboBox_1.addItem("")
                self.comboBox_1.setItemText(3, "ang(rad)")
                self.comboBox_2.addItem("")
                self.comboBox_2.setItemText(3, "ang(rad)")
                self.comboBox_3.addItem("")
                self.comboBox_3.setItemText(3, "ang(rad)")
        elif self.BoToFit_mode == 3:
            self.comboBox_1.removeItem(3)
            self.comboBox_2.removeItem(3)
            self.comboBox_3.removeItem(3)
    ##<--

    ##--> buttons
    def button_data_file(self):
        '''
        if {NoPolarisation} and {toolButton_data_file} is pressed: [user can choose only one file]
        elif {toolButton_data_file} is pressed: [user can choose several file]
        '''

        self.input_structure = [self.comboBox_1.currentText(), self.comboBox_2.currentText(), self.comboBox_3.currentText()]

        self.label_need_wavelength.setVisible(False)

        if self.BoToFit_mode in [0, 3]:
            data_files = QtWidgets.QFileDialog().getOpenFileName(None, "FileNames", current_dir)
        else: data_files = QtWidgets.QFileDialog().getOpenFileNames(None, "FileNames", current_dir)

        if data_files[0] == "": return

        self.lineEdit_data_file.setText(str(data_files[0]))

        # clear stuff after last run
        self.clear_stuff()
        self.tableWidget_data_points.clear()
        self.lineEdit_pts_num.clear()

        if not self.BoToFit_mode == 3 and self.lineEdit_wavelength.text() == "":
            self.label_need_wavelength.setVisible(True)
            self.statusbar.showMessage("Input wavelength and reimport the file")
        else:
            self.parse_data_files()
            self.draw_reflectivity()

    def button_add_layer(self):
        '''
        add lines into {tableWidget_film}
        '''

        if self.tableWidget_film.currentRow() >= 0:
            i = self.tableWidget_film.currentRow()
        else:
            i = 0

        self.tableWidget_film.insertRow(i)
        for j in range(0, 13):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            if j in (2, 4, 6, 8, 10, 12):
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                if j == 6:
                    item.setCheckState(QtCore.Qt.Checked)
                else:
                    item.setCheckState(QtCore.Qt.Unchecked)

            self.tableWidget_film.setItem(i, j, item)

        i = 0
        j = 0

    def button_remove_layer(self):
        '''
        remove lines from {tableWidget_film}
        '''

        if not self.tableWidget_film.rowCount() == self.tableWidget_film.currentRow() + 1:
            self.tableWidget_film.removeRow(self.tableWidget_film.currentRow())

    def button_save_at_dir(self):
        '''
        default {save_at_dit} folder is the one where "BoToFit.exe" is located
        otherwice: defined by user
        '''
        dir = QtWidgets.QFileDialog().getExistingDirectory(None, "FileNames", current_dir)
        if dir: self.lineEdit_save_at_dir.setText(str(dir))

    def button_redraw_refl(self):
        self.graphicsView_refl_profile.getPlotItem().clear()
        self.draw_reflectivity()

    def button_start_fitting(self):

        start_time = time.time()

        self.label_botofit_crashed.setVisible(0)

        data_files = []
        for file in self.lineEdit_data_file.text().split("'"):
            if len(file) > 2: data_files.append(file)

        # check if we have file to work with
        if not self.lineEdit_data_file.text(): return

        self.clear_stuff()
        self.draw_reflectivity()

        data_file_input_name = data_files[0][data_files[0].rfind("/") + 1: data_files[0].rfind(".")].replace(" ", "_")

        # create new directory or rewrite files if they already exists
        self.save_dir = current_dir
        if not self.lineEdit_save_at_dir.text():
            self.lineEdit_save_at_dir.setText(current_dir)
        else:
            # if there are "spaces" in "save at" path, we work in current dir and then copy everythong to "save at" one
            if self.lineEdit_save_at_dir.text().rfind(" ") > 0:
                self.save_dir = current_dir
            else:
                self.save_dir = self.lineEdit_save_at_dir.text()

        self.lineEdit_data_folder_name.setText(self.save_dir + "/" + data_file_input_name + "/")

        if not os.path.exists(self.lineEdit_data_folder_name.text()):
            os.makedirs(self.lineEdit_data_folder_name.text())

        # create entry for BoToFit
        self.create_input_data_file()
        self.create_entry_for_BoToFit()

        # define what BoToFit module to use
        if self.BoToFit_mode == 0: self.BoToFit_exe = "Film500x0.exe"
        elif self.BoToFit_mode == 1: self.BoToFit_exe = "Film500x2.exe"
        elif self.BoToFit_mode == 2: self.BoToFit_exe = "Film500x4.exe"
        elif self.BoToFit_mode == 3: self.BoToFit_exe = "FilmTOF500QX0.exe"

        # create .bat to run BoToFit module
        with open(self.lineEdit_data_folder_name.text() + "BoTo_Input.txt", "w") as file:
            file.write(self.lineEdit_data_folder_name.text().replace("/", "\\") + "entry.dat\n")
            file.write(self.lineEdit_data_folder_name.text().replace("/", "\\") + "data_file_reformatted.dat\n")
            file.write(self.lineEdit_exclude_first.text() + "\n")
            file.write(self.lineEdit_exclude_last.text() + "\n")

        with open(self.lineEdit_data_folder_name.text() + "Boto_run.bat", "w") as file:
            file.write("cd " + self.lineEdit_data_folder_name.text().replace("/", "\\") + "\n")
            file.write('type "' + self.lineEdit_data_folder_name.text().replace("/", "\\") + 'BoTo_Input.txt" | "' + current_dir.replace(
                "/", "\\") + '\\' + self.BoToFit_exe + '"')

        # define that BoToFit is done by checking the folder for "file_to_wait"
        if self.BoToFit_mode == 0: file_to_wait = "FitFunctX.dat"
        elif self.BoToFit_mode == 3: file_to_wait = "FitFunct.dat"
        else: file_to_wait = "Fit2DFunctDD.dat"

        # delete old FitFunct.dat file
        try:
            os.remove(self.lineEdit_data_folder_name.text() + file_to_wait)
        except:
            a = 1

        # run BoToFit
        os.startfile(self.lineEdit_data_folder_name.text() + "Boto_run.bat")

        # check every second if BoToFit is done
        while file_to_wait not in os.listdir(self.lineEdit_data_folder_name.text()):

            QtTest.QTest.qWait(1000)

            # check if it crashed
            proc_list = []
            # check if BoToFit crashed
            for proc in psutil.process_iter(): proc_list.append(proc.name())
            if self.BoToFit_exe not in proc_list:
                # if BoToFit crashes, show message and stop work
                self.clear_stuff()

                self.draw_reflectivity()
                self.label_botofit_crashed.setVisible(1)
                self.statusbar.showMessage("Crashed")

                return

        # wait 5 sec more to make sure that FitFunct file is ready
        QtTest.QTest.qWait(5000)

        # when its done, kill its process
        for proc in psutil.process_iter():
            if proc.name() == self.BoToFit_exe:
                proc.kill()

        # wait until fitting is done -> fill the table, draw graphs and create multiGrPr.ent using Fit2DBag.dat file
        self.graphicsView_refl_profile.getPlotItem().clear()
        self.draw_reflectivity()
        self.draw_and_export_reform_FitFunctX()
        self.create_fit_results_table_and_multiGrPr_entry()

        self.draw_diff()

        # create multiGrPr.bat file to run multiGrPr.exe
        with open(self.lineEdit_data_folder_name.text() + "multiGrPr.bat", "w") as file:
            file.write("cd " + self.lineEdit_data_folder_name.text().replace("/", "\\") + "\n")
            file.write('START /B CMD /C CALL "' + current_dir.replace("/", "\\") + '\\multiGrPr.exe"')

        # run multiGrPr and wait until it finished to work
        os.startfile(self.lineEdit_data_folder_name.text() + "multiGrPr.bat")
        while "SLD_profile.dat" not in os.listdir(self.lineEdit_data_folder_name.text()):
            QtTest.QTest.qWait(1000)

        while os.path.getsize(self.lineEdit_data_folder_name.text() + 'SLD_profile.dat') < 1:
            QtTest.QTest.qWait(1000)

        # draw SLD
        self.draw_SLD()

        # delete *bat files
        os.remove(self.lineEdit_data_folder_name.text() + "multiGrPr.bat")
        os.remove(self.lineEdit_data_folder_name.text() + "BoTo_Input.txt")
        os.remove(self.lineEdit_data_folder_name.text() + "Boto_run.bat")

        elapsed_time = time.time() - start_time
        self.statusbar.showMessage("Finished in " + str(round(float(elapsed_time), 1)) + " seconds")

        if "ang(Qz)" in self.input_structure: self.export_for_user()

        # if we worked from temporary directory, then we need to move files to requested "save at" dir
        if self.lineEdit_save_at_dir.text().rfind(" ") > 0:
            if data_file_input_name in os.listdir(self.lineEdit_save_at_dir.text()):
                shutil.rmtree(self.lineEdit_save_at_dir.text() + "/" + data_file_input_name, ignore_errors=True)
            try:
                os.rename(self.lineEdit_data_folder_name.text()[:-1],
                          self.lineEdit_save_at_dir.text() + "/" + data_file_input_name)
            except:
                shutil.copytree(self.lineEdit_data_folder_name.text()[:-1],
                                self.lineEdit_save_at_dir.text() + "/" + data_file_input_name)
                shutil.rmtree(self.lineEdit_save_at_dir.text() + "/" + data_file_input_name, ignore_errors=True)
    ##<--

    ##--> menu options
    def menu_info(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(current_dir + "\icon.png"))
        msgBox.setText("BoToFit V.190511\n\n"
                       "Algorithm: Boris.Toperverg@ruhr-uni-bochum.de\n"
                       "GUI: Alexey.Klechikov@gmail.com\n\n")
        msgBox.exec_()

    def menu_algorithm(self):
        # CHECK THIS
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(current_dir + "\icon.png"))
        msgBox.setText("Film description columns:\n"
                       "* name of the layer\n"
                       "* thickness of the layer (in A)\n"
                       "* SLD (*10e-6 Ae-2)\n"
                       "* iSLD (*10e-6 Ae-2)\n"
                       "* magnetic SLD (*10e-6 Ae-2)\n"
                       "* <cos(delta_gamma)>{over small domains}\n"
                       "* Debay-Waller in (AA)\n\n"
                       "Some notes (mainly for Mono-modes):\n"
                       "* Input correct wavelength (if Qz is used as an angle) and define file structure before importing the data\n"
                       "* BoToFit default unit for the angle value is radians, so all result files uses radians as an angle\n"
                       "* Mono 2 polarisations mode uses 2 data files which should contain '_du' and '_uu' in their names \n"
                       "* Mono 4 polarisations mode uses 4 data files which should contain '_du', '_ud', '_dd' and '_uu' in their names \n"
                       "* Use checkboxes when you want to fit corresponding values (checked = fixed)\n")
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

            if self.BoToFit_mode == 2:

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
                for line in data_file_input.readlines():

                    if "ang(Qz)" in self.input_structure: data_angle.append(float(line.split()[self.input_structure.index("ang(Qz)")]))
                    elif "ang(rad)" in self.input_structure: data_angle.append(float(line.split()[self.input_structure.index("ang(rad)")]))

                    data_I.append(float(line.split()[self.input_structure.index("I")]))
                    data_dI.append(float(line.split()[self.input_structure.index("dI")]))
                    exper_points_number += 1

            self.lineEdit_pts_num.setText(str(exper_points_number))
            self.tableWidget_data_points.item(j, 0).setText(str(data_angle))
            self.tableWidget_data_points.item(j, 1).setText(str(data_I))
            self.tableWidget_data_points.item(j, 2).setText(str(data_dI))

            j += 1

    def create_input_data_file(self):
        '''
        input data files for BoToFit should have [*I *dI *angle(rad)] format in Mono mode and [*I *dI *Qz] in TOF mode
        '''

        with open(self.lineEdit_data_folder_name.text() + "data_file_reformatted.dat", 'w') as data_file_output:
            # check hidden table with experimental points already reformatted in Q I dI format
            for i in range(0, 4):
                if self.tableWidget_data_points.item(i, 0).text() not in ("", "[]"):
                    data_angle = self.tableWidget_data_points.item(i, 0).text()[1: -1].replace(",", "").split()
                    data_I = self.tableWidget_data_points.item(i, 1).text()[1: -1].replace(",", "").split()
                    data_dI = self.tableWidget_data_points.item(i, 2).text()[1: -1].replace(",", "").split()

                    for j in range(0, len(data_angle)):
                        if self.BoToFit_mode == 3: data_file_output.write(data_I[j] + "  " + data_dI[j] + "    " + data_angle[j] + "\n")
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
        self.tableWidget_film.setCurrentCell(-1, -1)

        if self.lineEdit_wavelength.text() == "":
            if self.BoToFit_mode == 0 and "UserDefaults_nopol.dat" in os.listdir(current_dir):
                entry_file = current_dir + "/UserDefaults_nopol.dat"
            elif self.BoToFit_mode == 1 and "UserDefaults_2pol.dat" in os.listdir(current_dir):
                entry_file = current_dir + "/UserDefaults_2pol.dat"
            elif self.BoToFit_mode == 2 and "UserDefaults_4pol.dat" in os.listdir(current_dir):
                entry_file = current_dir + "/UserDefaults_4pol.dat"
            elif self.BoToFit_mode == 3 and "UserDefaults_TOF_nopol.dat" in os.listdir(current_dir):
                entry_file = current_dir + "/UserDefaults_TOF_nopol.dat"
        else:
            entry_file = QtWidgets.QFileDialog().getOpenFileName(None, "FileNames", current_dir)[0]

        if entry_file == "": return

        row = 0
        col = 1
        scaling_fact_line = piy_line = pfy_line = wavelength_line = cg_line = -1000

        with open(str(entry_file), "r") as file:
            for line_number, line in enumerate(file.readlines()):
                if not self.BoToFit_mode == 0 and not self.BoToFit_mode == 3 :
                    # Piy incident polarization (polariser)
                    if line.rfind("Piy") > 0:
                        self.lineEdit_piy.setText(line.split()[0])
                        piy_line = line_number + 1
                    if line_number == piy_line:
                        if line.split()[0] == "n": self.checkBox_piy.setCheckState(0)
                        elif line.split()[0] == "f": self.checkBox_piy.setCheckState(2)

                    # Pfy outgoing polarization (analyser)
                    if line.rfind("Pfy") > 0:
                        self.lineEdit_pfy.setText(line.split()[0])
                        pfy_line = line_number + 1
                    if line_number == pfy_line:
                        if line.split()[0] == "n": self.checkBox_pfy.setCheckState(0)
                        elif line.split()[0] == "f": self.checkBox_pfy.setCheckState(2)

                    # cg: mean value <cos(gamma)> over big domains
                    if line.rfind("cos(gamma)") > 0:
                        self.lineEdit_cg.setText(line.split()[0])
                        cg_line = line_number + 1
                    if line_number == cg_line:
                        if line.split()[0] == "n": self.checkBox_cg.setCheckState(0)
                        elif line.split()[0] == "f": self.checkBox_cg.setCheckState(2)
                    # sg: mean value <sin(gamma)> over big domains
                    if line_number == cg_line + 1: self.lineEdit_sg.setText(line.split()[0])
                    if line_number == cg_line + 2:
                        if line.split()[0] == "n": self.checkBox_sg.setCheckState(0)
                        elif line.split()[0] == "f": self.checkBox_sg.setCheckState(2)
                    # sg2: mean value <sin^2(gamma)> over big domains
                    if line_number == cg_line + 3: self.lineEdit_sg2.setText(line.split()[0])
                    if line_number == cg_line + 4:
                        if line.split()[0] == "n": self.checkBox_sg2.setCheckState(0)
                        elif line.split()[0] == "f": self.checkBox_sg2.setCheckState(2)

                # wavelength or incident angle
                '''
                BoToFit entry is almost the same for Mono and TOF modes.
                The only difference is that "incident angle" is used instead of "wavelength".
                '''
                if line.rfind("wavelength") > 0 or line.rfind("incident angle") > 0:
                    self.lineEdit_wavelength.setText(line.split()[0])
                    wavelength_line = line_number

                # number of experimental points in alpha
                if line_number == wavelength_line + 2: self.lineEdit_n_of_pts_f_resol_funct.setText(
                    line.split()[0])
                # step for resolution function (in mrad)
                if line_number == wavelength_line + 3: self.lineEdit_step_f_resol_funct.setText(line.split()[0])
                # "sigma" of resolution function (in mrad)
                if line_number == wavelength_line + 4: self.lineEdit_sigma.setText(line.split()[0])
                # correction of the detector 'zero' (in mrad): alpha-da
                if line.rfind("correction of the detector") > 0: self.lineEdit_zero_correction.setText(
                    line.split()[0])

                # ct  total scaling factor
                if line.rfind("scaling factor") > 0:
                    self.lineEdit_scaling_factor.setText(line.split()[0])
                    scaling_fact_line = line_number + 1
                if line_number == scaling_fact_line:
                    if line.split()[0] == "n":
                        self.checkBox_scaling_factor.setCheckState(0)
                    elif line.split()[0] == "f":
                        self.checkBox_scaling_factor.setCheckState(2)
                # alpha_0 crossover angle overillumination (in mrad)
                if line_number == scaling_fact_line + 1: self.lineEdit_cross_overill.setText(line.split()[0])
                if line_number == scaling_fact_line + 2:
                    if line.split()[0] == "n":
                        self.checkBox_cross_overill.setCheckState(0)
                    elif line.split()[0] == "f":
                        self.checkBox_cross_overill.setCheckState(2)
                # bgr 'background'
                if line_number == scaling_fact_line + 3: self.lineEdit_background.setText(line.split()[0])
                if line_number == scaling_fact_line + 4:
                    if line.split()[0] == "n":
                        self.checkBox_background.setCheckState(0)
                    elif line.split()[0] == "f":
                        self.checkBox_background.setCheckState(2)

                if line.rfind("number of layers") > 0:
                    number_of_layers = int(line.split()[0])  # excluding substrate
                    layers_description_line = line_number
                    # delete all layers except substrate
                    while not self.tableWidget_film.item(0, 0).text() == "substrate":
                        self.tableWidget_film.removeRow(0)
                    # add i layers
                    for i in range(0, number_of_layers):
                        self.button_add_layer()
                        self.tableWidget_film.item(0, 0).setText("Layer " + str(number_of_layers - i))

                try:
                    if line_number > layers_description_line + 1 and not line == "":

                        # I hide 4 columns in NoPol mode, so we skip them
                        if self.BoToFit_mode in [0, 3] and col == 7: col = 11

                        if col <= 12 and row <= number_of_layers:
                            if line.split()[0] == "n":
                                self.tableWidget_film.item(row, col).setCheckState(0)
                            elif line.split()[0] == "f":
                                self.tableWidget_film.item(row, col).setCheckState(2)
                            else:
                                self.tableWidget_film.item(row, col).setText(line.split()[0].replace("d", "e"))

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

        with open(self.lineEdit_data_folder_name.text() + 'entry.dat', 'w') as entry_file:

            if self.BoToFit_mode not in [0, 3]:
                # incident polarization (polariser)
                entry_file.write("0     Pix incident polarization (polariser)\nf\n")
                entry_file.write(self.lineEdit_piy.text() + '    Piy\n')
                if self.checkBox_piy.isChecked(): entry_file.write("f" + "   \n")
                else: entry_file.write("n" + "   \n")
                entry_file.write("0     Piz\nf\n\n")

                # outgoing polarization (analyser)
                entry_file.write("0     Pfx outgoing polarization (analyser)\nf\n")
                entry_file.write(self.lineEdit_pfy.text() + '    Piy\n')
                if self.checkBox_pfy.isChecked():
                    entry_file.write("f" + "   \n")
                else:
                    entry_file.write("n" + "   \n")
                entry_file.write("0     Pfz\nf\n\n")

            if not self.BoToFit_mode == 3:
                entry_file.write(self.lineEdit_wavelength.text() + '    wavelength (in Angstrem)\n')
            else:
                entry_file.write(self.lineEdit_wavelength.text() + '    incident angle (in mrad)\n')

            entry_file.write(self.lineEdit_pts_num.text() + "   *nn number of experimental points in alpha (<1001)\n")
            entry_file.write(self.lineEdit_n_of_pts_f_resol_funct.text() + "    *j0 number of points for resolution function (odd) (<102)\n")
            entry_file.write(self.lineEdit_step_f_resol_funct.text() + "    step for resolution function (in mrad)\n")
            entry_file.write(self.lineEdit_sigma.text() + "     *sigma of resolution function (in mrad)\n\n")
            entry_file.write(str(self.tableWidget_film.rowCount() - 1) + "   number of layers (excluding substrate) (<21)\n\n")
            # read the table
            for i in range(0, self.tableWidget_film.rowCount()):
                comment = ""
                # Thickness
                if not self.tableWidget_film.item(i, 0).text() == "substrate":
                    entry_file.write(self.tableWidget_film.item(i, 1).text() + "    layer " + str(i+1) + " ("+ self.tableWidget_film.item(i, 0).text() + ") thickness (in A)\n")
                    if self.tableWidget_film.item(i, 2).checkState() == 2: entry_file.write("f" + "   \n")
                    else: entry_file.write("n" + "   \n")
                else: comment = "substrate's"
                # SLD
                entry_file.write(self.tableWidget_film.item(i, 3).text() + "    " + comment + " nbr nuclear SLD Nb'  (in A**-2) *1e6\n")
                if self.tableWidget_film.item(i, 4).checkState() == 2: entry_file.write("f" + "   \n")
                else: entry_file.write("n" + "   \n")
                # iSDL
                entry_file.write(self.tableWidget_film.item(i, 5).text() + "    " + comment + " nbi nuclear SLD Nb'' (in A**-2) *1e6\n")
                if self.tableWidget_film.item(i, 6).checkState() == 2: entry_file.write("f" + "   \n")
                else: entry_file.write("n" + "   \n")

                if self.BoToFit_mode not in [0, 3]:
                    # magnetic SLD
                    entry_file.write(self.tableWidget_film.item(i, 7).text() + "    magnetic SLD Np (in A**-2)*1e6\n")
                    if self.tableWidget_film.item(i, 8).checkState() == 2: entry_file.write("f\n")
                    else: entry_file.write("n\n")
                    # c=<cos(delta_gamma)>
                    entry_file.write(self.tableWidget_film.item(i, 9).text() + "    c=<cos(delta_gamma)>\n")
                    if self.tableWidget_film.item(i, 10).checkState() == 2: entry_file.write("f\n")
                    else: entry_file.write("n\n")

                # roughness
                entry_file.write(self.tableWidget_film.item(i, 11).text() + "    dw Debye-Waller in [AA]\n")
                if self.tableWidget_film.item(i, 12).checkState() == 2: entry_file.write("f\n\n")
                else: entry_file.write("n\n\n")

            if self.BoToFit_mode not in [0, 3]:
                # cg
                entry_file.write(self.lineEdit_cg.text() + '    cg: mean value <cos(gamma)> over big domains\n')
                if self.checkBox_cg.isChecked(): entry_file.write("f" + "   \n")
                else: entry_file.write("n" + "   \n")
                # sg
                entry_file.write(self.lineEdit_sg.text() + '    sg: mean value <sin(gamma)> over big domains\n')
                if self.checkBox_sg.isChecked(): entry_file.write("f" + "   \n")
                else: entry_file.write("n" + "   \n")
                # sg2
                entry_file.write(self.lineEdit_sg2.text() + '    sg2: mean value <sin^2(gamma)> over big domains\n')
                if self.checkBox_sg2.isChecked(): entry_file.write("f" + "  \n\n")
                else: entry_file.write("n" + "   \n\n")

            # ct - total scaling factor
            entry_file.write(self.lineEdit_scaling_factor.text() + "   *ct  total scaling factor\n")
            if self.checkBox_scaling_factor.isChecked(): entry_file.write("f" + "   \n")
            else: entry_file.write("n" + "   \n")
            # alpha_0 crossover angle overillumination
            entry_file.write(self.lineEdit_cross_overill.text() + "   *alpha_0 crossover angle overillumination (in mrad)\n")
            if self.checkBox_cross_overill.isChecked(): entry_file.write("f" + "   \n")
            else: entry_file.write("n" + "   \n")
            # background
            entry_file.write(self.lineEdit_background.text() + "   *bgr background\n")
            if self.checkBox_background.isChecked(): entry_file.write("f" + "   \n")
            else: entry_file.write("n" + "   \n")
            # correction of the detector 'zero'
            entry_file.write("\n" + self.lineEdit_zero_correction.text() + "   correction of the detector 'zero' (in mrad)\n")
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

        for i in range(1, self.tableWidget_film.rowCount() - 1):
            multiGrPr_data.insert(5, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            multiGrPr_info.insert(5, ["Layer " + str(self.tableWidget_film.rowCount() - i) + " thickness in (A)", "real part of nuclear SLD Nb'  (in A**-2) *1e-6", "imaginary part of nuclear SLD Nb'' (in A**-2) *1e-6", "magn. scatt. length density (SLD) Np (in A**-2) *1e-6", "c=<cos(delta_gamma)>_{over small domains}", "dw Debye-Waller in [AA]", "grad_d", "grad_Nb", "grad_Np", "grad_DW"])

        last_itr_loc = 0

        multiGrPr = open(self.lineEdit_data_folder_name.text() + 'multiGrPr.ent', 'w')

        multiGrPr_data[2][0] = self.lineEdit_wavelength.text()
        multiGrPr_data[3][3] = self.tableWidget_film.rowCount() - 1

        # clear results_table before another fit
        for i in range(0, self.tableWidget_fit_results.rowCount()): self.tableWidget_fit_results.removeRow(0)

        # do fast run to find last iteration location
        fit_file_name = "Fit2DBag.dat" if not self.BoToFit_mode == 3 else "FitBag.dat"

        with open(self.lineEdit_data_folder_name.text() + fit_file_name, "r") as fit_file:
            for line_number, line in enumerate(fit_file.readlines()):
                if line.find(" iterate ") > 0:
                    last_itr_loc = line_number

        # show it in the table
        with open(self.lineEdit_data_folder_name.text() + fit_file_name, "r") as fit_file:
            layer_name = 0
            layer_num = 0
            i = 0
            for line_number, line in enumerate(fit_file.readlines()):
                if line_number >= last_itr_loc:

                    try:
                        if line.split()[0] == "Layer":
                            layer_name = "Layer " + str(line.split()[1]) + " "
                        elif line.split()[0] == "Substrate":
                            layer_name = "Substrate "
                        elif line.split()[1] == '<Cos(gamma)>':
                            layer_name = ""

                        if line.split()[1] == 'total':
                            line = line.replace("total scaling", "Scaling_factor")
                        elif line.split()[1] == 'alpha_0':
                            line = line.replace("alpha_0", "overillumination")
                        elif line.split()[1] == 'Re{Nb}':
                            line = line.replace("Re{Nb}", "SLD")
                        elif line.split()[1] == 'Im{Nb}':
                            line = line.replace("Im{Nb}", "iSLD")
                        elif line.split()[1] == 'N_p':
                            line = line.replace("N_p", "mSLD")
                        elif line.split()[1] == 'Debye-Waller':
                            line = line.replace("Debye-Waller", "roughness")
                        if line.split()[0] == "hi_sq.norm:":
                            self.lineEdit_chi_sq.setText(str(line.split()[1]))

                        if line.split()[1] == "iterate":
                            self.lineEdit_iter_number.setText(str(line.split()[0]))

                        # Fill table
                        if line.split()[1] in ['thickness', 'SLD', 'iSLD', 'roughness', 'mSLD', '<Cos(delta_gamma', 'Scaling_factor',
                                               'overillumination', 'background', '<Cos(gamma)>', '<Sin(gamma)>', '<Sin^2(gamma)>', 'Pi(x)', 'Pi(y)', 'Pi(z)', 'Pf(x)', 'Pf(y)', 'Pf(z)'] and not line.split()[3] == "fixed":

                            self.tableWidget_fit_results.insertRow(self.tableWidget_fit_results.rowCount())

                            try:
                                for j in range(0, 5):
                                    item = QtWidgets.QTableWidgetItem()
                                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                                    item.setFlags(
                                        QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable)
                                    self.tableWidget_fit_results.setItem(i, j, item)

                                self.tableWidget_fit_results.item(i, 0).setText(str(i + 1))
                                self.tableWidget_fit_results.item(i, 1).setText(layer_name + " " + line.split()[1])
                                if line.split()[1] in ['SLD', 'iSLD', 'mSLD']:
                                    self.tableWidget_fit_results.item(i, 2).setText(str(round(float(line.split()[2]) * 10e5, 4)))
                                else:
                                    self.tableWidget_fit_results.item(i, 2).setText(str(float(line.split()[2])))

                                if str(line.split()[3]) == "fixed":
                                    table_error = "fixed"
                                elif str(line.split()[4]) == "infinite":
                                    table_error = "infinite"
                                else:
                                    if line.split()[1] in ['SLD', 'iSLD', 'mSLD']:
                                        table_error = str(line.split()[3]) + str(round(float(line.split()[4])* 10e5, 4))
                                    else: table_error = str(line.split()[3]) + str(float(line.split()[4]))

                                self.tableWidget_fit_results.item(i, 3).setText(table_error)
                                self.tableWidget_fit_results.item(i, 4).setText(str(float(line.split()[5])))

                            except: a = 1 # print("create_fit_results_table_error_1")
                            i += 1

                        # Fill multiGrPr.ent
                        ## layers
                        if line.split()[1] in ['thickness', 'SLD', 'iSLD', 'roughness', 'mSLD', '<Cos(delta_gamma'] and not layer_name == "Substrate ":
                            if line.split()[1] == 'thickness': multiGrPr_data[4+layer_num][0] = float(line.split()[2])
                            elif line.split()[1] == 'SLD': multiGrPr_data[4+layer_num][1] = float(line.split()[2]) * 10e+5
                            elif line.split()[1] == 'iSLD': multiGrPr_data[4+layer_num][2] = float(line.split()[2]) * 10e+5
                            elif line.split()[1] == 'mSLD': multiGrPr_data[4+layer_num][3] = float(line.split()[2]) * 10e+5
                            elif line.split()[1] == '<Cos(delta_gamma': multiGrPr_data[4+layer_num][4] = float(line.split()[2])
                            elif line.split()[1] == 'roughness':
                                multiGrPr_data[4+layer_num][5] = float(line.split()[2])
                                layer_num += 1

                        ## substrate
                        elif line.split()[1] in ['SLD', 'iSLD', 'roughness', 'mSLD', '<Cos(delta_gamma'] and layer_name == "Substrate ":
                            if line.split()[1] == 'SLD': multiGrPr_data[4+layer_num][0] = float(line.split()[2]) * 10e+5
                            elif line.split()[1] == 'iSLD': multiGrPr_data[4+layer_num][1] = float(line.split()[2]) * 10e+5
                            elif line.split()[1] == 'mSLD': multiGrPr_data[4 + layer_num][2] = float(line.split()[2]) * 10e+5
                            elif line.split()[1] == '<Cos(delta_gamma': multiGrPr_data[4 + layer_num][3] = float(line.split()[2])
                            elif line.split()[1] == 'roughness': multiGrPr_data[4 + layer_num][4] = float(line.split()[2])

                        ## end of file
                        elif line.split()[1] in ['Scaling_factor', 'overillumination', 'background', '<Cos(gamma)>', 'sg:', 'sg2:']:
                            if line.split()[1] == '<Cos(gamma)>': multiGrPr_data[4+self.tableWidget_film.rowCount()][0] = float(line.split()[2])
                            if line.split()[1] == '<Sin(gamma)>': multiGrPr_data[4 + self.tableWidget_film.rowCount()][1] = float(line.split()[2])
                            if line.split()[1] == '<Sin^2(gamma)>': multiGrPr_data[4 + self.tableWidget_film.rowCount()][2] = float(line.split()[2])
                            if line.split()[1] == 'Scaling_factor': multiGrPr_data[4 + self.tableWidget_film.rowCount()+1][0] = float(line.split()[2])
                            if line.split()[1] == 'overillumination': multiGrPr_data[4 + self.tableWidget_film.rowCount()+1][1] = float(line.split()[2])
                            if line.split()[1] == 'background': multiGrPr_data[4 + self.tableWidget_film.rowCount()+1][2] = float(line.split()[2])

                        elif line.split()[1] == 'Pi(y)': multiGrPr_data[0][1] = float(line.split()[2])
                        elif line.split()[1] == 'Pf(y)': multiGrPr_data[1][1] = float(line.split()[2])

                    except: a = 1 #print("create_fit_results_table_error_2 - skip this : " + line)

        for i in range(0, len(multiGrPr_data)):
            for j in range(0, len(multiGrPr_data[i])):
                multiGrPr.write(str(multiGrPr_data[i][j]) + "     " + str(multiGrPr_info[i][j]) + "\n")
            multiGrPr.write("\n")

        multiGrPr.close()

        self.interface()
    ##<--

    ##--> draw graphs
    def draw_reflectivity(self):
        '''
        draw reflectivity in Angle vs. lg(I) scale using data from hidden table
        '''
        color = [0, 0, 0]

        if "ang(Qz)" in self.input_structure:
            self.label_graphs_refl_and_diff.setText("Reflectivity profile (Reflectivity [10e] vs. Qz [Å**-1]) and Difference (Exper/Fit):")
        elif "ang(rad)" in self.input_structure:
            self.label_graphs_refl_and_diff.setText("Reflectivity profile (Reflectivity [10e] vs. Angle [mrad]) and Difference (Exper/Fit):")

        for i in range(0, 4):
            if self.tableWidget_data_points.item(i, 0).text() not in ("", "[]"):
                data_angle = self.tableWidget_data_points.item(i, 0).text()[1: -1].replace(",", "").split()
                data_I = self.tableWidget_data_points.item(i, 1).text()[1: -1].replace(",", "").split()
                data_dI = self.tableWidget_data_points.item(i, 2).text()[1: -1].replace(",", "").split()

                # change color from black when 2 or 4 polarisations
                if self.BoToFit_mode == 1:
                    if i == 1: color = [255, 0, 0]
                elif self.BoToFit_mode == 2:
                    if i == 1: color = [255, 0, 0]
                    if i == 2: color = [0, 255, 0]
                    if i == 3: color = [0, 0, 255]

                # pyqtgraph can not rescale data in log scale, so we do it manually
                plot_I = []
                plot_angle = []
                plot_dI_err_bottom = []
                plot_dI_err_top = []

                for j in range(0, len(data_angle)):
                    if float(data_I[j]) != 0:
                        plot_angle.append(float(data_angle[j]))
                        plot_I.append(math.log10(float(data_I[j])))
                        plot_dI_err_top.append(abs(math.log10(float(data_I[j]) + float(data_dI[j])) - math.log10(float(data_I[j]))))

                        if float(data_I[j]) > float(data_dI[j]):
                            plot_dI_err_bottom.append(math.log10(float(data_I[j])) - math.log10(float(data_I[j]) - float(data_dI[j])))
                        else: plot_dI_err_bottom.append(0)

                s1 = pg.ErrorBarItem(x=numpy.array(plot_angle[int(self.lineEdit_exclude_first.text()): -int(self.lineEdit_exclude_last.text()) - 1]), y=numpy.array(plot_I[int(self.lineEdit_exclude_first.text()): -int(self.lineEdit_exclude_last.text()) - 1]), top=numpy.array(plot_dI_err_top[int(self.lineEdit_exclude_first.text()): -int(self.lineEdit_exclude_last.text()) - 1]), bottom=numpy.array(plot_dI_err_bottom[int(self.lineEdit_exclude_first.text()): -int(self.lineEdit_exclude_last.text()) - 1]), pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                self.graphicsView_refl_profile.addItem(s1)

                s2 = pg.ScatterPlotItem(x=plot_angle[int(self.lineEdit_exclude_first.text()): -int(self.lineEdit_exclude_last.text()) - 1], y=plot_I[int(self.lineEdit_exclude_first.text()): -int(self.lineEdit_exclude_last.text()) - 1], symbol="o", size=2, pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                self.graphicsView_refl_profile.addItem(s2)

    def draw_and_export_reform_FitFunctX(self):
        '''
        draw BoToFit final fit function on top of the graph with experimental points
        '''

        if self.BoToFit_mode == 0: fit_funct_files = [["FitFunctX.dat", [0, 0, 0]], []]
        elif self.BoToFit_mode == 3: fit_funct_files = [["FitFunct.dat", [0, 0, 0]], []]
        elif self.BoToFit_mode == 1: fit_funct_files = [["Fit2DFunctDD.dat", [0, 0, 0]], ["Fit2DFunctUU.dat", [255, 0, 0]]]
        elif self.BoToFit_mode == 2: fit_funct_files = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]], ["Fit2DFunctUD.dat", [0, 255, 0]], ["Fit2DFunctDU.dat", [0, 0, 255]]]

        for file in fit_funct_files:
            plot_I = []
            plot_angle = []

            if file == []: return

            # if user wants to work with data in Qz, he will get additional files during export
            if not self.BoToFit_mode == 3 and "ang(Qz)" in self.input_structure:
                export_fit_funct_file_name = self.lineEdit_data_folder_name.text() + "EXPORT - Qz_I - " + file[0]
                if self.BoToFit_mode == 1:
                    export_fit_funct_file_name = self.lineEdit_data_folder_name.text() + "EXPORT - Qz_I - " + file[0][:-5] + ".dat"

                export_fit_funct_file = open(export_fit_funct_file_name, "w")

            with open(self.lineEdit_data_folder_name.text() + file[0], 'r') as fit_funct_file:
                for line in fit_funct_file.readlines():
                    try:
                        plot_I.append(math.log10(float(line.split()[1])))
                        if self.BoToFit_mode == 3: plot_angle.append(float(line.split()[0]))
                        else:
                            if "ang(Qz)" in self.input_structure: plot_angle.append(self.angle_convert("rad", "Qz", float(line.split()[0])))
                            elif "ang(rad)" in self.input_structure: plot_angle.append(float(line.split()[0]))
                    except: a = 1

                    # export data for user in (Qz I) format if needed
                    if not self.BoToFit_mode == 3 and "ang(Qz)" in self.input_structure: export_fit_funct_file.write(str((4 * math.pi / float(self.lineEdit_wavelength.text())) * math.sin(float(line.split()[0]))) + "    " + str((line.split()[1])) + "\n")

                s3 = pg.PlotDataItem(plot_angle, plot_I, pen = pg.mkPen(color=(file[1][0], file[1][1], file[1][2]), width=2))
                self.graphicsView_refl_profile.addItem(s3)

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

        with open(self.lineEdit_data_folder_name.text() + 'SLD_profile.dat', 'r') as sld_file:
            for line_number, line in enumerate(sld_file.readlines()):
                try:
                    sld_1.append((float(line.split()[1].replace("D", "E"))))
                    sld_2.append((float(line.split()[2].replace("D", "E"))))
                    dist.append(float(line.split()[0].replace("D", "E")))
                except: a = 1
                points = line_number

            for i in range(1, points, 2):
                if not round(sld_1[points - i], 3) == round(sld_1[points], 3) and cut_1 == -1: cut_1 = points - i

            for i in range(1, points, 2):
                if not round(sld_2[points - i], 3) == round(sld_2[points], 3) and cut_2 == -1: cut_2 = points - i

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

        self.graphicsView_refl_diff.getPlotItem().clear()

        if self.BoToFit_mode == 0: fit_funct_files = [["FitFunctX.dat", [0, 0, 0]], []]
        elif self.BoToFit_mode == 3: fit_funct_files = [["FitFunct.dat", [0, 0, 0]], []]
        if self.BoToFit_mode == 1: fit_funct_files = [["Fit2DFunctDD.dat", [0, 0, 0]], ["Fit2DFunctUU.dat", [255, 0, 0]]]
        elif self.BoToFit_mode == 2: fit_funct_files = [["Fit2DFunctUU.dat", [0, 0, 0]], ["Fit2DFunctDD.dat", [255, 0, 0]], ["Fit2DFunctUD.dat", [0, 255, 0]], ["Fit2DFunctDU.dat", [0, 0, 255]]]

        for i, file in enumerate(fit_funct_files):
            fit_funct_I = []
            fit_funct_angle = []
            diff_I = []
            scale_angle = []
            zero_I = []

            if file == []: return

            with open(self.lineEdit_data_folder_name.text() + file[0], 'r') as fit_funct_file:
                for line in fit_funct_file.readlines():
                    try:
                        if self.BoToFit_mode == 3: fit_funct_angle.append((float(line.split()[0])))
                        else:
                            if "ang(rad)" in self.input_structure:
                                fit_funct_angle.append((float(line.split()[0])))
                            else: fit_funct_angle.append((4 * math.pi / float(self.lineEdit_wavelength.text())) * math.sin(float(line.split()[0])))
                        fit_funct_I.append(float(line.split()[1]))
                    except:
                        a = 1

                s = InterpolatedUnivariateSpline(numpy.array(fit_funct_angle), numpy.array(fit_funct_I), k=1)

            if self.tableWidget_data_points.item(i, 0).text() not in ("", "[]"):
                scale_angle = numpy.array(self.tableWidget_data_points.item(i, 0).text()[1: -1].replace(",", "").split()).astype(float)[int(self.lineEdit_exclude_first.text()) : -int(self.lineEdit_exclude_last.text())]
                data_I = numpy.array(self.tableWidget_data_points.item(i, 1).text()[1: -1].replace(",", "").split()).astype(float)[int(self.lineEdit_exclude_first.text()) : -int(self.lineEdit_exclude_last.text())]

                for i in range(0, len(scale_angle)):
                    if data_I[i] != 0:
                        diff_I.append(data_I[i] / s(scale_angle[i]))
                    else: zero_I.append(i)

            s6 = pg.PlotDataItem(numpy.delete(scale_angle, zero_I), diff_I, pen = pg.mkPen(color=(file[1][0], file[1][1], file[1][2]), width=2))
            self.graphicsView_refl_diff.addItem(s6)
    ##<--

    ##--> reformat data for user if he uses Qz as an angle
    def export_for_user(self):

        # create reformatted files (in Qz I dI) named "Export"
        if self.BoToFit_mode == 3: num_rows = 0
        elif self.BoToFit_mode == 0: num_rows = 1
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

            with open(self.lineEdit_data_folder_name.text() + file_name_export_data_points, "w") as export_data_points:
                data_Qz = self.tableWidget_data_points.item(i, 0).text()[1: -1].replace(",", "").split()
                data_I = self.tableWidget_data_points.item(i, 1).text()[1: -1].replace(",", "").split()
                data_dI = self.tableWidget_data_points.item(i, 2).text()[1: -1].replace(",", "").split()

                for j in range(0, len(data_I)):
                    export_data_points.write(str(data_Qz[j]) + "    " + str(data_I[j]) + "    " + str(data_dI[j]) + "\n")
    ##<--

    ##--> extra functions to shorten the code
    def clear_stuff(self):
        self.graphicsView_refl_profile.getPlotItem().clear()
        self.graphicsView_sld_profile.getPlotItem().clear()
        self.graphicsView_refl_diff.getPlotItem().clear()
        self.lineEdit_data_folder_name.clear()
        self.lineEdit_iter_number.clear()
        self.lineEdit_chi_sq.clear()
        for i in range(0, self.tableWidget_fit_results.rowCount()): self.tableWidget_fit_results.removeRow(0)

    def angle_convert(self, input_unit, output_unit, input_value):

        if output_unit == "Qz":
            if input_unit == "Qz": output_value = float(input_value)
            elif input_unit == "rad": output_value = (4 * math.pi / float(self.lineEdit_wavelength.text())) * math.sin(float(input_value))

        elif output_unit == "rad":
            if input_unit == "Qz": output_value = math.asin(float(input_value) * float(self.lineEdit_wavelength.text()) / (4 * math.pi))
            elif input_unit == "rad": output_value = float(input_value)

        return output_value

if __name__ == "__main__":
    import sys
    QtWidgets.QApplication.setStyle("Fusion")
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


