"""
"""
import click
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from pony.flask import Pony
from pony.orm import Database

from .user import UserRole
from .models import db, verify_user, get_all_users, get_all_items, create_user, create_item, update_user_status

app = Flask(__name__)
app.config.update(dict(
    DEBUG = False,
    SECRET_KEY = 'some-super-random-secret-key',
    PONY = {
        'provider': 'sqlite',
        'filename': 'db.sqlite3',
        'create_db': True
    }
))
login_manager = LoginManager()

db.bind(**app.config['PONY'])
db.generate_mapping(create_tables=True)

# initialize flask plugins
Pony(app)
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db.User.get(id=user_id)


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
    if current_user.role != "Admin":
        flash("Your are not authorized to view users page.", "warning")
        return redirect(url_for("dashboard"))
    return render_template("users.html.jinja2", users=get_all_users())


@app.route("/users/add", methods=["GET", "POST"])
@login_required
def add_user():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"].strip()
        fullname = request.form["fullname"].strip()
        try:
            create_user(email, password, fullname)
        except Exception as exp:
            app.logger.exception(exp)
            return render_template("add_user.html.jinja2", message="User already exists")
        else:
            return redirect(url_for('list_users'))
    return render_template("add_user.html.jinja2")


@app.route("/users/<userid>/reactivate")
@login_required
def reactivate_user(userid):
    update_user_status(userid, True)
    return redirect(url_for('list_users'))


@app.route("/users/<userid>/deactivate")
@login_required
def deactivate_user(userid):
    update_user_status(userid, False)
    return redirect(url_for('list_users'))


@app.route("/items")
@login_required
def list_items():
    all_items = []
    if current_user.role == "Admin":
        all_items = get_all_items()
    else:
        pass
    return render_template("items.html.jinja2", items=all_items)


@app.route("/items/add", methods=["GET", "POST"])
@login_required
def add_item():
    if request.method == "POST":
        name = request.form["name"].strip()
        count = request.form["count"].strip()
        try:
            create_item(name, count)
        except Exception as exp:
            app.logger.exception(exp)
            return render_template("add_item.html.jinja2", message="Item already exists")
        else:
            return redirect(url_for('list_items'))
    return render_template("add_item.html.jinja2")


# cli commands
@app.cli.command("create-admin")
@click.argument("email")
@click.argument("password")
def create_admin(email, password):
    try:
        create_user(email.strip(), password.strip(), "Admin", UserRole.admin)
    except Exception as exp:
        app.logger.exception(exp)
    else:
        app.logger.info("Admin created.")
