import bcrypt
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.orm import Session
from logger_config.logger_config import create_logger

from user import User


logger = create_logger('Users.log')


def validate_user(user_collection: Collection, username: str, password: str) -> bool:
    ...


def add_new_user(user_collection: Collection, first_name: str, last_name: str,
                 username: str, email: str, provided_password: str) -> bool:

    # Hash the provided password
    hashed_password = bcrypt.hashpw(provided_password.encode('utf-8'), bcrypt.gensalt())

    # Create a new user with the hashed password
    new_user = User(first_name=first_name, last_name=last_name,
                    username=username, email=email, password=hashed_password)

    try:
        user_collection.insert_one(new_user.to_dict())
        logger.info(f"New user added successfully - {username}")
        return True

    except PyMongoError as e:
        logger.error(f"New user could not be added - {username}")
        return False


# Deletes a user by user_id
def delete_existing_user(users_collection: Collection, user_id: str) -> bool:
    try:
        result = users_collection.delete_one({'user_id': user_id})
        print(f"Deleted: {result}")

        # Check if a document was deleted
        if result.deleted_count > 0:
            logger.info(f"Delete user account successfully - {user_id}")
            return True
        else:
            logger.info(f"Failed to delete user account : {user_id}")
            return False
    except PyMongoError as e:
        print(f"An error occurred: {e}")
        return False


def update_user_password(user_collection: Collection, username: str, old_password: str, new_password: str):
    ...


# Returns true if the username hasn't been used already, false otherwise
def unique_username_check(user_collection: Collection, username: str) -> bool:
    # Check if the username already exists
    existing_user = user_collection.find_one({"username": username})

    if existing_user:
        print("Username is already in use")
        logger.info(f"Attempted signup with registered username - {username}")
        return False
    else:
        return True


# Returns true if the email hasn't been used already, false otherwise
def unique_email_check(user_collection: Collection, email: str):
    # Check if the email already exists
    existing_user = user_collection.find_one({"email": email})

    if existing_user:
        print("Email is already in use")
        logger.info(f"Attempted signup with registered email - {email}")
        return False
    else:
        return True
