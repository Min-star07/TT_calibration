import pymysql as ms
import pandas as pd
import argparse
from datetime import datetime

# Establish connection parameters
host = "localhost"
user = "root"
password = "@Min08240707"
database = "TT_installation"


# Create a function to establish a connection
def create_connection():
    return ms.connect(
        host=host,
        user=user,
        password=password,
        db=database,
        charset="utf8mb4",
        cursorclass=ms.cursors.DictCursor,
    )


# Function to insert data into the table
def insert_data(sql_query, data):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query, data)
        connection.commit()
    finally:
        connection.close()


# Function to execute a select query
def select_query(sql_query):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()
        return result
    finally:
        connection.close()


# Function to execute an update query
def update_query(sql_query):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
        connection.commit()
    finally:
        connection.close()


# Function to delete a database
def delete_database(database_name):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql_query = f"DROP DATABASE IF EXISTS {database_name}"
            cursor.execute(sql_query)
            print(f"Database '{database_name}' deleted successfully.")
        connection.commit()
    finally:
        connection.close()


def databaseupolad(args, infile, outfile):
    df = pd.read_csv(infile, sep="\t", header=None)
    print("Input DataFrame:")
    print(df)

    # Insert additional columns
    df.insert(0, "FEB", [args.FEB] * len(df))
    df.insert(0, "ROB", [args.ROB] * len(df))
    df.insert(0, "CB", [args.CB] * len(df))
    df.insert(0, "WALL", [args.WALL] * len(df))
    df.insert(len(df.columns), "mode", [args.mode] * len(df))
    df.insert(len(df.columns), "HV", [args.HV] * len(df))

    print("Modified DataFrame:")
    print(df)

    # Save the modified DataFrame to the output file
    df.to_csv(outfile, sep="\t", header=None, index=False)

    for i in range(len(df)):
        data = tuple(df.iloc[i, :])
        print(data)
        insert_query = """INSERT INTO cb22_calibration(WALL, CB, ROB, FEB, Channel, Chi2NDF, N0, Error_N0, Q0, Error_Q0, Q1, Error_Q1, Sigma0, Error_sigma0, Sigma1, Error_sigma1, w, Error_w, alpha, Error_alpha, mu, Error_mu, Chi2NDF_pedestal, Chi2NDF_peak, Max_Q1_channel,gain, mode, HV)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        insert_data(insert_query, data)


# Example usage
# if __name__ == "__main__":

# # Example: Insert data into table
# insert_query = """INSERT INTO cb22_calibration(WALL, CB, ROB, FEB, Channel, Chi2NDF, fitstatus, N0, Error_N0, Q0, Error_Q0, Q1, Error_Q1, Sigma0, Error_sigma0, Sigma1, Error_sigma1, w, Error_w, alpha, Error_alpha, mu, Error_mu, xmin, xmax, ped_entries, ped_mean, ped_sigma, log, gain, mode, type, HV)
#                   VALUES (%d, %d, %d, %d, %d, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

# df = pd.read_csv("./WALL1_CB22_ROB15_WADC_Final_result.txt", sep="\t", header=None)
# df = df.iloc[:, 1:]
# df = df.fillna(-1)

# for i in range(len(df)):
#     data = tuple(df.iloc[i, :])
#     insert_data(insert_query, data)

# # Example: Select data from table
# result = select_query("SELECT * FROM cb22_calibration LIMIT 10")
# print(result)

# # Example: Update a table
# update_query("UPDATE cb22_calibration SET gain = 'high' WHERE id = 1")

# Example: Delete a table
# delete_table("ROB_list")

# # Example: Rename a table
# rename_table("cb22_calibration", "calibration_results")
# db_name = "tt"  # Specify the database you want to delete
# delete_database(db_name)
