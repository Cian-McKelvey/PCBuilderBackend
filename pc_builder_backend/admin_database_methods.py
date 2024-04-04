from datetime import datetime

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from pc_builder_backend.constants import MONGO_CONNECTION_URL, STAGING_DATABASE, BUILDS_COLLECTION, \
    BUILDS_INDEX_COLLECTION, USER_COLLECTION, BLACKLIST_COLLECTION

client = MongoClient(MONGO_CONNECTION_URL)
database = client[STAGING_DATABASE]
builds_collection = database[BUILDS_COLLECTION]
build_index_collection = database[BUILDS_INDEX_COLLECTION]
users_collection = database[USER_COLLECTION]
blacklisted_tokens_collection = database[BLACKLIST_COLLECTION]


def fetch_app_info(db: Database, user_collection: Collection, build_collection: Collection) -> dict:
    # Get the stats of the database
    stats = db.command("dbstats")
    # Calculate used storage
    used_storage = stats['dataSize']
    # Calculate available storage
    available_storage = stats['storageSize']

    # Fetch total number of users and builds created
    num_users = user_collection.count_documents({})
    num_builds = build_collection.count_documents({})

    app_info = {
        "used_storage": used_storage,
        "available_storage": available_storage,
        "Num Users": num_users,
        "Num Builds": num_builds
    }

    return app_info


def fetch_all_users(collection: Collection) -> list:
    # Fetch the username and registration_date of every user
    user_data = []
    for doc in collection.find({}, {"username": 1, "registration_date": 1, "_id": 0}):
        user_data.append({
            "username": doc["username"],
            "registration_date": datetime.fromtimestamp(doc["registration_date"].timestamp())
        })
    return user_data


# print(fetch_app_info(db=database, user_collection=users_collection, build_collection=builds_collection))
#
# user_data = fetch_all_users(collection=users_collection)
# for user in user_data:
#     print(f"Username: {user['username']}, Registration Date: {user['registration_date']}")
