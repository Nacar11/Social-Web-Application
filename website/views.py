from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
views = Blueprint('views', __name__)
from . import db
from .models import Note
import json

def time_ago(dt):
    now = datetime.now()
    delta = now - dt

    if delta < timedelta(minutes=1):
        return "just now"
    elif delta < timedelta(hours=1):
        return "{} minutes ago".format(int(delta.total_seconds() / 60))
    elif delta < timedelta(days=1):
        return "{} hours ago".format(int(delta.total_seconds() / 3600))
    elif delta < timedelta(days=7):
        return "{} days ago".format(int(delta.total_seconds() / 86400))
    elif delta < timedelta(weeks=4):
        return "{} weeks ago".format(int(delta.total_seconds() / 604800))
    else:
        return dt.strftime("%B %d, %Y")


@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method =="POST":
        note = request.form.get('note')
        print(note)

        if len(note) < 1:
            flash('Note is too short, try again.', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Noted Added!', category='success')
 
    print("asdasd")
    

    return render_template("home.html", user=current_user, timeago=1)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/sample', methods=['GET', 'POST'])
def sample_view():
    return render_template("facebooksample.html", user=current_user)

