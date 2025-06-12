import os
from dotenv import load_dotenv

def configure_app(app):
    load_dotenv()
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "clave-segura")
