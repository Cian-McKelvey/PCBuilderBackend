import datetime
from functools import wraps

import bcrypt
import jwt
from flask import Flask, request, make_response, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from build_database_methods import write_new_build, delete_build, edit_build, fetch_user_builds, update_build
from user_database_methods import (add_new_user, delete_existing_user,
                                   unique_username_check, update_user_password)
from admin_database_methods import fetch_app_info, fetch_all_users, admin_delete_user_account
from excel_methods.excel_helper_methods import generate_build_from_excel, read_excel_data
from constants import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
# csrf = CSRFProtect(app)  # Provide protection against XSS

cors_config = {
    "origins": ["http://localhost:4200"],
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["Content-Type", "Authorization", "x-access-token", "x-user-id"],
    "supports_credentials": False,
}
CORS(app, resources={r"/*": {"origins": cors_config["origins"]}}, **cors_config)


# CORS(app)

client = MongoClient(MONGO_CONNECTION_URL)
database = client[PRODUCTION_DATABASE]
builds_collection = database[BUILDS_COLLECTION]
build_index_collection = database[BUILDS_INDEX_COLLECTION]
users_collection = database[USER_COLLECTION]
blacklisted_tokens_collection = database[BLACKLIST_COLLECTION]

# Get the current directory of the script
current_dir = os.path.dirname(os.path.realpath(__file__))
# Construct the path to the Excel file relative to the project root
excel_file = os.path.abspath(os.path.join(current_dir, '../parts/components.xlsx'))

complete_parts_df = read_excel_data(excel_file)


# Decorator function used to protect from unregistered calls by requiring a valid token
def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({'message': 'Token is missing'}, 401))

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except Exception as e:
            return make_response(jsonify({'message': f'Error decoding token: {str(e)}'}, 401))

        blacklist_token = blacklisted_tokens_collection.find_one({"token": token})
        if blacklist_token is not None:
            return make_response(jsonify({"message": "Token is blacklisted, can no longer be used"}), 401)

        return func(*args, **kwargs)

    return jwt_required_wrapper


# Decorator Function to Check if the User is Admin
def admin_required(func):
    @wraps(func)
    def admin_required_wrapper(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({'message': 'Token is missing'}, 401))

        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if data['admin']:
            return func(*args, **kwargs)
        else:
            return make_response(jsonify({'message': 'Admin Access is required'}), 401)

    return admin_required_wrapper


@app.route("/")
def home_page():
    return render_template('home.html')


@app.route("/admin")
def admin_page():
    return "Admin Page"


"""
LOGIN AND LOGOUT ROUTES
"""


# Needs tweaked for this project but is super close, make sure user passwords are encrypted first though
# Will also need an admin check. Can create a user method in the class and run it as a super quick check
@app.route('/api/v1.0/login', methods=['GET'])
def login():
    auth = request.authorization
    if auth:
        username = str(auth.username)
        user = users_collection.find_one({'username': username})
        if user is not None:

            # Checks for a valid password, and if so returns token
            if bcrypt.checkpw(auth.password.encode('utf-8'), user['password']):
                # Token is created that contains the username and expiry time
                token = jwt.encode({
                    'user': auth.username,
                    'admin': user['admin'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                }, app.config['SECRET_KEY'])
                return make_response(jsonify({'token': token, "user_id": user['user_id'],
                                              "is_admin": user['admin']}), 200)

            # Otherwise returns an error
            else:
                return make_response(jsonify({'message': 'Bad password'}), 401)

        else:
            return make_response(jsonify({'message': 'Bad username'}), 401)

    return make_response(jsonify({'message': 'Authentication credentials were not provided'}), 401)


@app.route('/api/v1.0/logout', methods=['GET'])
# @jwt_required
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

    username = str(request.form["username"])
    password = str(request.form["password"])

    try:
        # Remove first and lastname from the args
        add_new_user(user_collection=users_collection, username=username, provided_password=password)
        return make_response(jsonify({"message": "New user and password added successfully",
                                      "username": request.form["username"]}), 201)

    except PyMongoError as e:
        print("Could not add new user")
        return make_response(jsonify({"message": "New user could not be added"}), 400)


@app.route('/api/v1.0/users/<string:id>/delete', methods=['DELETE'])
@jwt_required
def delete_user(id):
    token = None
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']
    if not token:
        return make_response(jsonify({'message': 'Token is missing'}, 401))

    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])

    # Requires that the person deleting the account is logged into the account
    username = data['user']
    delete_result = delete_existing_user(builds_collection=builds_collection,
                                         builds_index_collection=build_index_collection,
                                         users_collection=users_collection,
                                         user_id=id,
                                         username=username)

    if delete_result:
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({"message": "User account not found"}), 404)


