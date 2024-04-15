

# This is the app file for this Micro Blog

# importing important libraries and classes
from flask import Flask, request
from flask import render_template
import datetime as dt
from pymongo import MongoClient
from dotenv import load_dotenv
import os


# loading our environment variables
load_dotenv()


def create_app():
    # connecting to Mongo DB
    client = MongoClient(os.getenv("MONGODB_URI"), 27017)
    db = client.ZED_Blogs
    entries = db.blogs

    # creating app object
    app = Flask(__name__)

    # creating url
    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            # storing content of textarea
            content = request.form["content"]
            # creating date
            date = dt.datetime.today().strftime(" %b %Y")
            # storing date again in another format
            date_datetime = dt.datetime.today().strftime("%d-%m-%Y")
            # creating a dict to insert
            temp_dict = {
                "content": content,
                "date": date,
                "date_datetime": date_datetime
            }
            # inserting our entry into DB
            entries.insert_one(temp_dict)

        # for GET request
        return render_template("index.html", entries=entries)

    # running our app
    app.run(debug=True)


# running our app
if __name__ == "__main__":
    create_app()
