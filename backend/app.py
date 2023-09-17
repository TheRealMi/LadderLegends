import os
import requests
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from bson.objectid import ObjectId
from urllib.parse import quote

load_dotenv()
app = Flask(__name__, static_folder='dist', static_url_path='/')
# MongoDB setup and configuration
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
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
    "X-Riot-Token": os.environ.get("RIOT_API_KEY")
}

# Health check endpoint, fake news.
@app.route('/api/hello')
def hello():
    return jsonify({"message": "hey!"})

# ===== ORGANIZATION/USER ENDPOINTS =====
# LOGIN: Given a username and password, return the user object
@app.route('/api/login', methods=['POST'])
def login():
    user = db.Users.find_one({"username": request.json["username"], "password": request.json["password"]})
    if user:
        user["_id"] = str(user["_id"])
        user.pop("password", None)
        for i in range(0, len(user["Leaderboards"])):
            user["Leaderboards"][i] = str(user["Leaderboards"][i])
        return jsonify(user)
    else:
        return jsonify({"error": "Login failed, incorrect username or password"})

# REGISTER: Given a username, password, email, organization name, create a user document and add it to the db
@app.route('/api/register', methods=['POST'])
def register():
    username = request.json["username"]
    usr = users.find_one({"username": username})
    if usr:
        return jsonify({"error": "user already registered"})
    password = request.json["password"]
    email = request.json["email"]
    name = request.json["name"]
    try:
        usr = {
            "username": username,
            "password": password,
            "email": email,
            "name": name,
            "Leaderboards": []           
        }
        res = users.insert_one(usr)
    except Exception as e:
        return jsonify({"error": e})
    usr["_id"] = str(res.inserted_id)
    
    return jsonify(usr)

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
    new_values = {
        "_id": ObjectId(userid),
        "username": username,
        "password": password,
        "email": email,
        "name": name,
        "Leaderboards": Leaderboards
    }
    cmd = {"$set": new_values}
    try:
        users.update_one(query, cmd)
    except Exception as e:
        return jsonify({"error": e})
    # hooray!
    new_values["_id"] = str(new_values["_id"])
    return jsonify(new_values)

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
    # Helper function that takes a leaderboard, player object, and player id and adds them to the lb
    def add_to_lb(lbid, player, pid):
        # check if the player is already in the leaderboard
        lb = lbs.find_one({"_id": ObjectId(lbid)})
        for p in lb["players"]:
            if p["ign"] == player["ign"]:
                return jsonify({"error": "player already exists in leaderboard"})
        # append this player to the correct leaderboard
        query = { "_id": ObjectId(lbid) }
        push = {"$push": {"players": player}}
        # update the leaderboard
        try:
            lbs.update_one(query, push)
        except Exception as e:
            return jsonify({"error": e})
        
        # Set the id of the return object to the player id obtained earlier, then return the final player
        player["_id"] = str(pid)
        return jsonify(player)

    # extract summoner name
    summoner_name = request.json["summoner"]
    # just in case, see if this user already exists in the player collection
    player = players.find_one({"ign": summoner_name})
    if player:
        # player already exists, just add it to the leaderboard
        return add_to_lb(request.json["leaderboard"], player, player["_id"])

    # build url based on summoner name
    url = riot_url + '/lol/summoner/v4/summoners/by-name/' + quote(summoner_name)
    # make the request and pass in standard headers
    res = requests.get(url, headers=riot_headers)
    # if the request went bad, womp womp
    if res.status_code != 200:
        return jsonify({"error": "an error occured while loading player data"})
    # load data into json format and extract the summoner id
    res = res.json()
    summoner_id = res["id"] # from result
   
    # use the summoner id to grab the summor information including rank
    url = riot_url + '/lol/league/v4/entries/by-summoner/' + summoner_id
    # make the request and pass in the standard headers
    res = requests.get(url, headers=riot_headers)
    # If the request went bad, womp womp
    if res.status_code != 200:
        return jsonify({"error": "an error occured while loading player data"})
    # load data into json format and extract the summoner rank and tier (after ensuring the data exists)
    res = res.json()
    if len(res) < 1:
        return jsonify({"error": "player profile is likely private"})
    # extract the players rank and tier
    summoner_rank = res[0]["rank"]
    summoner_tier = res[0]["tier"]

    # build json with user summoner name, rank, and tier
    player = {
        "ign": summoner_name,
        "tier": summoner_tier,
        "rank": summoner_rank
    }
    # use json build to try and insert into the database
    try:
        res = players.insert_one(player)
    except Exception as e:
        print(e)
        return jsonify({"error": e})

    # collect the new players ObjectId and add it to the user object
    pid = res.inserted_id
    player["_id"] = pid

    return add_to_lb(request.json["leaderboard"], player, pid)


