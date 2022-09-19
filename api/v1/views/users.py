#!/usr/bin/python3
"""
Users's routes
"""

from models.user import User
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ Returns a list with all obj """
    users = []
    for i in storage.all('User').values():
        users.append(i.to_dict())
    return jsonify(users)


@app_views.route('users/<user_id>', methods=['GET'], strict_slashes=False)
def one_user_id(user_id):
    """ Return one obj """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user = user.to_dict()
    return jsonify(user)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a user obj """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def new_user():
    """ Create a new user """
    user = request.get_json()
    if user is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in user:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in user:
        return make_response(jsonify({"error": "Missing password"}), 400)

    new_user = User(**request.get_json())
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Update a user """
    user = storage.get(User, user_id)
    list_to_ignore = ["id", "email", "created_at", "updated_at"]

    if user is None:
        abort(404)
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, val in request.get_json().items():
        if key not in list_to_ignore:
            setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict())
