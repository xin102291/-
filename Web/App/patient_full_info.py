from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from App.SQL import *
import json

# 創建數據庫引擎
engine = create_engine('mysql://pqc:123456@localhost/server', pool_size=5, max_overflow=0)
Session = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

# 獲取患者資訊
def get_patient(id):
    with get_session() as session:
        patient = session.query(Patient).get(id)
        if patient:
            return [{
                'id': patient.id,
                'name': patient.name,
                'age': patient.age,
                'gender': patient.gender,
                'contact': patient.contact,
                'address': patient.address,
                'medical_history': patient.medical_history
            }]
        else:
            return None

# 獲取健康提醒
def get_health_reminders(patient_id):
    with get_session() as session:
        reminders = session.query(HealthReminder).filter_by(patient_id=patient_id).all()
        return [{
            'id': reminder.id,
            'patient_id': reminder.patient_id,
            'reminder': reminder.reminder,
            'reminder_date': reminder.reminder_date.strftime('%Y-%m-%d')
        } for reminder in reminders] if reminders else None

# 獲取病歷紀錄
def get_medical_records(patient_id):
    with get_session() as session:
        records = session.query(MedicalRecord).filter_by(patient_id=patient_id).all()
        return [{
            'id': record.id,
            'patient_id': record.patient_id,
            'record_date': record.record_date.strftime('%Y-%m-%d'),
            'record': record.record,
            'doctor_id': record.doctor_id,
            'doctor_name': record.doctor_name,
            'hospital_id': record.hospital_id,
            'hospital_name': record.hospital_name
        } for record in records] if records else None

# 獲取藥物信息
def get_medications(patient_id):
    with get_session() as session:
        medications = session.query(Medication).filter_by(patient_id=patient_id).all()
        return [{
            'id': medication.id,
            'patient_id': medication.patient_id,
            'medication_name': medication.medication_name,
            'dosage': medication.dosage,
            'start_date': medication.start_date.strftime('%Y-%m-%d'),
            'end_date': medication.end_date.strftime('%Y-%m-%d') if medication.end_date else None
        } for medication in medications] if medications else None

# 獲取檢查和檢驗結果
def get_tests_and_results(patient_id):
    with get_session() as session:
        tests = session.query(TestAndResult).filter_by(patient_id=patient_id).all()
        return [{
            'id': test.id,
            'patient_id': test.patient_id,
            'test_date': test.test_date.strftime('%Y-%m-%d'),
            'test_type': test.test_type,
            'results': test.results
        } for test in tests] if tests else None

# 獲取預約訊息
def get_appointments(patient_id):
    with get_session() as session:
        appointments = session.query(Appointment).filter_by(patient_id=patient_id).all()
        return [{
            'id': appointment.id,
            'patient_id': appointment.patient_id,
            'appointment_date': appointment.appointment_date.strftime('%Y-%m-%d'),
            'appointment_time': appointment.appointment_time.strftime('%H:%M:%S'),
            'doctor': appointment.doctor,
            'clinic': appointment.clinic
        } for appointment in appointments] if appointments else None

# 獲取醫療文件
def get_medical_documents(patient_id):
    with get_session() as session:
        documents = session.query(MedicalDocument).filter_by(patient_id=patient_id).all()
        return [{
            'id': document.id,
            'patient_id': document.patient_id,
            'document_name': document.document_name,
            'document_path': document.document_path,
            'upload_date': document.upload_date.strftime('%Y-%m-%d')
        } for document in documents] if documents else None

def get_sensor_readings(patient_id):
    with get_session() as session:
        # 查询并按 received_time 列进行排序
        measurements = session.query(SensorReading) \
                              .filter_by(patient_id=patient_id) \
                              .order_by(SensorReading.received_time) \
                              .all()
        
        if measurements:
            # 返回格式化的结果
            return [
                {
                    'id': m.id,
                    'patient_id': m.patient_id,
                    'heartbeat': m.heartbeat,
                    'blood_oxygen': m.blood_oxygen,
                    'received_time': m.received_time.strftime('%Y-%m-%d %H:%M:%S')
                } for m in measurements
            ]
        else:
            return None

        
def get_patient_full_info(patient_id):
    patient_info = get_patient(patient_id)
    if patient_info:
        patient_data = patient_info[0]
        patient_data['medical_records'] = get_medical_records(patient_id)
        patient_data['medications'] = get_medications(patient_id)
        patient_data['tests_and_results'] = get_tests_and_results(patient_id)
        patient_data['appointments'] = get_appointments(patient_id)
        patient_data['medical_documents'] = get_medical_documents(patient_id)
        patient_data['sensor_readings'] = get_sensor_readings(patient_id)
        
        return patient_data
    else:
        return None
    
