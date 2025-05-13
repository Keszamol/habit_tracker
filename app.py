from flask import Flask, render_template, redirect, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'dmEiud342HYPl2Eu2w5QB'

DATABASE = os.path.join(os.path.dirname(__file__), 'db', 'database.db')

@app.route("/", methods=["GET","POST"])
def habits():
    if not session:
        return redirect(url_for('login'))
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM habits").fetchall() 

    if request.method == "POST":
        habit = request.form.get("habit")
        description = request.form.get("description")
        date = request.form.get("date")
        interval = request.form.get("interval")

        if not habit or not date or not interval:
            return render_template("error.html", message="Bitte Fülle alle Felder aus. Die Beschreibung bleibt optional.")

        elif not interval.isdigit():
            return render_template("error.html", message="Der Intervall muss eine Zahl sein.")
        
        elif int(interval) < 1 or int(interval) > 365:
            return render_template("error.html", message="Der Intervall darf nicht kleiner als 1 oder größer als 365 sein.")
        
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO habits (habit, description, date, interval) VALUES (?, ?, ?, ?)',
                           (habit, description, date, interval))
            conn.commit()
        return redirect(url_for('habits'))

    return render_template("habits.html", rows=rows)

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not username or not password or not confirm:
            return render_template("error.html", message="Bitte fülle alle Felder aus.")
        elif password != confirm:
            return render_template("error.html", message="Die Passwortbestätigung muss identisch sein.")

        hashed_password = generate_password_hash(password)

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()      
            cursor.execute('SELECT username FROM users WHERE username=?', (username,))
            db_username = cursor.fetchone()

        if db_username:
            return render_template("error.html", message="Username bereits vergeben.")
        else:            
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password,))
                conn.commit()   
            return redirect(url_for('login'))
        
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template("error.html", message="Bitte gib deinen Username an.")
        elif not password:
            return render_template("error.html", message="Bitte gib dein Passwort ein.")
        
        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username=?', (username,))
            row = cursor.fetchone()

        if row and check_password_hash(row["password"], password):
            session["user_id"] = row["id"]
            return redirect(url_for('habits'))  
        else:
            return render_template("error.html", message="Username oder Passwort ist nicht korrekt.")

    return render_template("login.html")