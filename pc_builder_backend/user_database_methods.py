import bcrypt
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from logger_config.logger_config import create_logger
from user import User


user_logger = create_logger('Users.log')


def add_new_user(user_collection: Collection, username: str, provided_password: str) -> bool:
    """
    Adds a new user to the user collection.

    :param user_collection: Collection containing user data.
    :param username: Username of the new user.
    :param provided_password: Password provided by the user (plaintext).
    :return: True if the user is added successfully, False otherwise.
    """
    # Hash the provided password
    hashed_password = bcrypt.hashpw(provided_password.encode('utf-8'), bcrypt.gensalt())

    # Create a new user with the hashed password
    new_user = User(username=username, password=hashed_password)

    try:
        user_collection.insert_one(new_user.to_dict())
        user_logger.info(f"New user added successfully - {username}")
        return True

    except PyMongoError as e:
        user_logger.error(f"New user could not be added - {username}")
        return False


# Deletes a user by user_id - Should also delete all their builds
def delete_existing_user(builds_collection: Collection, builds_index_collection: Collection,
                         users_collection: Collection, user_id: str, username: str) -> bool:
    """
    Deletes an existing user account and associated builds.

    :param builds_collection: Collection containing build data.
    :param builds_index_collection: Collection containing index of builds.
    :param users_collection: Collection containing user data.
    :param user_id: ID of the user account to delete.
    :param username: Username of the user account to delete.
    :return: True if account and associated builds are deleted successfully, False otherwise.
    """
    try:
        result = users_collection.delete_one({'user_id': user_id, 'username': username})
        print(f"Deleted: {result}")

        # Check if a document was deleted
        if result.deleted_count > 0:
            user_logger.info(f"Delete user account successfully - {user_id}")

            # Fetches users builds
            user_created_builds = builds_index_collection.find_one({"user_id": user_id})
            if user_created_builds is not None:
                user_build_ids_list = user_created_builds.get("created_build_list", [])
                # Deletes all builds created by the user on account deletion
                for build_id in user_build_ids_list:
                    builds_collection.delete_one({"build_id": build_id})

                # After all builds are deleted, delete the user's entry from the index collection
                builds_index_collection.delete_one({"user_id": user_id})
                user_logger.info(f"Deleted all builds from user account - {user_id}")
                return True
            else:
                user_logger.info(f"No builds to be deleted for account = {user_id}")
                return True  # No builds to delete, still consider it a success

        else:
            user_logger.info(f"Failed to delete user account : {user_id}")
            return False
    except PyMongoError as e:
        print(f"An error occurred: {e}")
        return False


def update_user_password(user_collection: Collection, username: str, old_password: str, new_password: str) -> bool:
    """
    Updates the password of an existing user.

    :param user_collection: Collection containing user data.
    :param username: Username of the user to update.
    :param old_password: Old password of the user (plaintext).
    :param new_password: New password to set for the user (plaintext).
    :return: True if password is updated successfully, False otherwise.
    """
    user = user_collection.find_one({"username": username})

    if bcrypt.checkpw(old_password.encode('utf-8'), user['password']):
        new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        try:
            update_result = user_collection.update_one({"username": username},
                                                       {"$set": {"password": new_password_hash}})
            if update_result.modified_count > 0:
                user_logger.info(f"Password updated for account : {username}")
                return True

        except PyMongoError as e:
            user_logger.error(f"Error occurred updating password: {e}")
            return False

    else:
        user_logger.info(f"Attempted to change password on account {username} - Passwords didnt match")
        return False


# Returns true if the username hasn't been used already, false otherwise
def unique_username_check(user_collection: Collection, username: str) -> bool:
    """
    Checks if a username is unique (not already used).

    :param user_collection: Collection containing user data.
    :param username: Username to check for uniqueness.
    :return: True if the username is unique, False otherwise.
    """
    # Check if the username already exists
    existing_user = user_collection.find_one({"username": username})

    if existing_user:
        return False
    else:
        return True
