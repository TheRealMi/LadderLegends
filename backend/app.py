from flask import Flask, render_template
from flask_pymongo import PyMongo
import os

# initialize flask app and mongodb URI
app = Flask(__name__)
# save mongo URI
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)
# define the correct database to use
db = mongo.cx["LadderLegendsDB"]

# define app route
@app.route('/')
# return the render template of the hello world index
def index():
    user = db.Users.find_one({'name': 'myorgname'})
    print(user)
    username = user['name'] if user else None
    return render_template('index.html', name=username)
if __name__ == "__main__":
    app.run(debug=True)