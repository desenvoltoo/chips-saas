from flask import Blueprint, request, jsonify
import uuid
import bcrypt
from utils.db import db_query, db_execute

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():

    # ============================
    # CAPTURA DE DADOS (FORM + JSON)
    # ============================
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    # ============================
    # BUSCA DO USUÁRIO
    # ============================
    user = db_query("""
        SELECT id_usuario, id_empresa, senha_hash, tipo, ativo
        FROM usuarios
        WHERE email = %s AND ativo = TRUE
        LIMIT 1
    """, (email,))

    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    user = user[0]

    # ============================
    # VERIFICAÇÃO DA SENHA
    # ============================
    if not bcrypt.checkpw(senha.encode(), user["senha_hash"].encode()):
        return jsonify({"erro": "Senha incorreta"}), 400

    # ============================
    # CRIA TOKEN
    # ============================
    token = str(uuid.uuid4())

    db_execute("""
        INSERT INTO sessoes_login (id_sessao, id_usuario)
        VALUES (%s, %s)
    """, (token, user["id_usuario"]))

    # ============================
    # LOGIN OK → REDIRECIONA
    # ============================
    from flask import redirect

    return redirect("/dashboard")
