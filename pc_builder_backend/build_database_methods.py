from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from pc_builder_backend.pc_build import PCBuild
from logger_config.logger_config import create_logger
from pprint import pprint


"""
On the write new build method, the main thing that needs to be done is to define a structure for the database 
that holds the index of a user completed build, once that is done, the update_one method will be hashed out 
accordingly, and it all should work after whatever tweaks that are required are implemented.

BUILD STRUCTURE:
{
    "CPU": {"value": pc_build.cpu, "price": pc_build.cpu_price},
    "GPU": {"value": pc_build.gpu, "price": pc_build.gpu_price},
    "RAM": {"value": pc_build.ram, "price": pc_build.ram_price},
    "SSD": {"value": pc_build.ssd, "price": pc_build.ssd_price},
    "HDD": {"value": pc_build.hdd, "price": pc_build.hdd_price},
    "Motherboard": {"value": pc_build.motherboard, "price": pc_build.motherboard_price},
    "Power Supply": {"value": pc_build.power_supply, "price": pc_build.power_supply_price},
    "Overall Price": pc_build.overall_price,
    "build_id": build_id,
    "user_id" : user_id,
    "created_at": datetime.datetime.now()
}

BuildIndexStructure:
{
    "user_id": example_user_id,
    "created_build_list": []
}

"""

# Get the absolute path to the project root
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# # Specify the full path for the log file in the 'logs' directory
# log_file_path = os.path.join(project_root, 'logs', 'PCBuilds.log')
#
# logger = logging.getLogger(__name__)
#
# # Sets the lowest level of logger to the debug level (lowest)
# logger.setLevel(logging.DEBUG)  # This will need to be changed in the real app
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# # Create a console handler and set the formatter
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)
# # Sets the logging to write to app.log too
# file_handler = logging.FileHandler(filename=log_file_path)
# file_handler.setFormatter(formatter)  # Sets the format
# # Add the handlers to the logger
# logger.addHandler(console_handler)
# logger.addHandler(file_handler)


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
    fetched_builds = []

    user_build_ids = builds_index_collection.find_one({"user_id": user_id})
    user_build_ids_list = list(user_build_ids["created_build_list"])

    for build_id in user_build_ids_list:
        build = builds_collection.find_one({"build_id": build_id}, {"_id": 0})
        fetched_builds.append(build)

    return fetched_builds

"""
# Fetches all transfers associated with an email
def receive_transfer_by_email(transfer_collection: Collection, email: str):
    # Combined query fetches if the email = sender_email OR receiver_email
    combined_query = {
        "$or": [
            {"sender_email": email},
            {"receiver_email": email}
        ]
    }

    result = list(transfer_collection.find(combined_query, {"_id": 0}))
    result.reverse()  # Reverses the order of the fetched items, so they're shown most recent first in UI

    return result
"""