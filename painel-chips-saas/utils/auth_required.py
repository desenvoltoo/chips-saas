from flask import session, redirect

def login_required(func):
    def wrapper(*args, **kwargs):
        if "id_usuario" not in session:
            return redirect("/")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
