import webbrowser

# this file contains the design page class

# importing libraries
from flask.views import MethodView
from wtforms import Form, StringField, SubmitField, IntegerField
from flask import Flask, render_template, request, session


# Details Page class
class DetailsPage(MethodView):
    """
    This class generates a Details page on website where user can enter card details.
    """

    # post
    def post(self):
        return render_template("detailspage.html",
                               seatid=request.form.get('seat_id'))