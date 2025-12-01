from flask import Blueprint, render_template, request, redirect, session
from utils.security import verificar_hash
from utils.db import db_query

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    senha = request.form.get("senha")

    usuario = db_query("""
        SELECT 
            id_usuario,
            nome,
            email,
            senha_hash,
            tipo,           -- superadmin, admin, user
            id_empresa,
            ativo
        FROM usuarios
        WHERE email = %s
        LIMIT 1;
    """, (email,))

    if not usuario:
        return render_template("login.html", erro="Usuário não encontrado")

    usuario = usuario[0]

    if not usuario["ativo"]:
        return render_template("login.html", erro="Usuário inativo")

    if not verificar_hash(senha, usuario["senha_hash"]):
        return render_template("login.html", erro="Senha incorreta")

    # Define sessão
    session.clear()
    session["id_usuario"] = usuario["id_usuario"]
    session["tipo_usuario"] = usuario["tipo"]            # superadmin/admin/user
    session["id_empresa"] = usuario.get("id_empresa")    # superadmin não tem empresa vinculada

    # Redireciona por tipo
    if usuario["tipo"] == "superadmin":
        return redirect("/admin")

    return redirect("/dashboard")
