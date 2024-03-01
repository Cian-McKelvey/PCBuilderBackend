from pymongo.errors import PyMongoError
from pymongo.mongo_client import MongoClient

from build_database_methods import write_new_build, delete_build, edit_build, fetch_user_builds
from pc_builder_backend.pc_build import PCBuild

from constants import *

import pprint

client = MongoClient(MONGO_CONNECTION_URL)
database = client[STAGING_DATABASE]
builds_collection = database[BUILDS_COLLECTION]
build_index_collection = database[BUILDS_INDEX_COLLECTION]

# my_pc_build = PCBuild()
# my_pc_build.set_cpu(cpu="Intel Core i7", price=300)
# my_pc_build.set_gpu(gpu="NVIDIA GeForce RTX 3080", price=700)
# my_pc_build.set_ram(ram="32GB DDR4", price=150)
# my_pc_build.set_ssd(ssd="1TB NVMe", price=100)
# my_pc_build.set_hdd(hdd="2TB SATA", price=80)
# my_pc_build.set_motherboard(motherboard="ASUS ROG Strix Z590", price=250)
# my_pc_build.set_power_supply(power_supply="850W Gold-rated", price=120)
# my_pc_build.set_case(case="example", price=100)
#
# my_pc_build.display_info()
# print("\n---------------------------\n")
# print(my_pc_build)
#
# # Add build
# try:
#     write_new_build(builds_collection=builds_collection,
#                     builds_index_collection=build_index_collection,
#                     completed_build=my_pc_build,
#                     user_id="5")
#     print("Successfully created new build")
# except PyMongoError as e:
#     print(e)
#
# # Edit build
# pprint.pprint(builds_collection.find_one({"build_id": my_pc_build.build_id}))
# try:
#     new_item = {"LOLOLOLOL": 500}
#     result = edit_build(builds_collection=builds_collection, build_id=my_pc_build.build_id,
#                                   part_name="SSD", new_part=new_item)
#     print("Success")
# except Exception as e:
#     print(f"Failure {e}")
#
# pprint.pprint(builds_collection.find_one({"build_id": my_pc_build.build_id}))
#
# # Delete Build
# try:
#     delete_build(builds_collection=builds_collection,
#                  builds_index_collection=build_index_collection,
#                  build_id=my_pc_build.build_id,
#                  user_id="5")
#     print(f"Build {my_pc_build.build_id} successfully deleted")
# except PyMongoError as e:
#     print(e)

fetch_user_builds(builds_collection=builds_collection, builds_index_collection=build_index_collection, user_id="5")
