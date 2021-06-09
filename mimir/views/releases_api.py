from flask.blueprints import Blueprint
from flask.json import jsonify
from flask.views import MethodView

releases_api = Blueprint('releases_api', __name__, url_prefix='/releases')

@releases_api.route('/')
def get():
  return jsonify({'status': True})
