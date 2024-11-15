from flask_sqlalchemy import SQLAlchemy

# Initialiser l'instance SQLAlchemy
db = SQLAlchemy()

def init_app(app):
    """Initialize the app with the database."""
    db.init_app(app)