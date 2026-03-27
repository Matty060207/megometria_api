from flask import Flask, request, jsonify, render_template
import psycopg2

app = Flask(__name__)

def conectar():
    return psycopg2.connect(
        host="dpg-d72o1jhr0fns73dp2tug-a.oregon-postgres.render.com",
        database="megometria_db",
        user="megometria_db_user",
        password="26nx4HXIw1SCjyKmzCCnPxBLRpVR2fWd",
        port=5432
    )

def criar_tabela():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS medicoes (
        id SERIAL PRIMARY KEY,
        dispositivo TEXT,
        valor REAL,
        data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    cur.close()
    conn.close()

criar_tabela()

@app.route("/enviar", methods=["POST"])
def enviar():
    data = request.get_json()

    conn = conectar()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO medicoes (dispositivo, valor) VALUES (%s, %s)",
        (data["dispositivo"], data["valor"])
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "ok"}

@app.route("/dados", methods=["GET"])
def dados():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT * FROM medicoes ORDER BY id DESC LIMIT 50")
    dados = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(dados)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()