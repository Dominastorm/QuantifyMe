from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from flask import current_app as app
from app.models import User, Tracker, Log
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/', methods=['GET','POST'])
def login():
    flash("test")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        user = User.query.filter_by(User.username == username).first()

        if user:
            if bcrypt.check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Incorrect username or password', category='error')
        else:
            flash('User not found', category='error')
    return render_template('login.html', user = current_user)

@app.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        fullname = request.form.get('name')
        city = request.form.get('city')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        from .models import User
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email is already taken, try another email.', category='error')
        else:
            db = SQLAlchemy(app)
            # Add user to the database
            new_user = User(fullname=fullname, email=email,  password=bcrypt.generate_password_hash(password1, method='sha256'), city=city)
            db.session.add(new_user)
            db.session.commit()
            flash('Successfully signed up.', category='success')
    return render_template('sign_up.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('login'))

@app.route('/home', methods=['GET','POST'])
# @login_required
def dashboard():
    trackers = Tracker.query.all()
    return render_template('dashboard.html') #, trackers=trackers)

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
    tracker = Tracker.query.filter_by(name=tracker).first()
    return render_template('log_tracker.html', tracker=tracker)

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


