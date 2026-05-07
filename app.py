from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# ================= CONEXION BASE DE DATOS =================

DATABASE_URL = os.environ.get("DATABASE_URL")

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

# ================= PAGINA PRINCIPAL =================

@app.route("/", methods=["GET", "POST"])
def index():

    mensaje = ""

    if request.method == "POST":

        nombre = request.form["nombre"]
        bebida = request.form["bebida"]

        if nombre != "":

            cursor.execute(
                "INSERT INTO pedidos (nombre, bebida) VALUES (%s, %s)",
                (nombre, bebida)
            )

            conexion.commit()

            mensaje = f"Pedido para {nombre}: {bebida}"

    # MOSTRAR PEDIDOS
    cursor.execute("SELECT * FROM pedidos ORDER BY id DESC")
    pedidos = cursor.fetchall()

    return render_template(
        "index.html",
        mensaje=mensaje,
        pedidos=pedidos
    )

# ================= INICIAR APP =================

if __name__ == "__main__":
    app.run(debug=True)
