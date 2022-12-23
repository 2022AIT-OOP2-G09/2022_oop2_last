from flask import Flask, request, render_template
import sqlite3


#データベースにIDとパスワードを受付けて保存する処理
app = Flask(__name__)

@app.route('/touroku', methods = ["POST","POST"])
def touroku():
    username = request.form.get("id")
    password = request.form.get("password")
    password2 = request.form.get("password2")
    if password == password2:
        dbname = 'ID_pass_database.db'
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        cur.execute(f'INSERT INTO user_ID_Pass(name,pass) values({username},{password}),')
        conn.commit()
        cur.close()
        conn.close()

