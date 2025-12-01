from flask import Blueprint, render_template, request, redirect, session
from utils.is_admin import require_role
from db import db_query, db_execute
from utils.security import gerar_hash

admin_empresa_bp = Blueprint("admin_empresa", __name__)

@admin_empresa_bp.route("/empresa/usuarios")
@require_role("admin")
def empresa_usuarios():
    id_empresa = session["id_empresa"]

    usuarios = db_query("""
        SELECT * FROM usuarios
        WHERE id_empresa = %s
        ORDER BY id_usuario;
    """, (id_empresa,))

    return render_template("admin/empresa_usuarios.html", usuarios=usuarios)


@admin_empresa_bp.route("/empresa/usuarios/add", methods=["POST"])
@require_role("admin")
def empresa_add_user():
    id_empresa = session["id_empresa"]
    dados = request.form

    db_execute("""
        INSERT INTO usuarios (id_empresa, nome, email, senha_hash, tipo, ativo)
        VALUES (%s, %s, %s, %s, 'usuario', TRUE)
    """, (
        id_empresa,
        dados.get("nome"),
        dados.get("email"),
        gerar_hash(dados.get("senha")),
    ))

    return redirect("/empresa/usuarios")
