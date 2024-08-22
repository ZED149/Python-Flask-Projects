
# importing some important libraries
from flask import Blueprint
from ..models.user import User
from ..extensions import db

# name of the blueprint
main = Blueprint('main', __name__)

# creating routes
@main.route("/user/<name>")
def create_user(name):
    # storing name from the path varibale of the url
    user = User(name=name)
    # adding it to the db session
    db.session.add(user)
    # comitting changes
    db.session.commit()

    return f"User {name} added succesfully."