# DELETE: Remove a player from a leaderboard given their summoner name and leaderboard id
@app.route('/api/deleteplayer/<lbid>', methods=['PUT'])
def deleteplayer(lbid):
    # grab the correct leaderboard to work with
    lb = lbs.find_one({"_id": ObjectId(lbid)})
    # extract summoner name from request
    summoner = request.json["summoner"]

    # search to see if the summoner exists or not
    for i, player in enumerate(lb["players"]):
        if summoner == player["ign"]:
            idx = i # element exists, early exit
            break
    # womp womp, player didn't exist in this leaderboard
    if not idx:
        jsonify({"error": "player not found in leaderboard"})

    # Now we can just update the element directly with an update call
    query = {"_id": ObjectId(lbid)}
    update = {"$pull": {"players": {"ign": summoner}}}
    try:
        lbs.update_one(query, update)
    except Exception as e:
        return jsonify({"error": e})
    return jsonify({"message": "player removed!"})


# ===== LEADERBOARD ENDPOINTS =====
# GET: Get a full leaderboard object given a leaderboard id
@app.route('/api/getlb/<lbid>', methods=['GET'])
def getlb(lbid):
    lb = lbs.find_one({"_id": ObjectId(lbid)})
    if not lb:
        return jsonify({"error": "leaderboard not found"})
    
    # leaderboard was found, return the whole document pls
    lb["_id"] = str(lb["_id"])
    for i in range(0, len(lb["players"])):
        lb["players"][i]["_id"] = str(lb["players"][i]["_id"])
    return jsonify(lb)

# GET: Get ALL leaderboards
@app.route('/api/getalllb', methods=['GET'])
def getalllb():
    try:
        all_lb = list(lbs.find({}))
        # go through every leaderboard and convert the object IDs to strings
        for lb in all_lb:
            lb["_id"] = str(lb["_id"])
            # go through the array of players and convert those object IDs
            for player in lb["players"]:
                player["_id"] = str(player["_id"])
    except Exception as e:
        return jsonify({"error": e})
    return jsonify(all_lb)

# ADD: Create an empty leaderboard
@app.route('/api/createlb', methods=['POST'])
def createlb():
    # extract leaderboard name and organization
    name = request.json["name"]
    org = request.json["organization"]
    if not name or not org:
        return jsonify({"error": "invalid input, name and organization required"})
    new_lb = {
        "name": name,
        "organization": org,
        "players": []
    }
    try:
        res = lbs.insert_one(new_lb)
    except Exception as e:
        return jsonify({"error": "unable to add leaderboard"})
    new_lb["_id"] = str(res.inserted_id)
    query = {"name": org}
    cmd = {
        "$push": {
            "Leaderboards": ObjectId(new_lb["_id"])
        }
    }
    users.update_one(query, cmd)
    return jsonify(new_lb)

# DELETE: Delete a leaderboard given an id
@app.route('/api/deletelb/<lbid>', methods=['DELETE'])
def deletelb(lbid):
    lb = lbs.find_one({"_id": ObjectId(lbid)})
    if not lb:
        return jsonify({"error": "leaderboard does not exist"})
    org = lb["organization"]
    query = {"_id": ObjectId(lbid)}
    lbs.delete_one(query)
    query = {"name": org}
    cmd = {"$pull": {
        "Leaderboards": ObjectId(lbid)
    }}
    users.update_one(query, cmd)
    return jsonify({"message": "leaderboard deleted!"})

# Catch all, serve the frontend index
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run()