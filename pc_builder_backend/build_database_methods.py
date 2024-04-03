from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from pc_builder_backend.pc_build import PCBuild
from logger_config.logger_config import create_logger


# Need to get this create logger method working, compare to the user logger file cause that works for some reason
logger = create_logger('PCBuilds.log')


def write_new_build(builds_collection: Collection,
                    builds_index_collection: Collection,
                    completed_build: PCBuild,
                    user_id: str) -> bool:

    """
    Writes a new build to MongoDB collections.

    :param builds_collection: MongoDB collection for storing builds.
    :param builds_index_collection: MongoDB collection for storing build indexes.
    :param completed_build: Completed PCBuild object to be stored.
    :param user_id: User identifier associated with the build.
    """
    # Changes the build to a dict using the current user id
    build = completed_build.to_dict(user_id=user_id)
    try:
        builds_collection.insert_one(build)
        logger.info(f"New Build added to MongoDB collection {completed_build.build_id}")

        # Quick conditional, if a build index is already created, update it by adding the new builds id
        if builds_index_collection.find_one({"user_id": user_id}) is not None:
            builds_index_collection.update_one(
                {"user_id": user_id},
                {'$push': {'created_build_list': completed_build.build_id}}
            )
            return True
        # Otherwise create a new entry and add the builds id as the first item in a list
        else:
            new_index_entry = {
                "user_id": user_id,
                "created_build_list": [completed_build.build_id]
            }
            builds_index_collection.insert_one(new_index_entry)
            logger.info("New index for account added to MongoDB collection")
            return True

    # Throw pymongo errors to show exceptions
    except PyMongoError as e:
        logger.error(f"Build failed to be added {e}")
        return False


def edit_build(builds_collection: Collection, build_id: str, part_name: str, new_part: dict) -> bool:
    """
    Edits a specific build in the MongoDB collection.

    :param builds_collection: MongoDB collection for storing builds.
    :param build_id: ID of the build to be edited.
    :param part_name: Name of the part that is to be edited.
    :param new_part: Dictionary containing the part information to be edited.
    :return: A True/False value depending on if the edit was successful.
    """
    # Validates the correct data types are being supplied
    for key, value in new_part.items():
        if not isinstance(value, int):  # Only checks the value, keys must always be string in a dict
            logger.error(f"Invalid value type for key '{key}'. Expected int, got {type(value)}.")
            return False
        else:
            new_part_name = key
            new_part_price = value

    # Checks for a valid build_id
    valid_build_check = builds_collection.find_one({"build_id": build_id})
    if valid_build_check is None:
        logger.info(f"Build could not be found with ID: {build_id}")
        return False
    else:
        try:
            result = builds_collection.find_one({"build_id": build_id})
            if result and part_name in result:
                original_part_price = result[part_name].get('price')
                overall_price = result.get('OverallPrice')
            else:
                logger.error(f"{part_name} not found in the build with ID: {build_id}")
                return False

            builds_collection.update_one(
                {"build_id": build_id},
                {
                    "$set": {
                        f"{part_name}.price": new_part_price,
                        f"{part_name}.value": new_part_name,
                        f"OverallPrice": overall_price - original_part_price + new_part_price
                    }
                }
            )
            logger.info(f"{part_name} has been successfully updated - {build_id}")
            return True
        except PyMongoError as e:
            logger.error(f"Error updating that build: {e}")
            return False


def update_build(builds_collection: Collection, build_data: dict) -> bool:
    """
    Updates or inserts a build in the MongoDB collection based on the provided build data dictionary.

    :param builds_collection: MongoDB collection for storing builds.
    :param build_data: Dictionary representing the entire build.
    :return: A True/False value depending on if the update/insert was successful.
    """
    try:
        build_id = build_data.get("build_id")
        if not build_id:
            logger.error("Invalid build data: 'build_id' field is missing.")
            return False

        # Validate the build data (you can add more validation as per your requirements)
        if not isinstance(build_data, dict):
            logger.error("Invalid build data: Expected a dictionary.")
            return False

        # Check if the build exists in the database
        existing_build = builds_collection.find_one({"build_id": build_id})

        if existing_build:
            # Update the existing build
            result = builds_collection.replace_one({"build_id": build_id}, build_data)
            if result.modified_count > 0:
                logger.info(f"Build with ID {build_id} has been successfully updated.")
            else:
                logger.warning(f"No changes were made to the build with ID {build_id}.")
        else:
            # Insert a new build
            result = builds_collection.insert_one(build_data)
            if result.inserted_id:
                logger.info(f"New build with ID {build_id} has been successfully inserted.")

        return True
    except PyMongoError as e:
        logger.error(f"Error updating or inserting the build: {e}")
        return False


def delete_build(builds_collection: Collection,
                 builds_index_collection: Collection,
                 build_id: str,
                 user_id: str) -> bool:
    """
    Deletes a build from the MongoDB collection, will also remove the build_id from the user build
    index collection.

    :param builds_collection: MongoDB collection for storing builds.
    :param builds_index_collection: MongoDB collection for storing build indexes.
    :param build_id: ID of the build to be deleted.
    :param user_id: User identifier associated with the build.
    :return: Status message indicating the result of the deletion operation.
    """
    try:
        delete_result = builds_collection.delete_one({"build_id": build_id})
        logger.info(f"Deleted build {build_id}")
        if delete_result.deleted_count > 0:  # Checks if an object was deleted
            # Removes the build_id from index of the account who created it
            update_result = builds_index_collection.update_one(
                {"user_id": user_id},
                {"$pull": {"created_build_list": build_id}}
            )
            # Checks for a valid modification
            if update_result.modified_count > 0:
                return True
            else:
                logger.erorr(f"Build was deleted but index could not be deleted: {build_id}")
                return False
        else:

            return False
    except PyMongoError as e:
        logger.error(f"Build could not be deleted, ERROR: {e}")
        return False


def fetch_user_builds(builds_collection: Collection, builds_index_collection: Collection, user_id: str) -> list:
    """
    Fetches builds associated with a user from MongoDB collections.

    :param builds_collection: MongoDB collection for storing builds.
    :param builds_index_collection: MongoDB collection for storing build indexes.
    :param user_id: User identifier associated with the builds.
    :return: List of builds associated with the specified user (empty list otherwise).
    """
    fetched_builds = []

    user_build_ids = builds_index_collection.find_one({"user_id": user_id})

    if user_build_ids is not None:
        user_build_ids_list = list(user_build_ids["created_build_list"])

        for build_id in user_build_ids_list:
            build = builds_collection.find_one({"build_id": build_id}, {"_id": 0})
            fetched_builds.append(build)

    return fetched_builds
