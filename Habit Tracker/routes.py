

# this is the app for our Habit Tracker webapp

# importing some important libraries
from flask import Blueprint, render_template
from flask import request, redirect, url_for, current_app
import datetime as dt
import uuid


# creating our page Blueprint
pages = Blueprint("habits", __name__, template_folder="templates", static_folder="static")


def today_at_midnight():
    """
    Returns a datetime object for today in format (%Y%m%d).
    :return:
    """
    today = dt.datetime.today()
    return dt.datetime(today.year, today.month, today.day)


# creating habit context processor for rendered templates
@pages.context_processor
def inject_habits():
    # fetching habits on current date
    habits_on_curr_date = current_app.db.habits.find({"added": {"$lte": selected_date_formatter()['selected_date']}})
    return {'habits': habits_on_curr_date}


# creating selected_date context processor for rendered templates
@pages.context_processor
def selected_date_formatter():
    selected_date = ''
    date_str = request.args.get('date')
    # checking if date exists
    if date_str:
        # constructs a datetime object according to ISO formats from date_str object
        selected_date = dt.datetime.fromisoformat(date_str)
    else:
        selected_date = today_at_midnight()

    return {'selected_date': selected_date}


@pages.context_processor
def fetch_dates_wrapper():
    def fetch_dates(start: dt.datetime):
        # storing current date
        dates = [start + dt.timedelta(days=diff) for diff in range(-3, 4)]
        return dates

    return {"fetch_dates": fetch_dates}


# defining endpoint for Homepage
@pages.route("/")
def home():
    selected_date = selected_date_formatter()['selected_date']
    # reading habits from DB
    completions = [habit["habit"] for habit in current_app.db.completions.find({"date": selected_date})]
    return render_template("index.html",
                           title="ZED Habit Tracker - Home",
                           completions=completions)


# defining endpoint for add_habit
@pages.route("/add_habit/", methods=["GET", "POST"])
def add_habit():
    # getting today's date
    today = today_at_midnight()
    # checking if the method is post
    if request.method == 'POST':
        current_app.db.habits.insert_one({
            "_id": uuid.uuid4().hex,
            "added": today,
            "name": request.form.get('habit')
        })

    return render_template("add_habit.html", title="ZED Habit Tracker - Add Habit")


@pages.post("/complete")
def complete():
    # fetching date from our form
    date = request.form.get('date')
    # converting date into a date object
    date = dt.datetime.fromisoformat(date)
    # fetching habit from our form
    habit = request.form.get('habitId')
    # inserting new row to our collection on MongoDB
    current_app.db.completions.insert_one({"date": date, "habit": habit})
    return redirect(url_for('habits.home', date=date))

