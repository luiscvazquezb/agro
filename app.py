from flask import Flask, session, redirect, render_template
from routes.auth import auth_bp
from routes.menu import menu_bp
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta'
app.register_blueprint(auth_bp)
app.register_blueprint(menu_bp)

@app.route('/menu')
def menu():
    if 'cliente' not in session:
        return redirect('/')
    
    if session.get('es_admin'):
        # Redirecciona a vista especial para el admin
        return redirect('/clientes')

    return render_template('menu.html', cliente=session['cliente'])

@app.route('/clientes')
def ver_clientes():
    if not session.get('es_admin'):
        return redirect('/menu')

    buscar = request.args.get('buscar', '').strip().lower()
    result = supabase.table("clientes").select("*").execute()
    clientes = result.data

    if buscar:
        clientes = [c for c in clientes if buscar in c.get('nombre', '').lower()]

    return render_template("clientes.html", clientes=clientes)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
