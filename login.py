#########################################################################################
#########################################################################################
import datetime

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import *
import pymysql
from PyQt5.uic import loadUiType
import db
import admin
import doctor
import patient
import analyst
import searcher

#########################################################################################
#########################################################################################
LoginUI, _ = loadUiType('assets/ui/login.ui')

#########################################################################################
class Login(QMainWindow, LoginUI):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        QMainWindow.__init__(self)
        self.window = None
        self.setupUi(self)
        #########################################
        self.UI_Changes()
        self.Handle_Buttons()
        self.db = self.Db_Connect()

    #########################################
    def UI_Changes(self):
        self.password.setEchoMode(QLineEdit.Password)
        self.password_eye.setIcon(QtGui.QIcon('assets/icons/others/hide_pw.png'))

    #########################################
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #########################################
    def Db_Connect(self):
        return pymysql.connect(host='localhost', user='root', password='', db='pfe')

    #########################################
    def Handle_Buttons(self):
        self.loginBtn.clicked.connect(self.Handle_login)
        self.password_eye.clicked.connect(self.show_hide_password)

    #########################################
    def show_hide_password(self):
        if self.password.echoMode() == QLineEdit.Normal:
            self.password_eye.setIcon(QtGui.QIcon('assets/icons/others/hide_pw.png'))
            self.password_eye.setIconSize(QtCore.QSize(30, 30))
            self.password.setEchoMode(QLineEdit.Password)
        else:
            self.password_eye.setIcon(QtGui.QIcon('assets/icons/others/show_pw.png'))
            self.password_eye.setIconSize(QtCore.QSize(30, 30))
            self.password.setEchoMode(QLineEdit.Normal)

    #########################################
    def get_user(self, username='', password=''):
        query = db.Utilisateur.select().where(
            (db.Utilisateur.nom_utilisateur == username) & (db.Utilisateur.mot_de_passe == password)).order_by(
            db.Utilisateur.id).tuples()
        return query

    #########################################
    def get_admin(self, userid=0):
        query = db.Admin.select().where(db.Admin.id_utilisateur == userid).tuples()
        return query

    #########################################
    def get_doctor(self, userid=0):
        query = db.Medecin.select().where(db.Medecin.id_utilisateur == userid).tuples()
        return query

    #########################################
    def get_patient(self, userid=0):
        query = db.Patient.select().where(db.Patient.id_utilisateur == userid).tuples()
        return query

    #########################################
    def get_analyst(self, userid=0):
        query = db.Analyste.select().where(db.Analyste.id_utilisateur == userid).tuples()
        return query

    #########################################
    def get_searcher(self, userid=0):
        query = db.Chercheur.select().where(db.Chercheur.id_utilisateur == userid).tuples()
        return query

    #########################################
    def Handle_login(self):
        username = self.username.text()
        password = self.password.text()

        if len(self.get_user(username, password)) > 0:
            user = self.get_user(username, password)[0]
            role = user[4]
            userid = user[0]
            self.close()

            if role == '1':
                self.login_admin(userid, username)
            elif role == '2':
                self.login_doctor(userid)
            elif role == '3':
                self.login_patient(userid)
            elif role == '4':
                self.login_analyst(userid)
            elif role == '5':
                self.login_searcher((userid))
            else:
                self.window = Login()

            self.window.center()
            self.window.show()
        else:
            self.errLbl.setText('Wrong informations')

    #########################################
    def login_admin(self, userid, username):
        adm = self.get_admin(userid)[0]
        ui = admin.MainAdmin()
        ui.userid = userid
        ui.id = adm[0]
        ui.nom.setText(adm[1])
        ui.prenom.setText(adm[2])
        ui.email.setText(adm[3])
        ui.username_2.setText(username)
        ui.welcomeLbl.setText('Welcome ' + adm[1])
        self.window = ui

    #########################################
    def login_doctor(self, userid):
        d = self.get_doctor(userid)[0]
        ui = doctor.MainM()
        ui.nom.setText(d[1])
        ui.prenom.setText(d[2])
        ui.email.setText(d[3])
        ui.welcomeLbl.setText('Welcome Dr. ' + d[1])
        self.window = ui

    #########################################
    def login_patient(self, userid):
        ui = patient.MainP()
        p = self.get_patient(userid)[0]
        dossier_covid = p[7]
        all_tests = db.Test.select().where(db.Test.id_dossier_covid == dossier_covid).order_by(db.Test.id.desc())
        if len(all_tests) > 0:
            last_test = db.Test.select().where(db.Test.id_dossier_covid == dossier_covid).order_by(db.Test.id.desc())
            last_test = last_test.get()

            ui.test_date.setText(str(last_test.date_test))
            if last_test.resultat == '1':
                ui.test_result.setText('Negative')
            else:
                ui.test_result.setText('Positive')
            ui.testsTable.setRowCount(len(all_tests))
            line = 0
            for test in all_tests:
                id_test = QLabel(ui.testsTable)
                id_test.setText(str(test.id))
                id_covid = QLabel(ui.testsTable)
                id_covid.setText(str(test.id_dossier_covid))
                date = QLabel(ui.testsTable)
                date.setText(str(test.date_test))
                result = QLabel(ui.testsTable)
                if test.resultat == '1':
                    result.setText('Negative')
                else:
                    result.setText('Positive')

                id_test.setAlignment(Qt.AlignCenter)
                id_covid.setAlignment(Qt.AlignCenter)
                date.setAlignment(Qt.AlignCenter)
                result.setAlignment(Qt.AlignCenter)

                ui.testsTable.setColumnWidth(0, 200)
                ui.testsTable.setColumnWidth(1, 200)
                ui.testsTable.setColumnWidth(2, 200)
                ui.testsTable.setColumnWidth(3, 200)

                ui.testsTable.setCellWidget(line, 0, id_test)
                ui.testsTable.setCellWidget(line, 1, id_covid)
                ui.testsTable.setCellWidget(line, 2, date)
                ui.testsTable.setCellWidget(line, 3, result)

                line = line + 1

            ui.testsTable.horizontalHeader().setStretchLastSection(True)

        ui.nom.setText(p[1])
        ui.prenom.setText(p[2])
        ui.adresse.setText(p[3])
        ui.email.setText(p[4])
        if p[5] is datetime.date:
            date = QDate(p[5])
        else:
            date = QDate(datetime.date(1900, 1, 1))
        ui.date.setDate(date)
        if p[6] == '2':
            ui.genre.setCurrentIndex(0)
            ui.welcomeLbl.setText('Welcome . ' + p[2])
        else:
            ui.genre.setCurrentIndex(1)
            ui.welcomeLbl.setText('Welcome . ' + p[2])

        self.window = ui

    #########################################
    def login_analyst(self, userid):
        a = self.get_analyst(userid)[0]
        ui = analyst.MainA()

        ui.userid = userid
        ui.id = a[0]
        ui.welcomeLbl.setText('Welcome ' + a[1])

        self.window = ui

    #########################################
    def login_searcher(self, userid):
        s = self.get_searcher(userid)[0]
        ui = searcher.MainC()

        ui.userid = userid
        ui.id = s[0]
        ui.welcomeLbl.setText('Welcome ' + s[1])

        self.window = ui

#########################################################################################
