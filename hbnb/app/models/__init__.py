# app/models/__init__.py
from app.db import db


def init_db():
    # Import ici pour éviter les imports circulaires
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    from app.models.amenity import Amenity

    db.create_all()
