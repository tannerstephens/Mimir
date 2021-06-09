from flask_crontab import Crontab
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

crontab = Crontab()
migrate = Migrate()
db = SQLAlchemy()
