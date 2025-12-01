# routes/relacionamentos.py

from flask import Blueprint, render_template, request, redirect, jsonify, session
from utils.db import db_query, db_execute
from utils.auth_required import login_required

relacionamentos_bp = Blueprint("relacionamentos", __name__)


# =============================================================================
# 📌 LISTAR TODAS AS MOVIMENTAÇÕES (multi-empresa)
# =============================================================================
@relacionamentos_bp.route("/relacionamentos")
@login_required
def listar_relacionamentos():
    id_empresa = session["id_empresa"]

    movimentos = db_query("""
        SELECT f.*, 
               c.numero AS numero_chip,
               a.modelo AS modelo_aparelho
        FROM f_chip_aparelho f
        LEFT JOIN chips c ON c.sk_chip = f.sk_chip
        LEFT JOIN aparelhos a ON a.sk_aparelho = f.sk_aparelho
        WHERE f.id_empresa = %s
        ORDER BY f.data_movimento DESC;
    """, (id_empresa,))

    return render_template(
        "relacionamentos.html",
        relacionamentos=movimentos
    )


# =============================================================================
# ➕ INSERIR NOVO RELACIONAMENTO/MOVIMENTO
# =============================================================================
@relacionamentos_bp.route("/relacionamentos/add", methods=["POST"])
@login_required
def adicionar_relacionamento():
    id_empresa = session["id_empresa"]

    sk_chip = request.form.get("sk_chip")
    sk_aparelho = request.form.get("sk_aparelho")
    tipo = request.form.get("tipo")
    origem = request.form.get("origem", "Painel")
    observacao = request.form.get("observacao", "")

    if not sk_chip or not tipo:
        return "Dados incompletos", 400

    db_execute("""
        INSERT INTO f_chip_aparelho (
            id_empresa, sk_chip, sk_aparelho,
            tipo_movimento, origem, observacao
        )
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (id_empresa, sk_chip, sk_aparelho, tipo, origem, observacao))

    return redirect("/relacionamentos")


# =============================================================================
# 🔍 DETALHE DE UM MOVIMENTO (JSON)
# =============================================================================
@relacionamentos_bp.route("/relacionamentos/<int:sk_fato>")
@login_required
def detalhe_relacionamento(sk_fato):
    id_empresa = session["id_empresa"]

    movimento = db_query("""
        SELECT f.*, 
               c.numero AS numero_chip,
               a.modelo AS modelo_aparelho
        FROM f_chip_aparelho f
        LEFT JOIN chips c ON c.sk_chip = f.sk_chip
        LEFT JOIN aparelhos a ON a.sk_aparelho = f.sk_aparelho
        WHERE f.sk_fato = %s AND f.id_empresa = %s
        LIMIT 1;
    """, (sk_fato, id_empresa))

    if not movimento:
        return jsonify({"erro": "Movimento não encontrado"}), 404

    return jsonify(movimento[0])
