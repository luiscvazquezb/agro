from flask import Flask, session, redirect, render_template
from routes.auth import auth_bp
from routes.menu import menu_bp
from routes.clientes import clientes_bp
from routes.variedades import variedades_bp
from routes.tipo_cultivo import tipo_cultivo_bp
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta'
app.register_blueprint(auth_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(variedades_bp)
app.register_blueprint(tipo_cultivo_bp)



@app.route('/menu')
def menu():
    if 'cliente' not in session:
        return redirect('/')
    
    if session.get('es_admin'):
        # Redirecciona a vista especial para el admin
        return redirect('/clientes')

    return render_template('menu.html', cliente=session['cliente'])



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
