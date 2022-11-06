from flask import Flask
from flask_bootstrap import Bootstrap
from .extensions import mongo
from dotenv import load_dotenv
from .routes import main

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    Bootstrap(app)
    app.register_blueprint(main)
    mongo.init_app(app)
    return app







