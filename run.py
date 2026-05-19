from flask import Flask, request, session, redirect, url_for, render_template
from database import db
from controllers.medico_controller import medico_bp
from controllers.paciente_controller import paciente_bp
from controllers.consulta_controller import consulta_bp
from controllers.usuario_controller import usuario_bp
from models.usuario_model import Usuario
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones'

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clinica.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Registro de Blueprints
app.register_blueprint(medico_bp)
app.register_blueprint(paciente_bp)
app.register_blueprint(consulta_bp)
app.register_blueprint(usuario_bp)

# Inicialización de la base de datos (Compatible con Render/Gunicorn)
with app.app_context():
    db.create_all()
    # Crear usuario administrador por defecto si no existe
    if not Usuario.get_by_username('admin'):
        admin = Usuario("Administrador", "admin", "admin123", "admin")
        admin.save()

@app.route("/")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('usuario.login'))
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
