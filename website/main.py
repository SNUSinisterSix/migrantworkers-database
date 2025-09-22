from flask import Flask, render_template, url_for, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        con = sqlite3.connect("profiles.db")
        cur = con.cursor()
        cur.execute("SELECT username from profiles;")
        username_list = cur.fetchall()
        
        role = request.form.get("role")
        username = request.form.get("username")
        password = request.form.get("password")

        if (username,) in username_list:
            cur.execute(f"SELECT role, password FROM profiles WHERE username='{username}';")
            data = cur.fetchone()
            correct_role = data[0]
            correct_password = data[1]
            if password == correct_password and role == correct_role:
                session['username'] = username
                session['role'] = role
                return redirect(url_for(f'{role}'))
            elif password != correct_password:
                return render_template("login.html", error = "Wrong password")
            elif role != correct_role:
                return render_template("login.html", error = "Wrong role")
        else:
            return render_template("login.html", error = "User not found")
        
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        con = sqlite3.connect("profiles.db")
        cur = con.cursor()
        cur.execute("SELECT username from profiles;")

        username_list = cur.fetchall()

        role = request.form.get("role")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        phone = request.form.get("phone")
        gender = request.form.get("gender")

        if (username, ) in username_list:
            return render_template("signup.html", error="Username taken")
        else:
            cur.execute(f"INSERT INTO profiles VALUES ('{role}', '{username}', '{password}', '{email}', '{phone}', '{gender}', 'None');")
            con.commit()

            return redirect(url_for("login"))
        
@app.route("/patient", methods=["GET"])
def patient():
    if session.get("role") != "patient":
        return redirect(url_for("login"))
    username = session['username']
    con = sqlite3.connect("profiles.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM profiles where username='{username}';")
    patients=cur.fetchone()
    return render_template("patient_portal.html", username=username, patients=patients)

@app.route("/doctor", methods=["GET"])
def doctor():
    if session.get("role") != "doctor":
        return redirect(url_for("login"))
    username = session['username']
    con = sqlite3.connect("profiles.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM profiles where role='patient';")
    patients=cur.fetchall()
    return render_template("doctor_portal.html", username=username, patients=patients)

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/upload_prescription", methods=["POST"])
def upload_prescription():
    return redirect(url_for("doctor"))

if __name__ == "__main__":
    app.run()