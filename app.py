from flask import Flask, session, redirect, render_template
from routes.auth import auth_bp
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta'
app.register_blueprint(auth_bp)

@app.route('/menu')
def menu():
    if 'cliente' not in session:
        return redirect('/')
    return render_template('menu.html', cliente=session['cliente'])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
