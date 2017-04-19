# Something that is untested is broken.
import unittest

from flask import json, jsonify
from songs.app import app, db

TEST_DATA = []
with open('./seed/songs.json') as data:
    for line in data:
        TEST_DATA.append(json.loads(line))


def remove_ids(data):
    for item in data:
        item.pop('_id', None)

    return data


def compare_data(list1, list2):
    list1 = remove_ids(list1)
    list2 = remove_ids(list2)

    return list1 == list2


class SongsTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        """Remove all songs and repopulate it with data for the next test"""
        db.songs.delete_many({})
        db.songs.insert_many(TEST_DATA)

    def test_songs(self):
        response = self.app.get('/songs')
        songs = json.loads(response.data)
        fields_list = ['_id', 'artist', 'title', 'difficulty', 'level', 'released']

        self.assertTrue(all(k in songs[0].keys() for k in fields_list))
        self.assertTrue(compare_data(songs, TEST_DATA))


    def test_limit(self):
        response = self.app.get('/songs?limit=5')
        songs = json.loads(response.data)
        self.assertEqual(len(songs), 5)
        self.assertTrue(compare_data(songs, TEST_DATA[:5]))

    def test_limit_string_fail(self):
        response = self.app.get('/songs?limit=wrong')
        error = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error['error'], 'limit and offset have to be integer')

    def test_limit_negative_fail(self):
        response = self.app.get('/songs?limit=-5')
        error = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error['error'], 'limit and offset have to be positive integer')

    def test_offset(self):
        response = self.app.get('/songs')
        all_songs = json.loads(response.data)
        self.assertTrue(compare_data(all_songs, TEST_DATA))
        response = self.app.get('/songs?offset=2')
        offset_songs = json.loads(response.data)
        self.assertEqual(len(all_songs)-len(offset_songs), 2)
        self.assertTrue(compare_data(TEST_DATA[2:], offset_songs))

    def test_difficulty(self):
        def get_difficulty(data, level=None):
            difficulties = [item['difficulty'] for item in data
                            if (level is None or item['level'] == level)]

            return sum(difficulties)/len(difficulties)

        response = self.app.get('/songs/avg/difficulty')
        difficulty = json.loads(response.data)
        self.assertTrue('averageDifficulty' in difficulty)
        self.assertEqual(get_difficulty(TEST_DATA), difficulty['averageDifficulty'])

        response = self.app.get('/songs/avg/difficulty/3')
        difficulty = json.loads(response.data)
        self.assertEqual(get_difficulty(TEST_DATA, 3), difficulty['averageDifficulty'])

    def test_search(self):
        search_pattern = 'you'
        response = self.app.get('/songs/search/{}'.format(search_pattern))
        songs = json.loads(response.data)

        filtered_songs = [item for item in TEST_DATA
                          if search_pattern.lower() in item['title'].lower() or
                          search_pattern.lower() in item['artist'].lower()]
        self.assertTrue(compare_data(songs, filtered_songs))

    def test_search_not_exists(self):
        response = self.app.get('/songs/search/wrong')
        songs = json.loads(response.data)
        self.assertFalse(songs)


if __name__ == '__main__':
    unittest.main()
