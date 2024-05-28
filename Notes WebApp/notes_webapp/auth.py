

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for
)
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user


# creating blueprint for auth
auth = Blueprint("auth", __name__)


# login
@auth.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # query the user from the database based on its email
        # and return its first result
        # There will always be 1 result as we have a check on email is unique when we add email on sign_up form
        user = User.query.filter_by(email=email).first()
        if user:
            # if we found a user based on entered email on the login form
            # checking password hash
            if check_password_hash(user.password, password=password):
                flash("Logged in successfully!", category="success")
                # logging in the user
                login_user(user, remember=True)
                # redirecting the user to the homepage
                return redirect(url_for("views.home"))
            else:
                flash("Invalid Credentials", category="alert")
        else:
            flash("Email doesn't exist", category="alert")

    return render_template("login.html", title="ZED | LOGIN", user=current_user)


# logout
@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


# sign_up
@auth.route("/signUp/", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        email = request.form.get("email")

        # checking if the email already exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            if user.email == email:
                flash("Email already exists", category="alert")
                return redirect(url_for("auth.sign_up"))

        if password != confirm_password:
            flash("Passwords do not match", category="alert")
        else:
            # fetching name from the HTML form
            name = request.form.get("name")

            # creating new user object
            new_user = User(email=email, name=name,
                            password=generate_password_hash(password, method='scrypt')
                            )
            # adding new user to the Database
            db.session.add(new_user)
            # commiting changes to the database
            db.session.commit()

            # flashing user
            flash("Account Created.", category="success")

            # logging in the user
            if user:
                login_user(user, remember=True)

            # redirecting user to the homepage
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", title="ZED | SIGNUP", user=current_user)
