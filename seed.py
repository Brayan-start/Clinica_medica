from run import app
from database import db
from models.medico_model import Medico
from models.paciente_model import Paciente
from models.consulta_model import Consulta
from datetime import datetime

def seed_data():
    with app.app_context():
        # Médicos
        m1 = Medico("Dr. Juan Pérez", "Cardiología", "555-0101", "juan@clinica.com")
        m2 = Medico("Dra. María García", "Pediatría", "555-0102", "maria@clinica.com")
        m1.save()
        m2.save()

        # Pacientes
        p1 = Paciente("Carlos Rodríguez", 45, "Av. Central 123", "555-0201")
        p2 = Paciente("Ana López", 28, "Calle Norte 456", "555-0202")
        p1.save()
        p2.save()

        # Consultas
        c1 = Consulta(datetime.now(), "Arritmia leve", "Reposo y seguimiento", m1.id_medico, p1.id_paciente)
        c2 = Consulta(datetime.now(), "Gripe común", "Paracetamol cada 8h", m2.id_medico, p2.id_paciente)
        c1.save()
        c2.save()

        print("Datos de prueba cargados con éxito.")

if __name__ == "__main__":
    seed_data()
