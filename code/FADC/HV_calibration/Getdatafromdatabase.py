import pymysql as ms
import uproot
import pandas as pd
from datetime import datetime
import math
import argparse


class DatabaseConnector:
    def __init__(
        self, host="localhost", user="root", password="@Min08240707", database="test"
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        self.connection = ms.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset="utf8mb4",
            cursorclass=ms.cursors.DictCursor,
        )

    def fetch_data(self, FEB, CH):
        try:
            print(FEB)
            print(CH)
            with self.connection.cursor() as cursor:
                sql_query = (
                    "SELECT * FROM web_tt_calibration WHERE FEB_ID = %s and CH = %s"
                )

                cursor.execute(sql_query, (FEB, CH))
                print(sql_query)
                rows = cursor.fetchall()
                print(rows)
                df = pd.DataFrame(rows)
                df.to_csv("tt_calibration.csv", sep="\t", index=False)
                return df
        finally:
            self.connection.close()


class DataAnalyzer:
    @staticmethod
    def get_max_Q1(filepath):

        df = pd.read_csv(filepath, sep="\t")
        print(df)
        return df["Q_{1}"].max()

    @staticmethod
    def ADC_to_charge(Q1, a1):
        return Q1 / a1

    @staticmethod
    def calculate_gain(Q1, a1):
        charge = Q1 / a1
        gain = charge * 1e-12 / (1.602e-19)
        return gain

    @staticmethod
    def Get_Calibration_result(args):
        infile = args.outfilepath + "/" + args.outfile
        df = pd.read_csv(infile, sep="\t", header=None)
        print(df)
        db_connector = DatabaseConnector()
        db_connector.connect()
        Q1_max_index = args.max_channel
        data = db_connector.fetch_data(args.FEB, Q1_max_index)
        a1 = data.loc[0, "a1"]
        print(a1)
        df_select = df[[0, 7, 8]]
        df_select["a1"] = a1
        print(df_select)
        Q = 0.1602 * a1  # ADC @GAIN 1E6
        df_select["Q"] = Q
        for i, item in enumerate(df[0]):
            charge = df.iloc[i, 7] / a1
            # print(charge * (1e-12))
            gain = charge * (1e-12) / (1.602 * 1e-19)
            print(gain)
            outfile = (
                args.outfilepath
                + "/CB"
                + str(args.CB)
                + "_WALL"
                + str(args.WALL)
                + "_ROB"
                + str(args.ROB)
                + "_gain_calibration_result.txt"
            )
        df_select.to_csv(outfile, sep="\t", header=None, index=False)

    @staticmethod
    def Gain_result_a1(args):

        a1_result = []

        for i in range(64):
            db_connector = DatabaseConnector()
            db_connector.connect()
            data = db_connector.fetch_data(args.FEB, i)
            a1 = data.loc[0, "a1"]
            print(a1)

            a1_result.append(a1)
        print(a1_result)
        outfile = (
            args.outfilepath
            + "/WALL"
            + str(args.WALL)
            + "_CB"
            + str(args.CB)
            + "_ROB"
            + str(args.ROB)
            + "_a1_calibration_result.txt"
        )

        data = pd.DataFrame(a1_result, columns=["a1"])
        data["channel"] = range(64)
        data.to_csv(outfile, sep="\t", header=None, index=False)

    import pandas as pd

    def mergetxt(args):
        dict_sum = {}
        HV_delta = [-20, -15, -10, -5, 0, 5]
        for i in range(1, 6, 1):
            filepath = args.outfilepath + "/HV" + str(i)
            filename = (
                "CB"
                + str(args.CB)
                + "_WALL"
                + str(args.WALL)
                + "_ROB"
                + str(args.ROB)
                + "_WADC_Final_result.txt"
            )
            df = pd.read_csv(filepath + "/" + filename, header=None, sep="\t")
            # print(df)
            data = df[df[0] == args.max_channel]
            data = data.iloc[0].to_dict()
            # df = pd.DataFrame([data])
            # print(df)

            HV_calibrtion = args.HV + HV_delta[i]
            dict_sum[HV_calibrtion] = data
            #
        # print(dict_sum)
        df = pd.DataFrame(dict_sum)
        outfile = args.outfilepath + "/" + str(args.outfile)
        df.T.to_csv(outfile, sep="\t", header=None)
