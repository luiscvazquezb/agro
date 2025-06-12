# app.py (nuevo)

from flask import Flask
from config import configure_app

# Importar los blueprints
from routes.auth import auth_bp
from routes.clientes import clientes_bp
# from routes.usuarios import usuarios_bp
# from routes.sectores import sectores_bp
#from routes.produccion import produccion_bp

app = Flask(__name__)
configure_app(app)

# Registrar módulos (blueprints)
app.register_blueprint(auth_bp)
app.register_blueprint(clientes_bp)
#app.register_blueprint(usuarios_bp)
#app.register_blueprint(sectores_bp)
#app.register_blueprint(produccion_bp)

# Página de inicio redirige a login
@app.route("/")
def index():
    return "Bienvenido a AgroApp. Usa /login para ingresar."

if __name__ == '__main__':
    app.run(debug=True)