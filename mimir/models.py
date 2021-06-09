from enum import unique

from sqlalchemy.orm import backref
from .extensions import db

Column = db.Column
relationship = db.relationship

class Model(db.Model):
  __abstract__ = True
  id = Column(db.Integer, primary_key=True)

  def save(self, commit=True):
    db.session.add(self)
    if commit:
      db.session.commit()
    return self

  def delete(self, commit=True):
    db.session.delete(self)
    return commit and db.session.commit()


class Publisher(Model):
  name = Column(db.String, unique=True, nullable=False)
  releases = relationship('Release', backref='publisher', lazy=True)

class Release(Model):
  title = Column(db.String, unique=False, nullable=False)
  image_id = Column(db.String, unique=False, nullable=False)
  publisher = Column(db.Integer, db.ForeignKey('publisher.id'), nullable=False)
  release_id = Column(db.String, unique=False, nullable=False)
  series_id = Column(db.String, unique=False, nullable=False)
