from flask import render_template
from flask import current_app as app
from app.models import User, Tracker, Log

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user

import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        from .models import User

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('dashboard'))
            else:
                flash('Incorrect password, try again!', category='error')

        else:
            flash('User does not exist.', category='error')
    return render_template("login.html", user=current_user)

@app.route('/sign-up', methods=['GET','POST'])
def sign_up():
    return render_template('sign_up.html')

@app.route('/', methods=['GET','POST'])
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
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            tracker_type = request.form.get('tracker_type')
            settings = request.form.get('settings')
            
            print(tracker_type)
            from .models import Tracker
            current_user_id = 1
            tracker = Tracker.query.filter_by(name=name).first()
            print("works till line 41")
            if tracker and current_user_id == tracker.user_id:
                # flash('The tracker "' + name + '" is already added by you.', category='error')
                return redirect(url_for('dashboard'))
            else:
                print("Works till line 46")
                from .database import db
                new_tracker = Tracker(name=name, description=description, tracker_type=tracker_type, settings=settings,
                                      user_id=1)
                db.session.add(new_tracker)
                db.session.commit()
                print("works till line 52")
                # flash('New Tracker Added.', category='success')
                return redirect(url_for('dashboard'))
    except Exception as e:
        print(e)
        # flash('Something went wrong.', category='error')
    return render_template('create_tracker.html')

@app.route('/trackers/<tracker>/log', methods=['GET','POST'])
def log_tracker(tracker): 
    from .models import Tracker, Log
    tracker = Tracker.query.filter_by(name=tracker).first()
    import datetime
    now = datetime.datetime.now()
    try:
        if request.method == 'POST':
            when = request.form.get('date')
            when = datetime.datetime.strptime(when, '%Y-%m-%dT%H:%M')
            value = request.form.get('value')
            note = request.form.get('note')
            
            from .database import db
            new_log = Log(timestamp=when, value=value, note=note, tracker_id=tracker.tracker_id, user_id=1)
            db.session.add(new_log)
            db.session.commit() 
            
            # flash('New Log Added For ' + tracker.name + ' Tracker', category='success')
            return redirect(url_for('dashboard'))
    except Exception as e:
        print(e)
        # flash('Something went wrong.', category='error')  
    return render_template("log_tracker.html", user=current_user, tracker=tracker, now=now)
    
@app.route('/trackers/<tracker>/edit', methods=['GET','POST'])
def edit_tracker(tracker):
    tracker = Tracker.query.filter_by(name=tracker).first()
    tracker_name = tracker.name
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            tracker_type = request.form.get('type')
            settings = request.form.get('settings')

            current_user_id = 1
            tracker = Tracker.query.filter_by(name=name).first()
            if tracker and tracker.user_id == current_user_id and tracker_name != name:
                flash('The tracker "' + name + '" is already added by you, Try a new name for your tracker.',
                      category='error')
            else:
                from .database import db

                tracker.name = name
                tracker.description = description
                tracker.tracker_type = tracker_type
                tracker.settings = settings
                
                db.session.commit()
                flash('Tracker Updated Successfully.', category='success')
                return redirect(url_for('dashboard'))
    except Exception as e:
        print(e)
        flash('Something went wrong.', category='error')
    return render_template('edit_tracker.html', tracker=tracker)

@app.route('/trackers/<tracker>/delete', methods=['GET','POST'])
def delete_tracker(tracker):
    try:
        from .models import Tracker
        Tracker_details = Tracker.query.filter_by(name=tracker).first()
        Tracker_name = Tracker_details.name
        from .database import db
        db.session.delete(Tracker_details)
        db.session.commit()
        # flash(Tracker_name + ' Tracker Removed Successfully.', category='success')
    except Exception as e:
        print(e)
        # flash('Something went wrong.', category='error')
    return redirect(url_for('dashboard'))

    # return render_template('delete_tracker.html', tracker=tracker)

@app.route('/trackers/<tracker>/<log>/edit', methods=['GET','POST'])
def edit_log(tracker, log):
    tracker = Tracker.query.filter_by(name=tracker).first()
    log = Log.query.filter_by(id=log).first()
    this_tracker = Tracker.query.get(log.tracker_id)
    try:
        if request.method == 'POST':
            when = request.form.get('date')
            when = datetime.datetime.strptime(when, '%Y-%m-%dT%H:%M')
            value = request.form.get('value')
            note = request.form.get('note')

            log.timestamp = when
            log.value = value
            log.note = note
            
            from .database import db
            db.session.commit()
            # flash(this_tracker.name + ' Log Updated Successfully.', category='success')
            return redirect(url_for('journal', tracker=this_tracker.name))
            # return redirect(url_for('views.view_tracker', record_id=log.tracker_id))
    except Exception as e:
        print(e)
        # flash('Something went wrong.', category='error')

    return render_template('edit_log.html', log=log, tracker=tracker)

@app.route('/trackers/<tracker>/<log>/delete', methods=['GET','POST'])
def delete_log(tracker, log):
    try:
        log = Log.query.filter_by(id=log).first()
        from .database import db
        db.session.delete(log)
        db.session.commit()
        # flash('Log Deleted Successfully.', category='success')
    except Exception as e:
        print(e)
        # flash('Something went wrong.', category='error')
    return redirect(url_for('journal', tracker=tracker))
    # return redirect(url_for('views.view_tracker', record_id=log.tracker_id))