@app.route('/api/v1.0/users/edit/password', methods=['PUT'])
@jwt_required
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
@jwt_required
def new_pc_build():
    user_id = None
    if 'x-user-id' in request.headers:
        user_id = str(request.headers['x-user-id'])  # Makes sure the id is a string
    if not user_id:
        return jsonify({'message': 'user id not provided'}, 400)

    new_build_price = int(request.json['price'])
    if new_build_price > 2500:
        return make_response(jsonify({"message": "Price is too high to generate build"}), 400)
    new_build = generate_build_from_excel(build_price=new_build_price, complete_parts_df=complete_parts_df)

    if not new_build.is_valid():
        return make_response(jsonify({"message": "Error while generating new build"}), 400)

    try:
        write_new_build(builds_collection=builds_collection,
                        builds_index_collection=build_index_collection,
                        completed_build=new_build,
                        user_id=user_id)
        return make_response(jsonify({"Build": new_build.to_dict(user_id=user_id)}))
    except PyMongoError as e:
        return make_response(jsonify({"Message": str(e)}), 400)


@app.route('/api/v1.0/builds/<string:build_id>/delete', methods=['DELETE'])
@jwt_required
def delete_pc_build(build_id):
    user_id = None
    if 'x-user-id' in request.headers:
        user_id = str(request.headers['x-user-id'])
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
@jwt_required
def edit_pc_build(build_id):
    data = request.json

    part_type = data['part_type']
    new_part = data['new_part']
    part_dict = {new_part['part_name']: new_part['price']}

    try:
        success = edit_build(builds_collection=builds_collection,
                             build_id=build_id,
                             part_name=part_type,
                             new_part=part_dict)
        if success:
            return make_response(jsonify({"message": f"Successfully updated build - {build_id}"}), 200)
        else:
            return make_response(jsonify({"message": f"Failed to edit build - {build_id}"}), 400)

    except PyMongoError as e:
        return make_response(jsonify({"message": f"Error: {e}"}), 400)


@app.route('/api/v1.0/builds/<string:build_id>/replace', methods=['PUT'])
@jwt_required
def replace_pc_build(build_id):
    data = request.json

    try:
        success = update_build(builds_collection=builds_collection, build_data=data)
        if success:
            return make_response(jsonify({"message": "Successfully updated build"}), 200)
        else:
            return make_response(jsonify({"message": f"Build: {build_id} could not be updated"}), 400)

    except PyMongoError as e:
        return make_response(jsonify({"message": f"Error: {e}"}), 400)


@app.route('/api/v1.0/builds/fetch_all', methods=['GET'])
@jwt_required
def get_all_builds():
    user_id = request.headers.get('x-user-id')
    if not user_id:
        return make_response(jsonify({'message': 'user id not provided'}), 400)

    try:
        user_created_builds = fetch_user_builds(builds_collection=builds_collection,
                                                builds_index_collection=build_index_collection,
                                                user_id=user_id)

        return jsonify({'builds': user_created_builds}), 200

    except PyMongoError as e:
        return jsonify({"message": f"Error: {e}"}), 500


# This will need to create a list of all parts and send it to the frontend on initialisation of the frontend.
# Then it can be used to edit the build on the frontend etc...
@app.route('/api/v1.0/parts/fetch_all', methods=['GET'])
def fetch_all_parts():
    try:
        parts_list = complete_parts_df.values.tolist()
    except Exception as e:
        return make_response(jsonify({'message': f'Parts list could not be converted to list: {e}'}), 400)

    if len(parts_list) > 0:
        return make_response(jsonify({'parts': parts_list}), 200)
    else:
        return make_response(jsonify({'message': 'No Parts Could be found'}), 404)


"""
    ADMIN ROUTES
"""


@app.route('/api/v1.0/admin/app-data', methods=['GET'])
@jwt_required
@admin_required
def get_app_data():
    app_data = fetch_app_info(db=database, user_collection=users_collection, build_collection=builds_collection)
    if app_data:
        return make_response(jsonify({'AppInfo': app_data}), 200)
    else:
        return make_response(jsonify({'message': 'No data found'}), 404)


@app.route('/api/v1.0/admin/fetch-all-users', methods=['GET'])
@jwt_required
@admin_required
def get_all_users_data():
    user_info = fetch_all_users(collection=users_collection)
    if user_info:
        return make_response(jsonify({'users': user_info}), 200)
    else:
        return make_response(jsonify({'message': 'No user info could be found'}), 404)


@app.route('/api/v1.0/admin/delete-user/<string:id>', methods=['DELETE'])
@jwt_required
@admin_required
def admin_delete_user(id):
    try:
        success = admin_delete_user_account(builds_collection=builds_collection,
                                            builds_index_collection=build_index_collection,
                                            users_collection=users_collection,
                                            user_id=id)

        if success:
            return make_response(jsonify({'message': f"User account {id} deleted"}), 204)

    except PyMongoError as e:
        return make_response(jsonify({'message': str(e)}), 404)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
