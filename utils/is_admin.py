# -*- coding: utf-8 -*-
from functools import wraps
from flask import session, redirect


def login_required(f):
    """
    Bloqueia acesso se o usuário não estiver logado.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "id_usuario" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Bloqueia acesso de usuários comuns.
    Apenas superadmin ou admin de empresa.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        tipo = session.get("tipo_usuario")
        if tipo not in ("superadmin", "admin"):
            return redirect("/dashboard")
        return f(*args, **kwargs)
    return decorated_function


def superadmin_required(f):
    """
    Apenas SUPERADMIN pode acessar certas rotas.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("tipo_usuario") != "superadmin":
            return redirect("/dashboard")
        return f(*args, **kwargs)
    return decorated_function
