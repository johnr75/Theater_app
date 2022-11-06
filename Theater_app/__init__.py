from flask import Flask
from flask_bootstrap import Bootstrap
from .extensions import mongo
from dotenv import load_dotenv
from .routes import main

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app.config[ "MONGO_URI"] = \
        "mongodb+srv://jreinagel:FishRed2014@reinagel1.sge9k8m.mongodb.net/Theatrical_Tracking?retryWrites=true&w=majority"
    app.config["SECRET KEY"] = '01bad144149208534d8fbb22d0d5b8f8daddc1b39edd5d3f73c5becb16be04bb'
    Bootstrap(app)
    app.register_blueprint(main)
    mongo.init_app(app)
    return app







