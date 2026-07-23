import sqlite3
import mysql.connector
from config import DB_PATH

# --- Conexión a MySQL (origen) ---
mysql_conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="gym_app"
)
mysql_cursor = mysql_conexion.cursor(dictionary=True)

# --- Conexión a SQLite (destino) ---
sqlite_conexion = sqlite3.connect(DB_PATH)
sqlite_cursor = sqlite_conexion.cursor()

# --- Migrar usuarios ---
mysql_cursor.execute("SELECT * FROM usuarios")
usuarios = mysql_cursor.fetchall()
for u in usuarios:
    sqlite_cursor.execute(
        "INSERT INTO usuarios (id, nombre) VALUES (?, ?)",
        (u["id"], u["nombre"])
    )

# --- Migrar máquinas ---
mysql_cursor.execute("SELECT * FROM maquinas")
maquinas = mysql_cursor.fetchall()
for m in maquinas:
    sqlite_cursor.execute(
        "INSERT INTO maquinas (id, nombre, imagen_url, descripcion, dia) VALUES (?, ?, ?, ?, ?)",
        (m["id"], m["nombre"], m["imagen_url"], m["descripcion"], m["dia"])
    )

# --- Migrar registros de peso ---
mysql_cursor.execute("SELECT * FROM registros_peso")
registros = mysql_cursor.fetchall()
for r in registros:
    sqlite_cursor.execute(
        "INSERT INTO registros_peso (id, usuario_id, maquina_id, peso_kg, repeticiones, fecha) VALUES (?, ?, ?, ?, ?, ?)",
        (r["id"], r["usuario_id"], r["maquina_id"], float(r["peso_kg"]), r["repeticiones"], str(r["fecha"]))
    )

sqlite_conexion.commit()

print(f"Migrados: {len(usuarios)} usuarios, {len(maquinas)} máquinas, {len(registros)} registros de peso")

mysql_cursor.close()
mysql_conexion.close()
sqlite_conexion.close()