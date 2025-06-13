from flask import Blueprint, render_template, redirect, session

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/menu')
def menu():
    if 'cliente' not in session:
        return redirect('/')

    if session.get('es_admin'):
        return redirect('/clientes')

    return render_template('menu.html', cliente=session['cliente'])
