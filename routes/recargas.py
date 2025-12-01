# routes/recargas.py

from flask import Blueprint, request, redirect, session
from utils.db import db_query, db_execute
from utils.auth_required import login_required

recargas_bp = Blueprint("recargas", __name__)


# =======================================================
# ➕ REGISTRAR RECARGA (POSTGRESQL)
# =======================================================
@recargas_bp.route("/recargas/add", methods=["POST"])
@login_required
def registrar_recarga():
    id_empresa = session["id_empresa"]

    sk_chip = request.form.get("sk_chip")
    valor = request.form.get("valor")
    data_recarga = request.form.get("data_recarga")

    if not sk_chip or not valor or not data_recarga:
        return "Dados inválidos", 400

    # Atualiza os campos da recarga
    db_execute("""
        UPDATE chips
        SET
            ultima_recarga_valor = %s,
            ultima_recarga_data = %s,
            updated_at = NOW()
        WHERE sk_chip = %s AND id_empresa = %s;
    """, (
        valor,
        data_recarga,
        sk_chip,
        id_empresa
    ))

    return redirect("/dashboard")
