"""Base repository class for CRUD operations."""

from app.db import db


class BaseRepository:
    def __init__(self, model_class):
        self.model = model_class

    def add(self, entity):
        db.session.add(entity)
        db.session.commit()
        return entity

    def get(self, id):
        return self.model.query.get(id)

    def get_all(self):
        return self.model.query.all()

    def update(self, entity):
        db.session.commit()
        return entity

    def delete(self, entity):
        db.session.delete(entity)
        db.session.commit()
