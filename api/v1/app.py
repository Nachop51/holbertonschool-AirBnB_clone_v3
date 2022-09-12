#!/usr/bin/python3
''' Api v1 '''
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os
HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
PORT = os.getenv('HBNB_API_PORT', '5000')

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler(404)
def handle_404(exception):
    """ Hanldes 404 errors """
    return jsonify({'error': "Not found"}), 404


@app.teardown_appcontext
def handle(error):
    ''' handles teardown '''
    storage.close()


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, threaded=True, debug=True)
