import pymongo
from pymongo import MongoClient

from hq.routines import manager


def reset():
    client = MongoClient()
    db = client.get_database("memex")
    collection = db.get_collection("eventlog_v2")
    collection.remove({})

    memex_manager = manager.ImportManager()
    memex_manager.reset()


def mount_memex():
    memex_manager = manager.ImportManager()
    content = memex_manager.fetch_memex_first_import()

    client = MongoClient()
    db = client.get_database("memex")
    collection = db.get_collection("eventlog_v2")

    collection.remove({})
    collection.insert_many(list(content))
    memex_manager.mark_import_as_completed()

    collection.drop_indexes()
    collection.create_index([
        ("provider", pymongo.TEXT),
        ("activity", pymongo.TEXT),
        ("principal_entity", pymongo.TEXT),
        ("activity_entities", pymongo.TEXT),
        ("project_name", pymongo.TEXT),
        ("website_title", pymongo.TEXT),
        ("website_url", pymongo.TEXT),
        ("things_i_did", pymongo.TEXT),
        ("description", pymongo.TEXT),
        ("detail", pymongo.TEXT),
        ("summary", pymongo.TEXT),
    ])


def update_memex():
    memex_manager = manager.ImportManager()
    updates = memex_manager.fetch_updates()

    client = MongoClient()
    db = client.get_database("memex")
    collection = db.get_collection("eventlog_v2")

    collection.insert_many(list(updates))
    memex_manager.mark_import_as_completed()
