import datetime

import bcrypt
import jwt
from flask import Flask, request, make_response, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from build_database_methods import write_new_build, delete_build, edit_build
from user_database_methods import (add_new_user, delete_existing_user,
                                   unique_username_check, update_user_password)
from helper_methods import jwt_methods
from excel_methods.excel_helper_methods import generate_build_from_excel
from constants import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

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
blacklisted_tokens_collection = database[BLACKLIST_COLLECTION]


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
    if auth:
        user = users_collection.find_one({'username': auth.username})
        if user is not None:

            # Checks for a valid password, and if so returns token
            if bcrypt.checkpw(auth.password.encode('utf-8'), user['password']):
                # Token is created that contains the username and expiry time
                token = jwt.encode({
                    'user': auth.username,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                }, app.config['SECRET_KEY'])
                return make_response(jsonify({'token': token, "user_id": user['user_id']}), 200)

            # Otherwise returns an error
            else:
                return make_response(jsonify({'message': 'Bad password'}), 401)

        else:
            return make_response(jsonify({'message': 'Bad username'}), 401)

    return make_response(jsonify({'message': 'Authentication credentials were not provided'}), 401)


@app.route('/api/v1.0/logout', methods=['GET'])
def logout():
    # Gets the token, and writes it to a database of blacklisted tokens
    token = request.headers['x-access-token']
    blacklisted_tokens_collection.insert_one({"token": token})
    return make_response(jsonify({"message": "logout successful"}), 200)


"""
    USER ROUTES
"""


@app.route('/api/v1.0/users/new', methods=['POST'])
def new_user():
    # Checks that the username isn't already stored with an account
    is_unique_username = unique_username_check(users_collection, request.form["username"])
    if not is_unique_username:
        return make_response(jsonify({"message": "SIGNUP FAILED, that username is already in use"}), 404)

    try:
        add_new_user(user_collection=users_collection, first_name=request.form["first_name"],
                     last_name=request.form["last_name"], username=request.form["username"],
                     provided_password=request.form["password"])
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


@app.route('/api/v1.0/users/edit/password', methods=['PUT'])
def edit_user_password():

    non_valid_username = unique_username_check(user_collection=users_collection, username=request.form["username"])
    if non_valid_username:
        return make_response(jsonify({"message": "Invalid username"}), 400)

    try:
        password_update_result = update_user_password(user_collection=users_collection,
                                                      username=request.form["username"],
                                                      old_password=request.form["old_password"],
                                                      new_password=request.form["new_password"])

        if password_update_result:
            return make_response(jsonify({"message": "Password changed successfully"}), 200)
        else:
            return make_response(jsonify({"message": "Password was unable to be updated, "
                                                     "make sure the details provided are correct"}), 400)

    except PyMongoError as e:
        return make_response(jsonify({"message": f"Error with PyMongo - {e}"}), 500)


@app.route('/api/v1.0/users/<string:id>/edit/username', methods=['PUT'])
def edit_user_username(id):
    ...


"""
PC BUILD ROUTES
"""


@app.route('/api/v1.0/builds/new', methods=['POST'])
def new_pc_build():
    # This will require getting the user_id, pass it as the headers in the API request
    """
    Generate new build using excel method
    use the provided budget from the incoming http json and dataframe should be loaded at app start and be
    reloaded once per day


    write new build from helper methods - this will require the above build, and the user_id which can be
    passed in as a header
    e.g.
    write_new_build(builds_collection=builds_collection,
                    builds_index_collection=build_index_collection,
                    completed_build=my_pc_build,
                    user_id="5")
    """
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
                             part_name=request.json[''],  # This will be the part name
                             new_part=request.json[''])  # This will be a dict of the new part
        if success:
            return make_response(jsonify({"message": f"Successfully updated build - {build_id}"}), 200)
        else:
            return make_response(jsonify({"message": f"Failed to edit build - {build_id}"}), 400)

    except PyMongoError as e:
        print(f"ERROR: PyMongo Error Flagged - {e}")
        return make_response(jsonify({"message": f"Error: {e}"}))


if __name__ == "__main__":
    app.run(port=8000, debug=True)
