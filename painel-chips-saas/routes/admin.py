from flask import Blueprint, render_template, request, redirect
from utils.db import db_query, db_execute
from utils.is_admin import superadmin_only

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@superadmin_only
def home_admin():
    return render_template("admin/home.html")


# ---------------------
# Empresas
# ---------------------
@admin_bp.route("/empresas")
@superadmin_only
def empresas():
    lista = db_query("SELECT * FROM empresas ORDER BY id_empresa DESC;")
    return render_template("admin/empresas.html", empresas=lista)


@admin_bp.route("/empresa/add", methods=["POST"])
@superadmin_only
def add_empresa():
    nome = request.form.get("nome")
    status = request.form.get("status", "ATIVA")

    db_execute("""
        INSERT INTO empresas (nome, status)
        VALUES (%s, %s)
    """, (nome, status))

    return redirect("/admin/empresas")


# ---------------------
# Usuários
# ---------------------
@admin_bp.route("/usuarios")
@superadmin_only
def usuarios():
    lista = db_query("""
        SELECT u.*, e.nome AS empresa_nome
        FROM usuarios u
        LEFT JOIN empresas e ON e.id_empresa = u.id_empresa
        ORDER BY u.id_usuario DESC;
    """)
    return render_template("admin/usuarios.html", usuarios=lista)
