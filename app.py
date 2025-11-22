from flask import Flask, render_template, request, redirect, session
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import date

app = Flask(__name__)
app.secret_key = "mysecretkey123"

# ---------- DATABASE SETUP ----------

def init_db():
    if not os.path.exists("database.db"):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("""
            CREATE TABLE users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        """)

        c.execute("""
            CREATE TABLE students(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                roll TEXT UNIQUE
            )
        """)

        c.execute("""
            CREATE TABLE attendance(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll TEXT,
                date TEXT,
                status TEXT
            )
        """)

        c.execute("""
            CREATE TABLE marks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll TEXT,
                subject TEXT,
                marks INTEGER
            )
        """)

        # Default Teacher Login
        c.execute("INSERT INTO users(username, password, role) VALUES(?,?,?)",
                  ("teacher1", generate_password_hash("teacher123"), "teacher"))

        conn.commit()
        conn.close()

init_db()


# ---------- HOME PAGE ----------
@app.route("/")
def home():
    return render_template("home.html")


# ---------- TEACHER LOGIN ----------
@app.route("/teacher-login", methods=["GET", "POST"])
def teacher_login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND role='teacher'", (u,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], p):
            session["teacher"] = u
            return redirect("/teacher-dashboard")
        else:
            return "Invalid Teacher Login"

    return render_template("teacher_login.html")


# ---------- STUDENT LOGIN ----------
@app.route("/student-login", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        roll = request.form["roll"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE roll=?", (roll,))
        st = c.fetchone()
        conn.close()

        if st:
            session["student"] = roll
            return redirect("/student-dashboard")
        else:
            return "Student not found"

    return render_template("student_login.html")


# ---------- TEACHER DASHBOARD ----------
@app.route("/teacher-dashboard")
def teacher_dashboard():
    if "teacher" not in session:
        return redirect("/teacher-login")
    return render_template("teacher_dashboard.html")


# ---------- ADD STUDENT ----------
@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    if "teacher" not in session:
        return redirect("/teacher-login")

    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO students(name, roll) VALUES(?, ?)", (name, roll))
        conn.commit()
        conn.close()

        return redirect("/view-students")

    return render_template("add_student.html")


# ---------- VIEW STUDENTS ----------
@app.route("/view-students")
def view_students():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    data = c.fetchall()
    conn.close()
    return render_template("view_students.html", students=data)


# ---------- MARK ATTENDANCE ----------
@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    if "teacher" not in session:
        return redirect("/teacher-login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if request.method == "POST":
        today = str(date.today())
        for roll, status in request.form.items():
            if roll != "submit":
                c.execute("INSERT INTO attendance(roll, date, status) VALUES(?,?,?)",
                          (roll, today, status))

        conn.commit()
        conn.close()
        return redirect("/teacher-dashboard")

    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return render_template("attendance.html", students=students)


# ---------- ADD MARKS ----------
@app.route("/marks", methods=["GET", "POST"])
def marks():
    if "teacher" not in session:
        return redirect("/teacher-login")

    if request.method == "POST":
        subject = request.form["subject"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        for roll, marks in request.form.items():
            if roll != "subject":
                c.execute("INSERT INTO marks(roll, subject, marks) VALUES(?,?,?)",
                          (roll, marks))

        conn.commit()
        conn.close()
        return redirect("/teacher-dashboard")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()

    return render_template("marks.html", students=students)


# ---------- STUDENT DASHBOARD ----------
@app.route("/student-dashboard")
def student_dashboard():
    if "student" not in session:
        return redirect("/student-login")

    roll = session["student"]
    return render_template("student_dashboard.html", roll=roll)


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


#----------ATTENDANCE CHART API---------
@app.route("/attendance-chart-api")
def attendance_chart_api():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Fetch students
    c.execute("SELECT name, roll FROM students")
    students = c.fetchall()

    chart_data = {"labels": [], "data": []}

    for st in students:
        name = st[0]
        roll = st[1]

        c.execute("SELECT COUNT(*) FROM attendance WHERE roll=?", (roll,))
        total = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM attendance WHERE roll=? AND status='present'", (roll,))
        present = c.fetchone()[0]

        percent = (present / total * 100) if total > 0 else 0

        chart_data["labels"].append(name)
        chart_data["data"].append(percent)

    conn.close()
    return chart_data

#------------TEACHER REPORT------------
@app.route("/teacher-report")
def teacher_report():
    if "teacher" not in session:
        return redirect("/teacher-login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Fetch all students
    c.execute("SELECT * FROM students")
    students = c.fetchall()

    # Attendance percentage calculation
    attendance_data = []
    for st in students:
        roll = st[2]

        c.execute("SELECT COUNT(*) FROM attendance WHERE roll=?", (roll,))
        total = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM attendance WHERE roll=? AND status='present'", (roll,))
        present = c.fetchone()[0]

        percentage = (present / total * 100) if total > 0 else 0
        attendance_data.append([st[1], percentage])

    conn.close()

    return render_template("report_teacher.html", attendance_data=attendance_data)


if __name__== "__main__":
    app.run(debug=True)