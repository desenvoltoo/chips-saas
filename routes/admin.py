# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, session
from db import db_query, db_execute
from utils.auth_required import login_required
from utils.is_admin import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ==============================================================
# DASHBOARD ADMIN
# ==============================================================

@admin_bp.route("/")
@login_required
@admin_required
def admin_home():
    empresas = db_query("SELECT * FROM empresas ORDER BY id_empresa ASC")
    usuarios = db_query("""
        SELECT u.*, e.nome AS empresa_nome
        FROM usuarios u
        LEFT JOIN empresas e ON u.id_empresa = e.id_empresa
        ORDER BY u.id_usuario DESC
    """)

    return render_template(
        "admin/home.html",
        empresas=empresas,
        usuarios=usuarios
    )


# ==============================================================
# EMPRESAS – LISTAR
# ==============================================================

@admin_bp.route("/empresas")
@login_required
@admin_required
def empresas_list():
    empresas = db_query("SELECT * FROM empresas ORDER BY id_empresa DESC;")
    return render_template("admin/empresas.html", empresas=empresas)


# ==============================================================
# EMPRESAS – FORM
# ==============================================================

@admin_bp.route("/empresas/add", methods=["GET", "POST"])
@login_required
@admin_required
def empresas_add():
    if request.method == "GET":
        return render_template("admin/empresa_form.html")

    nome = request.form.get("nome")
    ativo = request.form.get("ativo") == "on"

    db_execute("""
        INSERT INTO empresas (nome, ativo)
        VALUES (%s, %s);
    """, (nome, ativo))

    return redirect("/admin/empresas")


# ==============================================================
# USUÁRIOS – LISTAR
# ==============================================================

@admin_bp.route("/usuarios")
@login_required
@admin_required
def usuarios_list():
    usuarios = db_query("""
        SELECT u.*, e.nome AS empresa_nome
        FROM usuarios u
        LEFT JOIN empresas e ON u.id_empresa = e.id_empresa
        ORDER BY u.id_usuario DESC
    """)
    empresas = db_query("SELECT * FROM empresas ORDER BY nome ASC;")

    return render_template(
        "admin/usuarios.html",
        usuarios=usuarios,
        empresas=empresas
    )


# ==============================================================
# USUÁRIOS – FORM
# ==============================================================

@admin_bp.route("/usuarios/add", methods=["GET", "POST"])
@login_required
@admin_required
def usuarios_add():

    empresas = db_query("SELECT * FROM empresas ORDER BY nome ASC;")

    if request.method == "GET":
        return render_template("admin/usuario_form.html", empresas=empresas)

    nome = request.form.get("nome")
    email = request.form.get("email")
    senha_hash = request.form.get("senha_hash")  # já será enviado pronto
    id_empresa = request.form.get("id_empresa")
    admin_flag = request.form.get("is_admin") == "on"

    db_execute("""
        INSERT INTO usuarios (nome, email, senha_hash, id_empresa, is_admin, ativo)
        VALUES (%s, %s, %s, %s, %s, TRUE);
    """, (nome, email, senha_hash, id_empresa, admin_flag))

    return redirect("/admin/usuarios")
