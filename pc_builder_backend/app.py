from flask import Flask, request, make_response, jsonify, render_template
from flask_cors import CORS


app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template('home.html')


"""
LOGIN AND LOGOUT ROUTES
"""


@app.route('/api/v1.0/login', methods=['GET'])
def login():
    pass


@app.route('/api/v1.0/logout', methods=['GET'])
def logout():
    pass


"""
USER ROUTES
"""


@app.route('/api/v1.0/users/new', methods=['POST'])
def new_user():
    pass


@app.route('/api/v1.0/users/<string:id>/delete', methods=['DELETE'])
def delete_user(id):
    pass


@app.route('/api/v1.0/users/<string:id>/edit', methods=['PUT'])
def edit_user(id):
    pass


"""
PC BUILD ROUTES
"""


@app.route('/api/v1.0/builds/new', methods=['POST'])
def new_build():
    pass


@app.route('/api/v1.0/builds/<string:build_id>/delete', methods=['DELETE'])
def delete_build(build_id):
    pass


@app.route('/api/v1.0/builds/<string:build_id>/edit', methods=['PUT'])
def edit_build(build_id):
    pass


if __name__ == "__main__":
    app.run(port=8000, debug=True)
