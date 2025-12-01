from flask import Blueprint, request, jsonify
import uuid
import bcrypt
from utils.db import db_query, db_execute

auth_bp = Blueprint("auth", __name__)

# --------------------------
# LOGIN
# --------------------------
@auth_bp.post("/login")
def login():
    try:
        data = request.get_json()

        print("DEBUG DATA:", data)  # <-- MOSTRA O QUE CHEGA DO FRONT

        if not data:
            return jsonify({"erro": "Nenhum dado recebido (JSON inválido)"}), 400

        email = data.get("email")
        senha = data.get("senha")

        print("EMAIL RECEBIDO:", email)
        print("SENHA RECEBIDA:", senha)

        if not email or not senha:
            return jsonify({"erro": "Email e senha são obrigatórios"}), 400

        # buscar usuário
        user = db_query("""
            SELECT id_usuario, id_empresa, senha_hash, tipo, ativo
            FROM usuarios
            WHERE email = %s AND ativo = TRUE
            LIMIT 1
        """, (email,))

        if not user:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        user = user[0]

        # ---------------------------
        # VERIFICAR SENHA BCRYPT
        # ---------------------------
        if not bcrypt.checkpw(senha.encode(), user["senha_hash"].encode()):
            print("DEBUG: Senha incorreta para:", email)
            return jsonify({"erro": "Senha incorreta"}), 400

        # gerar token de sessão
        token = str(uuid.uuid4())

        db_execute("""
            INSERT INTO sessoes_login (id_sessao, id_usuario)
            VALUES (%s, %s)
        """, (token, user["id_usuario"]))

        return jsonify({
            "token": token,
            "id_empresa": user["id_empresa"],
            "tipo": user["tipo"]
        }), 200

    except Exception as e:
        print("ERRO LOGIN:", e)
        return jsonify({"erro": "Erro interno no login", "detalhe": str(e)}), 500
