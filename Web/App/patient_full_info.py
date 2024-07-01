import mysql.connector as myconn
from mysql.connector import pooling
from contextlib import contextmanager
from datetime import datetime

# 創建連接池
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host='localhost',
    user='pqc',
    password='123456',
    database='server'
)

@contextmanager
def get_cursor():
    connection = connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)
    try:
        yield cursor
        connection.commit()
    finally:
        cursor.close()
        connection.close()

# 獲取患者資訊
def get_patient(id):
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM patients WHERE id = %s", (id,))
        patient = cursor.fetchone()
        if patient:
            return [{
                'id': patient[0],
                'name': patient[1],
                'age': patient[2],
                'gender': patient[3],
                'contact': patient[4],
                'address': patient[5],
                'medical_history': patient[6]
            }]
        else:
            return None
    
# 獲取健康提醒
def get_health_reminders(patient_id):
    with get_cursor() as cursor:
        cursor.execute(f"SELECT * FROM health_reminders WHERE patient_id = %s", (patient_id,))
        reminders = cursor.fetchall()
        if reminders:
            return [{
                'id': reminder[0],
                'patient_id': reminder[1],
                'reminder': reminder[2],
                'reminder_date': reminder[3].strftime('%Y-%m-%d')
            } for reminder in reminders]
        else:
            return None

# 獲取健康總覽
def get_health_overview(patient_id):
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM health_overview WHERE patient_id = %s", (patient_id,))
        overview = cursor.fetchone()
        if overview:
            return {
                'id': overview[0],
                'patient_id': overview[1],
                'overview': overview[2]
            }
        else:
            return None

# 獲取病歷記錄
def get_medical_records(patient_id):
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM medical_records WHERE patient_id = %s", (patient_id,))
        records = cursor.fetchall()
        return [{
            'id': record[0],
            'patient_id': record[1],
            'record_date': record[2].strftime('%Y-%m-%d'),
            'record': record[3]
        } for record in records] if records else None

# 獲取藥物信息
def get_medications(patient_id):
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM medications WHERE patient_id = %s", (patient_id,))
        medications = cursor.fetchall()
        return [{
            'id': medication[0],
            'patient_id': medication[1],
            'medication_name': medication[2],
            'dosage': medication[3],
            'start_date': medication[4].strftime('%Y-%m-%d'),
            'end_date': medication[5].strftime('%Y-%m-%d') if medication[5] else None
        } for medication in medications] if medications else None

# 獲取檢查和檢驗結果
def get_tests_and_results(patient_id):
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM tests_and_results WHERE patient_id = %s", (patient_id,))
        tests = cursor.fetchall()
        return [{
            'id': test[0],
            'patient_id': test[1],
            'test_date': test[2].strftime('%Y-%m-%d'),
            'test_type': test[3],
            'results': test[4]
        } for test in tests] if tests else None


def get_appointments(patient_id):
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM appointments WHERE patient_id = %s", (patient_id,))
        appointments = cursor.fetchall()
        return [{
            'id': appointment[0],
            'patient_id': appointment[1],
            'appointment_date': appointment[2].strftime('%Y-%m-%d') if isinstance(appointment[2], datetime) else str(appointment[2]),
            'appointment_time': appointment[3].strftime('%H:%M:%S') if isinstance(appointment[3], datetime) else str(appointment[3]),
            'doctor': appointment[4],
            'clinic': appointment[5]
        } for appointment in appointments] if appointments else None

# 獲取醫療文件
def get_medical_documents(patient_id):
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM medical_documents WHERE patient_id = %s", (patient_id,))
        documents = cursor.fetchall()
        return [{
            'id': document[0],
            'patient_id': document[1],
            'document_name': document[2],
            'document_path': document[3],
            'upload_date': document[4].strftime('%Y-%m-%d')
        } for document in documents] if documents else None

# 獲取健康教育資源
def get_health_education_resources():
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM health_education_resources")
        resources = cursor.fetchall()
        return [{
            'id': resource[0],
            'resource_name': resource[1],
            'resource_link': resource[2],
            'description': resource[3]
        } for resource in resources] if resources else None

# 獲取患者完整資訊
def get_patient_full_info(patient_id):
    patient_info = get_patient(patient_id)
    if patient_info:
        patient_data = patient_info[0]
        patient_data['health_overview'] = get_health_overview(patient_id)
        patient_data['medical_records'] = get_medical_records(patient_id)
        patient_data['medications'] = get_medications(patient_id)
        patient_data['tests_and_results'] = get_tests_and_results(patient_id)
        patient_data['appointments'] = get_appointments(patient_id)
        patient_data['medical_documents'] = get_medical_documents(patient_id)
        return patient_data
    else:
        return None