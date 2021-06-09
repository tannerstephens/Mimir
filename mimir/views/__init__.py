from flask import Flask
from flask.blueprints import Blueprint

from .releases_api import releases_api

def register_views(app: Flask):
  api = Blueprint('api', __name__, url_prefix='/v1')

  api.register_blueprint(releases_api)

  app.register_blueprint(api)
