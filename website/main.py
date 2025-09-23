from flask import Flask, render_template, url_for, request, redirect, session, jsonify
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
            cur.execute(f"SELECT role, password, id FROM profiles WHERE username='{username}';")
            data = cur.fetchone()
            correct_role = data[0]
            correct_password = data[1]
            id = data[2]
            if password == correct_password and role == correct_role:
                session['username'] = username
                session['role'] = role
                session['id'] = id
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
            cur.execute(f"INSERT INTO profiles (id, role, username, password, email, phone, gender, insurance) VALUES (NULL, '{role}', '{username}', '{password}', '{email}', '{phone}', '{gender}', NULL);")
            con.commit()

            return redirect(url_for("login"))
        
@app.route("/patient", methods=["GET", ])
def patient():
    if session.get("role") not in  ("patient", "mentor"):
        return redirect(url_for("login"))
    username = session['username']
    con = sqlite3.connect("profiles.db")
    cur = con.cursor()
    cur.execute(f"SELECT id, role, username, email, phone, gender, insurance FROM profiles where id='{session['id']}';")
    patients = cur.fetchone()
    prescriptions = [("Dr. Ananya Sharma", "Cardiologist", "2025-09-24", "Active"), ("Dr. Rohan Verma", "General Physician", "2025-08-17", "Active"), ("Dr. Priya Singh", "Dermatologist", "2025-08-21", "Expired"), ("Dr. Ananya Sharma", "Cardiologist", "2025-06-10", "Expired")]
    return render_template("patient_portal.html", username=patients[2], patients=patients, prescriptions=prescriptions)

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

@app.route("/insurance", methods=["GET"])
def insurance():
    if session.get("role") != "insurance":
        return redirect(url_for("login"))
    username = session['username']
    con = sqlite3.connect("profiles.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM profiles where insurance='{username}';")
    patients=cur.fetchall()
    return render_template("insurance_portal.html", username=username, patients=patients)

@app.route("/mentor", methods=["GET"])
def mentor():
    if session.get("role") != "mentor":
        return redirect(url_for("login"))
    username = session['username']
    return render_template("mentor_portal.html", username=username)


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/upload_prescription", methods=["POST"])
def upload_prescription():
    return redirect(url_for("doctor"))

@app.route("/patient_search", methods=["POST"])
def patient_search():
    data = request.get_json()
    con = sqlite3.connect("profiles.db")
    cur = con.cursor()
    cur.execute(f"SELECT * from profiles where id = {data['id']}")
    result = cur.fetchone()
    if result:
        return jsonify({"result":result})
    else:
        return jsonify({"result":None})

if __name__ == "__main__":
    app.run()