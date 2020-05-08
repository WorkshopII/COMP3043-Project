# Server-side code here.
# If you cannot understand the code below, go to 2.Flask-Templates.

# © 2019-current,
# authors at Computer Science and Technology,
# Division of Science and Technology,
# BNU-HKBU United International College
import datetime
from flask import Flask, render_template, request, redirect
from collections import deque
from wtforms import Form, BooleanField, StringField, PasswordField, validators, DateField
import pymysql
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = b'my-secret-key'   # !!! temp secret key, will be changed in production environment
app.config['TEMPLATES_AUTO_RELOAD'] = True
login_manager.login_view = 'login'

# launch the browser when flask runs
import threading, webbrowser
port = 5000
url = "http://127.0.0.1:{0}".format(port)
threading.Timer(1.25, lambda: webbrowser.open(url) ).start()
app.run(port=port, debug=False)

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.username.data == 'admin' and form.password.data == 'admin':
            message = '登录成功'
            # Create an object of the authorized user class.
            test_admin_user = SalesAdmin('admin')
            # Pass the user object ot `flask-login` method `login_user()`.
            login_user(test_admin_user)
            # Exit this function by redirect to the next page.
            return redirect('./')
        else:
            message = '登录失败'
        # otherwise, do something else
    else:
        message = '请输入用户名和密码（测试账号: admin, 密码：admin)'
    return render_template('login.html', message=message)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template('admin.html')

@app.route('/add_customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    return render_template('add_customer.html')

@app.route('/add_goods', methods=['GET', 'POST'])
@login_required
def add_goods():
    return render_template('add_goods.html')

@app.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    return render_template('buy.html')

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    return render_template('change_password.html')

@app.route('/customer', methods=['GET', 'POST'])
@login_required
def customer():
    return render_template('customer.html')

@app.route('/edit_customer', methods=['GET', 'POST'])
@login_required
def edit_customer():
    return render_template('edit_customer.html')

@app.route('/edit_goods', methods=['GET', 'POST'])
@login_required
def edit_goods():
    return render_template('edit_goods.html')

@app.route('/goods', methods=['GET', 'POST'])
@login_required
def goods():
    return render_template('goods.html')

@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    return render_template('history.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/register_validate', methods=['GET', 'POST'])
def register_validate():
    return render_template('register_validate.html')

@app.route('/remove_customer', methods=['GET', 'POST'])
@login_required
def remove_customer():
    return render_template('remove_customer.html')

@app.route('/remove_goods', methods=['GET', 'POST'])
@login_required
def remove_goods():
    return render_template('remove_goods.html')

@app.route('/return_goods', methods=['GET', 'POST'])
@login_required
def return_goods():
    return render_template('return_goods.html')
    
class RegistrationForm(Form):   # not complete yet
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class LoginForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')

class SalesAdmin(UserMixin):
    """User class for flask-login"""
    def __init__(self, id):
        self.id = id
        self.name = 'admin'
        self.password = 'admin'

@login_manager.user_loader
def load_user(user_id):
    return SalesAdmin(user_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    # Redirect to homepage
    return redirect('login')

class DatabaseOperations():
    # Fill in the information of your database server.
    __db_url = 'localhost'
    __db_username = 'root'
    __db_password = ''
    __db_name = 'project'
    __db = ''
    def __init__(self):
        """Connect to database when the object is created."""
        self.__db = self.db_connect()
    def __del__(self):
        """Disconnect from database when the object is destroyed."""
        self.__db.close()
    def db_connect(self):
        self.__db = pymysql.connect(self.__db_url, self.__db_username,
        self.__db_password, self.__db_name)
        return self.__db

    def query_template(self, parameter): # for each query, write a new function in this class
        cursor = self.__db.cursor()
        cursor.execute('SELECT * FROM users')
        result = cursor.fetchone()
        return result