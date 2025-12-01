# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, session, redirect
from db import db_query

bp_dashboard = Blueprint("dashboard", __name__)

# ===============================================================
# ROTA DO DASHBOARD (SAAS)
# ===============================================================
@bp_dashboard.route("/")
@bp_dashboard.route("/dashboard")
def dashboard():

    # Bloqueia acesso sem login
    if "id_empresa" not in session:
        return redirect("/")

    id_empresa = session["id_empresa"]

    # -----------------------------------------------------------
    # 1) Carregar chips (equivalente à antiga view vw_chips_painel)
    # -----------------------------------------------------------
    chips = db_query("""
        SELECT 
            c.id_chip,
            c.numero,
            c.operadora,
            c.operador,
            c.status,
            c.plano,
            c.dt_inicio,
            c.ultima_recarga_valor,
            c.ultima_recarga_data,
            c.total_gasto,
            a.modelo AS modelo_aparelho,
            a.marca AS marca_aparelho
        FROM chips c
        LEFT JOIN aparelhos a
            ON a.id_aparelho = c.id_aparelho_atual
        WHERE c.id_empresa = %s
        ORDER BY c.numero ASC
    """, (id_empresa,))

    # Convertendo para lista simples (já vem como dict)
    tabela = chips

    # -----------------------------------------------------------
    # 2) KPIs
    # -----------------------------------------------------------
    total_chips = len(tabela)
    chips_ativos = len([x for x in tabela if (x.get("status") or "").upper() == "ATIVO"])
    disparando = len([x for x in tabela if (x.get("status") or "").upper() == "DISPARANDO"])
    banidos = len([x for x in tabela if (x.get("status") or "").upper() == "BANIDO"])

    # -----------------------------------------------------------
    # 3) FILTROS / GRÁFICOS
    # -----------------------------------------------------------
    lista_status = sorted({ (x.get("status") or "").upper() for x in tabela if x.get("status") })
    lista_operadora = sorted({ x.get("operadora") for x in tabela if x.get("operadora") })

    # -----------------------------------------------------------
    # 4) ALERTAS - chips sem recarga > 80 dias
    # -----------------------------------------------------------
    alerta = db_query("""
        SELECT
            numero,
            status,
            operadora,
            ultima_recarga_data,
            EXTRACT(DAY FROM CURRENT_DATE - ultima_recarga_data) AS dias
        FROM chips
        WHERE id_empresa = %s
          AND ultima_recarga_data IS NOT NULL
          AND CURRENT_DATE - ultima_recarga_data > INTERVAL '80 days'
        ORDER BY dias DESC
    """, (id_empresa,))

    qtd_alerta = len(alerta)

    # -----------------------------------------------------------
    # 5) RENDERIZAÇÃO
    # -----------------------------------------------------------
    return render_template(
        "dashboard.html",

        # tabela principal
        tabela=tabela,

        # KPIs
        total_chips=total_chips,
        chips_ativos=chips_ativos,
        disparando=disparando,
        banidos=banidos,

        # filtros
        lista_status=lista_status,
        lista_operadora=lista_operadora,

        # alertas
        alerta_recarga=alerta,
        qtd_alerta=qtd_alerta,
    )
