# routes/chips.py

from flask import Blueprint, render_template, request, redirect, jsonify, session
from utils.db import db_query, db_execute
from utils.auth_required import login_required

chips_bp = Blueprint("chips", __name__)


# =============================================================================
# 📌 LISTA DE CHIPS (multi-empresa)
# =============================================================================
@chips_bp.route("/chips")
@login_required
def chips_list():
    id_empresa = session["id_empresa"]

    chips = db_query("""
        SELECT *
        FROM chips
        WHERE id_empresa = %s
        ORDER BY sk_chip DESC;
    """, (id_empresa,))

    aparelhos = db_query("""
        SELECT *
        FROM aparelhos
        WHERE id_empresa = %s
        ORDER BY modelo ASC;
    """, (id_empresa,))

    return render_template(
        "chips.html",
        chips=chips,
        aparelhos=aparelhos
    )


# =============================================================================
# ➕ ADICIONAR CHIP
# =============================================================================
@chips_bp.route("/chips/add", methods=["POST"])
@login_required
def chips_add():
    id_empresa = session["id_empresa"]

    numero = request.form.get("numero")
    operadora = request.form.get("operadora")
    operador = request.form.get("operador")
    plano = request.form.get("plano")
    status = request.form.get("status", "DISPONIVEL")
    observacao = request.form.get("observacao")
    dt_inicio = request.form.get("dt_inicio")

    db_execute("""
        INSERT INTO chips (
            id_empresa, numero, operadora, operador, plano, status,
            observacao, dt_inicio, ativo
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, TRUE);
    """, (
        id_empresa, numero, operadora, operador, plano, status,
        observacao, dt_inicio
    ))

    return redirect("/chips")


# =============================================================================
# 🔍 OBTER CHIP (JSON) – PARA MODAL DE EDIÇÃO
# =============================================================================
@chips_bp.route("/chips/<int:sk_chip>")
@login_required
def chips_get(sk_chip):
    id_empresa = session["id_empresa"]

    chip = db_query("""
        SELECT *
        FROM chips
        WHERE sk_chip = %s AND id_empresa = %s
        LIMIT 1;
    """, (sk_chip, id_empresa))

    if not chip:
        return jsonify({"erro": "Chip não encontrado"}), 404

    return jsonify(chip[0])


# =============================================================================
# 🔥 ATUALIZAR CHIP (JSON via Modal)
# =============================================================================
@chips_bp.route("/chips/update-json", methods=["POST"])
@login_required
def chips_update_json():
    dados = request.json
    id_empresa = session["id_empresa"]

    sk_chip = dados.get("sk_chip")
    if not sk_chip:
        return jsonify({"success": False, "erro": "ID inválido"}), 400

    db_execute("""
        UPDATE chips
        SET
            numero = %s,
            operadora = %s,
            operador = %s,
            plano = %s,
            status = %s,
            observacao = %s,
            dt_inicio = %s,
            ultima_recarga_valor = %s,
            ultima_recarga_data = %s,
            total_gasto = %s,
            sk_aparelho_atual = %s,
            updated_at = NOW()
        WHERE sk_chip = %s AND id_empresa = %s;
    """, (
        dados.get("numero"),
        dados.get("operadora"),
        dados.get("operador"),
        dados.get("plano"),
        dados.get("status"),
        dados.get("observacao"),
        dados.get("dt_inicio"),
        dados.get("ultima_recarga_valor"),
        dados.get("ultima_recarga_data"),
        dados.get("total_gasto"),
        dados.get("sk_aparelho_atual"),
        sk_chip,
        id_empresa
    ))

    return jsonify({"success": True})


# =============================================================================
# 🔄 REGISTRAR MOVIMENTO DE CHIP (POST)
# =============================================================================
@chips_bp.route("/chips/movimento", methods=["POST"])
@login_required
def chips_movimento():
    dados = request.json
    id_empresa = session["id_empresa"]

    db_execute("""
        INSERT INTO f_chip_aparelho (
            id_empresa, sk_chip, sk_aparelho, tipo_movimento, origem, observacao
        )
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (
        id_empresa,
        dados.get("sk_chip"),
        dados.get("sk_aparelho"),
        dados.get("tipo"),
        dados.get("origem", "Painel"),
        dados.get("observacao", "")
    ))

    return jsonify({"success": True})
