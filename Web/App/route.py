from flask import render_template
from flask import Flask,render_template,request,flash,redirect,url_for
import mysql.connector as myconn
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
import random
import bcrypt

global app
app = Flask(__name__,static_folder="static", static_url_path="/")


def index():
    return render_template('index.html') 
def dashboard():
    return render_template('dashboard.html') 

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
    pass

@login_manager.user_loader
def user_loader(student):
    if student not in users:
        return

    user = User()
    user.id = student
    return user


@login_manager.request_loader
def request_loader(request):
    
    if id not in users:
        return

    user = User()
    user.id = id
    my_cursor.execute(f"select password from `users` where id='{id}';")
    password = my_cursor.fetchone()
    user.is_authenticated = bcrypt.checkpw(pwd.encode(),password[0].encode())

    return user


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
        user = User()
        user.id = student
        login_user(user)
        flash(f'{student}！歡迎加入！')
        id = student
        iot_data = get_iot_data()
        return render_template("homepage.html", iot_data=iot_data)

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

@app.route("/homepage", methods=['GET', 'POST'])
@login_required
def homepage():
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

    return render_template("homepage.html", iot_data=iot_data, temp_min=temp_min, temp_max=temp_max, hum_min=hum_min, hum_max=hum_max)


def get_iot_data():
    # 生成隨機500筆資料
    iot_data = []
    for _ in range(500):
        temperature = round(random.uniform(20.0, 30.0), 2)
        humidity = round(random.uniform(40.0, 60.0), 2)
        iot_data.append({'temperature': temperature, 'humidity': humidity, 'date': '2024-06-01'})
    return iot_data