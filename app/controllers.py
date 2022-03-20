from flask import render_template
from flask import current_app as app
from app.models import User, Tracker, Log

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/sign-up', methods=['GET'])
def sign_up():
    return render_template('sign_up.html')

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

@app.route('/trackers/<tracker>/log', methods=['GET'])
def log_tracker(tracker):
    tracker = Tracker.query.filter_by(name=tracker).first()
    return render_template('log_tracker.html', tracker=tracker)

@app.route('/trackers/<tracker>/edit', methods=['GET'])
def edit_tracker(tracker):
    tracker = Tracker.query.filter_by(name=tracker).first()
    return render_template('edit_tracker.html', tracker=tracker)

@app.route('/trackers/<tracker>/delete', methods=['GET'])
def delete_tracker(tracker):
    # delete tracker
    return render_template('delete_tracker.html', tracker=tracker)

@app.route('/trackers/<tracker>/<log>/edit', methods=['GET'])
def edit_log(tracker, log):
    tracker = Tracker.query.filter_by(name=tracker).first()
    log = Log.query.filter_by(id=log).first()
    return render_template('edit_log.html', log=log, tracker=tracker)


