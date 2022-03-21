import os
from flask import Flask
from app.config import LocalDevelopmentConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
DB_NAME = 'appdb.sqlite3'
db = SQLAlchemy(app)

def create_database(app):
    if not os.path.exists('db/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

basedir = os.path.abspath(os.path.dirname(__file__))
SQLITE_DB_DIR = os.path.join(basedir, "../db")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "appdb.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.app_context().push()
app.config['SECRET_KEY']='thisisasecretkey'
db.init_app(app)
create_database(app)

# Import all the controllers so they are loaded
from app.controllers import *

if __name__ == '__main__':
    app.run(debug=True)