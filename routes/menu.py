from flask import Blueprint, render_template, redirect, session
from routes.utils import is_authenticated, is_admin  

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/menu')
def menu():
    if not is_authenticated():
        return redirect('/login')

    if is_admin():
        return redirect('/clientes')

    return render_template('menu.html', cliente=session['cliente'])

