from flask import request, redirect, url_for, Blueprint, session
from models.paciente_model import Paciente
from views import paciente_view

paciente_bp = Blueprint('paciente', __name__, url_prefix="/pacientes")

@paciente_bp.before_request
def check_session():
    if 'user_id' not in session and request.endpoint != 'usuario.login':
        return redirect(url_for('usuario.login'))

@paciente_bp.route("/")
def index():
    pacientes = Paciente.get_all()
    return paciente_view.list(pacientes)

@paciente_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        paciente = Paciente(nombre, edad, direccion, telefono)
        paciente.save()
        return redirect(url_for('paciente.index'))
    return paciente_view.create()

@paciente_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    paciente = Paciente.get_by_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        paciente.update(nombre=nombre, edad=edad, direccion=direccion, telefono=telefono)
        return redirect(url_for('paciente.index'))
    return paciente_view.edit(paciente)

@paciente_bp.route("/delete/<int:id>")
def delete(id):
    paciente = Paciente.get_by_id(id)
    paciente.delete()
    return redirect(url_for('paciente.index'))

@paciente_bp.route("/historial/<int:id>")
def historial(id):
    paciente = Paciente.get_by_id(id)
    return paciente_view.list_historial(paciente) # I should add this to view
