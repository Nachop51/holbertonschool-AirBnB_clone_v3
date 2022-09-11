#!/usr/bin/python3
''' Index python file '''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=["GET", "POST"])
def cities_from_state(state_id):
    ''' Retrieves all cities from a state '''
    state_list = [obj.to_dict() for obj in storage.all("State").values()]
    ids = [obj['id'] for obj in state_list]
    if state_id in ids:
        if request.method == "GET":
            cities = storage.all("City")
            state_cities = [obj.to_dict() for obj in cities.values()
                            if obj.state_id == state_id]
            return jsonify(state_cities)
        elif request.method == "POST":
            req_json = request.get_json()
            if not req_json:
                abort(400, 'Not a JSON')
            if 'name' not in req_json:
                abort(400, 'Missing name')
            req_json["state_id"] = state_id
            new_city = City(**req_json)
            new_city.save()
            return jsonify(new_city.to_dict()), 201
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=["GET", "DELETE", "PUT"])
def city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        if request.method == "GET":
            return jsonify(city.to_dict())
        if request.method == "DELETE":
            storage.delete(city)
            storage.save()
            return {}, 200
        elif request.method == "PUT":
            if not request.get_json():
                abort(400, 'Not a JSON')
            elif 'name' not in request.get_json():
                abort(400, 'Missing name')
            else:
                city = storage.get(City, city_id)
                for key, value in request.get_json().items():
                    if key not in ['id', 'created_at',
                                   'updated_at', 'state_id']:
                        setattr(city, key, value)
                storage.save()
                return jsonify(city.to_dict()), 200
