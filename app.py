# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, redirect, session
from utils.security import verificar_hash
from utils.db import db_query
from routes import register_blueprints

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")


# ============================
# HEALTH CHECK (para Render)
# ============================
@app.route("/healthz")
def healthz():
    return "ok", 200


# ============================
# LOGIN PRINCIPAL
# ============================
@app.route("/", methods=["GET", "POST"])
def login():

    # se GET → só exibe tela de login
    if request.method == "GET":
        return render_template("login.html")

    # captura do form
    email = request.form.get("email")
    senha = request.form.get("senha")

    if not email or not senha:
        return render_template("login.html", erro="Preencha email e senha.")

    # busca usuário
    user = db_query("""
        SELECT 
            id_usuario,
            id_empresa,
            senha_hash,
            tipo,          -- superadmin / admin / usuario
            ativo
        FROM usuarios
        WHERE email = %s
        LIMIT 1;
    """, (email,))

    if not user:
        return render_template("login.html", erro="Usuário não encontrado")

    user = user[0]

    if not user["ativo"]:
        return render_template("login.html", erro="Usuário inativo")

    # ============================
    # VERIFICA HASH BCRYPT
    # ============================
    if not verificar_hash(senha, user["senha_hash"]):
        return render_template("login.html", erro="Senha incorreta")

    # ============================
    # CRIA SESSÃO
    # ============================
    session.clear()
    session["id_usuario"] = user["id_usuario"]
    session["id_empresa"] = user["id_empresa"]
    session["tipo_usuario"] = user["tipo"]

    # superadmin vai para /admin
    if user["tipo"] == "superadmin":
        return redirect("/admin")

    # demais → dashboard
    return redirect("/dashboard")


# ============================
# LOGOUT
# ============================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ============================
# BLUEPRINTS
# ============================
register_blueprints(app)


# ============================
# RUN
# ============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
