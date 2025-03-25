import pymysql as ms

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


# Function to fetch calibration data based on mode
def fetch_calibration_by_mode(specific_mode):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # SQL query to join cb22_calibration with mode_list and filter by specific mode
            sql_query = """
                SELECT cb.*
                FROM cb22_calibration AS cb
                JOIN mode_list AS m ON cb.mode = m.id
                WHERE m.id = %s;  # Use 'm.id' to match with the foreign key
            """
            cursor.execute(sql_query, (specific_mode,))
            result = cursor.fetchall()  # Fetch all matching records
            return result
    finally:
        connection.close()  # Ensure the connection is closed


# Example usage
if __name__ == "__main__":
    mode_to_search = 1  # Replace with the actual mode ID you want to filter by
    calibrations = fetch_calibration_by_mode(mode_to_search)

    # Print the results
    if calibrations:
        print(f"Calibration data for mode ID '{mode_to_search}':")
        for calibration in calibrations:
            print(calibration)
    else:
        print(f"No calibration data found for mode ID '{mode_to_search}'.")
