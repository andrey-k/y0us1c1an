import datetime
import json
from bson.objectid import ObjectId
from werkzeug import Response


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def jsonifym(data):
    """jsonify with support for MongoDB ObjectId"""
    return Response(json.dumps(data, cls=JsonEncoder),
                    mimetype='application/json')
