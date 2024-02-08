import datetime

import jwt
from flask import Flask, request, make_response, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from sqlalchemy.orm import Session

from build_database_methods import write_new_build, delete_build, edit_build
from user_database_methods import add_new_user, delete_existing_user, unique_username_check, unique_email_check

from orm_setup import engine

from constants import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET_KEY"  # Used in JWT wrapper function, add this to constants

# This config might help at a later point, if the code does not work for any reason come back and try use it
cors_config = {
    "origins": ["http://localhost:4200"],
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["Content-Type", "Authorization"],
    "supports_credentials": True,
}
CORS(app)

client = MongoClient(MONGO_CONNECTION_URL)
database = client[STAGING_DATABASE]
builds_collection = database[BUILDS_COLLECTION]
build_index_collection = database[BUILDS_INDEX_COLLECTION]
users_collection = database[USER_COLLECTION]


@app.route("/")
def home_page():
    return render_template('home.html')


"""
LOGIN AND LOGOUT ROUTES
"""


# Needs tweaked for this project but is super close, make sure user passwords are encrypted first though
# Will also need an admin check. Can create a user method in the class and run it as a super quick check
@app.route('/api/v1.0/login', methods=['GET'])
def login():
    auth = request.authorization


@app.route('/api/v1.0/logout', methods=['GET'])
def logout():
    pass


"""
    USER ROUTES
"""


@app.route('/api/v1.0/users/new', methods=['POST'])
def new_user():
    # Checks if the email is already associated with an account
    is_unique_email = unique_email_check(users_collection, request.form["email"])
    if not is_unique_email:
        return make_response(jsonify({"message": "SIGNUP FAILED, that email is already in use"}), 404)

    is_unique_username = unique_username_check(users_collection, request.form["username"])
    if not is_unique_username:
        return make_response(jsonify({"message": "SIGNUP FAILED, that username is already in use"}), 404)

    try:
        add_new_user(user_collection=users_collection, first_name=request.form["first_name"],
                     last_name=request.form["last_name"], username=request.form["username"],
                     email=request.form["email"], provided_password=request.form["password"])
        return make_response(jsonify({"message": "New user and password added successfully"}), 201)

    except PyMongoError as e:
        print("Could not add new user")
        return make_response(jsonify({"message": "New user could not be added"}), 400)


@app.route('/api/v1.0/users/<string:id>/delete', methods=['DELETE'])
def delete_user(id):
    delete_result = delete_existing_user(users_collection, id)

    if delete_result:
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({"message": "User account not found"}), 404)


@app.route('/api/v1.0/users/<string:id>/edit', methods=['PUT'])
def edit_user(id):
    pass


"""
PC BUILD ROUTES
"""


@app.route('/api/v1.0/builds/new', methods=['POST'])
def new_pc_build():
    pass


@app.route('/api/v1.0/builds/<string:build_id>/delete', methods=['DELETE'])
def delete_pc_build(build_id):
    user_id = None
    if 'x-user-id' in request.headers:
        user_id = request.headers['x-user-id']
    if not user_id:
        return jsonify({'message': 'user id not provided'}, 400)

    try:
        success = delete_build(builds_collection=builds_collection,
                               builds_index_collection=build_index_collection,
                               build_id=build_id,
                               user_id=user_id)
        if success:
            return make_response(jsonify({"message": f"Successfully deleted build - {build_id}"}), 200)
        else:
            return make_response(jsonify({"message": f"Failed to delete build - {build_id}"}), 400)

    except PyMongoError as e:
        print(f"ERROR: PyMongo Error Flagged - {e}")
        return make_response(jsonify({"message": f"Error: {e}"}))


@app.route('/api/v1.0/builds/<string:build_id>/edit', methods=['PUT'])
def edit_pc_build(build_id):
    try:
        success = edit_build(builds_collection=builds_collection,
                             build_id=build_id,
                             part_name=request.json[''],
                             new_part=request.json[''])
        if success:
            return make_response(jsonify({"message": f"Successfully updated build - {build_id}"}), 200)
        else:
            return make_response(jsonify({"message": f"Failed to edit build - {build_id}"}), 400)

    except PyMongoError as e:
        print(f"ERROR: PyMongo Error Flagged - {e}")
        return make_response(jsonify({"message": f"Error: {e}"}))


if __name__ == "__main__":
    app.run(port=8000, debug=True)
