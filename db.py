import datetime
import email
import random
from unittest import result

from peewee import *

db = MySQLDatabase('pfe', user='root', password='', host='localhost', port=3306)


class BaseModel(Model):
    class Meta:
        database = db

    only_save_dirty = True


def generate_date(start_date=datetime.date(1900, 1, 1), end_date=datetime.date(2022, 6, 1)):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date


VACCINATION = (
    (1, 'NON'),
    (2, 'OUI')
)

ETAT_COVID = (
    (1, 'POSITIF'),
    (2, 'ACTIF'),
    (3, 'RETABLI'),
    (4, 'MORT')
)

RESULTAT_TEST = (
    (1, 'NEGACTIF'),
    (2, 'POSITIF')
)

ROLE_UTILISATEUR = (
    (1, 'ADMIN'),
    (2, 'MEDECIN'),
    (3, 'PATIENT'),
    (4, 'ANALYSTE'),
    (5, 'CHERCHEUR')
)

GENRE = (
    (1, 'MALE'),
    (2, 'FEMELE')
)

NIVEAU_CONFIDENTIALITE = (
    (0, 'TRES BAS'),
    (1, 'BAS'),
    (2, 'MOYEN'),
    (3, 'FORT'),
    (4, 'TRES FORT')
)


class DossierCovid(BaseModel):
    vaccination = CharField(choices=VACCINATION)
    etat = CharField(choices=ETAT_COVID)


class Vaccin(BaseModel):
    id_dossier_covid = ForeignKeyField(DossierCovid, backref='dossier_covid')
    date_vaccin = DateField()


class Test(BaseModel):
    id_dossier_covid = ForeignKeyField(DossierCovid, backref='dossier_covid')
    date_test = DateField()
    resultat = CharField(choices=RESULTAT_TEST)


class Statistique(BaseModel):
    date_statistique = DateField()
    nbre_test_covid = IntegerField()
    nbre_positif_covid = IntegerField()
    nbre_actif_covid = IntegerField()
    nbre_retablis_covid = IntegerField()
    nbre_nv_morts_covid = IntegerField()
    nbre_doses_covid = IntegerField()


class Confidentialite(BaseModel):
    niveau = CharField(choices=NIVEAU_CONFIDENTIALITE)


class Utilisateur(BaseModel):
    nom_utilisateur = CharField(unique=True)
    mot_de_passe = CharField()
    date_inscription = DateField()
    role = CharField(choices=ROLE_UTILISATEUR)


class Admin(BaseModel):
    nom = CharField()
    prenom = CharField()
    email = CharField()
    id_utilisateur = ForeignKeyField(Utilisateur, backref='utilisateur')


class Patient(BaseModel):
    nom = CharField()
    prenom = CharField()
    adresse = CharField()
    email = CharField()
    date_naissance = DateField()
    genre = CharField(choices=GENRE)
    dossier_covid = ForeignKeyField(DossierCovid, backref='dossier_covid')
    id_utilisateur = ForeignKeyField(Utilisateur, backref='utilisateur')


class Medecin(BaseModel):
    nom = CharField()
    prenom = CharField()
    email = CharField()
    id_utilisateur = ForeignKeyField(Utilisateur, backref='utilisateur')


class Analyste(BaseModel):
    nom = CharField()
    prenom = CharField()
    email = CharField()
    id_utilisateur = ForeignKeyField(Utilisateur, backref='utilisateur')


class Chercheur(BaseModel):
    nom = CharField()
    prenom = CharField()
    email = CharField()
    id_utilisateur = ForeignKeyField(Utilisateur, backref='utilisateur')


db.connect()
# db.create_tables([DossierCovid, Vaccin, Test, Statistique, Utilisateur, Admin, Patient, Medecin, Analyste, Chercheur])
# db.create_tables([Statistique])

# UTILISATEUR ADMIN
# db.Utilisateur.create(nom_utilisateur = 'admin1',mot_de_passe = 'admin1',date_inscription = datetime.datetime.now ,role = 1)
# db.Utilisateur.create(nom_utilisateur = 'admin2',mot_de_passe = 'admin2',date_inscription = datetime.datetime.now ,role = 1)
# db.Utilisateur.create(nom_utilisateur = 'admin3',mot_de_passe = 'admin3',date_inscription = datetime.datetime.now ,role = 1)

