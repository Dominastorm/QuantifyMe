from database import db
import datetime

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    settings = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TimeStamp, nullable=False)
    updated_at = db.Column(db.TimeStamp, nullable=False)

class TrackerType(db.Model):
    __tablename__ = 'tracker_types'
    tracker_type_id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TimeStamp, nullable=False)
    updated_at = db.Column(db.TimeStamp, nullable=False)

class Tracker(db.Model):
    __tablename__ = 'trackers'
    tracker_id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tracker_type = db.Column(db.Integer, db.ForeignKey('tracker_types.id'), nullable=False)
    created_at = db.Column(db.TimeStamp, nullable=False)
    updated_at = db.Column(db.TimeStamp, nullable=False)
    settings = db.Column(db.Text, nullable=False)
    user = db.relationship('User', backref=db.backref('trackers', lazy=True))

class TrackerLog(db.Model):
    __tablename__ = 'tracker_logs'
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    tracker_id = db.Column(db.Integer, db.ForeignKey('trackers.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.TimeStamp, nullable=False)
    value = db.Column(db.Float, nullable=False)
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TimeStamp, nullable=False)
    updated_at = db.Column(db.TimeStamp, nullable=False)

# SQL CODE FOR USERS
"""
CREATE TABLE "users" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"username"	VARCHAR(80) NOT NULL UNIQUE,
	"password"	VARCHAR(80) NOT NULL,
	"email"	VARCHAR(120) NOT NULL UNIQUE,
	"first_name"	VARCHAR(80) NOT NULL,
	"last_name"	VARCHAR(80) NOT NULL,
    "settings"	TEXT NOT NULL,
	"created_at"	TIMESTAMP NOT NULL,
	"updated_at"	TIMESTAMP NOT NULL
);
"""

# SQL CODE FOR TRACKERS
"""
CREATE TABLE "trackers" (
    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    "user_id"	INTEGER NOT NULL,
    "name"	VARCHAR(80) NOT NULL,
    "created_at"	TIMESTAMP NOT NULL,
    "updated_at"	TIMESTAMP NOT NULL,
    "settings"	TEXT NOT NULL,
    FOREIGN KEY("user_id") REFERENCES "users"("id")
);
"""

# SQL CODE FOR TRACKER LOGS
"""
CREATE TABLE "tracker_logs" (
    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    "tracker_id"	INTEGER NOT NULL,
    "user_id"	INTEGER NOT NULL,
    "timestamp"	TIMESTAMP NOT NULL,
    "value"	FLOAT NOT NULL,
    "note"	TEXT NOT NULL,
    "created_at"	TIMESTAMP NOT NULL,
    "updated_at"	TIMESTAMP NOT NULL,
    FOREIGN KEY("tracker_id") REFERENCES "trackers"("id"),
    FOREIGN KEY("user_id") REFERENCES "users"("id")
);
"""