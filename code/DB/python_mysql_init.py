import pymysql as ms
import pandas as pd
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


# Function to create a new table
def create_table(sql_query):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
        connection.commit()
    finally:
        connection.close()


# Function to delete a table
def delete_table(table_name):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql_query = f"DROP TABLE IF EXISTS {table_name}"
            cursor.execute(sql_query)
        connection.commit()
    finally:
        connection.close()


# Function to rename a table
def rename_table(old_name, new_name):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql_query = f"RENAME TABLE {old_name} TO {new_name}"
            cursor.execute(sql_query)
        connection.commit()
    finally:
        connection.close()


def add_column(table_name, column_definition, after_column=None):
    """
    Add a new column to the specified table at a specific location.

    :param table_name: Name of the table to add the column to.
    :param column_definition: Definition of the new column (e.g., "new_column_name INT").
    :param after_column: Name of the existing column after which to place the new column (if any).
    """
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            if after_column:
                sql_query = f"ALTER TABLE {table_name} ADD COLUMN {column_definition} AFTER {after_column};"
            else:
                sql_query = f"ALTER TABLE {table_name} ADD COLUMN {column_definition};"
            cursor.execute(sql_query)
        connection.commit()
        print(
            f"Column '{column_definition}' added to table '{table_name}' successfully."
        )
    except Exception as e:
        print(f"An error occurred while adding the column: {e}")
    finally:
        connection.close()


# Function to delete a column
def delete_column(table_name, column_name):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql_query = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
            cursor.execute(sql_query)
        connection.commit()
    finally:
        connection.close()


# Function to modify a column
def modify_column(table_name, column_modification):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql_query = f"ALTER TABLE {table_name} MODIFY COLUMN {column_modification}"
            cursor.execute(sql_query)
        connection.commit()
    finally:
        connection.close()


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


# Function to create a new database
def create_database(database_name):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql_query = f"CREATE DATABASE IF NOT EXISTS {database_name}"
            cursor.execute(sql_query)
            print(f"Database '{database_name}' created successfully.")
        connection.commit()
    finally:
        connection.close()


def add_index_to_column(table_name, column_name):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql_query = f"ALTER TABLE {table_name} ADD INDEX ({column_name})"
            cursor.execute(sql_query)
        connection.commit()
    except Exception as e:
        print(f"An error occurred while adding index: {e}")
    finally:
        connection.close()


# Function to modify column order
def adjust_column_order(table_name, column_name, column_definition, position):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql_query = f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} {column_definition} {position}"
            # sql_query = f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} AFTER{column_definition}"
            cursor.execute(sql_query)
            print(f"Column '{column_name}' has been moved to {position}.")
        connection.commit()
    finally:
        connection.close()


# Function to add a foreign key
def add_foreign_key(child_table, fk_name, child_column, parent_table, parent_column):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # SQL query to add the foreign key
            sql_query = f"""
            ALTER TABLE {child_table}
            ADD CONSTRAINT {fk_name}
            FOREIGN KEY ({child_column})
            REFERENCES {parent_table}({parent_column})
            ON DELETE CASCADE
            ON UPDATE CASCADE;
            """
            cursor.execute(sql_query)
            print(f"Foreign key {fk_name} added successfully.")
        connection.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()


# Function to delete a foreign key
def delete_foreign_key(table_name, constraint_name):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # SQL query to drop the foreign key
            sql_query = f"ALTER TABLE {table_name} DROP FOREIGN KEY {constraint_name};"
            cursor.execute(sql_query)
            print(
                f"Foreign key {constraint_name} from table {table_name} dropped successfully."
            )
        connection.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()


def modify_column_type(table_name, column_name, new_data_type):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql_query = (
                f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} {new_data_type};"
            )
            cursor.execute(sql_query)
        connection.commit()
        print(
            f"Column {column_name} in table {table_name} has been modified to type {new_data_type}."
        )
    finally:
        connection.close()


