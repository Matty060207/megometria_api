from flask import Flask, request, jsonify, render_template_string
import psycopg2

app = Flask(__name__)

# 🔌 CONEXÃO COM BANCO
def conectar():
    return psycopg2.connect(
        host="dpg-d72o1jhr0fns73dp2tug-a.oregon-postgres.render.com",
        database="megometria_db",
        user="megometria_db_user",
        password="26nx4HXIw1SCjyKmzCCnPxBLRpVR2fWd",
        port=5432
    )

# 🧱 CRIAR TABELA
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

# 📤 RECEBER DADOS
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

# 📥 BUSCAR DADOS
@app.route("/dados", methods=["GET"])
def dados():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT * FROM medicoes ORDER BY id DESC LIMIT 50")
    dados = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(dados)

# 🌐 INTERFACE WEB
@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Megôhmetro Online</title>

        <style>
            body {
                font-family: Arial;
                background: #111;
                color: #0f0;
                text-align: center;
            }

            h1 {
                margin-top: 20px;
            }

            table {
                margin: auto;
                border-collapse: collapse;
                width: 80%;
            }

            th, td {
                border: 1px solid #0f0;
                padding: 10px;
            }

            th {
                background: #222;
            }

            tr:hover {
                background: #333;
            }
        </style>
    </head>

    <body>
        <h1>📊 Megôhmetro Nuvem (VERSÃO NOVA 🔥)</h1>

        <table id="tabela">
            <tr>
                <th>ID</th>
                <th>Dispositivo</th>
                <th>Valor (MΩ)</th>
                <th>Data</th>
            </tr>
        </table>

        <script>
            async function atualizar() {
                const res = await fetch('/dados');
                const dados = await res.json();

                let tabela = document.getElementById("tabela");

                tabela.innerHTML = `
                <tr>
                    <th>ID</th>
                    <th>Dispositivo</th>
                    <th>Valor</th>
                    <th>Data</th>
                </tr>
                `;

                if (dados.length === 0) {
                    tabela.innerHTML += "<tr><td colspan='4'>Nenhum dado ainda...</td></tr>";
                } else {
                    dados.forEach(d => {
                        let linha = `
                        <tr>
                            <td>${d[0]}</td>
                            <td>${d[1]}</td>
                            <td>${d[2]}</td>
                            <td>${d[3]}</td>
                        </tr>
                        `;
                        tabela.innerHTML += linha;
                    });
                }
            }

            setInterval(atualizar, 3000);
            atualizar();
        </script>
    </body>
    </html>
    """)

# ▶️ RODAR LOCAL
if __name__ == "__main__":
    app.run()