

# importing some important libraries
from ..models.user import User
from flask import Blueprint

# creating new blueprint
api = Blueprint("api", __name__)

# creating routes
@api.route("/v1/<name>")
def get_user(name):
    user = User.query.filter_by(name=name).first()

    return {"name": user.name}
