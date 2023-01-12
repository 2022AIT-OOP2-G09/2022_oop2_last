from flask import Flask
from flask import jsonify
from flask import render_template, request, redirect


import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

import os
print(os.getcwd())

title = 'aB'
content = 'Ab'
picture = 'スクリーンショット 2022-11-10 14.07.13.png'
Spicture = f'/pictures/{picture}'
created_at = '2023-01-12 13:10:39.498340+09:00'
dbname = 'ID_pass_database.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute('SELECT * FROM Tweet')
        
cur.execute('INSERT INTO Tweet values(NULL,?,?,?,?)', (title,content,Spicture,created_at))
conn.commit()
cur.close()