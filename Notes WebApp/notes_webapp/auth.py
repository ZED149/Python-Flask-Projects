

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

# creating blueprint for auth
auth = Blueprint("auth", __name__)


# login
@auth.route("/login/")
def login():
    return render_template("login.html", title="ZED | LOGIN")


# logout
@auth.route("/logout/")
def logout():
    return render_template("logout.html", title="ZED | LOGOUT")


# sign_up
@auth.route("/signUp/", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password != confirm_password:
            flash("Passwords do not match", category="alert")
        else:
            # creating a new user and adding it to the database
            email = request.form.get("email")
            name = request.form.get("name")

            # creating new user object
            new_user = User(email=email, name=name,
                            password=generate_password_hash(password, method='scrypt')
                            )
            # adding new user to the Database
            db.session.add(new_user)
            # commiting changes to the database
            db.session.commit()

            # redirecting user to the homepage
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", title="ZED | SIGNUP")
