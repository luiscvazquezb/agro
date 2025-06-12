from flask import Blueprint, render_template, request, redirect, flash, session

auth_bp = Blueprint('auth', __name__)

USUARIO_VALIDO = "adminagro"
PASSWORD_VALIDA = "Admin@123Agro"

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        if usuario == USUARIO_VALIDO and contrasena == PASSWORD_VALIDA:
            session['autenticado'] = True
            return redirect('/clientes')
        else:
            flash("Usuario o contraseña incorrectos", "danger")
    return render_template("login.html")

@auth_bp.route('/logout')
def logout():
    session.pop('autenticado', None)
    return redirect('/login')
