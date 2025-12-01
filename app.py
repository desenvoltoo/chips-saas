# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, redirect, session
from utils.security import verificar_hash
from utils.db import db_query
from utils.is_admin import login_required
from routes import register_blueprints

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")


@app.route("/healthz")
def healthz():
    return "ok", 200


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    senha = request.form.get("senha")

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

    # ✅ AGORA usando bcrypt via verificar_hash
    if not verificar_hash(senha, user["senha_hash"]):
        return render_template("login.html", erro="Senha incorreta")

    # cria sessão
    session.clear()
    session["id_usuario"] = user["id_usuario"]
    session["id_empresa"] = user["id_empresa"]
    session["tipo_usuario"] = user["tipo"]

    # superadmin cai no /admin, resto no /dashboard
    if user["tipo"] == "superadmin":
        return redirect("/admin")

    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# blueprints (chips, aparelhos, recargas, relacionamentos, admin, dashboard)
register_blueprints(app)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
