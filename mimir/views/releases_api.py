from flask import request
from flask.blueprints import Blueprint
from flask.json import jsonify

from ..models import Release

releases_api = Blueprint('releases_api', __name__, url_prefix='/releases')

@releases_api.route('/<release_id>')
@releases_api.route('/', defaults={'release_id': None})
def releases(release_id):
  if release_id:
    release = Release.query.filter_by(id=release_id).first()

    return jsonify(release.serialize())
  else:
    page = int(request.args.get('p', 1))
    releases = Release.query.paginate(page, 25)

    return jsonify({
      'next_page': releases.has_next,
      'releases': [item.serialize() for item in releases.items]
    })