# Example usage
if __name__ == "__main__":

    ################################################################################
    ##Create database
    ################################################################################
    # db_name = "TT_installation"  # Specify the database name
    # create_database(db_name)
    ################################################################################
    ##Create table
    ################################################################################
    # create_table_query = """CREATE TABLE IF NOT EXISTS cb22_calibration(
    #     id INT AUTO_INCREMENT PRIMARY KEY,
    #     WALL int NOT NULL,
    #     CB int NOT NULL,
    #     ROB int NOT NULL,
    #     FEB int NOT NULL,
    #     Channel int,
    #     Chi2NDF varchar(45),
    #     N0 varchar(45),
    #     Error_N0 varchar(45),
    #     Q0 varchar(45),
    #     Error_Q0 varchar(45),
    #     Q1 varchar(45),
    #     Error_Q1 varchar(45),
    #     Sigma0 varchar(45),
    #     Error_sigma0 varchar(45),
    #     Sigma1 varchar(45),
    #     Error_sigma1 varchar(45),
    #     w varchar(45),
    #     Error_w varchar(45),
    #     alpha varchar(45),
    #     Error_alpha varchar(45),
    #     mu varchar(45),
    #     Error_mu varchar(45),
    #     Chi2NDF_pedestal varchar(45),
    #     Chi2NDF_peak varchar(45),
    #     gain varchar(45),
    #     mode varchar(45),
    #     HV int NOT NULL,
    #     Date DATETIME DEFAULT CURRENT_TIMESTAMP
    # ) default charset=utf8;"""

    # create_table_query = """
    #         CREATE TABLE IF NOT EXISTS tt_elec_calibration (
    #             FEB_ID INT,
    #             cat_ID INT,
    #             data_UID INT,
    #             CH INT,
    #             a0 FLOAT,
    #             a00_err FLOAT,
    #             a1 FLOAT,
    #             a1_err FLOAT,
    #             a2 FLOAT,
    #             a3 FLOAT,
    #             a4 FLOAT,
    #             a5 FLOAT,
    #             a5_err FLOAT,
    #             b FLOAT,
    #             ChiSq FLOAT,
    #             status VARCHAR(255)
    #         );
    #         """
    # create_table(create_table_query)
    # create_table_query = """
    #         CREATE TABLE IF NOT EXISTS mode_list (
    #             id INT AUTO_INCREMENT PRIMARY KEY,
    #             mode VARCHAR(255)
    #         );
    #         """
    # create_table(create_table_query)
    ################################################################################
    # Add foreign key
    ################################################################################
    # Example usage
    child_table = "cb22_calibration"  # Replace with your actual child table name
    fk_name = "id"  # Name of the foreign key
    child_column = "mode"  # Column in the child table (foreign key)
    parent_table = "mode_list"  # Parent table that has the referenced primary key
    parent_column = "id"  # Primary key column in the parent table

    add_foreign_key(child_table, fk_name, child_column, parent_table, parent_column)

    ################################################################################
    # DELETE foreign key
    ################################################################################
    # table_name = "WALL_list"  # Replace with your actual table name
    # constraint_name = "WALL"  # Replace with your actual foreign key constraint name

    # delete_foreign_key(table_name, constraint_name)

    # # Example: Select data from table
    # result = select_query("SELECT * FROM cb22_calibration LIMIT 10")
    # print(result)
    ################################################################################
    # DELETE foreign key
    ################################################################################
    # # Example: Update a table
    # update_query_str = "UPDATE cb22_calibration SET mode = 1"
    # update_query(update_query_str)

    # Example: Delete a table
    # delete_table("ROB_list")

    # # Example: Rename a table
    # rename_table("cb22_calibration", "calibration_results")
    # db_name = "tt"  # Specify the database you want to delete
    # delete_database(db_name)

    # table_name = "cb22_calibration"
    # column_name = "mode"
    # new_data_type = "INT"

    # # Modify column type
    # modify_column_type(table_name, column_name, new_data_type)

    ################################################################################
    # Add column location
    ################################################################################
    # table_name = "cb22_calibration"
    # column_name = "Date"
    # column_definition = "DATETIME DEFAULT CURRENT_TIMESTAMP"
    # position = "AFTER id"  # Change to "FIRST" if you want it first
    # adjust_column_order(table_name, column_name, column_definition, position)

    ################################################################################
    # Add column location
    ################################################################################
    # Example usage: Add a column to the 'cb22_calibration' table after the 'ROB' column
    # table_name = "cb22_calibration"
    # new_column_definition = "Max_Q1_channel int NOT NULL"  # Define the new column here
    # after_column = (
    #     "Chi2NDF_peak"  # Specify the existing column after which to add the new column
    # )
    # add_column(table_name, new_column_definition, after_column)
