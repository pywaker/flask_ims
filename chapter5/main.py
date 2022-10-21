"""
"""
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user

from .models import verify_user, get_user_by_id, get_all_users, get_all_items, create_user, create_item

app = Flask(__name__)
app.secret_key = "some-super-random-secret-key"
login_manager = LoginManager()

# initialize flask plugins
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


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
        user = verify_user(email, password)
        if user is not None:
            login_user(user)
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


@app.route("/users")
@login_required
def list_users():
    return render_template("users.html.jinja2", users=get_all_users())


@app.route("/users/add", methods=["GET", "POST"])
@login_required
def add_user():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"].strip()
        fullname = request.form["fullname"].strip()
        if create_user(email, password, fullname):
            return redirect(url_for('list_users'))
        else:
            return render_template("add_user.html.jinja2", message="User already exists")
    return render_template("add_user.html.jinja2")


@app.route("/items")
@login_required
def list_items():
    print(get_all_items())
    return render_template("items.html.jinja2", items=get_all_items())


@app.route("/items/add", methods=["GET", "POST"])
@login_required
def add_item():
    if request.method == "POST":
        name = request.form["name"].strip()
        count = request.form["count"].strip()
        if create_item(name, count):
            return redirect(url_for('list_items'))
        else:
            return render_template("add_item.html.jinja2", message="Item already exists")
    return render_template("add_item.html.jinja2")
