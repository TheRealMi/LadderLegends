import os
import requests
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from bson.objectid import ObjectId

# load dotenv variables
load_dotenv()

app = Flask(__name__, static_folder='dist', static_url_path='/')
# MongoDB setup and configuration
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
# define the correct database to use
db = mongo.cx["LadderLegendsDB"]
users = db.Users
lbs = db.Leaderboards
players = db.Players

# Set up riot api things
region = "na1"
riot_url = f'https://{region}.api.riotgames.com'
riot_headers = {
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": os.getenv("RIOT_API_KEY")
}

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
# ADD: Add player by summoner name:
@app.route('/api/addplayer', methods=['POST'])
def addplayer():
    # extract summoner name
    summoner_name = request.json["summoner"]
    print(summoner_name)
    # build url based on summoner name
    url = riot_url + '/lol/summoner/v4/summoners/by-name/' + summoner_name
    print(url)
    # make the request and pass in standard headers
    res = requests.get(url, headers=riot_headers)
    # if the request went bad, womp womp
    if res.status_code != 200:
        return jsonify({"error": "an error occured while loading player data"})
    # load data into json format and extract the summoner id
    res = res.json()
    print(res)
    summoner_id = res["id"] # from result
   
    # use the summoner id to grab the summor information including rank
    url = riot_url + '/lol/league/v4/entries/by-summoner/' + summoner_id
    print(url)
    # make the request and pass in the standard headers
    res = requests.get(url, headers=riot_headers)
    # If the request went bad, womp womp
    if res.status_code != 200:
        return jsonify({"error": "an error occured while loading player data"})
    # load data into json format and extract the summoner rank and tier (after ensuring the data exists)
    res = res.json()
    print(res)
    if len(res) < 1:
        return jsonify({"error": "player profile is likely private"})
    summoner_rank = res[0]["rank"]
    summoner_tier = res[0]["tier"]
    print(summoner_rank, summoner_tier)

    # build json with user summoner name, rank, and tier
    player = {
        "ign": summoner_name,
        "tier": summoner_tier,
        "rank": summoner_rank
    }
    print(player)
    # use json build to try and insert into the database
    try:
        res = players.insert_one(player)
        print("inserted...")
    except Exception as e:
        print(e)
        return jsonify({"error": e})
    # collect the new players ObjectId for future use
    print("try catch cleared")
    pid = res.inserted_id

    # Now extract leaderboard id from request, the player will be added to this leaderboard
    lbid = request.json["leaderboard"]
    print(lbid)
    # append this player to the correct leaderboard
    query = { "_id": ObjectId(lbid) }
    print(query)
    push = {"$push": {
        "players": ObjectId(pid)
    }}
    print(push)
    # update the leaderboard
    try:
        lbs.update_one(query, push)
    except Exception as e:
        return jsonify({"error": e})
    print("try catch cleared pt2")
    
    # Set the id of the return object to the player id obtained earlier, then return the final player
    player["_id"] = str(pid)
    return jsonify(player)

# 
# Catch all, serve the frontend index
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(port=5001, debug=True)