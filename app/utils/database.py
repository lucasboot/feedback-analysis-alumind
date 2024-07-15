import mysql.connector
import os

def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB')
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise
