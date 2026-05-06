from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Crear base de datos
def init_db():
    conexion = sqlite3.connect("cafeteria.db")
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        bebida TEXT
    )
    """)
    conexion.commit()
    conexion.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = ""

    if request.method == "POST":
        nombre = request.form["nombre"]
        bebida = request.form["bebida"]

        if nombre == "":
            mensaje = "Ingrese nombre"
        else:
            conexion = sqlite3.connect("cafeteria.db")
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO pedidos (nombre, bebida) VALUES (?, ?)",
                (nombre, bebida)
            )
            conexion.commit()
            conexion.close()

            mensaje = f"Pedido para {nombre}: {bebida}"

    return render_template("index.html", mensaje=mensaje)

if __name__ == "__main__":
    app.run(debug=True)