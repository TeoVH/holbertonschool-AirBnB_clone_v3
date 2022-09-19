#!/usr/bin/python3
"""
State's routes
"""

from models.state import State
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ Returns a list with all obj """
    states = []
    for i in storage.all('State').values():
        states.append(i.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def one_state_id(state_id):
    """ Return one obj """
    save = storage.get(State, state_id)
    if save is None:
        abort(404)
    save = save.to_dict()
    return jsonify(save)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State obj """
    save_temp = storage.get(State, state_id)
    if save_temp is None:
        abort(404)
    storage.delete(save_temp)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def new_state():
    """ Create a new State """
    state = request.get_json()
    if state is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in state:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_state = State(**request.get_json())
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ Update a state """
    state = storage.get(State, state_id)
    list_to_ignore = ["id", "created_at", "updated_at"]

    if state is None:
        abort(404)
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, val in request.get_json().items():
        if key not in list_to_ignore:
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict())
