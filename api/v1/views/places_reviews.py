#!/usr/bin/python3
''' Index python file '''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=["GET", "POST"])
def reviews_from_place(place_id):
    ''' Retrieves all cities from a state '''
    places_list = [obj.to_dict() for obj in storage.all("Place").values()]
    ids = [obj['id'] for obj in places_list]
    if place_id in ids:
        if request.method == "GET":
            reviews = storage.all("Review")
            place_reviews = [obj.to_dict() for obj in reviews.values()
                             if obj.place_id == place_id]
            return jsonify(place_reviews)
        elif request.method == "POST":
            req_json = request.get_json()
            if not req_json:
                abort(400, 'Not a JSON')
            if not req_json.get("user_id"):
                abort(400, "Missing user_id")
            user = storage.get(User, req_json.get("user_id"))
            if not user:
                abort(404, "Not found")
            if 'user_id' not in req_json:
                abort(400, 'Missing user_id')
            user = storage.get(User, req_json.get("user_id"))
            if not user:
                abort(404, "Not found")
            if 'text' not in req_json:
                abort(400, 'Missing text')
            req_json["place_id"] = place_id
            new_place = Review(**req_json)
            new_place.save()
            return jsonify(new_place.to_dict()), 201
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=["GET", "DELETE", "PUT"])
def review(review_id):
    ''' Retrieves, modifies, or deletes a particular review '''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        if request.method == "GET":
            return jsonify(review.to_dict())
        if request.method == "DELETE":
            storage.delete(review)
            storage.save()
            return {}, 200
        elif request.method == "PUT":
            if not request.get_json():
                abort(400, 'Not a JSON')
            else:
                for key, value in request.get_json().items():
                    if key not in ['id', 'created_at',
                                   'updated_at', 'place_id', 'user_id']:
                        setattr(review, key, value)
                storage.save()
                return jsonify(review.to_dict()), 200
