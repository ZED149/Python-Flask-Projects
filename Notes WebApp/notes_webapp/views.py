

# importing packages and modules
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    jsonify
)
from flask_login import login_required, current_user
from .models import Note
from . import db
import json


# creating blueprint for views
views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        # we need to add note to the database
        # fetching the note from the form
        note = request.form.get("note")
        # checking len of note
        if len(note) < 1:
            flash("Note is too short", category="alert")
        else:
            flash("Note added!", category="success")
            # creating new note object
            note = Note(data=note, user_id=current_user.id)
            # adding note to the database session
            db.session.add(note)
            # commiting changes to the database
            db.session.commit()

    return render_template("home.html",
                           title="ZED | HOME",
                           user=current_user)


# delete_note
@views.route("/delete_note/", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
