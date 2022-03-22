
import os
from flask import Flask
from app.config import LocalDevelopmentConfig
from app.database import db
from flask_login import LoginManager

app = None
DB_NAME = 'appdb.sqlite3'

def create_database(app):
    if not os.path.exists('db/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Staring Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

app = create_app()

# Import all the controllers so they are loaded
from app.controllers import *

if __name__ == '__main__':
    app.run(debug=True)
