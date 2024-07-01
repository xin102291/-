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

    my_cursor.execute(f"select password from `users` where id='{id}';")
    password = my_cursor.fetchone()
    if password and bcrypt.checkpw(pwd.encode(),password[0].encode()):
        user = User(id)
        user.is_authenticated = bcrypt.checkpw(pwd.encode(),password[0].encode())
        return user
    return None


# 修改路由函數，在每次操作時開啟和關閉連接
@app.route('/login', methods=['GET', 'POST'])
def login():
    global id, pwd
    if request.method == 'GET':
        return render_template("login.html")
    
    student = request.form['user_id']
    password = request.form['password']

    pwd = password
    id = student
    
    if not student or not password:
        error = '請輸入帳號或密碼'
        return render_template('login.html', error=error)

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(buffered=True)
            cursor.execute(f"SELECT password FROM `users` WHERE id='{student}';")
            correct_password = cursor.fetchone()
            
            if correct_password and bcrypt.checkpw(password.encode(), correct_password[0].encode()):
                user = User(student)
                user.id = student
                login_user(user)
                flash(f'{student}！歡迎加入！')
                id = student
                return redirect(url_for('home'))

            error = '帳號或密碼錯誤'
            return render_template('login.html', error=error)
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




@app.route('/home', methods=['GET', 'POST'])
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
        return render_template("error.html", message="患者信息未找到")

