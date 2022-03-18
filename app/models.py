from .database import db
import datetime

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tracker = db.relationship('Tracker', backref='user', lazy=True)
    log = db.relationship('Log', backref='user', lazy=True)

class Tracker(db.Model):
    __tablename__ = 'trackers'
    tracker_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tracker_type = db.Column(db.Integer, db.ForeignKey('tracker_types.id'), nullable=False)
    settings = db.Column(db.Text, nullable=False)

class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tracker_id = db.Column(db.Integer, db.ForeignKey('trackers.tracker_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)
    note = db.Column(db.Text, nullable=False)


# SQL CODE FOR USERS
"""
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(80) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL
    );
"""

# SQL CODE FOR TRACKERS
"""
CREATE TABLE trackers (
    tracker_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(80) NOT NULL,
    description TEXT NOT NULL,
    tracker_type INTEGER NOT NULL,
    settings TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
"""

# SQL CODE FOR LOGS
"""
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tracker_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    value FLOAT NOT NULL,
    note TEXT NOT NULL,
    FOREIGN KEY (tracker_id) REFERENCES trackers(tracker_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
"""