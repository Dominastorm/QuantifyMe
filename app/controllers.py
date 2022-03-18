from flask import render_template
from flask import current_app as app
from app.models import User, Tracker, Log

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET'])
def dashboard():
    trackers = Tracker.query.all()
    return render_template('dashboard.html', trackers=trackers)

@app.route('/trackers/<tracker>', methods=['GET'])
def journal(tracker):
    tracker = Tracker.query.filter_by(name=tracker).first()
    logs = Log.query.filter_by(tracker_id=tracker.tracker_id).all()
    return render_template('journal.html', tracker=tracker, logs=logs)

@app.route('/create-tracker', methods=['GET'])
def add_tracker():
    return render_template('create_tracker.html')