from flask import Flask
from flask_bootstrap import Bootstrap
from .extensions import mongo, login_manger
from dotenv import load_dotenv
from .routes import main
from .auth import auth
from flask_bcrypt import Bcrypt

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app.config.from_prefixed_env('config.cfg')
    mongo.init_app(app)

    #login_manger.init_app(app)

    Bootstrap(app)
    app.register_blueprint(main)
    app.register_blueprint(auth)
    return app







