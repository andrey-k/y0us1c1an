from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongo', 27017)
db = client.songs


@app.route('/')
def songs():
    song = db.songs.find_one()
    return song
