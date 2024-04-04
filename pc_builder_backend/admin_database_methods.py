from datetime import datetime
from typing import Union

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from pc_builder_backend.constants import MONGO_CONNECTION_URL, STAGING_DATABASE, BUILDS_COLLECTION, USER_COLLECTION, \
    BUILDS_INDEX_COLLECTION, BLACKLIST_COLLECTION

client = MongoClient(MONGO_CONNECTION_URL)
database = client[STAGING_DATABASE]
builds_collection = database[BUILDS_COLLECTION]
build_index_collection = database[BUILDS_INDEX_COLLECTION]
users_collection = database[USER_COLLECTION]
blacklisted_tokens_collection = database[BLACKLIST_COLLECTION]


def fetch_app_info(db: Database, user_collection: Collection, build_collection: Collection) -> Union[dict, None]:
    try:
        # Get the stats of the database
        stats = db.command("dbstats")
        # Calculate used storage
        used_storage = stats.get('dataSize')
        # Calculate available storage
        available_storage = stats.get('storageSize')

        if used_storage is None or available_storage is None:
            return None

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
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def fetch_all_users(collection: Collection) -> Union[list, None]:
    try:
        # Fetch the username and registration_date of every user
        user_data = []
        for doc in collection.find({}, {"username": 1, "registration_date": 1, "_id": 0}):
            user_data.append({
                "username": doc["username"],
                "registration_date": datetime.fromtimestamp(doc["registration_date"].timestamp())
            })

        if user_data:
            return user_data
        else:
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
