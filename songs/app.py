import re

from flask import Flask, jsonify, request
from pymongo import MongoClient
from songs.utils import jsonifym

app = Flask(__name__)
client = MongoClient('mongo', 27017)
db = client.songs


@app.route('/songs', methods=['GET'])
def songs():
    """Get list of songs"""
    try:
        limit = int(request.args.get('limit', 0))
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return jsonify({'error': 'limit and offset have to be integer'}), 400

    if limit < 0 or offset < 0:
        return jsonify({'error': 'limit and offset have to be positive integer'}), 400

    song = db.songs.find().skip(offset).limit(limit)
    return jsonifym(list(song))


@app.route('/songs/avg/difficulty', methods=['GET'], defaults={'level': None})
@app.route('/songs/avg/difficulty/<int(min=1):level>', methods=['GET'])
def average_difficulty(level):
    """Calculate average difficulty for all songs or for songs with provided level"""
    pipeline = list()
    if level:
        pipeline.append({'$match': {
            'level': level
        }})

    pipeline.append(
        {'$group': {
            '_id': None,
            'averageDifficulty': {'$avg': '$difficulty'}
        }}
    )

    difficulty = list(db.songs.aggregate(pipeline))
    if difficulty:
        difficulty = difficulty[0]
        difficulty.pop('_id')
    return jsonifym(difficulty)


@app.route('/songs/search/<message>', methods=['GET'])
def search_songs(message):
    """Search songs in artist/title field"""
    search_pattern = re.compile(re.escape(message), re.IGNORECASE)
    songs = db.songs.find({
        '$or': [
            {'artist': search_pattern},
            {'title': search_pattern}
        ]
    })
    return jsonifym(list(songs))
