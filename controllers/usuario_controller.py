from flask import request, redirect, url_for, Blueprint, session, flash
from models.usuario_model import Usuario
from views import usuario_view

usuario_bp = Blueprint('usuario', __name__, url_prefix="/usuarios")

@usuario_bp.route("/")
def index():
    if 'user_id' not in session: return redirect(url_for('usuario.login'))
    usuarios = Usuario.get_all()
    return usuario_view.list(usuarios)

@usuario_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        username = request.form['username']
        password = request.form['password']
        rol = request.form['rol']
        usuario = Usuario(nombre, username, password, rol)
        usuario.save()
        return redirect(url_for('usuario.index'))
    return usuario_view.create()

@usuario_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    if 'user_id' not in session: return redirect(url_for('usuario.login'))
    usuario = Usuario.get_by_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        username = request.form['username']
        password = request.form.get('password')
        rol = request.form['rol']
        usuario.update(nombre=nombre, username=username, password=password, rol=rol)
        return redirect(url_for('usuario.index'))
    return usuario_view.edit(usuario)

@usuario_bp.route("/delete/<int:id>")
def delete(id):
    if 'user_id' not in session: return redirect(url_for('usuario.login'))
    usuario = Usuario.get_by_id(id)
    usuario.delete()
    return redirect(url_for('usuario.index'))

@usuario_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = Usuario.get_by_username(username)
        if usuario and usuario.verify_password(password):
            session['user_id'] = usuario.id
            session['username'] = usuario.username
            session['rol'] = usuario.rol
            return redirect(url_for('home'))
        flash("Usuario o contraseña incorrectos")
    return usuario_view.login()

@usuario_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('usuario.login'))
