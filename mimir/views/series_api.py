from flask import request
from flask.blueprints import Blueprint
from flask.json import jsonify

from ..models import Series, Release

series_api = Blueprint('series_api', __name__, url_prefix='/series')

@series_api.route('/<series_id>')
@series_api.route('/', defaults={'series_id': None})
def serieses(series_id):
  if series_id:
    series = Series.query.filter_by(id=series_id).first()

    return jsonify(series.serialize())
  else:
    page = int(request.args.get('p', 1))
    series = Series.query.paginate(page, 25)

    return jsonify({
      'next_page': series.has_next,
      'series': [item.serialize() for item in series.items]
    })

@series_api.route('/<series_id>/releases/<release_id>')
@series_api.route('/<series_id>/releases', defaults={'release_id': None})
def series_releases(series_id, release_id):
  series = Series.query.filter_by(id=series_id).first()

  if release_id:
    release = Release.query.filter_by(series=series, id=release_id).first()

    return jsonify(release.serialize())

  page = int(request.args.get('p', 1))
  releases = Release.query.filter_by(series=series).paginate(page, 25)

  return jsonify({
      'next_page': releases.has_next,
      'releases': [item.serialize() for item in releases.items]
    })
