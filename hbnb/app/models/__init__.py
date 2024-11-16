# app/models/__init__.py
from app.db import db

def init_db():
    """Initialize database"""
    import app.models.user
    import app.models.place
    import app.models.review
    import app.models.amenity
    db.create_all()
