from flask import render_template
from flask import current_app as app
# from app.models import Dashboard

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/journal', methods=['GET'])
def journal():
    return render_template('journal.html')

@app.route('/create-tracker', methods=['GET'])
def add_tracker():
    return render_template('create_tracker.html')