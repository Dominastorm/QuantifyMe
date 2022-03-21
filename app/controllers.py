from flask import render_template
from flask import current_app as app
from app.models import User, Tracker, Log

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

import datetime

@app.route('/', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/sign-up', methods=['GET','POST'])
def sign_up():
    return render_template('sign_up.html')

@app.route('/home', methods=['GET','POST'])
def dashboard():
    trackers = Tracker.query.all()
    return render_template('dashboard.html', trackers=trackers)

@app.route('/trackers/<tracker>', methods=['GET','POST'])
def journal(tracker):
    tracker = Tracker.query.filter_by(name=tracker).first()
    logs = Log.query.filter_by(tracker_id=tracker.tracker_id).all()
    return render_template('journal.html', tracker=tracker, logs=logs)

@app.route('/create-tracker', methods=['GET','POST'])
def add_tracker():
    return render_template('create_tracker.html')

@app.route('/trackers/<tracker>/log', methods=['GET','POST'])
def log_tracker(tracker): 
    from .models import Tracker, Log
    this_tracker = Tracker.query.get(tracker)
    import datetime
    now = datetime.datetime.now()
    try:
        if request.method == 'POST':
            when = request.form.get('date')
            when = datetime.datetime.strptime(when, '%Y-%m-%dT%H:%M')
            print(when, type(when))
            value = request.form.get('value')
            note = request.form.get('note')
            print(note)
            from .database import db
            
            new_log = Log(timestamp=when, value=value, note=note, tracker_id=1, user_id=1)
            db.session.add(new_log)
            db.session.commit() 
            
            flash('New Log Added For ' + tracker.name + ' Tracker', category='success')
            return redirect(url_for('home'))
    except Exception as e:
        print(e)
        flash('Something went wrong.', category='error')
    tracker = Tracker.query.filter_by(name=tracker).first()    
    return render_template("log_tracker.html", user=current_user, tracker=tracker, now=now)
    
@app.route('/trackers/<tracker>/edit', methods=['GET','POST'])
def edit_tracker(tracker):
    tracker = Tracker.query.filter_by(name=tracker).first()
    return render_template('edit_tracker.html', tracker=tracker)

@app.route('/trackers/<tracker>/delete', methods=['GET','POST'])
def delete_tracker(tracker):
    # delete tracker
    return render_template('delete_tracker.html', tracker=tracker)

@app.route('/trackers/<tracker>/<log>/edit', methods=['GET','POST'])
def edit_log(tracker, log):
    tracker = Tracker.query.filter_by(name=tracker).first()
    log = Log.query.filter_by(id=log).first()
    return render_template('edit_log.html', log=log, tracker=tracker)


