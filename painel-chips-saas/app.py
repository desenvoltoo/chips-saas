# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, redirect, session

# Utils
from utils.security import verificar_hash
from utils.db import db_query
from utils.is_admin import login_required

# Blueprints
from routes import register_blueprints


# ===============================================================
# CONFIGURAÇÃO PRINCIPAL DO APP
# ===============================================================
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")


# ===============================================================
# HEALTH CHECK (Render exige esta rota)
# ===============================================================
@app.route("/healthz")
def healthz():
    return "ok", 200


# ===============================================================
# LOGIN
# - Carrega sessão completa
# - Valida HASH
# - Redireciona por tipo de usuário
# ===============================================================
@app.route("/", methods=["GET", "POST"])
def login():

    # GET → abre página
    if request.method == "GET":
        return render_template("login.html")

    # POST → valida login
    email = request.form.get("email")
    senha = request.form.get("senha")

    user = db_query("""
        SELECT 
            id_usuario,
            id_empresa,
            senha_hash,
            tipo,     -- superadmin / admin / usuario
            ativo
        FROM usuarios
        WHERE email = %s
        LIMIT 1;
    """, (email,))

    if not user:
        return render_template("login.html", erro="Usuário não encontrado")

    user = user[0]

    # Usuário desativado
    if not user["ativo"]:
        return render_template("login.html", erro="Usuário inativo")

    # Senha inválida
    if not verificar_hash(senha, user["senha_hash"]):
        return render_template("login.html", erro="Senha incorreta")

    # Cria sessão
    session.clear()
    session["id_usuario"] = user["id_usuario"]
    session["id_empresa"] = user["id_empresa"]
    session["tipo_usuario"] = user["tipo"]

    # Redirecionamento inteligente
    if user["tipo"] == "superadmin":
        return redirect("/admin")

    # Admin ou usuário comum → vai pro dashboard da empresa
    return redirect("/dashboard")


# ===============================================================
# LOGOUT
# ===============================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ===============================================================
# REGISTRA TODOS OS BLUEPRINTS
# ===============================================================
register_blueprints(app)


# ===============================================================
# EXECUÇÃO LOCAL (Render ignora)
# ===============================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
