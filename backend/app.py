from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import os

app = Flask(__name__, static_folder='dist', static_url_path='/')

# MongoDB setup and configuration
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)
# define the correct database to use
db = mongo.cx["LadderLegendsDB"]

@app.route('/api/hello')
def hello():
    return jsonify({"message": "hey!"})

@app.route('/api/getname/<username>')
def getname(username):
    user = db.Users.find_one({"username": username})
    if user:
        return jsonify({"name": user["name"]})
    else:
        return jsonify({"name": "not found"})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run()