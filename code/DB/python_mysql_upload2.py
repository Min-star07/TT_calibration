import pandas as pd
import pymysql as ms

# Establish connection parameters
host = "localhost"
user = "root"
password = "@Min08240707"
database = "TT_installation"  # Make sure this database exists


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
def insert_data(data):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            insert_query = """
            INSERT INTO tt_elec_calibration (
                FEB_ID, cat_ID, data_UID, CH, a0, a00_err, a1, a1_err, a2, a3, a4, a5, a5_err, b, ChiSq, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            for i in range(len(data)):
                row = data.iloc[i]
                cursor.execute(insert_query, tuple(row))
        connection.commit()
        print(f"Inserted {len(data)} rows into the table.")
    except Exception as e:
        print(f"An error occurred during data insertion: {e}")
    finally:
        connection.close()


# Function to read CSV and upload data
def upload_csv_to_database(csv_file_path):
    # Read the CSV file into a DataFrame
    data = pd.read_csv(csv_file_path)
    print("Data read from CSV:")
    print(data.head())  # Print the first few rows for verification
    insert_data(data)


# Function to insert values into the cb_LIST table
def insert_list_values(start, end):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            insert_query = "INSERT INTO WALL_list (WALL) VALUES (%s)"
            for cb_id in range(start, end + 1):
                cursor.execute(insert_query, (cb_id,))
        connection.commit()
        print(f"Inserted values from {start} to {end} into the cb_LIST table.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()


# Function to insert data into the customers table and retrieve the ID
def insert_customer(id, col):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            insert_query = "INSERT INTO mode_list (id, mode) VALUES (%s, %s)"
            cursor.execute(insert_query, (id, col))
            connection.commit()
    except Exception as e:
        print(f"An error occurred while inserting customer: {e}")
    finally:
        connection.close()


# Example usage
if __name__ == "__main__":
    # csv_file_path = "tt_elec_calibration.csv"  # Replace with your CSV file path
    # upload_csv_to_database(csv_file_path)

    # insert_list_values(1, 100)
    customer_id = insert_customer(1, "FADC")
    customer_id = insert_customer(2, "WADC")
