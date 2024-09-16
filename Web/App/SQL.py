from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum('男', '女'), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    medical_history = db.Column(db.Text, nullable=False)
    pk = db.Column(db.String(200), nullable=False)

    medical_records = relationship('MedicalRecord', back_populates='patient')
    medications = relationship('Medication', back_populates='patient')
    tests_and_results = relationship('TestAndResult', back_populates='patient')
    appointments = relationship('Appointment', back_populates='patient')
    health_reminders = relationship('HealthReminder', back_populates='patient')
    medical_documents = relationship('MedicalDocument', back_populates='patient')
    sensor_readings = relationship("SensorReading", back_populates="patient")

class Hospital(db.Model):
    __tablename__ = 'hospitals'
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(15), nullable=False)

    doctors = relationship('Doctor', back_populates='hospital')
    medical_records = relationship('MedicalRecord', back_populates='hospital')

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum('男', '女'), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    hospital_id = db.Column(db.String(10), db.ForeignKey('hospitals.id'), nullable=False)
    hospital_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)

    hospital = relationship('Hospital', back_populates='doctors')
    medical_records = relationship('MedicalRecord', back_populates='doctor')

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.String(10), db.ForeignKey('patients.id'), nullable=False)
    record_date = db.Column(db.Date, nullable=False)
    record = db.Column(db.Text, nullable=False)
    doctor_id = db.Column(db.String(10), db.ForeignKey('doctors.id'), nullable=False)
    doctor_name = db.Column(db.String(100), nullable=False)
    hospital_id = db.Column(db.String(10), db.ForeignKey('hospitals.id'), nullable=False)
    hospital_name = db.Column(db.String(100), nullable=False)

    patient = relationship('Patient', back_populates='medical_records')
    doctor = relationship('Doctor', back_populates='medical_records')
    hospital = relationship('Hospital', back_populates='medical_records')

class Medication(db.Model):
    __tablename__ = 'medications'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.String(10), db.ForeignKey('patients.id'), nullable=False)
    medication_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)

    patient = relationship('Patient', back_populates='medications')

class TestAndResult(db.Model):
    __tablename__ = 'tests_and_results'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.String(10), db.ForeignKey('patients.id'), nullable=False)
    test_date = db.Column(db.Date, nullable=False)
    test_type = db.Column(db.String(100), nullable=False)
    results = db.Column(db.Text, nullable=False)

    patient = relationship('Patient', back_populates='tests_and_results')

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.String(10), db.ForeignKey('patients.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    doctor = db.Column(db.String(100), nullable=False)
    clinic = db.Column(db.String(100), nullable=False)

    patient = relationship('Patient', back_populates='appointments')

class HealthReminder(db.Model):
    __tablename__ = 'health_reminders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.String(10), db.ForeignKey('patients.id'), nullable=False)
    reminder = db.Column(db.Text, nullable=False)
    reminder_date = db.Column(db.Date, nullable=False)

    patient = relationship('Patient', back_populates='health_reminders')

class MedicalDocument(db.Model):
    __tablename__ = 'medical_documents'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.String(10), db.ForeignKey('patients.id'), nullable=False)
    document_name = db.Column(db.String(100), nullable=False)
    document_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.Date, nullable=False)

    patient = relationship('Patient', back_populates='medical_documents')

class SensorReading(db.Model):
    __tablename__ = 'sensor_readings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.String(50), db.ForeignKey('patients.id'))
    iot_id = db.Column(db.String(50))
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    received_time = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship("Patient", back_populates="sensor_readings")

Patient.sensor_readings = db.relationship("SensorReading", order_by=SensorReading.received_time, back_populates="patient")