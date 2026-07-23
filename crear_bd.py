import sqlite3
from config import DB_PATH

conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS maquinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    imagen_url TEXT,
    descripcion TEXT,
    dia TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS registros_peso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    maquina_id INTEGER NOT NULL,
    peso_kg REAL NOT NULL,
    repeticiones INTEGER,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (maquina_id) REFERENCES maquinas(id)
)
""")

conexion.commit()
conexion.close()
print("Base de datos SQLite creada correctamente: gym.db")
