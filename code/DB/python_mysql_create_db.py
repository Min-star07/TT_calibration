import pymysql as ms

# Connection parameters (without specifying a database)
host = "localhost"
user = "root"
password = "@Min08240707"


# Function to create a connection to the MySQL server (no database specified)
def create_server_connection():
    return ms.connect(
        host=host,
        user=user,
        password=password,
        charset="utf8mb4",
        cursorclass=ms.cursors.DictCursor,
    )


# Function to create a new database
def create_database(database_name):
    connection = create_server_connection()
    try:
        with connection.cursor() as cursor:
            sql_query = f"CREATE DATABASE IF NOT EXISTS {database_name}"
            cursor.execute(sql_query)
            print(f"Database '{database_name}' created successfully.")
        connection.commit()
    finally:
        connection.close()


# Example usage
if __name__ == "__main__":
    db_name = "my_new_database"  # Specify the database name
    create_database(db_name)
