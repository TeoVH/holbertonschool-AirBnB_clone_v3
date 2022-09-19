#!/usr/bin/python3
"""
Citites's routes
"""

from models.user import User
from models.place import Place
from models.review import Review
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_reviews(place_id):
    """ Returns a list with all obj """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews_list = []
    for i in place.reviews:
        reviews_list.append(i.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def one_review(review_id):
    """ Return one obj """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review = review.to_dict()
    return jsonify(review)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a review obj """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """create a new review"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    place_request = request.get_json()
    if 'user_id' not in place_request:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get("User", place:request['user_id'])
    if user is None:
        abort(404)
    if 'text' not in place_request:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    place_request['place_id'] = place_id
    review = Review(**place_request)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Update a review """
    review = storage.get(Review, review_id)
    list_to_ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]

    if review is None:
        abort(404)
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, val in request.get_json().items():
        if key not in list_to_ignore:
            setattr(city, key, val)
    review.save()
    return jsonify(review.to_dict())
