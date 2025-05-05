from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def habits():
    return render_template("habits.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")