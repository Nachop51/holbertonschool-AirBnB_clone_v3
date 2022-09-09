#!/usr/bin/python3
''' Index python file '''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'])
def states():
    ''' retrieves the number of each objects by type '''
    if request.method == 'GET':
      return jsonify([obj.to_dict() for obj in storage.all("State").values()])
    elif request.method == 'POST':
      if not request.get_json():
        abort(400, 'Not a JSON')
      if 'name' not in request.get_json():
        abort(400, 'Missing name')
      new_state = State(**request.get_json())
      new_state.save()
      return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def state(state_id):
    ''' retrieves the number of each objects by type and ID '''
    state_list = [obj.to_dict() for obj in storage.all("State").values()]
    ids = [obj['id'] for obj in state_list]
    if state_id in ids:
      if request.method == 'GET':
        return jsonify(state_list[ids.index(state_id)])
      elif request.method == 'DELETE':
        storage.delete(storage.get(State, state_id))
        storage.save()
        return {}, 200
      elif request.method == 'PUT':
        if not request.get_json():
          abort(400, 'Not a JSON')
        else:
          state = storage.get(State, state_id)
          for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
              setattr(state, key, value)
          storage.save()
          return jsonify(state.to_dict()), 200
    else:
      abort(404)
