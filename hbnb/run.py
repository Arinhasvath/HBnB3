"""Run script for HBnB application."""

from app import create_app
from app.db import db
from app.models import User, Place, Review, Amenity
from collections.abc import Mapping

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Configure Flask shell context."""
    return {
        "db": db,
        "User": User,
        "Place": Place,
        "Review": Review,
        "Amenity": Amenity,
    }


if __name__ == "__main__":
    app.run()
