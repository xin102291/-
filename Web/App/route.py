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

global app
app = Flask(__name__,static_folder="static", static_url_path="/")


app.secret_key = os.urandom(20)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '請先登入'


# 全局變量
users = []
dbConn = None
is_first_request = True
id = ""
pwd = ""
user_type = ""

@app.before_request
def before_request():
    global is_first_request, dbConn, users
    if is_first_request:
        dbConn = create_connection()
        if dbConn:
            print("Database connection established.")
            update_users()
            print("Users list initialized.")
        is_first_request = False

@app.teardown_appcontext
def teardown_appcontext(exception=None):
    global dbConn
    close_connection(dbConn)
    print("Database connection closed.")

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
def update_users():
    global users, dbConn
    if dbConn:
        try:
            cursor = dbConn.cursor(buffered=True)
            cursor.execute("SELECT id FROM `users`;")
            users = [i[0] for i in cursor.fetchall()]
        finally:
            cursor.close()





class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id

@login_manager.user_loader
def user_loader(student):
    if student not in users:
        return

    user = User(student)
    user.id = student
    return user


@login_manager.request_loader
def request_loader(request):
    
    if id not in users:
        return
    connection = create_connection()
    cursor = connection.cursor(buffered=True)
    cursor.execute(f"select password from `users` where id='{id}';")
    password = cursor.fetchone()
    if password and bcrypt.checkpw(pwd.encode(),password[0].encode()):
        user = User(id)
        user.is_authenticated = bcrypt.checkpw(pwd.encode(),password[0].encode())
        return user
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    global id,pwd,user_type 
    if request.method == 'GET':
        return render_template("login.html")
    
    user_type = request.form.get('user_type')
    user_id = request.form.get('user_id')
    password = request.form.get('password')
    id = user_id
    pwd = password

    if not user_id or not password:
        return render_template('login.html', error='請輸入帳號和密碼')


    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(buffered=True)
            # 首先檢查用戶是否存在於 users 表中
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()

            if not user_data:
                return render_template('login.html', error='帳號不存在')

            if not bcrypt.checkpw(password.encode(),user_data[2].encode()):
                return render_template('login.html', error='密碼錯誤')

            # 檢查用戶是否存在於相應的表中（patients 或 doctors）
            table_name = 'patients' if user_type == 'patients' else 'doctors'
            cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (user_id,))
            specific_user_data = cursor.fetchone()

            if not specific_user_data:
                if user_type == "doctors":
                    return render_template('login.html', error='此帳號不是醫生')
                else:
                    return render_template('login.html', error='此帳號不是病患')

            # 登入成功
            user = User(user_id)
            user.id = id
            login_user(user)
            
            # 根據用戶類型重定向到不同的首頁
            if user_type == 'patients':
                return redirect(url_for('home'))
            else:
                return redirect(url_for('doctor_home'))

        finally:
            cursor.close()
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
    global dbConn
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form['username']
        account = request.form['account']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not username or not account or not password:
            return render_template('signup.html', error="請填寫所有欄位")
        if len(password) < 8 or len(password) > 15:
            return render_template('signup.html', error="密碼長度8~15")
        if password != confirm_password:
            return render_template('signup.html', error="密碼和確認密碼不一致")

        if account in users:
            return render_template('signup.html', error="該帳號已被使用")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        if dbConn:
            try:
                cursor = dbConn.cursor()
                sql = "INSERT INTO users (name, id, password) VALUES (%s, %s, %s)"
                val = (username, account, hashed_password)
                cursor.execute(sql, val)
                dbConn.commit()
                update_users()  # 更新 users 列表
                flash(f'{username}！註冊成功！')
                return redirect(url_for('login'))
            except myconn.Error as err:
                flash(f'註冊失敗：{err}', 'error')
                return render_template('signup.html', error="註冊失敗")
            finally:
                cursor.close()

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

