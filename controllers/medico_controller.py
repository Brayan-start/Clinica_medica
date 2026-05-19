from flask import request, redirect, url_for, Blueprint, session
from models.medico_model import Medico
from views import medico_view

medico_bp = Blueprint('medico', __name__, url_prefix="/medicos")

@medico_bp.before_request
def check_session():
    if 'user_id' not in session and request.endpoint != 'usuario.login':
        return redirect(url_for('usuario.login'))

@medico_bp.route("/")
def index():
    medicos = Medico.get_all()
    return medico_view.list(medicos)

@medico_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        especialidad = request.form['especialidad']
        telefono = request.form['telefono']
        correo = request.form['correo']
        medico = Medico(nombre, especialidad, telefono, correo)
        medico.save()
        return redirect(url_for('medico.index'))
    return medico_view.create()

@medico_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    medico = Medico.get_by_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        especialidad = request.form['especialidad']
        telefono = request.form['telefono']
        correo = request.form['correo']
        medico.update(nombre=nombre, especialidad=especialidad, telefono=telefono, correo=correo)
        return redirect(url_for('medico.index'))
    return medico_view.edit(medico)

@medico_bp.route("/delete/<int:id>")
def delete(id):
    medico = Medico.get_by_id(id)
    medico.delete()
    return redirect(url_for('medico.index'))
