#!/usr/bin/python3
''' Index python file '''
from api.v1.views import app_views
from flask import jsonify, abort, request
from api.v1.views.amenities import amenities
from models import storage
from models.review import Review
from models.place import Place
from models.amenity import Amenity
import os

STRG = os.environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=["GET"])
def place_amenities(place_id):
    ''' Retrieves all cities from a state '''
    place = storage.get(Place, place_id)
    if place is None:
            abort(404, 'Not found')
    else:
        place_amenities = place.amenities
        place_amenities = [obj.to_dict() for obj in place_amenities]
        return jsonify(place_amenities)


@app_views.route('/api/v1/places/<place_id>/amenities/<amenity_id>',
                 methods=["DELETE", "POST"])
def place_amenity(place_id, amenity_id):
    ''' Retrieves, modifies, or deletes a particular amenity '''
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404, 'Not found')
    elif amenity is None:
        abort(404, 'Not found')
    else:
        if request.method == "DELETE":
            if amenity not in place.amenities:
                    abort(404, 'Not found')
            storage.delete(amenity)
            storage.save()
            return {}, 200
        elif request.method == "POST":
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            return jsonify(amenity.to_dict()), 201
