#!/usr/bin/python3
''' Index python file '''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=["GET", "POST"])
def amenities():
    ''' Retrieves all amenities '''
    if request.method == "GET":
        amenities_list = [obj.to_dict() for obj in storage.all("Amenity").values()]
        return jsonify(amenities_list)
    elif request.method == "POST":
        req_json = request.get_json()
        if not req_json:
            abort(400, 'Not a JSON')
        if 'name' not in req_json:
            abort(400, 'Missing name')
        new_amenity = Amenity(**req_json)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=["GET", "DELETE", "PUT"])
def amenity(amenity_id):
    ''' Retrieves, modifies or deletes an amenity '''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        if request.method == "GET":
            return jsonify(amenity.to_dict())
        if request.method == "DELETE":
            storage.delete(amenity)
            storage.save()
            return {}, 200
        elif request.method == "PUT":
            if not request.get_json():
                abort(400, 'Not a JSON')
            else:
                amenity = storage.get(Amenity, amenity_id)
                for key, value in request.get_json().items():
                    if key not in ['id', 'created_at',
                                   'updated_at']:
                        setattr(amenity, key, value)
                storage.save()
                return jsonify(amenity.to_dict()), 200
