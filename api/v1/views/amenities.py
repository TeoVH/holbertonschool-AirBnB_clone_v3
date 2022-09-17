#!/usr/bin/python3
"""
Amenities's routes
"""

from models.state import State
from models.city import City
from models.amenity import Amenity
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ Returns a list with all amenities obj """
    amenities = []
    for i in storage.all('Amenity').values():
        amenities.append(i.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def one_amenity_id(amenity_id):
    """ Return one amenity obj """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity = amenity.to_dict()
    return jsonify(amenity)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an amenity obj """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def new_amenity():
    """ Create a new amenity """
    amenity = request.get_json()
    if amenity is None:
        return make_response(jsonify({"error": "Not a JSON"}), 404)
    if "name" not in amenity:
        return make_response(jsonify({"error": "Missing name"}), 404)

    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Update an amenity """
    amenity = storage.get(Amenity, amenity_id)
    new_data = request.get_json().items()
    list_to_ignore = ["id", "created_at", "updated_at"]

    if amenity is None:
        abort(404)
    if new_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 404)

    for key, val in new_data:
        if key not in list_to_ignore:
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_dict())