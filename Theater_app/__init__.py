from flask import Flask, g
from flask_bootstrap import Bootstrap
from .extensions import mongo, login_manger
from dotenv import load_dotenv
from .routes import main
from .auth_route import auth, User
from itsdangerous import SignatureExpired, BadTimeSignature, URLSafeTimedSerializer
from .auth import serial_load

load_dotenv()


def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    mongo.init_app(app)
    login_manger.init_app(app)
    Bootstrap(app)

    @login_manger.user_loader
    def load_user(session_token):
        db = mongo.db.Users
        try:
            serial_load(session_token)
        except (SignatureExpired, BadTimeSignature):
            edit_items = {'session_token': ""}
            db.update_one({'session_token': session_token}, {"$set": edit_items}, upsert=False)
            return None

        user_data = db.find_one({'session_token': session_token})
        if user_data:
            return User(user_data)
        return None

    login_manger.login_view = 'auth.login'
    login_manger.refresh_view = 'auth.login'


    app.register_blueprint(main)
    app.register_blueprint(auth)
    return app


