#########################################################################################
#########################################################################################
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import datetime
import pymysql
import db
#########################################################################################
#########################################################################################
import login

MainAdminUI, _ = loadUiType('assets/ui/admin.ui')


#########################################################################################
class MainAdmin(QMainWindow, MainAdminUI):
    def __init__(self, parent=None):
        super(MainAdmin, self).__init__(parent)
        QMainWindow.__init__(self)
        self.completer = None
        self.users_ids = None
        self.users_names = None
        self.setupUi(self)
        self.userid = None
        self.id = None
        #########################################
        self.Db_Connect()
        self.UI_Changes()
        self.Open_Home()
        self.Handle_Buttons()
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

    #########################################
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #########################################
    def UI_Changes(self):
        self.mainTabWidget.tabBar().setVisible(False)
        self.usersListTab.tabBar().setVisible(False)

        self.users_names = []
        self.users_ids = {}
        users = self.Get_Users()
        for u in users:
            username = u[1]
            self.users_names.append(username)
            self.users_ids[username] = u[0]

        self.completer = QCompleter(self.users_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)

    #########################################
    def Db_Connect(self):
        self.db = pymysql.connect(host='localhost', user='root', password='', db='pfe')
        self.cur = self.db.cursor()

    #########################################
    def Get_Privacy(self):
        query1 = db.Confidentialite.select().order_by(db.Confidentialite.id.desc()).get()
        query2 = db.Confidentialite.select().where(db.Confidentialite.id == query1).get()
        return query2.niveau

    #########################################
    def Get_Users(self):
        query = db.Utilisateur.select().where(db.Utilisateur.role != 1).order_by(db.Utilisateur.role).tuples()
        return query

    #########################################
    def Get_Patients(self):
        query = db.Utilisateur.select().where(db.Utilisateur.role == 3).order_by(db.Utilisateur.id).tuples()
        return query

    #########################################
    def Get_Doctors(self):
        query = db.Utilisateur.select().where(db.Utilisateur.role == 2).order_by(db.Utilisateur.id).tuples()
        return query

    #########################################
    def Get_Analysts(self):
        query = db.Utilisateur.select().where(db.Utilisateur.role == 4).order_by(db.Utilisateur.id).tuples()
        return query

    #########################################
    def Get_Searchers(self):
        query = db.Utilisateur.select().where(db.Utilisateur.role == 5).order_by(db.Utilisateur.id).tuples()
        return query

    #########################################
    def Get_One_User(self, userid=None):
        query = db.Utilisateur.select().where(db.Utilisateur.id == userid).get()
        return query

    #########################################
    def Get_One_Patient(self, userid=None):
        query = db.Patient.select().where(db.Patient.id_utilisateur == userid).get()
        return query

    #########################################
    def Get_One_Doctor(self, userid=None):
        query = db.Medecin.select().where(db.Medecin.id_utilisateur == userid).get()
        return query

    #########################################
    def Get_One_Analyst(self, userid=None):
        query = db.Analyste.select().where(db.Analyste.id_utilisateur == userid).get()
        return query

    #########################################
    def Get_One_Searcher(self, userid=None):
        query = db.Chercheur.select().where(db.Chercheur.id_utilisateur == userid).get()
        return query

    #########################################
    def Handle_Buttons(self):
        ## Main Tab Buttons
        self.homeBtn.clicked.connect(self.Open_Home)
        self.usersBtn.clicked.connect(self.Open_Users_Tab)
        self.privacyBtn.clicked.connect(self.Open_Privacy)
        self.accountLeftBtn.clicked.connect(self.Open_Account)
        self.logoutBtn.clicked.connect(self.Open_Logout)
        self.accountBtn.clicked.connect(self.Open_Account)
        self.usersListTab.blockSignals(True)
        self.usersListTab.currentChanged.connect(self.Open_Users_Tab)
        #########################################
        ## Home Buttons
        self.homePatientsBtn.clicked.connect(self.Open_Patients)
        self.homeDoctorsBtn.clicked.connect(self.Open_Doctors)
        self.homeAnalystsBtn.clicked.connect(self.Open_Analysts)
        self.homeSearchersBtn.clicked.connect(self.Open_Searchers)
        ## Logout Tab Buttons
        self.logoutBtnNo.clicked.connect(self.Open_Home)
        self.logoutBtnYes.clicked.connect(self.Handle_logout)
        ## Add User Buttons
        self.saveAddUserBtn.clicked.connect(self.Open_SaveUser)
        self.saveEditUserBtn.clicked.connect(self.Open_SaveUser)
        self.savePrivacyBtn.clicked.connect(self.Open_SavePrivacy)
        self.privacySlider.valueChanged.connect(self.Set_Privacy_Label)
        self.infoContentSaveBtn.clicked.connect(self.Update_Me)

        self.addUserBtn.clicked.connect(self.Open_Add)
        self.editUserBtn.clicked.connect(self.Open_Edit)
        self.deleteUserBtn.clicked.connect(self.Open_Delete)

        self.searchbtn.clicked.connect(self.Open_Search)

        self.minus_btn.clicked.connect(lambda: self.Open_Privacy_Minus_Plus_Btn(0))
        self.plus_btn.clicked.connect(lambda: self.Open_Privacy_Minus_Plus_Btn(1))

    #########################################
    def Handle_logout(self):
        self.close()
        self.window = login.Login()
        self.window.center()
        self.window.show()

    #########################################
    def Open_Home(self):
        self.mainTabWidget.setCurrentIndex(0)
        medecins = len(db.Utilisateur.select().where(db.Utilisateur.role == 2).order_by(db.Utilisateur.id).tuples())
        patients = len(db.Utilisateur.select().where(db.Utilisateur.role == 3).order_by(db.Utilisateur.id).tuples())
        analystes = len(db.Utilisateur.select().where(db.Utilisateur.role == 4).order_by(db.Utilisateur.id).tuples())
        chercheur = len(db.Utilisateur.select().where(db.Utilisateur.role == 5).order_by(db.Utilisateur.id).tuples())

        self.homeDoctorsLbl.setText(str(medecins))
        self.homePatientsLbl.setText(str(patients))
        self.homeAnalystsLbl.setText(str(analystes))
        self.homeSearchersLbl.setText(str(chercheur))

    #########################################
    def Open_Documents(self):
        self.mainTabWidget.setCurrentIndex(2)

    #########################################
    def Open_Privacy(self):
        self.mainTabWidget.setCurrentIndex(3)
        self.privacy = self.Get_Privacy()
        value = 0
        if self.privacy == '0':
            value = 0
        elif self.privacy == '1':
            value = 25
        elif self.privacy == '2':
            value = 50
        elif self.privacy == '3':
            value = 75
        else:
            value = 100
        self.privacySlider.setValue(value)
        self.Set_Privacy_Label(value)

    #########################################
    def Open_Privacy_Minus_Plus_Btn(self, option=0):
        value = self.privacySlider.value()
        if option == 0:
            if (value - 25) >= 0:
                self.privacySlider.setValue(value - 25)
                self.Set_Privacy_Label(value - 25)
            else:
                self.privacySlider.setValue(0)
                self.Set_Privacy_Label(0)
        else:
            if (value + 25) <= 100:
                self.privacySlider.setValue(value + 25)
                self.Set_Privacy_Label(value + 25)
            else:
                self.privacySlider.setValue(100)
                self.Set_Privacy_Label(100)

    #########################################
    def Open_Account(self):
        self.mainTabWidget.setCurrentIndex(4)

    #########################################
    def Update_Me(self):
        print(self.userid)
        username = self.username_2.text()
        password = self.password.text()
        res = (db.Utilisateur
               .update({db.Utilisateur.mot_de_passe: password})
               .where(id == self.userid)
               .execute())
        if res:
            self.Handle_logout()
        else:
            self.Open_Home()

    #########################################
    def Open_Logout(self):
        self.mainTabWidget.setCurrentIndex(5)

    #########################################
    def Open_Edit(self, ids=None):
        if ids is None:
            ids = []
        currentRow = self.tableWidget.currentRow()
        if currentRow != -1:
            self.mainTabWidget.setCurrentIndex(1)
            self.usersListTab.setCurrentIndex(1)

            userid = ids[currentRow]
            user = self.Get_One_User(userid)

            self.username.setText(user.nom_utilisateur)
        else:
            self.Open_Users_Tab()

    #########################################
    def Open_Edit_Search(self, ids=None):
        if ids is None:
            ids = []
        currentRow = self.tableWidget.currentRow()
        if currentRow != -1:
            self.mainTabWidget.setCurrentIndex(1)
            self.usersListTab.setCurrentIndex(1)

            userid = ids[currentRow]
            user = self.Get_One_User(int(userid))
            self.username.setText(user.nom_utilisateur)
        else:
            self.Open_Users_Tab()

    #########################################
    def Open_Add(self, option=0):
        self.mainTabWidget.setCurrentIndex(1)
        self.usersListTab.setCurrentIndex(2)

    #########################################
    def Open_SaveUser(self):
        username = self.newUserUsername.text()
        password = self.newUserPassword.text()
        role = self.newUserRole.currentIndex() + 1
        if 1 <= role <= 5:
            db.Utilisateur.create(nom_utilisateur=username, mot_de_passe=password, date_inscription=datetime.datetime.now,
                              role=role)
            last_user = db.Utilisateur.select().order_by(db.Utilisateur.id.desc()).get()
            userid = last_user.id
            if role == 1:
                db.Admin.create(id_utilisateur=userid)
            elif role == 2:
                db.Medecin.create(id_utilisateur=userid)
            elif role == 3:
                db.DossierCovid.create(vaccination=1, etat=1)
                covid = db.DossierCovid.select().order_by(db.DossierCovid.id.desc()).get()
                c_id = covid.id
                db.Patient.create(dossier_covid=c_id, id_utilisateur=userid)
            elif role == 4:
                db.Analyste.create(id_utilisateur=userid)
            else:
                db.Chercheur.create(id_utilisateur=userid)
        self.Open_Home()

    #########################################
    def Open_Delete(self, userid=None):
        self.mainTabWidget.setCurrentIndex(1)
        self.usersListTab.setCurrentIndex(3)

    #########################################
    def Open_Delete_Search(self, userid=None):
        self.mainTabWidget.setCurrentIndex(1)
        self.usersListTab.setCurrentIndex(3)

    #########################################
    def Open_Search(self):
        self.mainTabWidget.setCurrentIndex(1)
        self.usersListTab.setCurrentIndex(0)
        self.Display_Search()

    #########################################
    def Open_Users_Tab(self):
        self.mainTabWidget.setCurrentIndex(1)
        self.usersListTab.setCurrentIndex(0)
        self.Create_Patients_Table(0)

    #########################################
    def Open_Patients(self):
        self.mainTabWidget.setCurrentIndex(1)
        self.usersListTab.setCurrentIndex(0)
        self.Create_Patients_Table(1)

    #########################################
    def Open_Doctors(self):
        self.mainTabWidget.setCurrentIndex(1)
        self.usersListTab.setCurrentIndex(0)
        self.Create_Patients_Table(2)

    #########################################
    def Open_Analysts(self):
        self.mainTabWidget.setCurrentIndex(1)
        self.usersListTab.setCurrentIndex(0)
        self.Create_Patients_Table(3)

    #########################################
    def Open_Searchers(self):
        self.mainTabWidget.setCurrentIndex(1)
        self.usersListTab.setCurrentIndex(0)
        self.Create_Patients_Table(4)

    #########################################
    def Open_SavePrivacy(self):
        value = self.privacySlider.value()
        niveau = 0
        if value == 0:
            niveau = 0
        elif 0 < value <= 25:
            niveau = 1
        elif 25 < value <= 50:
            niveau = 2
        elif 50 < value <= 75:
            niveau = 3
        else:
            niveau = 4
        db.Confidentialite.create(niveau=niveau)
        self.Open_Home()

    #########################################
    def Set_Privacy_Label(self, val):
        if val is None:
            val = self.privacySlider.value()
        epsilon = val / 100
        self.epsilon_lbl.setText('Epsilon = ' + str(epsilon))

    #########################################
    def Create_Patients_Table(self, option=0):
        rows = tuple()
        if option == 0:
            rows = self.Get_Users()
            self.usersLabel.setText('Liste des utilisateurs')
        elif option == 1:
            rows = self.Get_Patients()
            self.usersLabel.setText('Liste des patients')
        elif option == 2:
            rows = self.Get_Doctors()
            self.usersLabel.setText('Liste des médecins')
        elif option == 3:
            rows = self.Get_Analysts()
            self.usersLabel.setText('Liste des analystes')
        elif option == 4:
            rows = self.Get_Searchers()
            self.usersLabel.setText('Liste des chercheurs')
        else:
            self.Open_Home()

        self.tableWidget.setRowCount(len(rows))
        table = self.tableWidget
        line = 0
        ids = []
        for row in rows:
            userid = QTableWidgetItem(str(row[0]))

            username = QLabel(table)
            username.setText(row[1])

            nom = QLabel(table)
            prenom = QLabel(table)
            email = QLabel(table)
            role = QLabel(table)
            date = QLabel(table)
            date.setText(str(row[3]))

            user = None
            if row[4] == '2':
                user = self.Get_One_Doctor(row[0])
                role.setText('MÉDECIN')
            elif row[4] == '3':
                user = self.Get_One_Patient(row[0])
                role.setText('PATIENT')
            elif row[4] == '4':
                user = self.Get_One_Analyst(row[0])
                role.setText('ANALYSTE')
            elif row[4] == '5':
                user = self.Get_One_Searcher(row[0])
                role.setText('CHERCHEUR')

            nom.setText(user.nom)
            prenom.setText(user.prenom)
            email.setText(user.email)

            style = """
                       QPushButton{
                         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2596be, stop: 0.4 #2586be, stop: 0.5 #2576be, stop: 1.0 #2566be);
                         padding: 5px;
                         color: #eff9fe;
                         border-radius: 15px;
                       }

                       QPushButton:hover {
                         background-color: #2580be;
                       }
                   """

            table.setColumnWidth(0, 50)
            table.setColumnWidth(1, 100)
            table.setColumnWidth(2, 150)
            table.setColumnWidth(3, 150)
            table.setColumnWidth(4, 250)
            table.setColumnWidth(5, 150)
            table.setColumnWidth(6, 150)
            # table.setColumnWidth(7, 200)

            table.setItem(line, 0, userid)
            table.setCellWidget(line, 1, username)
            table.setCellWidget(line, 2, nom)
            table.setCellWidget(line, 3, prenom)
            table.setCellWidget(line, 4, email)
            table.setCellWidget(line, 5, date)
            table.setCellWidget(line, 6, role)
            # table.setCellWidget(line, 7, btnWidgets)

            userid.setTextAlignment(Qt.AlignCenter)
            username.setAlignment(Qt.AlignCenter)
            nom.setAlignment(Qt.AlignCenter)
            prenom.setAlignment(Qt.AlignCenter)
            email.setAlignment(Qt.AlignCenter)
            date.setAlignment(Qt.AlignCenter)
            role.setAlignment(Qt.AlignCenter)

            ids.insert(line + 1, row[0])

            line = line + 1

        self.editUserBtn.clicked.connect(lambda: self.Open_Edit(ids))
        self.deleteUserBtn.clicked.connect(lambda: self.Open_Delete(ids))

        table.horizontalHeader().setStretchLastSection(True)

    #########################################
    def Display_Search(self):

        search = self.searchbar.text()
        user_id = self.users_ids[search]

        user = self.Get_One_User(user_id)

        self.tableWidget.setRowCount(1)
        table = self.tableWidget

        userid = QTableWidgetItem(str(user_id))
        username = QLabel(table)
        username.setText(user.nom_utilisateur)

        nom = QLabel(table)
        prenom = QLabel(table)
        email = QLabel(table)
        role = QLabel(table)
        date = QLabel(table)
        date.setText(str(user.date_inscription))

        infos = None
        if user.role == '2':
            infos = self.Get_One_Doctor(user_id)
            role.setText('MÉDECIN')
        elif user.role == '3':
            infos = self.Get_One_Patient(user_id)
            role.setText('PATIENT')
        elif user.role == '4':
            infos = self.Get_One_Analyst(user_id)
            role.setText('ANALYSTE')
        elif user.role == '5':
            infos = self.Get_One_Searcher(user_id)
            role.setText('CHERCHEUR')

        nom.setText(infos.nom)
        prenom.setText(infos.prenom)
        email.setText(infos.email)

        style = """
                   QPushButton{
                     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2596be, stop: 0.4 #2586be, stop: 0.5 #2576be, stop: 1.0 #2566be);
                     padding: 5px;
                     color: #eff9fe;
                     border-radius: 15px;
                   }

                   QPushButton:hover {
                     background-color: #2580be;
                   }
               """

        table.setColumnWidth(0, 50)
        table.setColumnWidth(1, 100)
        table.setColumnWidth(2, 150)
        table.setColumnWidth(3, 150)
        table.setColumnWidth(4, 250)
        table.setColumnWidth(5, 150)
        table.setColumnWidth(6, 150)

        table.setItem(0, 0, userid)
        table.setCellWidget(0, 1, username)
        table.setCellWidget(0, 2, nom)
        table.setCellWidget(0, 3, prenom)
        table.setCellWidget(0, 4, email)
        table.setCellWidget(0, 5, date)
        table.setCellWidget(0, 6, role)

        userid.setTextAlignment(Qt.AlignCenter)
        username.setAlignment(Qt.AlignCenter)
        nom.setAlignment(Qt.AlignCenter)
        prenom.setAlignment(Qt.AlignCenter)
        email.setAlignment(Qt.AlignCenter)
        date.setAlignment(Qt.AlignCenter)
        role.setAlignment(Qt.AlignCenter)

        self.editUserBtn.clicked.connect(lambda: self.Open_Edit_Search(user_id))
        self.deleteUserBtn.clicked.connect(lambda: self.Open_Delete_Search())

        table.horizontalHeader().setStretchLastSection(True)

#########################################################################################
