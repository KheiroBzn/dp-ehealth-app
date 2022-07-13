#########################################################################################
#########################################################################################
import os

import qpageview
from PyQt5 import QtWebEngineWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import db
import login

#########################################################################################
#########################################################################################
MainPUI, _ = loadUiType('assets/ui/patient.ui')


#########################################################################################
class MainP(QMainWindow, MainPUI):
    def __init__(self, parent=None):
        super(MainP, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        #########################################
        self.UI_Changes()
        self.Open_Home()
        self.Handle_Buttons()

    #########################################
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #########################################
    def UI_Changes(self):
        self.mainTabWidget.tabBar().setVisible(False)
        self.accountTabWidget.tabBar().setVisible(False)
        self.id.setVisible(False)

    #########################################
    def Db_Connect(self):
        pass

    #########################################
    def Handle_Buttons(self):
        ## Main Tab Buttons
        self.homeBtn.clicked.connect(self.Open_Home)
        self.informationsBtn.clicked.connect(self.Open_Infos)
        self.accountLeftBtn.clicked.connect(self.Open_Account)
        self.logoutBtn.clicked.connect(self.Open_Logout)
        self.asideBtn.clicked.connect(self.Open_Account)
        self.accountBtn.clicked.connect(self.Open_Account)
        self.more_tests.clicked.connect(self.Open_Tests)
        #########################################
        ## Logout Tab Buttons
        self.logoutBtnNo.clicked.connect(self.Open_Home)
        self.logoutBtnYes.clicked.connect(self.Handle_logout)
        #########################################
        ## Account Tab Buttons
        self.infoHomeBtn.clicked.connect(self.Open_InfoHome)
        self.medicalHomeBtn.clicked.connect(self.Open_MedicalHome)

    #########################################
    def Handle_logout(self):
        self.close()
        self.window = login.Login()
        self.window.center()
        self.window.show()

    #########################################
    def Open_Home(self):
        self.mainTabWidget.setCurrentIndex(0)

    #########################################
    def Open_Infos(self):
        self.mainTabWidget.setCurrentIndex(1)

        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path = "assets/files/infos.pdf"
        abs_file_path = os.path.join(script_dir, rel_path)

        view = QtWebEngineWidgets.QWebEngineView(self.infosFrame)
        settings = view.settings()
        settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        url = QtCore.QUrl.fromLocalFile(abs_file_path)
        view.load(url)
        view.resize(1050, 580)
        view.show()

    #########################################
    def Open_Account(self):
        self.mainTabWidget.setCurrentIndex(2)
        self.accountTabWidget.setCurrentIndex(0)

    #########################################
    def Open_Logout(self):
        self.mainTabWidget.setCurrentIndex(3)

    #########################################
    def Open_Tests(self):
        self.mainTabWidget.setCurrentIndex(4)

    #########################################
    def Open_InfoHome(self):
        self.accountTabWidget.setCurrentIndex(0)

    #########################################
    def Open_MedicalHome(self):
        self.accountTabWidget.setCurrentIndex(1)
        self.medicalContentTabWidget.setCurrentIndex(0)

    #########################################
    def Get_Patient(self, userid=0):
        query = db.Patient.select().where(db.Patient.id_utilisateur == userid).tuples()
        return query
#########################################################################################
