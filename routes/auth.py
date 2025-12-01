from flask import Blueprint, request, jsonify, make_response
import uuid
from utils.db import db_query, db_execute   # vamos criar

auth_bp = Blueprint("auth", __name__)

# --------------------------
# LOGIN
# --------------------------
@auth_bp.post("/login")
def login():
    data = request.json
    email = data.get("email")
    senha = data.get("senha")

    user = db_query("""
        SELECT id_usuario, id_empresa, senha_hash, permissao
        FROM usuarios
        WHERE email = %s AND ativo = TRUE
        LIMIT 1
    """, (email,))

    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    user = user[0]

    # segurança: compare senhas reais (bcrypt recomendado)
    if senha != user["senha_hash"]:
        return jsonify({"erro": "Senha incorreta"}), 400

    # Criar token de sessão
    token = str(uuid.uuid4())

    db_execute("""
        INSERT INTO sessoes_login (id_sessao, id_usuario)
        VALUES (%s, %s)
    """, (token, user["id_usuario"]))

    return jsonify({
        "token": token,
        "id_empresa": user["id_empresa"],
        "permissao": user["permissao"]
    })
