import mysql.connector
def get_connection(): return mysql.connector.connect( host="localhost", user="root", password="#Jasdelop67",
  database="matricula", port=3307, 
  connection_timeout=30 )