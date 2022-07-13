import datetime
import random
from datetime import date, timedelta

from IPython.display import clear_output
from pipeline_dp import combiners

clear_output()

import pipeline_dp
import pymysql
import pandas as pd

import db


# def Db_Connect(self):
#     self.db = pymysql.connect(host='localhost', user='root', password='', db='pfe')
#     self.cur = self.db.cursor()


# def daterange(start_date, end_date):
#     for n in range(int((end_date - start_date).days)):
#         yield start_date + timedelta(n)


# def Get_Patients(single_date=None):
#     if single_date is None:
#         query = ((db.Patient.select(db.Patient, db.DossierCovid, db.Test).join(
#             db.DossierCovid).order_by(
#             db.Patient.id.asc())).join(db.Test))
#     else:
#         query = ((db.Patient.select(db.Patient, db.DossierCovid, db.Test).where(db.Test.date_test == single_date).join(
#             db.DossierCovid).order_by(
#             db.Patient.id.asc())).join(db.Test))
#     return query


# #########################################
# def Get_One_Patients(id=0, single_date=datetime.date.today()):
#     query = ((db.Patient.select(db.Patient, db.DossierCovid, db.Test).where(
#         (db.Patient.id == id) & (db.Test.date_test == single_date)).join(
#         db.DossierCovid).order_by(db.Patient.id.asc())).join(db.Test)).tuples()
#     return query


# #########################################
# def Get_Positive_Cases(result='1', single_date=datetime.date.today()):
#     query = ((db.Patient.select(db.Patient, db.DossierCovid, db.Test).where(
#         (db.Test.resultat == result) & (db.Test.date_test == single_date)).join(
#         db.DossierCovid).order_by(db.Patient.id.asc())).join(db.Test)).tuples()
#     return query


# #########################################
# def Get_Active_Cases(etat='2', single_date=datetime.date.today()):
#     query = ((db.Patient.select(db.Patient, db.DossierCovid, db.Test).where((db.DossierCovid.etat == etat) & (db.Test.date_test == single_date)).join(
#         db.DossierCovid).order_by(db.Patient.id.asc())).join(db.Test)).tuples()
#     return query


# #########################################
# def Get_Doses(vaccination='2', single_date=datetime.date.today()):
#     query = ((db.Patient.select(db.Patient, db.DossierCovid, db.Test).where(
#         (db.DossierCovid.vaccination == vaccination) & (db.Test.date_test == single_date)).join(db.DossierCovid).order_by(db.Patient.id.asc())).join(
#         db.Test)).tuples()
#     return query


def main():
    # start_date = datetime.date(2022, 5, 1)
    # end_date = datetime.date(2022, 6, 1)
    # # daterange(start_date, end_date)
    # total = 0

    # tests, positives, actives, recovereds, deaths, doses = 0, 0, 0, 0, 0, 0

    #@markdown Load and inspect the data
    df = pd.read_csv('assets/db/covid.csv')
    rows = [index_row[1] for index_row in df.iterrows()]
    df.head()

    backend = pipeline_dp.LocalBackend()
    budget_accountant = pipeline_dp.NaiveBudgetAccountant(total_epsilon=0.25, total_delta=1e-6)
    dp_engine = pipeline_dp.DPEngine(budget_accountant, backend)
    data_extractors = pipeline_dp.DataExtractors(
        partition_extractor=lambda line: line.etat,
        privacy_id_extractor=lambda line: line.id,
        value_extractor=lambda line: line.id_test)
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

    for row in dp_result:
        nbre = int(str(row[1]).replace(")", "").split('=')[1].split('.')[0])
        print('( '+str(row[0])+', '+str(nbre)+' )')


    # for single_date in daterange(start_date, end_date):
    #     test = len(Get_Patients(single_date))
    #     positive = len(Get_Positive_Cases('2', single_date))
    #     active = len(Get_Active_Cases('2', single_date))
    #     recovered = len(Get_Active_Cases('3', single_date))
    #     death = len(Get_Active_Cases('4', single_date))
    #     dose = len(Get_Doses('2', single_date))

    #     tests += test
    #     positives += positive
    #     actives += active
    #     recovereds += recovered
    #     deaths += death
    #     doses += dose

    #     db.Statistique.create(date_statistique = single_date,
    #                           nbre_test_covid = test,
    #                           nbre_positif_covid = positive,
    #                           nbre_actif_covid = active,
    #                           nbre_retablis_covid = recovered,
    #                           nbre_nv_morts_covid = death,
    #                           nbre_doses_covid = dose)

    #     print(
    #         "Test => " + str(test) +
    #         " Positive => " + str(positive) +
    #         " Active => " + str(active) +
    #         " Recovered => " + str(recovered) +
    #         " Death => " + str(death) +
    #         " Doses => " + str(dose)
    #     )

    # print(
    #     "<< Test => " + str(tests) + " >> "
    #     "<< Positive => " + str(positives) + " >> "
    #     "<< Active => " + str(actives) + " >> "
    #     "<< Recovered => " + str(recovereds) + " >> "
    #     "<< Death => " + str(deaths) + " >> "
    #     "<< Doses => " + str(doses) + " >> "
    # )


#########################################################################################
#########################################################################################
if __name__ == '__main__':
    main()
#########################################################################################
#########################################################################################
