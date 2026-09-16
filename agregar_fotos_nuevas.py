import sqlite3
from config import DB_PATH

conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

fotos_nuevas = [
    ("Pantorrilla", "Pantorrilla2.jpg"),
    ("Hack sentadilla", "Hacka_sentadilla2.jpg"),
    ("Remo espalda alta", "remo_espalda_alta2.jpg"),
    ("Jalón al pecho agarre supino", "jalon_pecho_supino2.jpg"),
]

for nombre_maquina, archivo in fotos_nuevas:
    cursor.execute("SELECT id FROM maquinas WHERE nombre = ?", (nombre_maquina,))
    resultado = cursor.fetchone()
    if resultado:
        maquina_id = resultado[0]
        cursor.execute(
            "INSERT INTO fotos_maquinas (maquina_id, imagen_url) VALUES (?, ?)",
            (maquina_id, archivo)
        )
        print(f"Agregada foto '{archivo}' a '{nombre_maquina}' (id {maquina_id})")
    else:
        print(f"⚠️ No se encontró la máquina '{nombre_maquina}'")

conexion.commit()
conexion.close()