from flask import Flask, render_template, url_for, request, redirect
import pandas as pd
from openpyxl import load_workbook

app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        profiles = pd.read_excel('profiles.xlsx')
        
        role = request.form.get("role")
        username = request.form.get("username")
        password = request.form.get("password")
        if username in profiles["Username"].values:
            correct_password = profiles[profiles["Username"]==username].iloc[0]["Password"]
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
        profiles_wb = load_workbook('profiles.xlsx')
        profiles = pd.read_excel('profiles.xlsx')

        role = request.form.get("role")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        if username in profiles["Username"].values:
            return render_template("signup.html", error="Username taken")
        else:
            profiles_wb.active.append([role, username, password, email])
            profiles_wb.save('profiles.xlsx')

            return redirect(url_for("login"))

if __name__ == "__main__":
    app.run()