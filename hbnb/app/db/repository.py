"""SQLAlchemy repository implementation."""

from typing import Optional, List, Type
from app.db import db
from sqlalchemy.exc import SQLAlchemyError


class SQLAlchemyRepository:
    """Base repository for all models."""

    def __init__(self, model: Type[db.Model]):
        """Initialize with model class."""
        self.model = model

    def get(self, obj_id: str) -> Optional[db.Model]:
        """Get object by ID."""
        return self.model.query.get(obj_id)

    def get_all(self) -> List[db.Model]:
        """Get all objects."""
        return self.model.query.all()

    def add(self, obj: db.Model) -> None:
        """Add object to database."""
        try:
            db.session.add(obj)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Database error: {str(e)}")

    def update(self, obj_id: str, data: dict) -> Optional[db.Model]:
        """Update object by ID."""
        obj = self.get(obj_id)
        if obj:
            try:
                for key, value in data.items():
                    setattr(obj, key, value)
                db.session.commit()
                return obj
            except SQLAlchemyError as e:
                db.session.rollback()
                raise ValueError(f"Database error: {str(e)}")
        return None

    def delete(self, obj_id: str) -> bool:
        """Delete object by ID."""
        obj = self.get(obj_id)
        if obj:
            try:
                db.session.delete(obj)
                db.session.commit()
                return True
            except SQLAlchemyError as e:
                db.session.rollback()
                raise ValueError(f"Database error: {str(e)}")
        return False
