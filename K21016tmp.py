from flask import Flask, request, render_template, jsonify
import sqlite3


#データベースにIDとパスワードを受付けて保存する処理
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False 

@app.route('/touroku', methods = ["POST","POST"])
def touroku():
    username = request.form.get("id")
    password = request.form.get("password")
    password2 = request.form.get("password2")
    if password == password2:
        dbname = 'ID_pass_database.db'
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        cur.execute('SELECT * FROM user_ID_Pass')
        count = 0
        for row in cur:
            if row[1] == username:
                count=count+1
        if count > 0:
            
            ret = {
                "message": "既に使用されている名前です",
            }
            return jsonify(ret)
        else:
            params = (username,password)
            cur.execute('INSERT INTO user_ID_Pass values(NULL,?,?)',params)
            conn.commit()
            cur.close()
            conn.close()
            ret = {
                "message": "登録が完了しました",
            }
            return jsonify(ret)
    else:
        ret = {
                "message": "パスワードが一致しません",
            }
        return jsonify(ret)

