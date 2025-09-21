from flask import Flask, render_template, url_for, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for("login"))

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
            cur.execute(f"SELECT password from profiles where username='{username}'")
            correct_password = cur.fetchone()[0]
            if password == correct_password:
                return render_template("user.html", username=username, role=role)
            else:
                return render_template("login.html", error = "Wrong password")
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

        if (username, ) in username_list:
            return render_template("signup.html", error="Username taken")
        else:
            cur.execute(f"INSERT INTO profiles VALUES ('{role}', '{username}', '{password}', '{email}');")
            con.commit()

            return redirect(url_for("login"))

if __name__ == "__main__":
    app.run()