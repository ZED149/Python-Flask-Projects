from os.path import split

# importing some important libraries
from flask import Flask
from os import path, getcwd
from .extensions import db

# Database name
DATABASE_NAME = getcwd()
DATABASE_NAME = DATABASE_NAME.split('\\')[1].replace(" ", "_")

print(DATABASE_NAME)


# create app function
def create_app():
    # initializing our app object
    app = Flask(__name__)

    # registering my blueprints
    from .routes.main import main
    app.register_blueprint(main, url_prefix="/")
    from .routes.api import api
    app.register_blueprint(api, url_prefix="/api")

    # configuring our database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_NAME}.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # initializing SQL Alchemy db
    db.init_app(app)

    # creating our tables
    create_database(app)
    
    # Return
    return app
    


# create_database()
def create_database(app):
    if not path.exists("./" + DATABASE_NAME + ".db"):
        with app.app_context():
            # creating our DB
            try:
                db.create_all()
            except:
                print("Failed to created database")
                exit(0)
            else:
                print("Database created")
