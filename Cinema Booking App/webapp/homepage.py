
# this page contains homepage class

# importing libraries
from flask.views import MethodView
from flask import Flask, render_template, request, url_for, redirect
import os

# changing path of template and static folders for flask
template_folder_path = os.path.abspath("templates/")
static_folder_path = os.path.abspath('static/')
# configuring app variable
app = Flask(__name__, template_folder=template_folder_path,
            static_folder=static_folder_path)


# HomePage class
class HomePage(MethodView):
    """
    This class contains homepage for the website.
    """

    # get
    def get(self):
        return render_template("homepage.html")

    @app.after_request
    def after_request(response):
        response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return response

    @app.teardown_request
    def teardown_request(response):
        redirect(url_for('home_page'))
        return response