

from flask import Flask
from routes import pages
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# loading our environments
# this will load our environments to our program, which we can use further
load_dotenv()


# starting point
def create_app():
    # initializing our app object for Flask
    app = Flask(__name__)
    # connecting to our DB
    client = MongoClient(os.environ.get("MONGODB_URI"))
    # fetching our concerned DB(document) from MongoDB
    app.db = client.habit_tracker

    # registering our blue prints
    app.register_blueprint(pages)

    return app
