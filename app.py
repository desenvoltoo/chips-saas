# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, redirect, session
from utils.db import db_query
from utils.security import verificar_hash
from utils.auth_required import login_required
from routes import register_blueprints

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")
 

# ==========================
# HEALTH CHECK (Render)
# ==========================
@app.route("/healthz")
def healthz():
    return "ok", 200


# ==========================
# LOGIN
# ==========================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    senha = request.form.get("senha")

    user = db_query("""
        SELECT id_usuario, id_empresa, senha_hash
        FROM usuarios
        WHERE email = %s AND ativo = TRUE
        LIMIT 1;
    """, (email,))

    if not user:
        return render_template("login.html", erro="Usuário não encontrado")

    user = user[0]

    if not verificar_hash(senha, user["senha_hash"]):
        return render_template("login.html", erro="Senha incorreta")

    # Sessão criada
    session["id_usuario"] = user["id_usuario"]
    session["id_empresa"] = user["id_empresa"]

    return redirect("/dashboard")


# ==========================
# LOGOUT
# ==========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ==========================
# BLUEPRINTS
# chips.py, aparelhos.py, recargas.py, relacionamentos.py, dashboard.py
# ==========================
register_blueprints(app)


# ==========================
# RUN SERVER LOCAL
# ==========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
