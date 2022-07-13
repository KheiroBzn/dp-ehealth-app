#########################################################################################
#########################################################################################
import datetime
import random

import pipeline_dp
import pymysql
from PyQt5.QtChart import QBarSet, QPercentBarSeries, QChart, QBarCategoryAxis, QChartView, QPieSeries
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import pandas as pd
import db
import login

#########################################################################################
#########################################################################################
MainCUI, _ = loadUiType('assets/ui/searcher.ui')


#########################################################################################
class MainC(QMainWindow, MainCUI):
    def __init__(self, parent=None):
        super(MainC, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        #########################################
        self.UI_Changes()
        self.Open_Home()
        self.Handle_Buttons()
        self.epsilon = 1
        self.tests = len(self.Get_Patients())
        self.positives = len(self.Get_Positive_Cases('2'))
        self.negatives = self.tests - self.positives
        self.actives = len(self.Get_Active_Cases('2'))
        self.nn_actives = self.positives - self.actives
        self.recovered = len(self.Get_Active_Cases('3'))
        self.deaths = len(self.Get_Active_Cases('4'))
        self.doses = len(self.Get_Doses('2'))
        self.privacy = self.Get_Privacy()
        self.epsilon = 1
        if self.privacy == '1':
            self.epsilon = 0.25
        elif self.privacy == '2':
            self.epsilon = 0.5
        elif self.privacy == '3':
            self.epsilon = 0.75
        else:
            self.epsilon = 1
        self.Get_Stats()

        #########################################
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #########################################
    def UI_Changes(self):
        self.mainTabWidget.tabBar().setVisible(False)
        self.tabWidget.tabBar().setVisible(False)

    #########################################
    def Db_Connect(self):
        self.db = pymysql.connect(host='localhost', user='root', password='', db='pfe')
        self.cur = self.db.cursor()

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
        self.logoutBtnNo.clicked.connect(self.Open_Home)
        self.logoutBtnYes.clicked.connect(self.Handle_logout)
        self.logoutBtnYes.clicked.connect(self.Handle_logout)

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
        self.homePatientsLbl.setText('COVID19 Statistics')

    #########################################
    def Open_Home_Info(self, option=0):
        self.mainTabWidget.setCurrentIndex(0)
        # self.tabWidget.setCurrentIndex(4)

        if option == 1:
            self.homePatientsLbl.setText('Tests')
        elif option == 2:
            self.homePatientsLbl.setText('Positive cases')
        elif option == 3:
            self.homePatientsLbl.setText('Active cases')
        elif option == 4:
            self.homePatientsLbl.setText('Recovered')
        elif option == 5:
            self.homePatientsLbl.setText('Deaths')
        elif option == 6:
            self.homePatientsLbl.setText('Vaccine doses')
        else:
            self.homePatientsLbl.setText('')


        if option == 1:
            self.tabWidget.setCurrentIndex(10)
            self.Create_Private_Patients_Table(1)
            #self.tabWidget.setCurrentIndex(4)
            #self.create_chart(1)
        elif option == 2:
            self.tabWidget.setCurrentIndex(10)
            self.Create_Private_Patients_Table(2)
            #self.tabWidget.setCurrentIndex(5)
            #self.create_chart(2)
        elif option == 3:
            self.tabWidget.setCurrentIndex(10)
            self.Create_Private_Patients_Table(3)
            #self.tabWidget.setCurrentIndex(6)
            #self.create_chart(3)
        elif option == 4:
            self.tabWidget.setCurrentIndex(10)
            self.Create_Private_Patients_Table(4)
            #self.tabWidget.setCurrentIndex(7)
            #self.create_chart(4)
        elif option == 5:
            self.tabWidget.setCurrentIndex(10)
            self.Create_Private_Patients_Table(5)
            #self.tabWidget.setCurrentIndex(8)
            #self.create_chart(5)
        elif option == 6:
            self.tabWidget.setCurrentIndex(10)
            self.Create_Private_Patients_Table(6)
            #self.tabWidget.setCurrentIndex(9)
            #self.create_chart(6)
        else:
            self.Open_Home()

    #########################################
    def Open_More(self, option=0, id_patient=None):
        if id_patient is None:
            id_patient = []
        self.mainTabWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(3)
        self.homePatientsLbl.setText('')

        currentRow = self.homePatientsTableWidget_2.currentRow()
        if currentRow != -1:
            id_p = id_patient[currentRow]
            patient = self.Get_One_Patients(id_p)[0]
            identity = ''
            if self.privacy == '0':
                identity = 'Patient: '+patient[1]+' '+patient[2]+'\n'
            elif self.privacy == '1':
                identity = 'ID: '+str(id_p)+'\n'
            age = 2022 - int(str(patient[5]).split('-')[0])
            statut = ''
            if patient[10] == '1':
                statut = 'Healthy'
            else:
                statut = 'Achieved'
            vaccination = ''
            if patient[10] == '1':
                vaccination = 'Not Vaccinated'
            else:
                vaccination = 'Vaccinated'
            self.patientInfoLbl_2.setText(identity + str(age) + ' years\n' + statut + '\n' + vaccination)

        else:
            self.Open_Home_Info(option)

    #########################################
    def Open_More_Private(self, option=0, id_patient=None):
        print(id_patient)
        if id_patient is None:
            id_patient = {}
        self.mainTabWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(3)
        self.homePatientsLbl.setText('')
        currentRow = self.homePatientsTableWidget_2.currentRow()
        print(currentRow)
        if currentRow != -1:
            id_p = id_patient[currentRow]
            patient = self.Get_One_Patients(id_p)[0]
            age = 2022 - int(str(patient[5]).split('-')[0]) + random.randrange(-3, 3, 1)
            statut = ''
            if patient[10] == '1':
                statut = 'Healthy'
            else:
                statut = 'Achieved'
            vaccination = ''
            if patient[10] == '1':
                vaccination = 'Not Vaccinated'
            else:
                vaccination = 'Vaccinated'
            self.patientInfoLbl_2.setText(str(age) + ' years\n' + statut + '\n' + vaccination)

        else:
            self.Open_Home_Info(option)

    #########################################
    def Create_Private_Patients_Table(self, option=0):
        table = QTableWidget()
        patients = None
        if option == 0:
            patients = self.Get_Patients()
            table = self.homePatientsTableWidget
        elif option == 1:
            patients = self.Get_Patients()
            table = self.homePatientsTableWidget_2
        elif option == 2:
            patients = self.Get_Positive_Cases('2')
            table = self.homePatientsTableWidget_2
        elif option == 3:
            patients = self.Get_Active_Cases('2')
            table = self.homePatientsTableWidget_2
        elif option == 4:
            patients = self.Get_Active_Cases('3')
            table = self.homePatientsTableWidget_2
        elif option == 5:
            patients = self.Get_Active_Cases('4')
            table = self.homePatientsTableWidget_2
        elif option == 6:
            patients = self.Get_Doses('2')
            table = self.homePatientsTableWidget_2
        else:
            self.Open_Home()

        table.setRowCount(len(patients))
        line = 0
        buttons = []
        ids = []
        horizontalHeaderLabels = []
        cols_width = []
        for row in patients:
            col = 0
            if (self.privacy == '0') or (self.privacy == '1'):
                id = QLabel()
                id.setText(str(row[0]))
                id.setAlignment(Qt.AlignCenter)
                table.setCellWidget(line, col, id)
                horizontalHeaderLabels.append('ID')
                cols_width.append(50)
                col += 1

                if self.privacy == '0':
                    nom = QLabel(table)
                    nom.setText(row[1])
                    nom.setAlignment(Qt.AlignCenter)
                    table.setCellWidget(line, col, nom)
                    horizontalHeaderLabels.append('Name')
                    cols_width.append(150)
                    col += 1

                    prenom = QLabel(table)
                    prenom.setText(row[2])
                    prenom.setAlignment(Qt.AlignCenter)
                    table.setCellWidget(line, col, prenom)
                    horizontalHeaderLabels.append('First Name')
                    cols_width.append(150)
                    col += 1

            vaccin = QLabel()
            if row[10] == '1':
                vaccin.setText('NON-VACCINÉ')
            else:
                vaccin.setText('VACCINÉ')

            statut = QLabel()
            if row[11] == '1':
                statut.setText('POSITIVE/CONFINED')
            elif row[11] == '2':
                statut.setText('ACTIVE/HOSPITALISED')
            elif row[11] == '3':
                statut.setText('RECOVERED')
            else:
                statut.setText('DEATH')

            test = QLabel()
            if row[15] == '1':
                test.setText('NEGATIVE')
            else:
                test.setText('POSITIVE')

            vaccin.setAlignment(Qt.AlignCenter)
            statut.setAlignment(Qt.AlignCenter)
            test.setAlignment(Qt.AlignCenter)
            table.setCellWidget(line, col, statut)
            horizontalHeaderLabels.append('Statut')
            col += 1
            table.setCellWidget(line, col, vaccin)
            horizontalHeaderLabels.append('Vaccine')
            col += 1
            table.setCellWidget(line, col, test)
            horizontalHeaderLabels.append('Last Test')
            col += 1

            if (self.privacy == '0') or (self.privacy == '1') or (self.privacy == '2') or (self.privacy == '3'):
                moreBtn = QPushButton(table)
                moreBtn.setText('View more')
                moreBtn.setObjectName('p_'+str(row[0]))
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
                table.setCellWidget(line, col, moreBtn)
                horizontalHeaderLabels.append('')
                buttons.insert(line+1, moreBtn)
                if self.privacy == '0':
                    table.setColumnCount(7)
                    cols_width.append(150)
                    cols_width.append(200)
                    cols_width.append(200)
                    cols_width.append(100)
                elif self.privacy == '1':
                    table.setColumnCount(5)
                    cols_width.append(250)
                    cols_width.append(250)
                    cols_width.append(250)
                    cols_width.append(150)
                else:
                    table.setColumnCount(4)
                    cols_width.append(250)
                    cols_width.append(250)
                    cols_width.append(250)
                    cols_width.append(200)
            else:
                table.setColumnCount(3)
                cols_width.append(333)
                cols_width.append(333)
                cols_width.append(333)

            print(col)
            ids.insert(line+1, row[0])
            line = line + 1

        table_cols = table.columnCount()
        i = 0
        while i < table_cols:
            table.setColumnWidth(i, cols_width[i])
            i += 1

        table.setHorizontalHeaderLabels(horizontalHeaderLabels)

        i = 0
        if (self.privacy == '3') or (self.privacy == '4'):
            while i < len(buttons):
                button = buttons[i]
                button.clicked.connect(lambda: self.Open_More_Private(option, ids))
                i += 1
        else:
            while i < len(buttons):
                button = buttons[i]
                button.clicked.connect(lambda: self.Open_More(option, ids))
                i += 1

        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)

    #########################################
    def Open_Consulting(self):
        self.mainTabWidget.setCurrentIndex(1)
        self.statsTab.setCurrentIndex(0)

    #########################################
    def Open_Documents(self):
        self.mainTabWidget.setCurrentIndex(2)

    #########################################
    def Open_Account(self):
        self.mainTabWidget.setCurrentIndex(3)

    #########################################
    def Open_Logout(self):
        self.mainTabWidget.setCurrentIndex(4)

    #########################################
    def Open_InfoHome(self):
        self.accountTabWidget.setCurrentIndex(0)

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
    def Get_Privacy(self):
        query1 = db.Confidentialite.select().order_by(db.Confidentialite.id.desc()).get()
        query2 = db.Confidentialite.select().where(db.Confidentialite.id == query1).get()
        return query2.niveau

    #########################################
    def Display_Stats(self):
        self.totalTestsLbl.setText(str(self.tests))
        self.totalPositivesLbl.setText(str(self.positives))
        self.totalActivesLbl.setText(str(self.actives))
        self.totalRecoverecLbl.setText(str(self.recovered))
        self.totalDeathsLbl.setText(str(self.deaths))
        self.totalDosesLbl.setText(str(self.doses))

    #########################################
    def Get_Stats(self):
        if self.privacy == '0':
            self.Display_Stats()
        else:
            if self.privacy == '1':
                self.epsilon = 0.25
            elif self.privacy == '2':
                self.epsilon = 0.5
            elif self.privacy == '3':
                self.epsilon = 0.75
            else:
                self.epsilon = 1

            df = pd.read_csv('assets/db/covid.csv')
            rows = [index_row[1] for index_row in df.iterrows()]
            df.head()

            backend = pipeline_dp.LocalBackend()
            budget_accountant = pipeline_dp.NaiveBudgetAccountant(total_epsilon=self.epsilon, total_delta=1e-6)
            dp_engine = pipeline_dp.DPEngine(budget_accountant, backend)
            data_extractors = pipeline_dp.DataExtractors(
                partition_extractor=lambda line: line.etat,
                privacy_id_extractor=lambda line: line.id,
                value_extractor=lambda line: line.test)
            params = pipeline_dp.AggregateParams(
                noise_kind=pipeline_dp.NoiseKind.LAPLACE,
                metrics=[pipeline_dp.Metrics.COUNT],
                max_partitions_contributed=3,
                max_contributions_per_partition=2,
                min_value=0,
                max_value=60)
            public_partitions = list(range(1, 5))
            dp_result = dp_engine.aggregate(rows, params, data_extractors)
            budget_accountant.compute_budgets()
            dp_result = list(dp_result)

            if len(dp_result) > 0:
                for row in dp_result:
                    val = int(str(row[1]).replace(")", "").split('=')[1].split('.')[0])
                    if val > 0:
                        if row[0] == 1:
                            self.nn_actives = val
                        elif row[0] == 2:
                            self.actives = val
                        elif row[0] == 3:
                            self.recovered = val
                        else:
                            self.deaths = val
                self.positives = self.actives + self.nn_actives

            #########################################
            backend = pipeline_dp.LocalBackend()
            budget_accountant = pipeline_dp.NaiveBudgetAccountant(total_epsilon=self.epsilon, total_delta=1e-6)
            dp_engine = pipeline_dp.DPEngine(budget_accountant, backend)
            data_extractors = pipeline_dp.DataExtractors(
                partition_extractor=lambda line: line.resultat,
                privacy_id_extractor=lambda line: line.id,
                value_extractor=lambda line: line.test)
            params = pipeline_dp.AggregateParams(
                noise_kind=pipeline_dp.NoiseKind.LAPLACE,
                metrics=[pipeline_dp.Metrics.COUNT],
                max_partitions_contributed=3,
                max_contributions_per_partition=2,
                min_value=0,
                max_value=60)
            public_partitions = list(range(1, 3))
            dp_result = dp_engine.aggregate(rows, params, data_extractors)
            budget_accountant.compute_budgets()
            dp_result = list(dp_result)
            if len(dp_result) > 0:
                for row in dp_result:
                    val = int(str(row[1]).replace(")", "").split('=')[1].split('.')[0])
                    if val > 0:
                        if row[0] == 1:
                            self.negatives = val
                        else:
                            self.positives = val
                self.tests = self.positives + self.negatives

            #########################################
            df = pd.read_csv('assets/db/covid_vaccin.csv')
            rows = [index_row[1] for index_row in df.iterrows()]
            df.head()

            backend = pipeline_dp.LocalBackend()
            budget_accountant = pipeline_dp.NaiveBudgetAccountant(total_epsilon=self.epsilon, total_delta=1e-6)
            dp_engine = pipeline_dp.DPEngine(budget_accountant, backend)
            data_extractors = pipeline_dp.DataExtractors(
                partition_extractor=lambda line: line.vaccination,
                privacy_id_extractor=lambda line: line.id,
                value_extractor=lambda line: line.id_vaccin)
            params = pipeline_dp.AggregateParams(
                noise_kind=pipeline_dp.NoiseKind.LAPLACE,
                metrics=[pipeline_dp.Metrics.COUNT],
                max_partitions_contributed=3,
                max_contributions_per_partition=2,
                min_value=0,
                max_value=60)
            public_partitions = list(range(1, 3))
            dp_result = dp_engine.aggregate(rows, params, data_extractors)
            budget_accountant.compute_budgets()
            dp_result = list(dp_result)
            if len(dp_result) > 0:
                for row in dp_result:
                    val = int(str(row[1]).replace(")", "").split('=')[1].split('.')[0])
                    if val > 0:
                        self.doses = val

            self.Display_Stats()

    #########################################
#########################################################################################
