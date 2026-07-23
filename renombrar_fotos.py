import os

CARPETA = "static/imagenes"

# Lista de nombres nuevos en el ORDEN en que quieres asignarlos
nombres_nuevos = [
    "pecho_inclinado_power.jpg",
    "aperturas_pecho.jpg",
    "pull_over_maquina.jpg",
    "remo_t.jpg",
    "triceps_tras_nuca_jueves.jpg",
    "curl_predicador_maquina.jpg",
    "elevaciones_laterales_n14_jueves.jpg",
    "pecho_inclinado.jpg",
    "elevaciones_laterales_pecho_n5.jpg",
    "jalon_pecho_supino.jpg",
    "remo_espalda_alta.jpg",
    "triceps_banco_predicador.jpg",
    "curl_martillo_soga.jpg",
    "elevaciones_laterales_mancuerna.jpg",
    "aductores.jpg",
    "hack_sentadilla.jpg",
    "extension_cuadriceps.jpg",
    "curl_femoral_sentado.jpg",
    "pantorrilla.jpg",
    "jalon_pecho.jpg",
    "elevacion_lateral_n14_viernes.jpg",
    "hombro_posterior_aperturas.jpg",
    "press_militar_maquina.jpg",
    "triceps_tras_nuca_viernes.jpg",
    "triceps_polea_barra_v.jpg",
    "curl_martillo_banco_inclinado.jpg",
    "curl_biceps_banco_scott.jpg",
]

# PASO 1: Solo mostrar los archivos actuales (no renombra todavía)
archivos_actuales = sorted(os.listdir(CARPETA))
archivos_actuales = [f for f in archivos_actuales if not f.startswith(".")]

print(f"Encontré {len(archivos_actuales)} archivos en '{CARPETA}':\n")
for i, nombre in enumerate(archivos_actuales):
    print(f"{i+1}. {nombre}")

    print("\n--- Renombrando ---\n")

    for archivo_viejo, nombre_nuevo in zip(archivos_actuales, nombres_nuevos):
        ruta_vieja = os.path.join(CARPETA, archivo_viejo)
        ruta_nueva = os.path.join(CARPETA, nombre_nuevo)
        os.rename(ruta_vieja, ruta_nueva)
        print(f"{archivo_viejo}  →  {nombre_nuevo}")

    print("\n✅ Listo, todas las fotos fueron renombradas.")