from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from config import DB_PATH

app = Flask(__name__)

def get_conexion():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion

@app.route("/")
def index():
    dia_seleccionado = request.args.get("dia", "Lunes")

    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM maquinas WHERE dia = ?", (dia_seleccionado,))
    maquinas = [dict(row) for row in cursor.fetchall()]

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
    pesos = [dict(row) for row in cursor.fetchall()]

    conexion.close()

    pesos_por_maquina = {}
    for p in pesos:
        pesos_por_maquina.setdefault(p["maquina_id"], []).append(p)

    for m in maquinas:
        m["pesos"] = pesos_por_maquina.get(m["id"], [])

    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    return render_template("index.html", maquinas=maquinas, dias=dias, dia_seleccionado=dia_seleccionado)


@app.route("/maquina/<int:id>")
def detalle_maquina(id):
    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM maquinas WHERE id = ?", (id,))
    maquina = dict(cursor.fetchone())

    cursor.execute("""
        SELECT registros_peso.id, registros_peso.peso_kg, registros_peso.repeticiones, registros_peso.fecha, usuarios.nombre
        FROM registros_peso
        JOIN usuarios ON registros_peso.usuario_id = usuarios.id
        WHERE registros_peso.maquina_id = ?
        ORDER BY registros_peso.fecha DESC
    """, (id,))
    registros = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM usuarios")
    usuarios = [dict(row) for row in cursor.fetchall()]

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
        "INSERT INTO registros_peso (usuario_id, maquina_id, peso_kg, repeticiones) VALUES (?, ?, ?, ?)",
        (usuario_id, id, peso_kg, repeticiones)
    )
    conexion.commit()
    conexion.close()

    return redirect(url_for("detalle_maquina", id=id))


@app.route("/registro/<int:id>/editar", methods=["POST"])
def editar_registro(id):
    peso_kg = request.form["peso_kg"]
    repeticiones = request.form["repeticiones"]

    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT maquina_id FROM registros_peso WHERE id = ?", (id,))
    registro = cursor.fetchone()
    maquina_id = registro["maquina_id"]

    cursor.execute(
        "UPDATE registros_peso SET peso_kg = ?, repeticiones = ? WHERE id = ?",
        (peso_kg, repeticiones, id)
    )
    conexion.commit()
    conexion.close()

    return redirect(url_for("detalle_maquina", id=maquina_id))


@app.route("/registro/<int:id>/borrar", methods=["POST"])
def borrar_registro(id):
    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT maquina_id FROM registros_peso WHERE id = ?", (id,))
    registro = cursor.fetchone()
    maquina_id = registro["maquina_id"]

    cursor.execute("DELETE FROM registros_peso WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()

    return redirect(url_for("detalle_maquina", id=maquina_id))


@app.route("/usuarios")
def usuarios():
    conexion = get_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios ORDER BY nombre")
    usuarios = [dict(row) for row in cursor.fetchall()]
    conexion.close()
    return render_template("usuarios.html", usuarios=usuarios)


@app.route("/usuarios/agregar", methods=["POST"])
def agregar_usuario():
    nombre = request.form["nombre"].strip()

    if nombre:
        conexion = get_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre) VALUES (?)", (nombre,))
        conexion.commit()
        conexion.close()

    return redirect(url_for("usuarios"))


if __name__ == "__main__":
    app.run(debug=True)