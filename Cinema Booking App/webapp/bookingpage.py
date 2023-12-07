import jinja2
# this file contains the bookingpage class

# importing libraries
from flask.views import MethodView
from flask import Flask, render_template, request, redirect
import sqlite3
import os
from webapp.homepage import app

# global variables
# fetching database folder path for database(s)
c = os.path.abspath('databases/')
DATABASE_FILE = f"{c}/cinema.db"
path_to_templates = os.path.abspath('templates')


# BookingPage class
class BookingPage(MethodView):
    """
    This class loads cinema details from database and displays
     available seats on the website in form of table. Then user can choose from it.
    """

    # get
    def get(self):
        # i need to generate dynamic data from database file
        content = self.read_from_db()
        return render_template("bookingpage.html", content=content)


    # read_from_db
    def read_from_db(self):
        """
        This function will read from database file.
        :return:
        """

        # connecting to DB
        conn = sqlite3.connect(DATABASE_FILE)
        if conn:
            # reading from DB
            cursor = conn.cursor()
            cursor.execute("""
            SELECT "seat_id", "price" FROM "Seat" WHERE "taken"=0
            """)
            result = cursor.fetchall()
            conn.close()
            return result
        else:
            print("Unable to open db file")
            result = []
            return result
