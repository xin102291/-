from flask import render_template
from flask import Flask,render_template,request,flash,redirect,url_for, jsonify
import mysql.connector as myconn
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import os
import random
import bcrypt
import pandas as pd
from mysql.connector import Error
from App.patient_full_info import *
from App.key import *
from App.id_card import *
from App.asym import *
import logging

global app
app = Flask(__name__,static_folder="static", static_url_path="/")
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app.secret_key = os.urandom(20)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'



# 全局變量
users = []
is_first_request = True
id = ""
pwd = ""
q = 999999937
n = 3
scale = 10000
bound = 5
A_size = 8
B_size = 32
sk_size = 12

E = authentication(n, q, bound, scale, A_size, B_size, sk_size)

@app.before_request
def before_request():
    global is_first_request, dbConn, users
    if is_first_request:
        dbConn = create_connection()
        if dbConn:
            print("Database connection established.")
            update_users(dbConn)
            print("Users list initialized.")
        is_first_request = False

# 數據庫連接函數
def create_connection():
    try:
        connection = myconn.connect(
            host='localhost',
            user='pqc',
            password='123456',
            database='server'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# 關閉數據庫連接函數
def close_connection(connection):
    if connection:
        connection.close()

# 更新 users 列表的函數
def update_users(dbConn):
    global users
    if dbConn:
        try:
            cursor = dbConn.cursor(buffered=True)
            cursor.execute("SELECT id FROM `patients`;")
            users = [i[0] for i in cursor.fetchall()]
        finally:
            cursor.close()

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id

@login_manager.user_loader
def user_loader(patient):
    if patient not in users:
        return

    user = User(patient)
    user.id = patient
    return user


@login_manager.request_loader
def request_loader(request):
    
    if id not in users:
        return
    connection = create_connection()
    cursor = connection.cursor(buffered=True)
    (pk, sk) = asym_key(id, pwd, n, q, bound, A_size, B_size, sk_size)
    cursor.execute("SELECT pk FROM patients WHERE id = %s", (id,))
    pk = cursor.fetchone()[0]
    print("id: ",id)
    print("pk: ",pk)
    if Authentication(pk,sk):
        print("成!")
        user = User(id)
        user.is_authenticated = True
        return user
    return None


def Authentication(pk,sk):
    m = random.randrange(0,9999,1)
    # 私鑰產生簽章
    c = E.encrypt(m, pk, sk)
    # 公鑰驗證簽章
    p = E.decrypt(c, pk)
    # 驗證原本生成的訊息與簽章是否一致
    if m == p:
        return 1
    else:
        return 0


@app.route('/login', methods=['GET', 'POST'])
def login():
    global id,pwd
    if request.method == 'GET':
        return render_template("login.html")
    
    user_id = request.form.get('user_id')
    hashed_password = request.form.get('hashed_password')
    id = user_id
    pwd = hashed_password

    if not user_id or not hashed_password:
        return render_template('login.html', error='請輸入帳號和密碼')


    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(buffered=True)
            # 首先檢查用戶是否存在於 users 表中
            cursor.execute("SELECT * FROM patients WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()

            if not user_data:
                return render_template('login.html', error='帳號不存在')
            (pk, sk) = asym_key(id, hashed_password, n, q, bound, A_size, B_size, sk_size)
            cursor.execute("SELECT pk FROM patients WHERE id = %s", (user_id,))
            pk = cursor.fetchone()[0]
            print("pk:",pk)
            if Authentication(pk,sk):
                # 登入成功
                user = User(user_id)
                user.id = user_id
                login_user(user)
                print("成功")
                return jsonify({"success": True, "message": "註冊成功！"}), 200
                # return redirect(url_for('home'))
            else:
                return jsonify({"error": "帳號或密碼輸入錯誤"}), 400
        finally:
            close_connection(connection)

    error = '無法連接到數據庫'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    logout_user()
    flash(f'{id}！歡迎下次再來！')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global n,q,bound,A_size,B_size,sk_size

    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        
        patient_id = request.form.get('id')
        name = request.form.get('name')
        hashed_password = request.form.get('hashed_password')
        age = request.form.get('age')
        gender = request.form.get('gender')
        contact = request.form.get('contact')
        address = request.form.get('address')
        medical_history = request.form.get('medical_history')
        #檢查id是否輸入錯誤
        if checkID(patient_id) == 0:
            return jsonify({"error": "身分證字號輸入錯誤"}), 400
        # 檢查ID是否已存在
        connection = create_connection()
        
        if connection:
            try:
                cursor = connection.cursor(buffered=True)
                cursor.execute("SELECT id FROM patients WHERE id = %s", (patient_id,))
                if cursor.fetchone():
                    cursor.close()
                    print("該病患ID已被使用")
                    return jsonify({"error": "該病患ID已被使用"}), 400
                # 建立公鑰
                print(hashed_password)
                (pk, sk) = asym_key(patient_id, hashed_password, n, q, bound, A_size, B_size, sk_size)
                # 插入病患資料
                sql_patient = """
                INSERT INTO patients (id, name, age, gender, contact, address, medical_history,pk) 
                VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
                """
                val_patient = (patient_id, name, age, gender, contact, address, medical_history,pk)
                cursor.execute(sql_patient, val_patient)

                connection.commit()
                return jsonify({"success": True, "message": f"{name}！註冊成功！"}), 200
            except Exception as e:
                connection.rollback()
                return jsonify({"error": f"註冊失敗：{str(e)}"}), 500
            finally:
                close_connection(connection)
               

        return render_template('signup.html', error="無法連接到數據庫")

@app.route("/datepage", methods=['GET', 'POST'])
@login_required
def datepage():
    temp_min = request.args.get('temp_min')
    temp_max = request.args.get('temp_max')
    hum_min = request.args.get('hum_min')
    hum_max = request.args.get('hum_max')
    iot_data = get_iot_data()

    if temp_min or temp_max or hum_min or hum_max:
        filtered_data = []
        for item in iot_data:
            if temp_min and float(item['temperature']) < float(temp_min):
                continue
            if temp_max and float(item['temperature']) > float(temp_max):
                continue
            if hum_min and float(item['humidity']) < float(hum_min):
                continue
            if hum_max and float(item['humidity']) > float(hum_max):
                continue
            filtered_data.append(item)
        iot_data = filtered_data

    return render_template("datepage.html", iot_data=iot_data, temp_min=temp_min, temp_max=temp_max, hum_min=hum_min, hum_max=hum_max)

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    temp_min = request.args.get('temp_min')
    temp_max = request.args.get('temp_max')
    hum_min = request.args.get('hum_min')
    hum_max = request.args.get('hum_max')
    iot_data = get_iot_data()
    if temp_min or temp_max or hum_min or hum_max:
        filtered_data = []
        for item in iot_data:
            if temp_min and float(item['temperature']) < float(temp_min):
                continue
            if temp_max and float(item['temperature']) > float(temp_max):
                continue
            if hum_min and float(item['humidity']) < float(hum_min):
                continue
            if hum_max and float(item['humidity']) > float(hum_max):
                continue
            filtered_data.append(item)
        iot_data = filtered_data

    return render_template("dashboard.html", iot_data=iot_data, temp_min=temp_min, temp_max=temp_max, hum_min=hum_min, hum_max=hum_max)

def get_iot_data():
    # 生成隨機500筆資料
    iot_data = []
    for _ in range(500):
        temperature = round(random.uniform(20.0, 30.0), 2)
        humidity = round(random.uniform(40.0, 60.0), 2)
        iot_data.append({'temperature': temperature, 'humidity': humidity, 'date': '2024-06-01'})
    return iot_data



# 載入健康報告數據
health_data = pd.read_csv('Web\App\health_report.csv', encoding='utf-8')

@app.route('/health', methods=['GET', 'POST'])
@login_required
def health():
    return render_template("health.html")

@app.route('/api/data')
def get_data():
    data = health_data.to_dict(orient='records')
    return jsonify(data)




@app.route('/home')
@login_required
def home():
    global id
    patient_info = get_patient(id)
    
    if patient_info:
        patient_name = patient_info[0]['name']
        # 獲取健康提醒
        reminders = get_health_reminders(id)
        # 獲取預約看診日期
        appointments = get_appointments(id)
        return render_template("home.html", 
                               name=patient_name, 
                               reminders=reminders,
                               appointments=appointments)
    else:
        # 處理患者信息不存在的情況
        return render_template("home.html", name="患者信息未找到")

@app.route('/patient_personal_info')
def patient_personal_info():
    global id
    patient_info = get_patient(id)
    if patient_info:
        patient = patient_info[0]
        return render_template('patient_personal_info.html', patient=patient)
    
@app.route('/patient_test_results')
def patient_test_results():
    global id
    patient_info = get_patient(id)
    if patient_info:    
        patient = patient_info[0]
        tests_results = get_tests_and_results(id)
        return render_template('patient_test_results.html', patient=patient, tests_results=tests_results)
    

@app.route('/patient_medical_records')
def patient_medical_records():
    global id
    patient_info = get_patient(id)
    if patient_info:
        patient = patient_info[0]['name']
        records = get_medical_records(id)
        return render_template('patient_medical_records.html', patient_name=patient, medical_records=records)
    
@app.route('/patient_medications')
def patient_medications():
    global id
    patient_info = get_patient(id)
    if patient_info:
        patient = patient_info[0]['name']
        medications = get_medications(id)
        return render_template('patient_medications.html', patient_name=patient, medications=medications)
    
@app.route('/patient_medical_documents')
@login_required
def patient_medical_documents():
    global id
    patient_info = get_patient(id)
    if patient_info:
        patient = patient_info[0]['name']
        documents = get_medical_documents(id)
    return render_template('patient_medical_documents.html', patient_name=patient,documents=documents)

