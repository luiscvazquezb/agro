from flask import Blueprint, render_template, request, redirect, flash, session
from supabase import create_client
import os

auth_bp = Blueprint('auth', __name__)

# Usuario maestro fijo (admin general)
USUARIO_VALIDO = "adminagro"
PASSWORD_VALIDA = "Admin@123Agro"

# Conexión a Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

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
            session['es_admin'] = True
            print("✅ Login como administrador")
            return redirect('/menu')

        # 2. Validación contra Supabase
        result = supabase.table("clientes").select("*").eq("username", usuario).eq("password", password).execute()
        data = result.data

        if data:
            session['cliente'] = data[0]['nombre']
            session['cliente_id'] = data[0]['id']
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
