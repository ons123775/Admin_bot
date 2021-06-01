import mysql.connector
from mysql.connector import Error

# open connection


def open_connection():
    try:

        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='judy-bot',
            user='root',
            password=''
        )

        return connection

    except Error as e:
        print('Error: ', e)
        return None


# close connection
def close_connection(connection, cursor):
    if connection:
        cursor.close()
        connection.close()
