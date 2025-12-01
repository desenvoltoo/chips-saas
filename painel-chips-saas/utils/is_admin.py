from flask import session, redirect

def login_required(f):
    def wrapper(*args, **kwargs):
        if "id_usuario" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    return wrapper


def admin_only(f):
    def wrapper(*args, **kwargs):
        if session.get("tipo_usuario") not in ("admin", "superadmin"):
            return "Acesso negado (admin)", 403
        return f(*args, **kwargs)
    return wrapper


def superadmin_only(f):
    def wrapper(*args, **kwargs):
        if session.get("tipo_usuario") != "superadmin":
            return "Acesso negado (superadmin)", 403
        return f(*args, **kwargs)
    return wrapper


def empresa_only(f):
    def wrapper(*args, **kwargs):
        if "id_empresa" not in session:
            return "Acesso negado (empresa)", 403
        return f(*args, **kwargs)
    return wrapper
