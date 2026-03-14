from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

import webbrowser
import threading



def init_db():
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        department TEXT,
        role TEXT,
        salary INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "manager" and password == "1234":
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()

    conn.close()

    return render_template("dashboard.html", employees=employees)


@app.route("/add", methods=["GET","POST"])
def add_employee():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        department = request.form["department"]
        role = request.form["role"]
        salary = request.form["salary"]

        conn = sqlite3.connect("employees.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO employees(name,age,department,role,salary) VALUES(?,?,?,?,?)",
            (name, age, department, role, salary)
        )

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("add_employee.html")


def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)