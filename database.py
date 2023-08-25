import mysql.connector

database = mysql.connector.connect(
    host="localhost",
    user='root',
    password='Alvarez&26'
)

mysql_cursor = database.cursor()
mysql_cursor.execute("CREATE DATABASE prueba_base")