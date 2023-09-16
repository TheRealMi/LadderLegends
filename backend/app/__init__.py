# import flask and render template along with pymongo
from flask import Flask
from flask_pymongo import PyMongo
import os

# initialize flask app and mongodb URI
app = Flask(__name__)
# save mongo URI
#app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGO_URI"] = "mongodb+srv://superuser:dumbsuperuserLL123@cluster0.yheaxbu.mongodb.net/?retryWrites=true&w=majority"
mongo = PyMongo(app)