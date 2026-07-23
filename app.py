from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)

def get_conexion():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def index():
    dia_seleccionado = request.args.get("dia", "Lunes")

    conexion = get_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM maquinas WHERE dia = %s", (dia_seleccionado,))
    maquinas = cursor.fetchall()

    cursor.execute("""
        SELECT rp.maquina_id, u.nombre, rp.peso_kg, rp.repeticiones
        FROM registros_peso rp
        JOIN usuarios u ON rp.usuario_id = u.id
        INNER JOIN (
            SELECT maquina_id, usuario_id, MAX(fecha) AS max_fecha
            FROM registros_peso
            GROUP BY maquina_id, usuario_id
        ) ultimo ON rp.maquina_id = ultimo.maquina_id
                 AND rp.usuario_id = ultimo.usuario_id
                 AND rp.fecha = ultimo.max_fecha
    """)
    pesos = cursor.fetchall()

    cursor.close()
    conexion.close()

    pesos_por_maquina = {}
    for p in pesos:
        pesos_por_maquina.setdefault(p["maquina_id"], []).append(p)

    for m in maquinas:
        m["pesos"] = pesos_por_maquina.get(m["id"], [])

    dias = ["Lunes", "Martes", "Jueves", "Viernes"]

    return render_template("index.html", maquinas=maquinas, dias=dias, dia_seleccionado=dia_seleccionado)


@app.route("/maquina/<int:id>")
def detalle_maquina(id):
    conexion = get_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM maquinas WHERE id = %s", (id,))
    maquina = cursor.fetchone()

    cursor.execute("""
        SELECT registros_peso.id, registros_peso.peso_kg, registros_peso.repeticiones, registros_peso.fecha, usuarios.nombre
        FROM registros_peso
        JOIN usuarios ON registros_peso.usuario_id = usuarios.id
        WHERE registros_peso.maquina_id = %s
        ORDER BY registros_peso.fecha DESC
    """, (id,))

    registros = cursor.fetchall()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("maquina.html", maquina=maquina, registros=registros, usuarios=usuarios)


@app.route("/maquina/<int:id>/agregar", methods=["POST"])
def agregar_registro(id):
    usuario_id = request.form["usuario_id"]
    peso_kg = request.form["peso_kg"]
    repeticiones = request.form["repeticiones"]

    conexion = get_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO registros_peso (usuario_id, maquina_id, peso_kg, repeticiones) VALUES (%s, %s, %s, %s)",
        (usuario_id, id, peso_kg, repeticiones)
    )
    conexion.commit()
    cursor.close()
    conexion.close()

    return redirect(url_for("detalle_maquina", id=id))


@app.route("/registro/<int:id>/editar", methods=["POST"])
def editar_registro(id):
    peso_kg = request.form["peso_kg"]
    repeticiones = request.form["repeticiones"]

    conexion = get_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT maquina_id FROM registros_peso WHERE id = %s", (id,))
    registro = cursor.fetchone()
    maquina_id = registro["maquina_id"]

    cursor.execute(
        "UPDATE registros_peso SET peso_kg = %s, repeticiones = %s WHERE id = %s",
        (peso_kg, repeticiones, id)
    )
    conexion.commit()
    cursor.close()
    conexion.close()

    return redirect(url_for("detalle_maquina", id=maquina_id))


@app.route("/registro/<int:id>/borrar", methods=["POST"])
def borrar_registro(id):
    conexion = get_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT maquina_id FROM registros_peso WHERE id = %s", (id,))
    registro = cursor.fetchone()
    maquina_id = registro["maquina_id"]

    cursor.execute("DELETE FROM registros_peso WHERE id = %s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()

    return redirect(url_for("detalle_maquina", id=maquina_id))

@app.route("/usuarios")
def usuarios():
    conexion = get_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios ORDER BY nombre")
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("usuarios.html", usuarios=usuarios)


@app.route("/usuarios/agregar", methods=["POST"])
def agregar_usuario():
    nombre = request.form["nombre"].strip()

    if nombre:
        conexion = get_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre) VALUES (%s)", (nombre,))
        conexion.commit()
        cursor.close()
        conexion.close()

    return redirect(url_for("usuarios"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)