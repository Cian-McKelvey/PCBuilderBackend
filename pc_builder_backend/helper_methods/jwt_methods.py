# Decorator function used to protect from unregistered calls by requiring a valid token
from functools import wraps

import jwt
from flask import request, jsonify, app, make_response
from pymongo.collection import Collection


def jwt_required(func, blacklist_collection: Collection, secret_key):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}, 401)

        try:
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
        except Exception as e:
            return jsonify({'message': f'Error decoding token: {str(e)}'}, 401)

        blacklist_token = blacklist_collection.find_one({"token": token})
        if blacklist_token is not None:
            return make_response({"message": "Token is blacklisted, can no longer be used"}, 401)

        return func(*args, **kwargs)

    return jwt_required_wrapper
