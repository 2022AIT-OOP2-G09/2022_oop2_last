from flask import Flask
from flask import jsonify
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

from datetime import datetime
import time
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
class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))

# ユーザーDBの作成
class User_ID_Pass(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)   # ユーザー名は重複なし
    password = db.Column(db.String(12), nullable=False)   # パスワードは12文字以内
    
# ログインに必要
@login_manager.user_loader
def load_user(user_id):
    return User_ID_Pass.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('login.html')

# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.POST.get('username')   # HTMLのフォームからユーザー名を取得
        password = request.POST.get('password')   # HTMLのフォームからパスワードを取得
        
        user = User_ID_Pass.query.filter_by(username=username).first()   # ユーザー名が一致するユーザーを取得
    
        try:
            if check_password_hash(user.password, password):
                login_user(user)
                # ログインしたらトップページに移動
                return redirect('/index')
        except AttributeError:   # ユーザーが存在しない場合、再びログインページに戻る
            return render_template('login.html')
    
    else:   # request.method == 'GET'
        return render_template('login.html')

@app.route('/signUp_form', methods = ["GET","POST"])
def touroku():
    if request.method == 'GET':
        print('ページ移動しました')
        return render_template('signUp_form.html')
    elif request.method == 'POST':
        print('入力を受け付けました')
        username = request.form.get("id")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        print(username)
        print(password)
        print(password2)
        if password == password2:
            dbname = 'ID_pass_database.db'
            conn = sqlite3.connect(dbname)
            cur = conn.cursor()
            cur.execute('SELECT * FROM User_ID_Pass')
            count = 0
            for row in cur:
                if row[1] == username:
                    count=count+1
            if count > 0:
                print('この名前は使われています') 
                ##ret = {
                ##        "message": "既に使用されている名前です",##メッセージが出てないパスワードの不一致は確認
                ##}
                cur.close()
                conn.close()
                return render_template('signUp_form.html')
            else:
                params = (username,password)
                cur.execute('INSERT INTO User_ID_Pass values(NULL,?,?)',params)
                print('登録が完了しました')
                conn.commit()
                cur.close()
                conn.close()
                ##ret = {
                ##        "message": "登録が完了しました",##メッセージが出てないパスワードの不一致は確認
                ##    }
                return render_template('login.html')
        else:
            print('パスワードが一致していません')
            ##ret = {
            ##        "message": "パスワードが一致しません",##メッセージが出てないパスワードの不一致は確認
            ##    }    
            return render_template('login.html') 
    



# TOPページ担当の人へ
@app.route('/index')
def toppage():
    return render_template('index.html')



if __name__=='__main__':
    app.run(debug=True)
