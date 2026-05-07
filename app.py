from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# ================= DATABASE =================

DATABASE_URL = os.environ.get("DATABASE_URL")

# ================= PAGINA PRINCIPAL =================

@app.route("/", methods=["GET", "POST"])
def index():

    conexion = psycopg2.connect(DATABASE_URL)
    cursor = conexion.cursor()

    # Crear tabla si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id SERIAL PRIMARY KEY,
        nombre TEXT,
        bebida TEXT
    )
    """)

    conexion.commit()

    mensaje = ""

    if request.method == "POST":

        nombre = request.form["nombre"]
        bebida = request.form["bebida"]

        cursor.execute(
            "INSERT INTO pedidos (nombre, bebida) VALUES (%s, %s)",
            (nombre, bebida)
        )

        conexion.commit()

        mensaje = f"Pedido realizado para {nombre}"

    conexion.close()

    return render_template(
        "index.html",
        mensaje=mensaje
    )

# ================= PANEL ADMIN =================

@app.route("/admin")
def admin():

    conexion = psycopg2.connect(DATABASE_URL)
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM pedidos ORDER BY id DESC")

    pedidos = cursor.fetchall()

    conexion.close()

    return render_template(
        "admin.html",
        pedidos=pedidos
    )

# ================= MAIN =================

if __name__ == "__main__":
    app.run(debug=True)
