# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, redirect, session
from utils.security import verificar_hash
from utils.db import db_query
from utils.is_admin import login_required
from routes import register_blueprints

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")


# =========================================================
# HEALTH CHECK
# =========================================================
@app.route("/healthz")
def healthz():
    return "ok", 200


# =========================================================
# LOGIN
# =========================================================
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    # --------------------------
    # Sanitização do input
    # --------------------------
    email = request.form.get("email", "").strip().lower()
    senha = request.form.get("senha", "").strip()

    # --------------------------
    # Busca usuário
    # --------------------------
    user = db_query("""
        SELECT 
            id_usuario,
            id_empresa,
            senha_hash,
            tipo,       -- superadmin / admin / usuario
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

    # --------------------------
    # Verifica senha Bcrypt
    # --------------------------
    if not verificar_hash(senha, user["senha_hash"]):
        return render_template("login.html", erro="Senha incorreta")

    # --------------------------
    # Cria sessão
    # --------------------------
    session.clear()
    session["id_usuario"] = user["id_usuario"]
    session["id_empresa"] = user["id_empresa"]
    session["tipo_usuario"] = user["tipo"]

    # superadmin cai no /admin
    if user["tipo"] == "superadmin":
        return redirect("/admin")

    # admin e usuario normal
    return redirect("/dashboard")


# =========================================================
# LOGOUT
# =========================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# =========================================================
# REGISTER BLUEPRINTS
# =========================================================
register_blueprints(app)


# =========================================================
# EXEC LOCAL
# =========================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
