

# This file contains Database models for our app
# we are going to have db models for our users as well as for our apps

# importing database
from . import db
from flask_login import UserMixin       # custom class that we can inherit from
from sqlalchemy.sql import func


# User class
class User(db.Model, UserMixin):
    # defining columns for our database
    id = db.Column(db.Integer, primary_key=True)       # PK and ID for user's
    email = db.Column(db.String(150), unique=True)      # email for the user, and it is unique, means it cannot be same
    password = db.Column(db.String(150))                # password for the user account
    name = db.Column(db.String(150))                    # name of the user
    notes = db.relationship("Note")


# Notes class
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                # PK and ID for the notes
    data = db.Column(db.String(10000))                                          # note
    date = db.Column(db.DateTime(timezone=True), default=func.now())            # date at which note created
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))                   # FK for the user


# end