# UTILISATEUR MEDECIN
# m_id = 1
# while m_id < 11:
#     username = 'm'+str(m_id)
#     Utilisateur.create(nom_utilisateur=username, mot_de_passe=username, date_inscription=datetime.date.today(), role=2)
#     m_id += 1

# UTILISATEUR PATIENT
# p_id = 1
# while p_id < 1001:
#     username = 'p'+str(p_id)
#     Utilisateur.create(nom_utilisateur=username, mot_de_passe=username, date_inscription=datetime.date.today(), role=3)
#     p_id += 1

# UTILISATEUR ANALYSTE
# a_id = 1
# while a_id < 11:
#     username = 'a'+str(a_id)
#     Utilisateur.create(nom_utilisateur=username, mot_de_passe=username, date_inscription=datetime.date.today(), role=A)
#     a_id += 1

# UTILISATEUR CHERCHEUR
# c_id = 1
# while c_id < 11:
#     username = 'c'+str(c_id)
#     Utilisateur.create(nom_utilisateur=username, mot_de_passe=username, date_inscription=datetime.date.today(), role=A)
#     c_id += 1

# ADMIN
# db.Admin.create(nom = 'admin1',prenom = 'admin1',email = 'admin1@admin1.com',id_utilisateur = 1)
# db.Admin.create(nom = 'admin2',prenom = 'admin2',email = 'admin2@admin2.com',id_utilisateur = 2)
# db.Admin.create(nom = 'admin3',prenom = 'admin3',email = 'admin3@admin3.com',id_utilisateur = 3)

# MEDECIN
# db.Medecin.create(nom = 'medecin1',prenom = 'medecin1',email = 'medecin1@medecin1.com',id_utilisateur = 4)
# db.Medecin.create(nom = 'medecin2',prenom = 'medecin2',email = 'medecin2@medecin2.com',id_utilisateur = 5)
# db.Medecin.create(nom = 'medecin3',prenom = 'medecin3',email = 'medecin3@medecin3.com',id_utilisateur = 6)
# db.Medecin.create(nom = 'medecin4',prenom = 'medecin4',email = 'medecin4@medecin4.com',id_utilisateur = 7)
# db.Medecin.create(nom = 'medecin5',prenom = 'medecin5',email = 'medecin5@medecin5.com',id_utilisateur = 8)
# db.Medecin.create(nom = 'medecin6',prenom = 'medecin6',email = 'medecin6@medecin6.com',id_utilisateur = 9)
# db.Medecin.create(nom = 'medecin7',prenom = 'medecin7',email = 'medecin7@medecin7.com',id_utilisateur = 10)
# db.Medecin.create(nom = 'medecin8',prenom = 'medecin8',email = 'medecin8@medecin8.com',id_utilisateur = 11)
# db.Medecin.create(nom = 'medecin9',prenom = 'medecin9',email = 'medecin9@medecin9.com',id_utilisateur = 12)
# db.Medecin.create(nom = 'medecin10',prenom = 'medecin10',email = 'medecin10@medecin10.com',id_utilisateur = 13)

# DOSSIER COVID
# x = 1
# while x < 1001:
#     vac = random.randrange(1, 3, 1)
#     eta = random.randrange(1, 5, 1)
#     #date = generate_date(datetime.date(2022, 5, 1), datetime.date(2022, 6, 10))
#     DossierCovid.create(vaccination=vac, etat=eta)
#     x += 1

# PATIENT
# p_id = 1
# u_id = 44
# c_id = 1
# while p_id < 1001:
#     username = 'patient'+str(p_id)
#     pemail = username+'@'+username+'.com'
#     pdate = generate_date(datetime.date(1930, 1, 1), datetime.date(2000, 6, 1))
#     gnr = random.randrange(1, 3, 1)
#     Patient.create(nom = username,prenom = username,adresse = 'algérie',email = pemail,date_naissance = pdate, genre = gnr, dossier_covid = c_id, id_utilisateur = u_id)
#     p_id += 1
#     c_id += 1
#     u_id += 1

