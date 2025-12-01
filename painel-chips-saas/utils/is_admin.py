from functools import wraps
from flask import session, redirect

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get("is_admin") != True:
            return redirect("/dashboard")
        return f(*args, **kwargs)
    return wrap
