from flask import Blueprint, request, jsonify
import uuid
from utils.db import db_query, db_execute

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/login")
def login():
    data = request.json
    email = data.get("email")
    senha = data.get("senha")

    user = db_query("""
        SELECT id_usuario, id_empresa, senha_hash, tipo
        FROM usuarios
        WHERE email = %s AND ativo = TRUE
        LIMIT 1
    """, (email,))

    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    user = user[0]

    # Aqui futuramente vamos usar bcrypt
    if senha != user["senha_hash"]:
        return jsonify({"erro": "Senha incorreta"}), 400

    token = str(uuid.uuid4())

    db_execute("""
        INSERT INTO sessoes_login (id_sessao, id_usuario)
        VALUES (%s, %s)
    """, (token, user["id_usuario"]))

    return jsonify({
        "token": token,
        "id_empresa": user["id_empresa"],
        "tipo": user["tipo"]
    })
