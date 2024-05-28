
# Created by Salman Ahmad
# Dated on 5-May-2024 Sat
# This file contains the Notes WebApp


# importing packages and modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


# defining our DB
db = SQLAlchemy()
DB_NAME = "notes.db"


# create_app
def create_app():
    # initializing our app
    app = Flask(__name__)
    # configuring SECRET_KEY for cookies and sessions
    app.config['SECRET_KEY'] = "sada as dakdqw d e1  wq12  wqe12omdldl1 123 1@#wqQD"
    # configuring SQLALCHEMY_DATABASE_NAME for our app
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"

    # initializing our DB
    db.init_app(app)

    # registering Blueprints for our app
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix="/auth/")

    # checking either we have created our DB or not
    # importing our Database Models
    from .models import User, Note
    # creating our tables
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app=app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# create_database
def create_database(app):
    if not path.exists("notes_webapp/" + DB_NAME):
        with app.app_context():
            # creating our DB
            db.create_all()
            print("DATABASE CREATED")
