#!/usr/bin/python3
''' Initialize Flask Blueprint '''
from flask import Blueprint, render_template, abort
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from jinja2 import TemplateNotFound
from api.v1.views.index import *
