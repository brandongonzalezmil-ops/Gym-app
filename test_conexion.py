import mysql.connector
from config import DB_CONFIG

conexion = mysql.connector.connect(**DB_CONFIG)

if conexion.is_connected():
    print("✅ Conexión exitosa a MySQL")
    conexion.close()
