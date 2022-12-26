from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user

from werkzeug.security import generate_password_hash, check_password_hash
import os

from datetime import datetime
import pytz

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ID_pass_database.db'
# configure the secret key
app.config['SECRET_KEY'] = os.urandom(24)
# initialize the app with the extendion
db.init_app(app)

# ログイン機能に必要な設定
login_manager = LoginManager()   # LoginManagerクラスのインスタンスを作成
# ログイン機能を持ったLoginManagerと今回のアプリを紐づける
login_manager.init_app(app)  

# 投稿DBの作成
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))

# ユーザーDBの作成
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)   # ユーザー名は重複なし
    password = db.Column(db.String(12), nullable=False)   # パスワードは12文字以内
    
# ログインに必要
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.POST.get('username')   # HTMLのフォームからユーザー名を取得
        password = request.POST.get('password')   # HTMLのフォームからパスワードを取得
        
        user = User.query.filter_by(username=username).first()   # ユーザー名が一致するユーザーを取得
    
        if check_password_hash(user.password, password):
            login_user(user)
            # ログインしたらトップページに移動
            return redirect('/index')
    
    else:   # request.method == 'GET'
        return render_template('login.html')

# TOPページ担当の人へ
@app.route('/index')
def toppage():
    return render_template('index.html')