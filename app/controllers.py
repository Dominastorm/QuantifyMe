from flask import Flask, request
from flask import render_template
from flask import current_app as app
# from app.models import Dashboard

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')