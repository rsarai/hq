import json
import pytz

from datetime import datetime

from flask import Flask, request, jsonify
from bson import json_util
from pymongo import MongoClient
import pymongo


app = Flask(__name__)

page_size = 100
max_page_size = 2000
page_query_param = 'page'


client = MongoClient()
db = client.get_database("memex")
collection = db.get_collection("eventlog_v2")


def parse_json(data):
    return json.loads(json_util.dumps(data, default=json_util.default))

"""
https://www.programmersought.com/article/89681527397/
https://medium.com/swlh/mongodb-pagination-fast-consistent-ece2a97070f3
“$date”: <dateAsMilliseconds>
"""
@app.route('/api/nodes/', methods=['GET'])
def retrieve():
    kwargs = request.args.to_dict(flat=True)
    page = int(kwargs.pop(page_query_param, 1))

    filters = {}
    for key, value in kwargs.items():
        if key and value == '' or key == 'qs':
            filters.update({"$text": { "$search": key }})
        elif key == 'date':
            timezone = pytz.timezone("America/Recife")
            d = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            parsed_date = timezone.localize(d)
            utc_date = parsed_date.astimezone(pytz.UTC)
            filters.update({"datetime": {"$lte": utc_date}})
        else:
            filters[key] = value

    print(filters)
    count = collection.find(filters).sort('datetime', pymongo.DESCENDING).count()
    data = (
        collection
        .find(filters)
        .sort('datetime', pymongo.DESCENDING)
        .skip(page_size * (page - 1))
        .limit(page_size)
    )

    next_page_number = page + 1
    if count == 0:
        next_page_number = None

    response = jsonify(results=parse_json(list(data)), count=count, next_page_number=next_page_number)
    # Enable Access-Control-Allow-Originn
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
