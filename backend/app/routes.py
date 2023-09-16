# import flask and render template along with pymongo
from flask import render_template
from app import app, mongo

# define the correct database to use
db = mongo.cx["LadderLegendsDB"]
cols = 
# define app route
@app.route('/')
# return the render template of the hello world index
def index():
    user = db.Users.find_one({'name': 'helloname'})
    print(user)
    username = user['name'] if user else None
    return render_template('index.html', name=username)

if __name__ == "__main__":
    app.run(debug=True)