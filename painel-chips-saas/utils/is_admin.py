from functools import wraps
from flask import session, redirect

def require_role(*roles):
    """
    Exemplo:
    @require_role("superadmin")
    @require_role("admin")
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "tipo_usuario" not in session:
                return redirect("/")

            if session["tipo_usuario"] not in roles:
                return redirect("/dashboard")

            return f(*args, **kwargs)
        return wrapper
    return decorator
