from flask import render_template

def list(consultas):
    return render_template('consultas/index.html', consultas=consultas)

def create(medicos, pacientes):
    return render_template('consultas/create.html', medicos=medicos, pacientes=pacientes)

def edit(consulta, medicos, pacientes):
    return render_template('consultas/edit.html', consulta=consulta, medicos=medicos, pacientes=pacientes)
