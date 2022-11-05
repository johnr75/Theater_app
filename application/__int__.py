from flask import Flask
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo


mongo = PyMongo()

app = Flask(__name__)
Bootstrap(app)
config_object = 'application.settings'
app.config['SECRET_KEY'] = '01bad144149208534d8fbb22d0d5b8f8daddc1b39edd5d3f73c5becb16be04bb'
app.config[
    'MONGO_URI'] = "mongodb+srv://jreinagel:FishRed2014@reinagel1.sge9k8m.mongodb.net/Theatrical_Tracking?retryWrites=true&w=majority"

mongo.init_app(app)

from application import routes