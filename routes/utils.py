# utils.py
from flask import session

def is_authenticated():
    """Devuelve True si el usuario ha iniciado sesión."""
    return session.get('autenticado') is True

def is_admin():
    """Devuelve True si el usuario es el administrador maestro."""
    return session.get('es_admin') is True

def current_username():
    """Devuelve el nombre de usuario si está en sesión."""
    return session.get('cliente')
