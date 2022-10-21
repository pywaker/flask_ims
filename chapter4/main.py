"""
"""
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user

from .user import User

app = Flask(__name__)
app.secret_key = "some-super-random-secret-key"
login_manager = LoginManager()

# initialize flask plugins
login_manager.init_app(app)
login_manager.login_view = "login"

USERS = {
    "test@example.net": "SecretPassword"
}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if user_id in USERS else None


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html.jinja2'), 404


@app.route("/")
def index():
    return render_template("index.html.jinja2")


@app.route("/login", methods=["GET", "POST"])
def login():
    # if email and password is submitted from login page
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"].strip()
        # if provided email is in our USERS dictionary
        # and value for that email is same password provided by user
        # then we create session so that user can use our dashboard
        if email in USERS and USERS[email] == password:
            # session["email"] = email
            login_user(User(email))
            next = request.args.get('next')
            return redirect(next or url_for('dashboard'))
        else:
            return render_template("login.html.jinja2", message="Invalid Username or Password")

    return render_template("login.html.jinja2")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html.jinja2")
