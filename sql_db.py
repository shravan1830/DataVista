import mysql.connector
from mysql.connector import Error


def connect_to_mysql(user, database, password=""):
    try:
        # Replace with your actual database configuration
        connection = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            return connection

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


def run_sql_query(connection, query):
    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = []
        if query.strip().lower().startswith("select"):
            results.append(cursor.column_names)
            results.extend(cursor.fetchall())
            print(results)
            return results
        else:
            connection.commit()
            return "Query executed successfully"

    except Error as e:
        print(f"Error executing query: {e}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Example usage

# query = "SELECT * FROM students;"  # Replace with your actual query
# results = execute_query(query)

# if results is not None:
#     for row in results:
#         print(row)
