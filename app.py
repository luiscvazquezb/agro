from flask import Flask, render_template, request, redirect, session, flash
from supabase import create_client
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Conexión a Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        result = supabase.table("clientes").select("*").eq("nombre", usuario).eq("password", password).execute()
        data = result.data

        if data:
            session['cliente'] = data[0]['nombre']
            session['cliente_id'] = data[0]['id']
            return redirect('/menu')
        else:
            flash("Usuario o contraseña incorrectos.")
    
    return render_template('login.html')


@app.route('/menu')
def menu():
    if 'cliente' not in session:
        return redirect('/')
    return render_template('menu.html', cliente=session['cliente'])


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render define PORT, si no existe usa 5000
    app.run(debug=True, host='0.0.0.0', port=port)