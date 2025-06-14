from flask import Blueprint, render_template, request, redirect, flash, session
from supabase_client import supabase  # Carga conexión desde supabase_client.py
from routes.utils import is_authenticated, is_admin  # Opcional si lo quieres usar luego

auth_bp = Blueprint('auth', __name__)

# Usuario maestro fijo (admin general)
USUARIO_VALIDO = "adminagro"
PASSWORD_VALIDA = "Admin@123Agro"

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        print(f"🔐 Intento de login: {usuario} / {password}")

        # 1. Validación como usuario maestro
        if usuario == USUARIO_VALIDO and password == PASSWORD_VALIDA:
            session['cliente'] = 'ADMIN'
            session['cliente_id'] = 0
            session['autenticado'] = True
            session['es_admin'] = True
            print("✅ Login como administrador")
            return redirect('/menu')

        # 2. Validación contra Supabase
        result = supabase.table("clientes").select("*").eq("username", usuario).eq("password", password).execute()
        data = result.data

        if data:
            session['cliente'] = data[0]['nombre']
            session['cliente_id'] = data[0]['id']
            session['autenticado'] = True
            session['es_admin'] = False
            print("✅ Login cliente Supabase:", data[0]['nombre'])
            return redirect('/menu')
        else:
            flash("Usuario o contraseña incorrectos.")
            print("❌ Falló el login")
    
    return render_template("login.html")

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
