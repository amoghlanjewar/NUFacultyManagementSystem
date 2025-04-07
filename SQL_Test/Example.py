import mysql.connector
conn = mysql.connector.connect(host='localhost', password='Amogh@123', user='root')
if conn.is_connected():
    print("Connection established...")
