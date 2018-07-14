from flask import request,redirect,url_for,session,redirect,request
import controladorBaseDatos as BD
from functools import update_wrapper

def rol_required(rol):
    def decorator(fn):
        def wrapped_function(*args, **kwargs):
            # First check if user is authenticated.
            if not ("rol" in session) and (request.method!="POST"):## tengo que ver si creo un metodo de seguridad para los post desde jquery
                return redirect(url_for('login'))
            else:
                if session["rol"]!=rol:
                    return("No tienes permiso rol")
            return fn(*args, **kwargs)
        return update_wrapper(wrapped_function, fn)
    return decorator

def login_required(rol):
    def decorator(fn):
        def wrapped_function(*args, **kwargs):
            # First check if user is authenticated.
            if not ("user" in session and "password" in session) and (request.method!="POST"):
                return redirect(url_for('login'))
            else:
                if not(BD.checkPassword(session["user"],session["password"])):
                    return("No tienes permiso login")
            return fn(*args, **kwargs)
        return update_wrapper(wrapped_function, fn)
    return decorator