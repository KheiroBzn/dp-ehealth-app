#########################################################################################
#########################################################################################
import datetime

from PyQt5.QtChart import QChart, QBarCategoryAxis, QChartView, QBarSet, QPercentBarSeries, QPieSeries
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.QtCore import Qt, QPointF
import pipeline_dp
import pandas as pd
import pymysql
import db
import random
import login

#########################################################################################
#########################################################################################

MainAUI, _ = loadUiType('assets/ui/analyst.ui')


#########################################################################################
class MainA(QMainWindow, MainAUI):
    def __init__(self, parent=None):
        super(MainA, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        #########################################
        self.Db_Connect()
        self.UI_Changes()
        self.Open_Home()
        self.Handle_Buttons()
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
        self.privacy = self.Get_Privacy()

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
        ## Logout Tab Buttons
        self.logoutBtnNo.clicked.connect(self.Open_Home)
        self.logoutBtnYes.clicked.connect(self.Handle_logout)
        ## Logout Tab Buttons
        ## Patients Table ButtonsS
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
        # self.Get_DP_Tests()

    #########################################
    def Open_Home_Info(self, option=0):
        self.mainTabWidget.setCurrentIndex(0)

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
            self.tabWidget.setCurrentIndex(4)
            self.create_chart(1)
        elif option == 2:
            self.tabWidget.setCurrentIndex(5)
            self.create_chart(2)
        elif option == 3:
            self.tabWidget.setCurrentIndex(6)
            self.create_chart(3)
        elif option == 4:
            self.tabWidget.setCurrentIndex(7)
            self.create_chart(4)
        elif option == 5:
            self.tabWidget.setCurrentIndex(8)
            self.create_chart(5)
        elif option == 6:
            self.tabWidget.setCurrentIndex(9)
            self.create_chart(6)
        else:
            self.Open_Home()
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
                metrics=[pipeline_dp.Metrics.COUNT, pipeline_dp.Metrics.SUM],
                max_partitions_contributed=4,
                max_contributions_per_partition=2,
                min_value=0,
                max_value=1000)
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
                metrics=[pipeline_dp.Metrics.COUNT, pipeline_dp.Metrics.SUM],
                max_partitions_contributed=4,
                max_contributions_per_partition=2,
                min_value=0,
                max_value=1000)
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
                metrics=[pipeline_dp.Metrics.COUNT, pipeline_dp.Metrics.SUM],
                max_partitions_contributed=4,
                max_contributions_per_partition=2,
                min_value=0,
                max_value=1000)
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
    def month_str(self, month=0):
        if month == 1:
            return "January"
        elif month == 2:
            return  "February"
        elif month == 3:
            return "March"
        elif month == 4:
            return "April"
        elif month == 5:
            return "May"
        elif month == 6:
            return "June"
        elif month == 7:
            return "July"
        elif month == 8:
            return "August"
        elif month == 9:
            return "September"
        elif month == 10:
            return  "October"
        elif month == 11:
            return  "November"
        elif month == 12:
            return  "December"
        else: return ""


    #########################################
    def create_chart(self, option=0):
        privacy = self.Get_Privacy()
        if option == 1:
            positives1 = len(db.Test.select().where(((db.Test.resultat == 2) & ((
                        datetime.date(2022, 5, 1) <= db.Test.date_test <= datetime.date(2022, 5, 5))))))
            positives2 = len(db.Test.select().where(((db.Test.resultat == 2) & ((
                        datetime.date(2022, 5, 6) <= db.Test.date_test <= datetime.date(2022, 5, 10))))))
            positives3 = len(db.Test.select().where(((db.Test.resultat == 2) & ((
                        datetime.date(2022, 5, 11) <= db.Test.date_test <= datetime.date(2022, 5, 15))))))
            positives4 = len(db.Test.select().where(((db.Test.resultat == 2) & ((
                        datetime.date(2022, 5, 16) <= db.Test.date_test <= datetime.date(2022, 5, 20))))))
            positives5 = len(db.Test.select().where(((db.Test.resultat == 2) & ((
                        datetime.date(2022, 5, 21) <= db.Test.date_test <= datetime.date(2022, 5, 25))))))
            positives6 = len(db.Test.select().where(((db.Test.resultat == 2) & ((
                        datetime.date(2022, 5, 26) <= db.Test.date_test <= datetime.date(2022, 5, 31))))))

            negatives1 = len(db.Test.select().where(((db.Test.resultat == 1) & ((
                    datetime.date(2022, 5, 1) <= db.Test.date_test <= datetime.date(2022, 5, 5))))))
            negatives2 = len(db.Test.select().where(((db.Test.resultat == 1) & ((
                    datetime.date(2022, 5, 6) <= db.Test.date_test <= datetime.date(2022, 5, 10))))))
            negatives3 = len(db.Test.select().where(((db.Test.resultat == 1) & ((
                    datetime.date(2022, 5, 11) <= db.Test.date_test <= datetime.date(2022, 5, 15))))))
            negatives4 = len(db.Test.select().where(((db.Test.resultat == 1) & ((
                    datetime.date(2022, 5, 16) <= db.Test.date_test <= datetime.date(2022, 5,  20))))))
            negatives5 = len(db.Test.select().where(((db.Test.resultat == 1) & ((
                    datetime.date(2022, 5, 21) <= db.Test.date_test <= datetime.date(2022, 5,  25))))))
            negatives6 = len(db.Test.select().where(((db.Test.resultat == 1) & ((
                    datetime.date(2022, 5, 26) <= db.Test.date_test <= datetime.date(2022, 5, 31))))))
            # create barseries
            set0 = QBarSet("Positive")
            set1 = QBarSet("Negative")
            # insert data to the barseries
            set0 << (positives1) << (positives2 - positives1) << (positives3 - positives2) << (positives4 - positives3) << (positives5 - positives4) << (positives6 - positives5)
            set1 << (negatives1) << (negatives2 - negatives1) << (negatives3 - negatives2) << (negatives4 - negatives3) << (negatives5 - negatives4) << (negatives6 - negatives5)
            # we want to create percent bar series
            series = QPercentBarSeries()
            series.append(set0)
            series.append(set1)
            # create chart and add the series in the chart
            chart = QChart()
            chart.addSeries(series)
            month = datetime.date.today().month
            if month == 1:
                chart.setTitle(self.month_str(12) + " Statistics")
            else:
                chart.setTitle(self.month_str(month-1)+" Statistics")
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chart.setTheme(QChart.ChartThemeDark)
            # create axis for the chart
            categories = ["01-05", "06-10", "11-15", "16-20", "21-25", "25-31"]
            axis = QBarCategoryAxis()
            axis.append(categories)
            chart.createDefaultAxes()
            chart.setAxisX(axis, series)
            # create chartview and add the chart in the chartview
            chartview = QChartView(chart)
            vbox = QVBoxLayout()
            vbox.addWidget(chartview)
            self.testsFrame.setLayout(vbox)
        elif option == 2:
            negatives = self.tests - self.positives
            pp = int(self.positives / self.tests * 100)
            np = int(negatives / self.tests * 100)
            series = QPieSeries()
            series.setHoleSize(0.40)
            series.append("Negative "+str(np)+"%", np)
            my_slice = series.append("Positive "+str(pp)+"%", pp)
            my_slice.setExploded(True)
            my_slice.setLabelVisible(True)
            chart = QChart()
            chart.addSeries(series)
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chart.setTitle("Tests")
            chart.setTheme(QChart.ChartThemeBlueCerulean)
            chartview = QChartView(chart)
            vbox = QVBoxLayout()
            vbox.addWidget(chartview)
            self.positivesFrame.setLayout(vbox)
        elif option == 3:
            non_actives = self.positives - self.actives
            act = int(self.actives / self.positives * 100)
            n_act = int(non_actives / self.positives * 100)
            series = QPieSeries()
            series.setHoleSize(0.40)
            series.append("Inactive " + str(n_act) + "%", n_act)
            my_slice = series.append("Active " + str(act) + "%", act)
            my_slice.setExploded(True)
            my_slice.setLabelVisible(True)
            chart = QChart()
            chart.addSeries(series)
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chart.setTitle("Positive cases")
            chart.setTheme(QChart.ChartThemeBlueCerulean)
            chartview = QChartView(chart)
            vbox = QVBoxLayout()
            vbox.addWidget(chartview)
            self.activesFrame.setLayout(vbox)
        elif option == 4:
            non_actives = self.positives - self.actives
            act = int(self.actives / self.tests * 100)
            n_act = int(non_actives / self.tests * 100)
            rec = int(self.recovered / self.tests * 100)
            dea = int(self.deaths / self.tests * 100)
            # create pieseries
            series = QPieSeries()
            # append some data to the series
            series.append("Inactive", n_act)
            series.append("Active", act)
            series.append("Recovered", rec)
            series.append("Deaths", dea)
            # slice
            my_slice = series.slices()[2]
            my_slice.setExploded(True)
            my_slice.setLabelVisible(True)
            my_slice.setPen(QPen(Qt.green, 4))
            my_slice.setBrush(Qt.green)
            # create QChart object
            chart = QChart()
            chart.addSeries(series)
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chart.setTitle("Recovered")
            chart.setTheme(QChart.ChartThemeDark)
            # create QChartView object and add chart in thier
            chartview = QChartView(chart)
            vbox = QVBoxLayout()
            vbox.addWidget(chartview)
            self.recoveredFrame.setLayout(vbox)
        elif option == 5:
            non_actives = self.positives - self.actives
            act = int(self.actives / self.tests * 100)
            n_act = int(non_actives / self.tests * 100)
            rec = int(self.recovered / self.tests * 100)
            dea = int(self.deaths / self.tests * 100)
            # create pieseries
            series = QPieSeries()
            # append some data to the series
            series.append("Inactive", n_act)
            series.append("Active", act)
            series.append("Recovered", rec)
            series.append("Deaths", dea)
            # slice
            my_slice = series.slices()[3]
            my_slice.setExploded(True)
            my_slice.setLabelVisible(True)
            my_slice.setPen(QPen(Qt.green, 4))
            my_slice.setBrush(Qt.green)
            # create QChart object
            chart = QChart()
            chart.addSeries(series)
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chart.setTitle("Deaths")
            chart.setTheme(QChart.ChartThemeDark)
            # create QChartView object and add chart in thier
            chartview = QChartView(chart)
            vbox = QVBoxLayout()
            vbox.addWidget(chartview)
            self.deathFrame.setLayout(vbox)
        elif option == 6:
            vac = self.doses
            n_vac = self.tests - vac
            pvac = int(vac / self.tests * 100)
            p_nvac = int(n_vac / self.tests * 100)
            series = QPieSeries()
            series.setHoleSize(0.40)
            series.append("Not vaccinated " + str(p_nvac) + "%", p_nvac)
            my_slice = series.append("Vaccinated " + str(pvac) + "%", pvac)
            my_slice.setExploded(True)
            my_slice.setLabelVisible(True)
            chart = QChart()
            chart.addSeries(series)
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chart.setTitle("Vaccination")
            chart.setTheme(QChart.ChartThemeBlueCerulean)
            chartview = QChartView(chart)
            vbox = QVBoxLayout()
            vbox.addWidget(chartview)
            self.dosesFrame.setLayout(vbox)
        else:
            pass

#########################################################################################
