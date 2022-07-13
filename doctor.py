#########################################################################################
#########################################################################################
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.QtCore import Qt, QModelIndex
import pymysql
import db
import login

#########################################################################################
#########################################################################################
MainMUI, _ = loadUiType('assets/ui/doctor.ui')


#########################################################################################
class MainM(QMainWindow, MainMUI):
    def __init__(self, parent=None):
        super(MainM, self).__init__(parent)
        QMainWindow.__init__(self)
        self.patients_ids = None
        self.patients_names = None
        self.completer = None
        self.setupUi(self)
        #########################################
        self.Db_Connect()
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
        self.patientsListTab.tabBar().setVisible(False)
        self.tabWidget.tabBar().setVisible(False)

        self.patients_names = []
        self.patients_ids = {}
        patients = self.Get_Patients()
        for p in patients:
            name = p[1]+' '+p[2]
            self.patients_names.append(name)
            self.patients_ids[name] = p[0]
        
        self.completer = QCompleter(self.patients_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)
    #########################################

    def Db_Connect(self):
        self.db = pymysql.connect(host='localhost', user='root', password='', db='pfe')
        self.cur = self.db.cursor()

    #########################################
    def Get_Patients(self):
        query = ((db.Patient.select(db.Patient, db.DossierCovid, db.Test).join(db.DossierCovid).order_by(
            db.Patient.id.asc())).join(db.Test)).tuples()
        return query

    #########################################
    def Get_One_Patients(self, id=0):
        query = ((db.Patient.select(db.Patient, db.DossierCovid, db.Test).where(db.Patient.id == id).join(
            db.DossierCovid).order_by(db.Patient.id.asc())).join(db.Test)).tuples()
        return query

    #########################################
    def Get_Positive_Cases(self, resultat='1'):
        query = ((db.Patient.select(db.Patient, db.DossierCovid, db.Test).where(db.Test.resultat == resultat).join(
            db.DossierCovid).order_by(db.Patient.id.asc())).join(db.Test)).tuples()
        return query

    #########################################
    def Get_Active_Cases(self, etat='2'):
        query = ((db.Patient.select(db.Patient, db.DossierCovid, db.Test).where(db.DossierCovid.etat == etat).join(
            db.DossierCovid).order_by(db.Patient.id.asc())).join(db.Test)).tuples()
        return query

    #########################################
    def Get_Doses(self, vaccination='2'):
        query = ((db.Patient.select(db.Patient, db.DossierCovid, db.Test).where(
            db.DossierCovid.vaccination == vaccination).join(db.DossierCovid).order_by(db.Patient.id.asc())).join(
            db.Test)).tuples()
        return query

    #########################################
    def Handle_Buttons(self):
        ## Main Tab Buttons
        self.homeBtn.clicked.connect(self.Open_Home)
        self.consultingBtn.clicked.connect(self.Open_Consulting)
        self.accountLeftBtn.clicked.connect(self.Open_Account)
        self.logoutBtn.clicked.connect(self.Open_Logout)
        self.accountBtn.clicked.connect(self.Open_Account)
        #########################################
        ## Main Tab Buttons
        self.card1btn.clicked.connect(lambda: self.Open_Home_Info(1))
        self.card2btn.clicked.connect(lambda: self.Open_Home_Info(2))
        self.card3btn.clicked.connect(lambda: self.Open_Home_Info(3))
        self.card4btn.clicked.connect(lambda: self.Open_Home_Info(4))
        self.card5btn.clicked.connect(lambda: self.Open_Home_Info(5))
        self.card6btn.clicked.connect(lambda: self.Open_Home_Info(6))
        #########################################
        ## Logout Tab Buttons
        self.logoutBtnNo.clicked.connect(self.Open_Home)
        self.logoutBtnYes.clicked.connect(self.Handle_logout)
        ## Patients Table Buttons
        self.logoutBtnYes.clicked.connect(self.Handle_logout)
        self.searchbtn.clicked.connect(self.Open_Search)

    #########################################
    def Handle_logout(self):
        self.close()
        self.window = login.Login()
        self.window.center()
        self.window.show()

    #########################################
    def Open_Home(self):
        self.mainTabWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.homePatientsLbl.setText('Statistiques récentes')

        tests = len(self.Get_Patients())
        positive = len(self.Get_Positive_Cases('2'))
        active = len(self.Get_Active_Cases('2'))
        recovered = len(self.Get_Active_Cases('3'))
        death = len(self.Get_Active_Cases('4'))
        doses = len(self.Get_Doses('2'))

        self.totalTestsLbl.setText(str(tests))
        self.totalPositivesLbl.setText(str(positive))
        self.totalActivesLbl.setText(str(active))
        self.totalRecoverecLbl.setText(str(recovered))
        self.totalDeathsLbl.setText(str(death))
        self.totalDosesLbl.setText(str(doses))

    #########################################
    def Open_Home_Info(self, option=0):
        self.mainTabWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(1)

        if option == 1:
            self.Create_Patients_Table(1)
            self.homePatientsLbl.setText('Tests faits')
        elif option == 2:
            self.Create_Patients_Table(2)
            self.homePatientsLbl.setText('Cas positifs')
        elif option == 3:
            self.Create_Patients_Table(3)
            self.homePatientsLbl.setText('Cas actifs')
        elif option == 4:
            self.Create_Patients_Table(4)
            self.homePatientsLbl.setText('Cas rétablis')
        elif option == 5:
            self.Create_Patients_Table(5)
            self.homePatientsLbl.setText('Décès')
        elif option == 6:
            self.Create_Patients_Table(6)
            self.homePatientsLbl.setText('Doses de vaccin')
        else:
            self.Open_Home()

    #########################################
    def Open_Consulting(self):
        self.mainTabWidget.setCurrentIndex(1)
        self.patientsListTab.setCurrentIndex(0)

        self.Create_Patients_Table(0)

    #########################################
    def Open_Account(self):
        self.mainTabWidget.setCurrentIndex(2)

    #########################################
    def Open_Logout(self):
        self.mainTabWidget.setCurrentIndex(3)

    #########################################
    def Open_InfoHome(self):
        self.accountTabWidget.setCurrentIndex(0)

    #########################################
    def Open_More(self, option=0, id_patient=None):
        if id_patient is None:
            id_patient = {}
        self.mainTabWidget.setCurrentIndex(1)
        self.patientsListTab.setCurrentIndex(1)
        currentRow = None
        if option == 0:
            currentRow = self.patientsTableWidget.currentRow()
        else:
            currentRow = self.homePatientsTableWidget.currentRow()

        id_p = id_patient[currentRow]

        patient = self.Get_One_Patients(int(id_p))[0]

        nom = patient[1]
        prenom = patient[2]
        age = 2022 - int(str(patient[5]).split('-')[0])
        statut = ''
        if patient[11] == '1':
            statut = 'Atteint / Confiné'
        elif patient[11] == '2':
            statut = 'Atteint / Actif'
        elif patient[11] == '3':
            statut = 'Sain'
        else:
            statut = 'Mort'

        vaccination = ''
        if patient[10] == '1':
            vaccination = 'Non-Vacciné'
        else:
            vaccination = 'Vacciné'
        self.patientInfoLbl.setText(nom + ' ' + prenom + '\n' + str(age) + ' ans\n' + statut + '\n' + vaccination)

    #########################################

    def Open_Search(self, option=0):
        self.mainTabWidget.setCurrentIndex(1)
        self.patientsListTab.setCurrentIndex(1)

        search = self.searchbar.text()
        id_p = self.patients_ids[search]
        patient = self.Get_One_Patients(int(id_p))[0]

        nom = patient[1]
        prenom = patient[2]
        age = 2022 - int(str(patient[5]).split('-')[0])
        statut = ''
        if patient[11] == '1':
            statut = 'Atteint / Confiné'
        elif patient[11] == '2':
            statut = 'Atteint / Actif'
        elif patient[11] == '3':
            statut = 'Sain'
        else:
            statut = 'Mort'

        vaccination = ''
        if patient[10] == '1':
            vaccination = 'Non-Vacciné'
        else:
            vaccination = 'Vacciné'
        self.patientInfoLbl.setText(nom + ' ' + prenom + '\n' + str(age) + ' ans\n' + statut + '\n' + vaccination)

    #########################################
    def Create_Patients_Table(self, option=0):
        table = QTableWidget()
        patients = tuple()
        if option == 0:
            patients = self.Get_Patients()
            table = self.patientsTableWidget
        elif option == 1:
            patients = self.Get_Patients()
            table = self.homePatientsTableWidget
        elif option == 2:
            patients = self.Get_Positive_Cases('2')
            table = self.homePatientsTableWidget
        elif option == 3:
            patients = self.Get_Active_Cases('2')
            table = self.homePatientsTableWidget
        elif option == 4:
            patients = self.Get_Active_Cases('3')
            table = self.homePatientsTableWidget
        elif option == 5:
            patients = self.Get_Active_Cases('4')
            table = self.homePatientsTableWidget
        elif option == 6:
            patients = self.Get_Doses('2')
            table = self.homePatientsTableWidget
        else:
            self.Open_Home()

        table.setRowCount(len(patients))
        line = 0
        button_dict = {}
        id_dict = {}
        for row in patients:
            id_patient = QTableWidgetItem(str(row[0]))
            id_dict[line] = id_patient.text()

            nom = QLabel(table)
            nom.setText(row[1])

            prenom = QLabel(table)
            prenom.setText(row[2])

            vaccin = QLabel(table)
            if row[10] == '1':
                vaccin.setText('NON-VACCINÉ')
            else:
                vaccin.setText('VACCINÉ')

            statut = QLabel(table)
            if row[11] == '1':
                statut.setText('POSITIF/CONFINÉ')
            elif row[11] == '2':
                statut.setText('ACTIF/HOSPITALISÉ')
            elif row[11] == '3':
                statut.setText('RÉTABLIE')
            else:
                statut.setText('MORT')

            test = QLabel(table)
            if row[15] == '1':
                test.setText('NÉGATIF')
            else:
                test.setText('POSITIF')

            moreBtn = QPushButton(table)
            moreBtn.setText('Voir plus')
            moreBtn.setStyleSheet("""
                            QPushButton{
                              background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2596be, stop: 0.4 #2586be, stop: 0.5 #2576be, stop: 1.0 #2566be);
                              padding: 5px;
                              color: #eff9fe;
                              border-radius: 15px;
                            }

                            QPushButton:hover {
                              background-color: #2580be;
                            }
                            """)

            table.setColumnWidth(0, 50)
            table.setColumnWidth(1, 150)
            table.setColumnWidth(2, 150)
            table.setColumnWidth(3, 150)
            table.setColumnWidth(4, 200)
            table.setColumnWidth(5, 200)
            table.setColumnWidth(6, 100)

            table.setItem(line, 0, id_patient)
            table.setCellWidget(line, 1, nom)
            table.setCellWidget(line, 2, prenom)
            table.setCellWidget(line, 3, vaccin)
            table.setCellWidget(line, 4, statut)
            table.setCellWidget(line, 5, test)
            table.setCellWidget(line, 6, moreBtn)

            id_patient.setTextAlignment(Qt.AlignCenter)
            nom.setAlignment(Qt.AlignCenter)
            prenom.setAlignment(Qt.AlignCenter)
            vaccin.setAlignment(Qt.AlignCenter)
            statut.setAlignment(Qt.AlignCenter)
            test.setAlignment(Qt.AlignCenter)

            button_dict[line] = moreBtn
            id_dict[line] = id_patient.text()

            line = line + 1

        for button in button_dict.values():
            button.clicked.connect(lambda: self.Open_More(option, id_dict))

        table.horizontalHeader().setStretchLastSection(True)

#########################################################################################
