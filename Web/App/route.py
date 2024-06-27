from flask import render_template
from flask import Flask,render_template,request,flash,redirect,url_for, jsonify
import mysql.connector as myconn
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import os
import random
import bcrypt
import pandas as pd

global app
app = Flask(__name__,static_folder="static", static_url_path="/")


app.secret_key = os.urandom(20)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '請先登入'


dbConn = myconn.connect(
    host = 'localhost',
    user = 'pqc',
    password = '123456',
    database = 'server'
)

my_cursor = dbConn.cursor(buffered=True)
my_cursor.execute("select id from `users`;")
users=my_cursor.fetchall()
users=[i[0] for i in users]

id=""
pwd = ""

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

    my_cursor.execute(f"select password from `users` where id='{id}';")
    password = my_cursor.fetchone()
    if password and bcrypt.checkpw(pwd.encode(),password[0].encode()):
        user = User(id)
        user.is_authenticated = bcrypt.checkpw(pwd.encode(),password[0].encode())
        return user
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    global id,pwd
    if request.method == 'GET':
        return render_template("login.html")
    
    student = request.form['user_id']
    password = request.form['password']

    pwd = password
    id = student
    
    if not student or not password:
        error = '請輸入帳號或密碼'
        return render_template('login.html', error=error)

    my_cursor.execute(f"SELECT password FROM `users` WHERE id='{student}';")
    correct_password = my_cursor.fetchone()
    
    if correct_password and bcrypt.checkpw(password.encode(), correct_password[0].encode()):
        user = User(student)
        user.id = student
        login_user(user)
        flash(f'{student}！歡迎加入！')
        id = student
        return redirect(url_for('datepage'))

    error = '帳號或密碼錯誤'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    logout_user()
    flash(f'{id}！歡迎下次再來！')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form['username']
        account = request.form['account']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not username:
            return render_template('signup.html',error = "請輸入名稱")
        if not account:
            return render_template('signup.html',error = "請輸入帳號")
        if not password:
            return render_template('signup.html',error = "請輸入密碼")
        if len(password) < 8 or len(password) > 15:
            return render_template('signup.html',error = "密碼長度8~15")
        
        # 檢查密碼是否一致
        if password != confirm_password:
            return render_template('signup.html',error = "密碼和確認密碼不一致")

        # 檢查用戶名是否已存在
        my_cursor.execute(f"SELECT * FROM users WHERE id = '{account}'")
        if my_cursor.fetchone():
            return render_template('signup.html',error = "該帳號已被使用")
        # 將密碼進行雜湊處理
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # 將用戶信息插入數據庫
        try:
            sql = "INSERT INTO users (name,id, password) VALUES (%s,%s, %s)"
            val = (username, account,hashed_password)
            my_cursor.execute(sql, val)
            dbConn.commit()
            flash(f'{username}！註冊成功！')
            return redirect(url_for('login'))
        except myconn.Error as err:
            flash(f'註冊失敗：{err}', 'error')
            return render_template('signup.html',error = "註冊失敗")

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




@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html")


# # 獲取所有病人資料
# @app.route('/api/patients')
# def get_patients():
#     my_cursor.execute("SELECT * FROM patients")
#     patients = my_cursor.fetchall()
#     return jsonify([{
#         'id': patient[0],
#         'name': patient[1],
#         'age': patient[2],
#         'gender': patient[3],
#         'contact': patient[4],
#         'address': patient[5],
#         'medical_history': patient[6]
#     } for patient in patients])

# 獲取特定病人資料
@app.route('/api/patients')
def get_patient():
    my_cursor.execute(f"SELECT * FROM patients WHERE id = '{id}'")
    patient = my_cursor.fetchone()
    if patient:
        return jsonify({
            'id': patient[0],
            'name': patient[1],
            'age': patient[2],
            'gender': patient[3],
            'contact': patient[4],
            'address': patient[5],
            'medical_history': patient[6]
        })
    else:
        return jsonify({'message': 'Patient not found'}), 404

