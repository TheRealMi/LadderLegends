import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from bson.objectid import ObjectId

app = Flask(__name__, static_folder='dist', static_url_path='/')
# MongoDB setup and configuration
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)
# define the correct database to use
db = mongo.cx["LadderLegendsDB"]
users = db.Users
lbs = db.Leaderboards
players = db.Players

# Health check endpoint, fake news.
@app.route('/api/hello')
def hello():
    return jsonify({"message": "hey!"})

# TEST ENDPOINT: Given a username, return the organization name
@app.route('/api/getname/<username>')
def getname(username):
    user = db.Users.find_one({"username": username})
    if user:
        return jsonify({"name": user["name"]})
    else:
        return jsonify({"name": "not found"})

# ===== ORGANIZATION/USER ENDPOINTS =====
# LOGIN: Given a username and password, return the user object
@app.route('/api/login', methods=['POST'])
def login():
    user = db.Users.find_one({"username": request.json["username"], "password": request.json["password"]})
    if user:
        user["_id"] = str(user["_id"])
        user.pop("password", None)
        return jsonify(user)
    else:
        return jsonify({"error": "Login failed, incorrect username or password"})

# REGISTER: Given a username, password, email, organization name, create a user document and add it to the db
@app.route('/api/register', methods=['POST'])
def register():
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    name = request.json["name"]
    try:
        users.insert_one(
            {
                "username": username,
                "password": password,
                "email": email,
                "name": name,
                "Leaderboards": []
            }
        )
    except Exception as e:
        print(e)
        return jsonify({"error": e})
    
    return jsonify({"message": "User registered!"})

# UPDATE: Given all the attributes of a user, update its values
@app.route('/api/updateuser/<userid>', methods=['PUT'])
def updateuser(userid):
    # check if the user exists at all
    user = users.find_one({"_id": ObjectId(userid)})
    if not user:
        return jsonify({"error": "user doesn't exist"})

    # extract updated fields from request    
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    name = request.json["name"]
    Leaderboards = request.json["Leaderboards"]

    # If the user exists, update their entry/document
    query = { "_id": ObjectId(userid) }
    new_values = {"$set": {
        "_id": ObjectId(userid),
        "username": username,
        "password": password,
        "email": email,
        "name": name,
        "Leaderboards": Leaderboards
    }}
    print(query, new_values)
    users.update_one(query, new_values)
    # hooray!
    return jsonify({"message": "Updated user!"})

# DELETE: Given a user id, delete their entry from the database
@app.route('/api/deleteuser/<userid>', methods=['DELETE'])
def deleteuser(userid):
    # check if the user exists
    user = users.find_one({"_id": ObjectId(userid)})
    if not user:
        return jsonify({"error": "user doesn't exist"})

    query = {"_id": ObjectId(userid)}
    users.delete_one(query)
    return jsonify({"message": "User deleted!"})

# GET: Given a user id, return all the user information (except password)
@app.route('/api/getuser/<userid>', methods=['POST'])
def getuser(userid):
    user = users.find_one({"_id": ObjectId(userid)})
    if not user:
        return jsonify({"error": "user doesn't exist"})
    
    user["_id"] = str(user["_id"])
    for i in range(0, len(user["Leaderboards"])):
        user["Leaderboards"][i] = str(user["Leaderboards"][i])
    user.pop("password", None)
    return jsonify(user)


# ===== PLAYER ENDPOINTS =====

# Catch all, serve the frontend index
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run()
