
from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask import abort
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

# Credenciales fijas para acceso
USUARIO_VALIDO = "adminagro"
PASSWORD_VALIDA = "Admin@123Agro"

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/clientes')
def ver_clientes():
    if not session.get('autenticado'):
        return redirect('/login')

    buscar = request.args.get('buscar', '').strip().lower()

    try:
        resultado = supabase.table("clientes").select("*").order("fecha_alta", desc=True).execute()
        clientes = resultado.data if resultado.data else []

        if buscar:
            clientes = [c for c in clientes if buscar in c['nombre'].lower()]
    except Exception as e:
        clientes = []
        flash(f"Error al cargar clientes: {str(e)}", "danger")

    return render_template("clientes.html", clientes=clientes)





@app.route('/editar-cliente/<uuid:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    if not session.get('autenticado'):
        return redirect('/login')

    if request.method == 'POST':
        datos = {
            "nombre": request.form.get("nombre"),
            "representante": request.form.get("representante"),
            "telefono": request.form.get("telefono"),
            "whatsapp": request.form.get("whatsapp"),
            "telegram": request.form.get("telegram"),
            "correo": request.form.get("correo"),
            "logo_url": request.form.get("logo_url"),
            "colorhex": request.form.get("colorhex"),
            "pagina": request.form.get("pagina"),
            "password": request.form.get("password"),
            "username": request.form.get("username")
        }
        try:
            supabase.table("clientes").update(datos).eq("id", str(id)).execute()
            flash("Cliente actualizado exitosamente", "success")
            return redirect('/clientes')
        except Exception as e:
            flash(f"Error al actualizar cliente: {str(e)}", "danger")

    resultado = supabase.table("clientes").select("*").eq("id", str(id)).single().execute()
    if resultado.data:
        return render_template("editar_cliente.html", cliente=resultado.data)
    else:
        abort(404)



@app.route('/logout')
def logout():
    session.pop('autenticado', None)
    return redirect('/login')

@app.route('/nuevo-cliente', methods=['GET', 'POST'])
def nuevo_cliente():
    if not session.get('autenticado'):
        return redirect('/login')

    if request.method == 'POST':
        datos = {
            "nombre": request.form.get("nombre"),
            "representante": request.form.get("representante"),
            "telefono": request.form.get("telefono"),
            "whatsapp": request.form.get("whatsapp"),
            "telegram": request.form.get("telegram"),
            "correo": request.form.get("correo"),
            "logo_url": request.form.get("logo_url"),
            "colorhex": request.form.get("colorhex"),
            "pagina": request.form.get("pagina"),
            "password": request.form.get("password"),
            "username": request.form.get("username")
        }

        try:
            supabase.table("clientes").insert(datos).execute()
            flash("Cliente registrado exitosamente", "success")
        except Exception as e:
            flash(f"Error al registrar cliente: {str(e)}", "danger")
             
        return redirect('/nuevo-cliente')

    return render_template("nuevo_cliente.html")

if __name__ == '__main__':
    app.run(debug=True)
