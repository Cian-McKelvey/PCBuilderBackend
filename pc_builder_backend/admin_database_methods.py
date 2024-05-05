from datetime import datetime
from pprint import pprint
from typing import Union

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError

from pc_builder_backend.constants import MONGO_CONNECTION_URL, STAGING_DATABASE, BUILDS_COLLECTION, USER_COLLECTION, \
    BUILDS_INDEX_COLLECTION, BLACKLIST_COLLECTION


def fetch_app_info(db: Database, user_collection: Collection, build_collection: Collection) -> Union[dict, None]:
    """
    Fetches application information including database statistics and user/build counts.

    :param db: MongoDB database instance.
    :param user_collection: Collection containing user data.
    :param build_collection: Collection containing build data.
    :return: Dictionary containing application information or None if an error occurs.
    """
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
            "num_users": num_users,
            "num_builds": num_builds
        }

        return app_info
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def fetch_all_users(collection: Collection) -> Union[list, None]:
    """
    Fetches information about all users from the given collection.

    :param collection: Collection containing user data.
    :return: List of user information dictionaries or None if an error occurs.
    """
    try:
        # Fetch the username and registration_date of every user
        user_data = []
        for doc in collection.find({}, {"username": 1, "registration_date": 1, "user_id": 1, "_id": 0}):
            user_data.append({
                "user_id": doc["user_id"],
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


def admin_delete_user_account(builds_collection: Collection, builds_index_collection: Collection,
                              users_collection: Collection, user_id: str) -> bool:
    """
    Admin function to delete a user account and associated builds.

    :param builds_collection: Collection containing build data.
    :param builds_index_collection: Collection containing index of builds.
    :param users_collection: Collection containing user data.
    :param user_id: ID of the user account to delete.
    :return: True if account and associated builds are deleted successfully, False otherwise.
    """
    try:
        result = users_collection.delete_one({'user_id': user_id})
        print(f"Deleted: {result}")

        # Check if a document was deleted
        if result.deleted_count > 0:
            print(f"ADMIN - Deleted user account successfully - {user_id}")

            # Fetches users builds
            user_created_builds = builds_index_collection.find_one({"user_id": user_id})
            if user_created_builds is not None:
                user_build_ids_list = user_created_builds.get("created_build_list", [])
                # Deletes all builds created by the user on account deletion
                for build_id in user_build_ids_list:
                    builds_collection.delete_one({"build_id": build_id})

                # After all builds are deleted, delete the user's entry from the index collection
                builds_index_collection.delete_one({"user_id": user_id})
                print(f"ADMIN - Deleted all builds from user account - {user_id}")
                return True
            else:
                print(f"ADMIN - No builds to be deleted for account = {user_id}")
                return True  # No builds to delete, still consider it a success

        else:
            print(f"ADMIN - Failed to delete user account : {user_id}")
            return False
    except PyMongoError as e:
        print(f"An error occurred: {e}")
        return False
