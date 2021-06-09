from flask import Flask

from .extensions import (
  crontab,
  db,
  migrate
)

from .views import register_views
from .cronjobs import register_cronjobs

def create_app(config='mimir.config.Config'):
  app = Flask(__name__)
  app.config.from_object(config)

  register_extensions(app)
  register_views(app)
  register_cronjobs()

  return app

def register_extensions(app: Flask):
  crontab.init_app(app)
  db.init_app(app)
  migrate.init_app(app, db)
