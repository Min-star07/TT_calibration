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


# Function to download data and save it into a CSV file
def download_data_to_csv(sql_query, output_file):
    data = select_query(sql_query)

    if data:  # Check if any data was returned
        # Convert the data to a Pandas DataFrame
        df = pd.DataFrame(data)
        # Save the DataFrame to a CSV file
        df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")
    else:
        print("No data found for the given query.")


# Example usage
if __name__ == "__main__":
    # SQL query to select data (modify this query as needed)
    sql_query = "SELECT * FROM cb22_calibration"  # Change to your actual table name

    # Output file path
    output_file = "output_data.csv"

    # Download data and save to CSV
    download_data_to_csv(sql_query, output_file)
