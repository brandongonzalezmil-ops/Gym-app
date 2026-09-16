import sqlite3
from config import DB_PATH

conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS fotos_maquinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maquina_id INTEGER NOT NULL,
    imagen_url TEXT NOT NULL,
    FOREIGN KEY (maquina_id) REFERENCES maquinas(id)
)
""")

cursor.execute("SELECT id, imagen_url FROM maquinas WHERE imagen_url IS NOT NULL AND imagen_url != ''")
maquinas_con_foto = cursor.fetchall()

for maquina_id, imagen_url in maquinas_con_foto:
    cursor.execute(
        "INSERT INTO fotos_maquinas (maquina_id, imagen_url) VALUES (?, ?)",
        (maquina_id, imagen_url)
    )

conexion.commit()
conexion.close()
print(f"Tabla creada. Se migraron {len(maquinas_con_foto)} fotos existentes.")