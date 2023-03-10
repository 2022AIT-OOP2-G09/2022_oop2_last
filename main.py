import os
from flask import Flask, redirect
from flask import render_template, request

import sqlite3

from datetime import datetime
import pytz



# create the app
app = Flask(__name__)

username = ""
count = 0

@app.route('/')
def index():
    return render_template('index.html')

# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global username
        username = request.form.get('username')   # HTMLのフォームからユーザー名を取得
        password = request.form.get('password')   # HTMLのフォームからパスワードを取得


        dbname = 'ID_pass_database.db'
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        cur.execute('SELECT * FROM User_ID_Pass')
        count_name = 0
        count_pass = 0
        for row in cur:
            if row[1] == username:
                count_name=count_name+1
            if row[2] == password:
                count_pass=count_pass+1
        if count_name==0:
            print('このユーザ名は登録されておりません')
            cur.close()
            conn.close()
            count_name=0
            count_pass=0
            return render_template('login_UnregisteredName.html')
        elif count_name==1:
            if count_pass==0:
                print('パスワードが間違っています')
                cur.close()
                conn.close()
                count_name=0
                count_pass=0
                return render_template('login_IncorrectPass.html')
            else:
                print('ログイン完了しました')
                cur.close()
                count_name=0
                count_pass=0

                curs = conn.cursor()
                curs.execute('SELECT * FROM Tweet')
                data = curs.fetchall()
                datalist = []
                for i in range(len(data)):
                    datalist.insert(0, list(data[i]))
                print(data)
                curs.close()
                conn.close()
                return render_template('home.html', data = datalist)

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
            print('入力待ちです')
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
                return render_template('signUp_form_AlreadyName.html')
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
                return render_template('signUp_form_RegistrationDone.html')
        else:
            print('パスワードが一致していません')
            ##ret = {
            ##        "message": "パスワードが一致しません",##メッセージが出てないパスワードの不一致は確認
            ##    }
            return render_template('signUp_form_NotMatchPass.html') 
        
# 新規投稿ページ
@app.route('/post', methods=['POST', 'GET'])
def post():
    if request.method == 'POST':
        dbname = 'ID_pass_database.db'
        conn = sqlite3.connect(dbname)
        global count
        if count == 1:
            global username
            title = request.form.get('title')
            content = request.form.get('content')
            file = request.files['picture']    

            Spicture = f'static/pictures/{file.filename}'
            if Spicture != 'static/pictures/':
                file.save(os.path.join('static/pictures', file.filename))        
            created_at = datetime.now(pytz.timezone('Asia/Tokyo'))
            cur = conn.cursor()
            cur.execute('SELECT * FROM Tweet')
            
            cur.execute('INSERT INTO Tweet values(?,?,?,?,?)', (username,title,content,Spicture,created_at))

            conn.commit()
            cur.close()

        
        curs = conn.cursor()
        curs.execute('SELECT * FROM Tweet')
        data = curs.fetchall()
        datalist = []
        for i in range(len(data)):
            datalist.insert(0, list(data[i]))
        curs.close()
        conn.close()
        count = 0
        
        return render_template('home.html', data = datalist)    
    else:
        if username == "":
            dbname = 'ID_pass_database.db'
            conn = sqlite3.connect(dbname)
            curs = conn.cursor()
            curs.execute('SELECT * FROM Tweet')
            data = curs.fetchall()
            datalist = []
            for i in range(len(data)):
                datalist.insert(0, list(data[i]))
            curs.close()
            conn.close()
            return render_template('home.html', data = datalist) 
        else:
            count = 1 
            return render_template('post.html')

# 投稿リストページ
@app.route('/mypost')
def mypost():
    if username == "":
        dbname = 'ID_pass_database.db'
        conn = sqlite3.connect(dbname)
        curs = conn.cursor()
        curs.execute('SELECT * FROM Tweet')
        data = curs.fetchall()
        datalist = []
        for i in range(len(data)):
            datalist.insert(0, list(data[i]))
        curs.close()
        conn.close()
        return render_template('home.html', data = datalist) 
    else:
        dbname = 'ID_pass_database.db'
        conn = sqlite3.connect(dbname)
        curs = conn.cursor()
        curs.execute('SELECT * FROM Tweet')
        data = curs.fetchall()
        print(data)
        print(username)
        my_data = []
        for i in range(len(data)):
            if data[i][0] == username:
                my_data.append(list(data[i]))
                    
        print(my_data)
        curs.close()
        conn.close()
        return render_template('mypost.html', data = my_data, dataLen = len(my_data))

@app.route('/home')
def home():
    dbname = 'ID_pass_database.db'
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute('SELECT * FROM Tweet')
    data = curs.fetchall()
    datalist = []
    for i in range(len(data)):
        datalist.insert(0, list(data[i]))
    curs.close()
    conn.close()
    return render_template('home.html', data = datalist)

@app.route('/index')
def toppage():
    return render_template('index.html')
    
if __name__=='__main__':
    app.run()