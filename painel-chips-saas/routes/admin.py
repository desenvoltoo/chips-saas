from flask import Blueprint, render_template, request, redirect, session
from utils.is_admin import require_role
from db import db_query, db_execute
from utils.security import gerar_hash

admin_bp = Blueprint("admin", __name__)

# ================================
# LISTAR EMPRESAS
# ================================
@admin_bp.route("/admin/empresas")
@require_role("superadmin")
def empresas_list():
    empresas = db_query("SELECT * FROM empresas ORDER BY id_empresa;")
    return render_template("admin/empresas.html", empresas=empresas)


# ================================
# CRIAR EMPRESA
# ================================
@admin_bp.route("/admin/empresas/nova", methods=["POST"])
@require_role("superadmin")
def empresa_add():
    nome = request.form["nome"]
    cnpj = request.form["cnpj"]
    email = request.form["email_contato"]
    telefone = request.form["telefone"]

    db_execute("""
        INSERT INTO empresas (nome, cnpj, email_contato, telefone)
        VALUES (%s, %s, %s, %s)
    """, (nome, cnpj, email, telefone))

    return redirect("/admin/empresas")


# ================================
# LISTAR USUÁRIOS DA EMPRESA
# ================================
@admin_bp.route("/admin/empresa/<id_empresa>/usuarios")
@require_role("superadmin")
def usuarios_empresa(id_empresa):
    usuarios = db_query("""
        SELECT *
        FROM usuarios
        WHERE id_empresa = %s
        ORDER BY id_usuario;
    """, (id_empresa,))

    empresa = db_query("SELECT * FROM empresas WHERE id_empresa = %s;", (id_empresa,))
    empresa = empresa[0]

    return render_template(
        "admin/usuarios.html",
        usuarios=usuarios,
        empresa=empresa
    )


# ================================
# ADICIONAR USUÁRIO
# ================================
@admin_bp.route("/admin/usuario/add", methods=["POST"])
@require_role("superadmin")
def usuario_add():
    dados = request.form

    db_execute("""
        INSERT INTO usuarios (id_empresa, nome, email, senha_hash, tipo, ativo)
        VALUES (%s, %s, %s, %s, %s, TRUE)
    """, (
        dados.get("id_empresa"),
        dados.get("nome"),
        dados.get("email"),
        gerar_hash(dados.get("senha")),
        dados.get("tipo")  # superadmin, admin, usuario
    ))

    return redirect(f"/admin/empresa/{dados.get('id_empresa')}/usuarios")