# ANALYSTE
# Analyste.create(nom = 'analyste1',prenom = 'analyste1',email = 'analyste1@analyste1.com',id_utilisateur = 54)
# Analyste.create(nom = 'analyste2',prenom = 'analyste2',email = 'analyste2@analyste2.com',id_utilisateur = 55)
# Analyste.create(nom = 'analyste3',prenom = 'analyste3',email = 'analyste3@analyste3.com',id_utilisateur = 56)
# Analyste.create(nom = 'analyste4',prenom = 'analyste4',email = 'analyste4@analyste4.com',id_utilisateur = 57)
# Analyste.create(nom = 'analyste5',prenom = 'analyste5',email = 'analyste5@analyste5.com',id_utilisateur = 58)
# Analyste.create(nom = 'analyste6',prenom = 'analyste6',email = 'analyste6@analyste6.com',id_utilisateur = 59)
# Analyste.create(nom = 'analyste7',prenom = 'analyste7',email = 'analyste7@analyste7.com',id_utilisateur = 60)
# Analyste.create(nom = 'analyste8',prenom = 'analyste8',email = 'analyste8@analyste8.com',id_utilisateur = 61)
# Analyste.create(nom = 'analyste9',prenom = 'analyste9',email = 'analyste9@analyste9.com',id_utilisateur = 62)
# Analyste.create(nom = 'analyste10',prenom = 'analyste10',email = 'analyste10@analyste10.com',id_utilisateur = 63)

# CHERCHEUR
# Chercheur.create(nom = 'chercheur1',prenom = 'chercheur1',email = 'chercheur1@chercheur1.com',id_utilisateur = 64)
# Chercheur.create(nom = 'chercheur2',prenom = 'chercheur2',email = 'chercheur2@chercheur2.com',id_utilisateur = 65)
# Chercheur.create(nom = 'chercheur3',prenom = 'chercheur3',email = 'chercheur3@chercheur3.com',id_utilisateur = 66)
# Chercheur.create(nom = 'chercheur4',prenom = 'chercheur4',email = 'chercheur4@chercheur4.com',id_utilisateur = 67)
# Chercheur.create(nom = 'chercheur5',prenom = 'chercheur5',email = 'chercheur5@chercheur5.com',id_utilisateur = 68)
# Chercheur.create(nom = 'chercheur6',prenom = 'chercheur6',email = 'chercheur6@chercheur6.com',id_utilisateur = 69)
# Chercheur.create(nom = 'chercheur7',prenom = 'chercheur7',email = 'chercheur7@chercheur7.com',id_utilisateur = 70)
# Chercheur.create(nom = 'chercheur8',prenom = 'chercheur8',email = 'chercheur8@chercheur8.com',id_utilisateur = 71)
# Chercheur.create(nom = 'chercheur9',prenom = 'chercheur9',email = 'chercheur9@chercheur9.com',id_utilisateur = 72)
# Chercheur.create(nom = 'chercheur10',prenom = 'chercheur10',email = 'chercheur10@chercheur10.com',id_utilisateur = 73)

# VACCIN
# rows = DossierCovid.select().where(DossierCovid.vaccination == '2').tuples()
# for row in rows:
#     c_id = int(row[0])
#     Vaccin.create(id_dossier_covid = c_id,date_vaccin = generate_date(datetime.date(2022, 5, 1), datetime.date(2022, 6, 1)))

# TEST
# c_id = 1
# while c_id < 1001:
#     tdate = generate_date(datetime.date(2022, 5, 1), datetime.date(2022, 6, 1))
#     res = random.randrange(1, 3, 1)
#     Test.create(id_dossier_covid = c_id,date_test = tdate, resultat = res)
#     c_id += 1

# db.Statistique.create(nom = 'medecin1',prenom = 'medecin1',email = 'medecin1@medecin1.com',id_utilisateur = 4)
db.close()