# 獲取健康總覽
@app.route('/api/health_overview/<string:patient_id>')
def get_health_overview(patient_id):
    my_cursor.execute(f"SELECT * FROM health_overview WHERE patient_id = '{patient_id}'")
    overview = my_cursor.fetchone()
    if overview:
        return jsonify({
            'id': overview[0],
            'patient_id': overview[1],
            'overview': overview[2]
        })
    else:
        return jsonify({'message': 'Health overview not found'}), 404

# 獲取病歷記錄
@app.route('/api/medical_records/<string:patient_id>')
def get_medical_records(patient_id):
    my_cursor.execute(f"SELECT * FROM medical_records WHERE patient_id = '{patient_id}'")
    records = my_cursor.fetchall()
    return jsonify([{
        'id': record[0],
        'patient_id': record[1],
        'record_date': record[2].strftime('%Y-%m-%d'),
        'record': record[3]
    } for record in records])

# 獲取藥物信息
@app.route('/api/medications/<string:patient_id>')
def get_medications(patient_id):
    my_cursor.execute(f"SELECT * FROM medications WHERE patient_id = '{patient_id}'")
    medications = my_cursor.fetchall()
    return jsonify([{
        'id': medication[0],
        'patient_id': medication[1],
        'medication_name': medication[2],
        'dosage': medication[3],
        'start_date': medication[4].strftime('%Y-%m-%d'),
        'end_date': medication[5].strftime('%Y-%m-%d') if medication[5] else None
    } for medication in medications])

# 獲取檢查和檢驗結果
@app.route('/api/tests_and_results/<string:patient_id>')
def get_tests_and_results(patient_id):
    my_cursor.execute(f"SELECT * FROM tests_and_results WHERE patient_id = '{patient_id}'")
    tests = my_cursor.fetchall()
    return jsonify([{
        'id': test[0],
        'patient_id': test[1],
        'test_date': test[2].strftime('%Y-%m-%d'),
        'test_type': test[3],
        'results': test[4]
    } for test in tests])

# 獲取預約管理
@app.route('/api/appointments/<string:patient_id>')
def get_appointments(patient_id):
    my_cursor.execute(f"SELECT * FROM appointments WHERE patient_id = '{patient_id}'")
    appointments = my_cursor.fetchall()
    return jsonify([{
        'id': appointment[0],
        'patient_id': appointment[1],
        'appointment_date': appointment[2].strftime('%Y-%m-%d'),
        'appointment_time': appointment[3].strftime('%H:%M:%S'),
        'doctor': appointment[4],
        'clinic': appointment[5]
    } for appointment in appointments])

# 獲取健康提醒
@app.route('/api/health_reminders/<string:patient_id>')
def get_health_reminders(patient_id):
    my_cursor.execute(f"SELECT * FROM health_reminders WHERE patient_id = '{patient_id}'")
    reminders = my_cursor.fetchall()
    return jsonify([{
        'id': reminder[0],
        'patient_id': reminder[1],
        'reminder': reminder[2],
        'reminder_date': reminder[3].strftime('%Y-%m-%d')
    } for reminder in reminders])

# 獲取醫療文件
@app.route('/api/medical_documents/<string:patient_id>')
def get_medical_documents(patient_id):
    my_cursor.execute(f"SELECT * FROM medical_documents WHERE patient_id = '{patient_id}'")
    documents = my_cursor.fetchall()
    return jsonify([{
        'id': document[0],
        'patient_id': document[1],
        'document_name': document[2],
        'document_path': document[3],
        'upload_date': document[4].strftime('%Y-%m-%d')
    } for document in documents])

# 獲取健康教育資源
@app.route('/api/health_education_resources')
def get_health_education_resources():
    my_cursor.execute("SELECT * FROM health_education_resources")
    resources = my_cursor.fetchall()
    return jsonify([{
        'id': resource[0],
        'resource_name': resource[1],
        'resource_link': resource[2],
        'description': resource[3]
    } for resource in resources])


