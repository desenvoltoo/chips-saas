from flask import Blueprint, render_template, request, redirect, session
from db import db_query
from utils.security import verificar_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    senha = request.form.get("senha")

    user = db_query("""
        SELECT id_usuario, id_empresa, senha_hash, tipo
        FROM usuarios
        WHERE email = %s AND ativo = TRUE
        LIMIT 1;
    """, (email,))

    if not user:
        return render_template("login.html", erro="Usuário não encontrado")

    user = user[0]

    if not verificar_hash(senha, user["senha_hash"]):
        return render_template("login.html", erro="Senha incorreta")

    # Sessão
    session["id_usuario"] = user["id_usuario"]
    session["id_empresa"] = user["id_empresa"]
    session["tipo_usuario"] = user["tipo"]  # superadmin, admin, usuario

    return redirect("/dashboard")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
