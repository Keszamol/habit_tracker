import os
import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for


app = Flask(__name__)
app.secret_key = 'dmEiud342HYPl2Eu2w5QB'

DATABASE = os.path.join(os.path.dirname(__file__), 'db', 'database.db')

@app.route("/")
def habits():
    return render_template("habits.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not username or not password or not confirm:
            render_template("error.html", message="Bitte fülle alle Felder aus.")
        elif password != confirm:
            render_template("error.html", message="Die Passwortbestätigung muss identisch sein.")
        else:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password,))
            conn.commit()
            conn.close()
            return redirect(url_for('habits'))
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")