from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route('/touroku', methods = ["POST","POST"])
def touroku():
    
    pass
