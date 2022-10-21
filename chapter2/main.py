"""
"""
from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = "some-super-random-secret-key"

USERS = {
    "test@example.net": "SecretPassword"
}


@app.route("/")
def index():
    # if user is logged in show them dashboard page
    if "email" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html.jinja2")


@app.route("/login", methods=["GET", "POST"])
def login():
    # if user is already logged in show dashboard
    if "email" in session:
        return redirect(url_for("dashboard"))
    # if email and password is submitted from login page
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"].strip()
        # if provided email is in our USERS dictionary
        # and value for that email is same password provided by user
        # then we create session so that user can use our dashboard
        app.logger.debug(email, password)
        if email in USERS and USERS[email] == password:
            session["email"] = email
            return redirect(url_for("dashboard"))

    return render_template("login.html.jinja2")


@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    # if user has not logged in using their email and password
    # redirect them back to login page so they can login from there
    if "email" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html.jinja2", username=session["email"])
