from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import os

app = Flask(__name__, static_folder='dist', static_url_path='/')

@app.route('/api/hello')
def hello():
    return jsonify({"message": "hey!"})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run()