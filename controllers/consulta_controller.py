from flask import request, redirect, url_for, Blueprint, session, make_response
from datetime import datetime
from models.consulta_model import Consulta
from models.medico_model import Medico
from models.paciente_model import Paciente
from views import consulta_view
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

consulta_bp = Blueprint('consulta', __name__, url_prefix="/consultas")

@consulta_bp.before_request
def check_session():
    if 'user_id' not in session and request.endpoint != 'usuario.login':
        return redirect(url_for('usuario.login'))

@consulta_bp.route("/")
def index():
    fecha_filtro = request.args.get('fecha')
    if fecha_filtro:
        fecha_dt = datetime.strptime(fecha_filtro, '%Y-%m-%d')
        consultas = Consulta.query.filter(db.func.date(Consulta.fecha) == fecha_dt.date()).all()
    else:
        consultas = Consulta.get_all()
    return consulta_view.list(consultas)

@consulta_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        fecha_str = request.form['fecha']
        fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamiento']
        id_medico = request.form['id_medico']
        id_paciente = request.form['id_paciente']
        
        consulta = Consulta(fecha, diagnostico, tratamiento, id_medico, id_paciente)
        consulta.save()
        return redirect(url_for('consulta.index'))
    
    medicos = Medico.get_all()
    pacientes = Paciente.get_all()
    return consulta_view.create(medicos, pacientes)

@consulta_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    consulta = Consulta.get_by_id(id)
    if request.method == 'POST':
        fecha_str = request.form['fecha']
        fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamiento']
        id_medico = request.form['id_medico']
        id_paciente = request.form['id_paciente']
        
        consulta.update(fecha=fecha, diagnostico=diagnostico, tratamiento=tratamiento, id_medico=id_medico, id_paciente=id_paciente)
        return redirect(url_for('consulta.index'))
        
    medicos = Medico.get_all()
    pacientes = Paciente.get_all()
    return consulta_view.edit(consulta, medicos, pacientes)

@consulta_bp.route("/delete/<int:id>")
def delete(id):
    consulta = Consulta.get_by_id(id)
    consulta.delete()
    return redirect(url_for('consulta.index'))

@consulta_bp.route("/reporte/pdf")
def reporte_pdf():
    consultas = Consulta.get_all()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "REPORTE DE CONSULTAS MÉDICAS")
    y = 700
    for c in consultas:
        p.drawString(100, y, f"Fecha: {c.fecha} - Paciente: {c.paciente.nombre} - Médico: {c.medico.nombre}")
        p.drawString(100, y-15, f"Diagnóstico: {c.diagnostico[:50]}...")
        y -= 40
        if y < 50:
            p.showPage()
            y = 750
    p.save()
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_consultas.pdf'
    return response

# To handle db.func in the filter, I need to import db
from database import db
