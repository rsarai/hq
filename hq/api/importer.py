import pymongo
from pymongo import MongoClient

from hq.routines import manager

memex_manager = manager.ImportManager()
content = memex_manager.fetch_memex_first_import()

client = MongoClient()
db = client.get_database("memex")
collection = db.get_collection("eventlog")

collection.remove({})
collection.insert_many(list(content))
memex_manager.mark_import_as_completed()

# collection.create_index([
#     ("provider", pymongo.TEXT),
#     ("activity", pymongo.TEXT),
#     ("principal_entity", pymongo.TEXT),
#     ("activity_entities", pymongo.TEXT),
#     ("project_name", pymongo.TEXT),
#     ("website_title", pymongo.TEXT),
#     ("website_url", pymongo.TEXT),
# ], { "default_language": "english" }, unique=True)

