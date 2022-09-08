#!/usr/bin/python3
''' Index python file '''
from api.v1.views.__init__ import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    ''' Return the status of the API '''
    return jsonify({"status": "OK"})
